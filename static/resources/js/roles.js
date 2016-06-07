$(document).ready(function(){

    $('#roles-error').hide();

    getRoles();

    $('#add-role-button').click(function() {
        $('#role-modal-label').html("Add a new role");
        $('#required-fields-alert').hide();
        $('#role-modal').modal('show');
    });

    $('#save-role').click(function() {
        addRole();
    });

    $('#roles-list').on("click", '[id^="remove-"]', function() {
        var id = this.id.split('remove-');
        deleteRole(id[1]);
    });

});

function getRoles() {

    ecblockui();
    $('#roles-empty').hide();
    $('#roles-list tbody').html("");

    $.ajax({
        type: 'GET',
        url: '/api/roles/getAll',
        dataType: 'json',
        success: function (data) {
            ecunblockui();
            if(data && data.length > 0) {
                $('#roles-list tbody').html("");

                $.each(data, function(i, item) {
                    var role = item.fields;
                    $('#roles-list tbody').append('<tr>' +
                        '<td>' + role.name + '</td>' +
                        '<td>' + role.description + '</td>' +
                        '<td><button type="button" class="btn btn-default btn-sm" id="view-'+ item.pk +'"><i class="fa fa-edit fa-fw"></i></td>' +
                        '<td><button type="button" class="btn btn-danger btn-sm" id="remove-'+ item.pk +'"><i class="fa fa-trash fa-fw"></i></td>' +
                    '</tr>');
                });

            }

            else {
                $('#roles-empty').show();
            }

        }
    });

}

function addRole() {

    $('#required-fields-alert').hide();

    if($('#role-name').val()!="") {
        ecblockui();
        $.ajax({
            type: 'POST',
            url: '/api/roles/add',
            dataType: 'json',
            data: {    name : $('#role-name').val(),
                       description : $('#role-description').val(),
                       csrfmiddlewaretoken : getCookie('csrftoken')
                    },
            success: function (data) {
                ecunblockui();
                $("#role-modal").modal('hide');
                getRoles();
            }
        });

    }

    else {
       $('#required-fields-alert').show();
    }

}

function deleteRole(id) {

    $('#delete-modal-label').html("Delete role");
    $('#delete-modal').modal('show');

    $('#delete-confirm').click(function() {
        $('#delete-modal').modal('hide');
        ecblockui();

        $.ajax({
            type: 'POST',
            url: '/api/roles/delete',
            dataType: 'json',
            data: {    id : id,
                       csrfmiddlewaretoken : getCookie('csrftoken')
                    },
            success: function (data) {
                ecunblockui();
                if(data.success) {
                    getRoles();
                }
                else {
                    $('#error-msg').html(data.error);
                    $('#roles-error').show();
                    setTimeout(function () {
                        $('#roles-error').hide();
                    }, 3000);
                }
            }
        });

    });

}