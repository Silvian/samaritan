$(document).ready(function(){

    $('#email-submit-form').submit(function(e) {
        e.preventDefault();
    });

    $('#send-recovery-email').click(function() {
        sendRecoveryEmail();
    });

});


function sendRecoveryEmail() {
    $.ajax({
        type: 'POST',
        url: '/authenticate/forgot_password/',
        dataType: 'json',
        data: {

            email : $('#email').val(),
            csrfmiddlewaretoken : getCookie('csrftoken')
        },
        success: function (data) {
            ecunblockui();
            if(data['success']) {
                $('#invalid-email').hide();
                $('#success-email').show();
            }
            else {
                $('#success-email').hide();
                $('#invalid-email').show();
                setTimeout(function () {
                    $('#invalid-email').hide();
                }, 5000);
            }
        }
    });

}
