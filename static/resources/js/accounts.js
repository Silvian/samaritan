$(document).ready(function(){

    //enable the powerful data table sorting, pagination and searching controls
    var users_table = $('#accounts-list').DataTable({
    'ajax': {
        "type"   : "GET",
        "url"    : '/api/accounts/getAll',

        "dataSrc": ""
    },
        'columns': [
            {"mRender": function(data, type, row) {
                            return htmlEntities(row.fields.username);
                        }
            },
            {"mRender": function(data, type, row) {
                            return getEmailLink(htmlEntities(row.fields.email));
                        }
            },

            {"mRender": function(data, type, row) {
                            if(row.fields.last_login) {
                                return getFormattedDate(new Date(htmlEntities(row.fields.last_login)));
                            }
                            else {
                                return "Never";
                            }
                        }
            },
            {"mRender": function(data, type, row) {
                            return getGDPR(htmlEntities(row.fields.is_staff));
                        }
            },
            {"mRender": function(data, type, row) {
                            return activeButton(htmlEntities(row.fields.is_active), htmlEntities(row.pk));
                        }
            },
            {"mRender": function (data, type, row) {
                            return '<button type="button" class="btn btn-default btn-sm" id="edit-'+ htmlEntities(row.pk)
                            +'"><i class="fa fa-pencil-square-o fa-fw"></i></td>';
                        }
            },
            {"mRender": function (data, type, row) {
                            return '<button type="button" class="btn btn-danger btn-sm" id="remove-'+ htmlEntities(row.pk)
                            +'"><i class="fa fa-trash fa-fw"></i></td>';
                        }
            },
        ],

    });

    $("#add-account-button").click(function(event) {
        $('#user-id').val("");
        $('#required-fields-alert').hide();
        $('#user-modal-label').html("Add new user account");
        $('#is_staff').prop('checked', false);
        $('#delete-user').hide();
        $("#user-modal").modal('show');
        clearFields();
    });

    $("#clear-user").click(function(event) {
        clearFields();
    });

    $("#save-user").click(function(event) {
        submitUser(users_table);
    });

    $('#accounts-list').on("click", '[id^="active-"]', function() {
        var id = this.id.split('active-');
        var is_active = "";
        if($(this).hasClass("btn-success")) {
            is_active = "False";
        }
        else {
            is_active = "True";
        }
        activateUser(id[1], is_active, users_table);
    });

    $('#accounts-list').on("click", '[id^="edit-"]', function() {
        clearFields();
        var id = this.id.split('edit-');
        editUsers(id[1], users_table, "User account details");
    });

    $('#accounts-list').on("click", '[id^="remove-"]', function() {
        var id = this.id.split('remove-');
        $('#delete-id').val(id[1]);
        $('#delete-modal-label').html("Delete user account?");
        $('#delete-modal').modal('show');
    });

    $('#delete-user').click(function(event) {
        $('#delete-id').val($('#user-id').val());
        $('#delete-modal-label').html("Delete user account?");
        $('#delete-modal').modal('show');
    });

    $('#delete-confirm').click(function() {
        $('#delete-modal').modal('hide');
        $("#user-modal").modal('hide');
        deleteUser($('#delete-id').val(), users_table);
    });

    $('#resend-activation').click(function() {
        resendActivationEmail($('#user-id').val());
    });

});

function clearFields() {
    $('#user_name').val("");
    $('#first_name').val("");
    $('#last_name').val("");
    $('#email').val("");
    $('#mobile').val("");
}

function activeButton(is_active, row_id) {
    if(is_active) {
        return '<button type="button" class="btn btn-success btn-sm" id="active-'+ row_id
                        +'"><i class="fa fa-check fa-fw"></i></td>';
    }

    else {
        return '<button type="button" class="btn btn-danger btn-sm" id="active-'+ row_id
                        +'"><i class="fa fa-close fa-fw"></i></td>';
    }

}

function submitUser(users_table) {

    if($('#user_name').val()=="" || $('#email').val()==""){
        $('#required-fields-alert').show();

        return;
    }

    if(!$('#email').val().includes("@")) {
        $('#required-fields-alert').show();

        return;
    }

    var is_staff = false;
    if($('#is_staff').prop("checked") == true){
        is_staff = true;
    }

    var id = $('#user-id').val();
    if(id == "") {
        id = null;
        url = '/api/accounts/add';
    }

    else {
        url = '/api/accounts/update';
    }

    /* Send the data using post */
    var posting = $.post( url, {
                      id              : id,
                      username        : $('#user_name').val(),
                      first_name      : $('#first_name').val(),
                      last_name       : $('#last_name').val(),
                      email           : $('#email').val(),
                      mobile_number   : $('#mobile').val(),
                      is_staff        : is_staff,
                      csrfmiddlewaretoken : getCookie('csrftoken')
    });

    /* Alerts the results */
    posting.done(function(data) {
        if(data.success || data.user) {
            ecunblockui();
            $("#user-modal").modal('hide');
            users_table.ajax.reload();
        }

    });

}

function editUsers(id, users_table, title) {
    ecblockui();
    $.ajax({
	    type: 'GET',
	    url: '/api/accounts/getSingle',
	    dataType: 'json',
	    data: { id: id},
	    success: function(data) {
	         ecunblockui();
	         var user = data;

             $('#user-id').val(id);
             $('#user_name').val(user.username);
             $('#first_name').val(user.first_name);
             $('#last_name').val(user.last_name);
             $('#email').val(user.email);
             $('#mobile').val(user.mobile_number);
             setCheckbox('#is_staff', user.is_staff);

             $('#required-fields-alert').hide();
             $('#user-modal-label').html(title);
             $('#delete-user').show();
             $("#user-modal").modal('show');
	    }
	});

}

function activateUser(id, is_active, users_table) {
    ecblockui();
    $.ajax({
        type: 'POST',
        url: '/api/accounts/activate',
        dataType: 'json',
        data: {    id : id,
                   is_active: is_active,
                   csrfmiddlewaretoken : getCookie('csrftoken')
                },
        success: function (data) {
            ecunblockui();
            if(data.success) {
                users_table.ajax.reload();
            }
            else {
                $('#error-msg').html("Cannot deactivate your own user account");
                $('#accounts-error').show();
                setTimeout(function () {
                    $('#accounts-error').hide();
                }, 3000);
            }
        }
    });
}

function deleteUser(id, users_table) {
    ecblockui();
    $.ajax({
        type: 'POST',
        url: '/api/accounts/delete',
        dataType: 'json',
        data: {    id : id,
                   csrfmiddlewaretoken : getCookie('csrftoken')
                },
        success: function (data) {
            ecunblockui();
            if(data.success) {
                users_table.ajax.reload();
            }
            else {
                $('#error-msg').html("Cannot delete your own user account");
                $('#accounts-error').show();
                setTimeout(function () {
                    $('#accounts-error').hide();
                }, 3000);
            }
        }
    });
}

function resendActivationEmail(id) {
    ecblockui();
    $.ajax({
        type: 'POST',
        url: '/api/accounts/resendEmail',
        dataType: 'json',
        data: {    id : id,
                   csrfmiddlewaretoken : getCookie('csrftoken')
                },
        success: function (data) {
            ecunblockui();
            if(data.success) {
                $('#activation-sent-alert').show();
                setTimeout(function () {
                    $('#activation-sent-alert').hide();
                }, 3000);
            }
        }
    });
}
