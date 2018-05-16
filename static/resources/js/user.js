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
            }

        }
    });
}


function updateProfileDetails() {
    ecblockui();

    $.ajax({
        type: 'POST',
        url: '/api/profile/update',
        dataType: 'json',
        data: {
                    first_name      : $('#first_name').val(),
                    last_name       : $('#last_name').val(),
                    email           : $('#email').val(),
                    mobile_number   : $('#mobile').val(),
                    username        : $('#username').val(),
                    csrfmiddlewaretoken : getCookie('csrftoken')
                },
        success: function (data) {
            ecunblockui();
            getProfileDetails();
        }
    });
}
