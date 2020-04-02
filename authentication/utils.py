import hashlib
import math
import random
import requests
import time

from os import urandom
from random import choice
from time import sleep

from django.conf import settings


class PasswordGenerator:
    """Password Generator."""

    CHAR_SET = {
        'lowercase': 'abcdefghijklmnopqrstuvwxyz',
        'numbers': '0123456789',
        'uppercase': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
        'special': '@$%&?!#'
    }

    def __init__(self):
        pass

    @staticmethod
    def check_prev_char(password, current_char_set):
        """Function to ensure that there are no consecutive
        UPPERCASE/lowercase/numbers/special-characters."""

        index = len(password)
        if index == 0:
            return False
        else:
            prev_char = password[index - 1]
            if prev_char in current_char_set:
                return True
            else:
                return False

    def generate_password(self, length=16):
        """Function to generate a password."""

        password = []

        while len(password) < length:
            key = choice(self.CHAR_SET.keys())
            a_char = urandom(1)
            if a_char in self.CHAR_SET[key]:
                if self.check_prev_char(password, self.CHAR_SET[key]):
                    continue
                else:
                    password.append(a_char)
        return ''.join(password)


class PasswordEntropyCalculator:
    """Password Entropy Calculator."""

    def __init__(self):
        self.threshold = settings.PASSWORD_ENTROPY_THRESHOLD

    LOWER_CASE = {"LENGTH": 26, "RANGE": "abcdefghijklmnopqrstuvwxyz"}
    UPPER_CASE = {"LENGTH": 26, "RANGE": "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
    NUMBERS = {"LENGTH": 10, "RANGE": "0123456789"}
    ASCII_SYMB = {"LENGTH": 33, "RANGE": " !@#$%^&*(){}[]-_+=|\\~`<>,./?'\""}
    UNICODE = 100

    def character_space_calc(self, text):
        """
        Returns the pool of characters possible for all combined ranges possible
        that are found in the given text input.

        :param text:
        :return: count
        """
        count = 0
        text_set = set(text)
        all_set = set()

        for space in ["LOWER_CASE", "UPPER_CASE", "NUMBERS", "ASCII_SYMB"]:
            s = getattr(self, space)
            s_set = set(s.get("RANGE"))
            all_set |= s_set

            if s_set & text_set:
                count += s.get("LENGTH")

        if text_set - all_set:
            count += self.UNICODE

        return count

    def calculate(self, password):
        """
        Calculates the entropy and the strength score for any given password
        Using the entropy formula:
        E = log2(R^L)
        :param password:
        :return entropy:
        """
        char_space = self.character_space_calc(password)
        passwd_length = len(password)

        # Using the formula E = log2(R^L)
        entropy = int(math.log(char_space ** passwd_length, 2))

        return entropy


class PasswordPwnedChecker:
    """Password pwned checker."""

    def __init__(self):
        self.url = settings.PWNED_API_URL
        self.timeout = settings.PWNED_API_TIMEOUT

    @staticmethod
    def hash_password(password):
        h = hashlib.sha1()
        password = password.encode("utf-8")
        h.update(password)
        return h.hexdigest().upper()

    def pwned_check(self, password):
        """
        Checks is any given password is in the I have been pwned password database.
        Returns the number of occurrences if found otherwise returns 0.
        :param password:
        :return count:
        """
        sha1_hash = self.hash_password(password)
        # first 5 characters is to be used as the key
        key_fragment = sha1_hash[:5]
        # remaining characters to be used as the lookup hash
        hash_fragment = sha1_hash[5:]

        url = self.url + key_fragment
        attempts = 1 + int(settings.PWNED_API_RETRIES)
        while attempts > 0:
            try:
                response = requests.get(url, timeout=self.timeout)
                if response.status_code == 200:
                    if hasattr(response, "text") and response.text:
                        results = list(response.text.split("\r\n"))
                        for result in results:
                            parts = list(result.split(":"))
                            if len(parts) == 2:
                                match = parts[0]  # the remaining hash to be matched
                                count = int(parts[1])  # no of occurrences matched
                                if hash_fragment == match:
                                    return count

                    # if we haven't found a match then password is not compromised
                    return 0

                if response.status_code == 423:
                    return None

            except requests.exceptions.Timeout:
                return None

            except requests.exceptions.ConnectionError:
                return None

            # If response is not 200 then wait 2 secs and retry request
            if attempts > 1:
                sleep(2)

            attempts -= 1

        return None


class MultiFactorCodeGenerator:
    """Multi factor unique random code generator."""

    def __init__(self, salt=settings.SECRET_KEY):
        self.salt = salt

    def generate_random_hash(self):
        """Generate random hash based on secure random and time."""
        random_bits = random.getrandbits(256)
        unique_time = time.time()
        random_string = self.salt + str(random_bits) + str(unique_time)
        h = hashlib.sha1()
        encoded_string = random_string.encode("utf-8")
        h.update(encoded_string)
        return h.hexdigest()

    @staticmethod
    def calculate_six_digit_code(input_hash):
        """Calculate six digit code."""
        six_digit_pin = str(int(input_hash, 16))[:6]
        return six_digit_pin

    def hash_six_digit_code(self, code):
        """Hash the six digit code for db storage and comparisons."""
        h = hashlib.sha256()
        code = str(code)
        encoded_value = code.encode("utf-8")
        encoded_salt = self.salt.encode("utf-8")
        hash_value = encoded_salt + encoded_value
        h.update(hash_value)
        return h.hexdigest()
