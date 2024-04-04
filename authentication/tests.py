"""Tests for authentication module"""
import factory
import mock

from django.test import TestCase
from django_common.auth_backends import User

from factory.django import DjangoModelFactory

from api.tests.integration import UserFactory
from authentication.models import (
    LoginToken,
    MFACode,
    Profile,
)


class ProfileFactory(DjangoModelFactory):
    """Factory for the profile data model."""
    user = factory.SubFactory(UserFactory)
    mobile_number = factory.Faker('random_int', min=0, max=99999999)
    profile_pic = None
    password_strength = 100
    password_breached = False
    password_reset = False
    password_last_updated = None
    mfa_enabled = False

    class Meta:
        model = Profile


class LoginTokenFactory(DjangoModelFactory):
    """Factory for login token model."""
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = LoginToken


class MFACodeFactory(DjangoModelFactory):
    """Factory for MFA code model."""
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = MFACode


class TestProfileTestCase(TestCase):
    """Test the profile model test case."""

    def setUp(self):
        self.user = UserFactory(is_superuser=False)
        self.profile = self.user.profile
        self.token = LoginTokenFactory(user=self.user)

    def test_generate_login_link(self):
        test_url = "test_url"
        expected_link = "http://{url}/authenticate/url/{token}".format(url=test_url, token=self.token)
        link = self.profile.generate_login_link(site_url=test_url)
        self.assertEqual(expected_link[:-36], link[:-36])

    def test_generate_temp_password(self):
        password = self.profile.generate_temp_password()
        self.assertTrue(self.profile.password_reset)
        self.assertEqual(16, len(password))

    def test_verify_password_strength(self):
        weak_password = "weak"
        average_password = "good_enough"
        strong_password = "correct_horse_battery_staples_747"

        self.assertFalse(self.profile.verify_password_strength(weak_password))
        self.assertEqual(18, self.profile.password_strength)
        self.assertTrue(self.profile.verify_password_strength(average_password))
        self.assertEqual(64, self.profile.password_strength)
        self.assertTrue(self.profile.verify_password_strength(strong_password))
        self.assertEqual(201, self.profile.password_strength)

    @mock.patch("authentication.utils.PasswordPwnedChecker.pwned_check")
    def test_verify_password_breached(self, pwned_check):
        pwned_check.return_value = True
        breached_password = "lamepassword"
        self.profile.verify_password_breached(breached_password)
        self.assertTrue(self.profile.password_breached)

    @mock.patch("authentication.utils.PasswordPwnedChecker.pwned_check")
    def test_verify_password_not_breached(self, pwned_check):
        pwned_check.return_value = False
        breached_password = "super_secure_strong_password"
        self.profile.verify_password_breached(breached_password)
        self.assertFalse(self.profile.password_breached)


class TestMFACodeTestCase(TestCase):
    """Test the MFA Code model test case."""

    def setUp(self):
        self.mfa_code = MFACodeFactory()

    def test_calculate_six_digit_code(self):
        six_digit_pin = self.mfa_code.calculate_six_digit_code()
        self.assertEqual(6, len(six_digit_pin))
        self.assertTrue(six_digit_pin.isdigit())


class TestAuthenticationIntegrationTestCase(TestCase):
    """Test the authentication integration."""

    def setUp(self):
        self.user_name = "test"
        self.password = "letmein"
        self.email = "test@samaritan.com"
        self.user = User.objects.create_user(username=self.user_name, password=self.password)

    def test_login_view(self):
        response = self.client.get("/authenticate/login")
        self.assertEqual(response.status_code, 301)
        self.assertRedirects(response, response.url, 301, 200)

    def test_logout_view(self):
        self.client.force_login(user=self.user)
        response = self.client.get("/authenticate/logout")
        self.assertEqual(response.status_code, 301)
        self.assertRedirects(response, response.url, 301, 302)

    def test_reset_view(self):
        self.client.force_login(user=self.user)
        response = self.client.get("/authenticate/reset")
        self.assertEqual(response.status_code, 301)
        self.assertRedirects(response, response.url, 301, 200)

    def test_forgot_view(self):
        response = self.client.get("/authenticate/forgot")
        self.assertEqual(response.status_code, 301)
        self.assertRedirects(response, response.url, 301, 200)

    def test_passwordless_view(self):
        response = self.client.get("/authenticate/passwordless")
        self.assertEqual(response.status_code, 301)
        self.assertRedirects(response, response.url, 301, 200)

    def test_mfa_view(self):
        response = self.client.get("/authenticate/mfa/374415ce-9ed3-4b55-8c30-8156e49ec4fd")
        self.assertEqual(response.status_code, 301)
        self.assertRedirects(response, response.url, 301, 200)

    def test_authenticate_user(self):
        self.client.force_login(user=self.user)
        request_data = {
            "username": self.user_name,
            "password": self.password,
        }
        response = self.client.post("/authenticate/access", data=request_data)
        self.assertEqual(response.status_code, 301)

        response = self.client.get("/api/members/getActive")
        self.assertEqual(response.status_code, 200)

    @mock.patch("authentication.tasks.send_reset_email.delay")
    def test_forgot_password(self, _):
        request_data = {"email": self.user.email}
        response = self.client.post("/authenticate/forgot_password", data=request_data)
        self.assertEqual(response.status_code, 301)
