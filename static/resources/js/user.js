$(document).ready(function(){

    getProfileDetails();

    $('#password-reset').click(function() {
        window.location = '/authenticate/reset/';
    });

    $('#save-profile').click(function() {
        updateProfileDetails()
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
                $('#profile_image').attr('src', data['profile_image'])
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

    var formData = new FormData()
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
