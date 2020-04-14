$(document).ready(function(){

    getProfileDetails();

    $('#password-reset').click(function() {
        window.location = '/authenticate/reset/';
    });

    $('#save-profile').click(function() {
        updateProfileDetails();
    });

    $('#enable-mfa').click(function () {
        enableMultiFactorAuth();
    });

    $('#verify-code').click(function () {
        verifyMFACode();
    });

    $('#disable-mfa').click(function () {
        $("#mfa-disable-modal").modal('show');
    });

    $('#disable-mfa-confirm').click(function () {
        disableMultiFactorAuth();
    });

});


function getProfileDetails() {
    ecblockui();

    $.ajax({
        type: 'GET',
        url: '/api/profile/get',
        dataType: 'json',
        success: function (data) {
            ecunblockui();
            if(data) {
                $('#first_name').val(data['first_name']);
                $('#last_name').val(data['last_name']);
                $('#email').val(data['email']);
                $('#mobile').val(data['mobile_number']);
                $('#username').val(data['username']);
                $('#profile_image').attr('src', data['profile_image']);

                if(data['mfa_enabled']) {
                    $('#enable-mfa').hide();
                    $('#disable-mfa').show();
                }
                else {
                    $('#enable-mfa').show();
                    $('#disable-mfa').hide();
                }
            }

        }
    });
}


function updateProfileDetails() {
    ecblockui();
    $('#required-fields-alert').hide();

    if($('#username').val()=="" || $('#email').val()=="") {
        $('#required-fields-alert').show();
        ecunblockui();
        return
    }

    var formData = new FormData();
    formData.append('first_name', $('#first_name').val());
    formData.append('last_name', $('#last_name').val());
    formData.append('email', $('#email').val());
    formData.append('mobile_number', $('#mobile').val());
    formData.append('username', $('#username').val());
    formData.append('profile_image', $('#profile_pic')[0].files[0]);
    formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));

    $.ajax({
        type: 'POST',
        url: '/api/profile/update',
        data: formData,
        contentType: false,
        processData: false,
        success: function (data) {
            ecunblockui();
            getProfileDetails();
            $('#saved-success').show();
            setTimeout(function () {
                $('#saved-success').hide();
            }, 3000);
        }
    });
}

function enableMultiFactorAuth() {
    ecblockui();
    $("#mfa-enable-modal").modal('show');

    $.ajax({
        type: 'GET',
        url: '/api/profile/sendCode',
        dataType: 'json',
        success: function (data) {
            ecunblockui();
            if(data) {
                if(data['success']) {
                    $('#code-sent-success').show();
                    setTimeout(function () {
                        $('#code-sent-success').hide();
                    }, 3000);
                }
                else {
                    $('#code-sent-failure').show();
                    setTimeout(function () {
                        $('#code-sent-success').hide();
                    }, 3000);
                }
            }

        }
    });
}

function verifyMFACode() {
    if($('#code').val() == null || $('#code').val() == "") {
        $('#code-required-fields-alert').show();
        return
    }

    ecblockui();

    $.ajax({
        type: 'POST',
        url: '/api/profile/verifyCode',
        dataType: 'json',
        data: {
            code : $('#code').val(),
            csrfmiddlewaretoken : getCookie('csrftoken')
        },
        success: function (data) {
            ecunblockui();
            getProfileDetails();
            $('#code-required-fields-alert').hide();
            if(data['success']) {
                $("#mfa-enable-modal").modal('hide');
                $('#mfa-activated-success').show();
                setTimeout(function () {
                    $('#mfa-activated-success').hide();
                }, 3000);
            }
            else {
                $('#code-verified-failure').show();
                setTimeout(function () {
                    $('#code-verified-failure').hide();
                }, 3000);
            }

        }

    });
}

function disableMultiFactorAuth() {
    ecblockui();

    $.ajax({
        type: 'POST',
        url: '/api/profile/disableMFA',
        dataType: 'json',
        data: {
            csrfmiddlewaretoken : getCookie('csrftoken')
        },
        success: function (data) {
            ecunblockui();
            getProfileDetails();
            if(data['success']) {
                $("#mfa-disable-modal").modal('hide');
                $('#mfa-deactivated-success').show();
                setTimeout(function () {
                    $('#mfa-deactivated-success').hide();
                }, 3000);
            }

        }
    });
}
