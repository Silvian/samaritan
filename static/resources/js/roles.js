$(document).ready(function(){

    $('#roles-error').hide();

    getRoles();

    $('#add-role-button').click(function() {
        clearRoleFields();
        $('#role-modal-label').html("Add a new role");
        $('#required-fields-alert').hide();
        $('#role-modal').modal('show');
    });

    $('#save-role').click(function() {
        saveRole();
    });

    $('#roles-list').on("click", '[id^="view-"]', function() {
        var id = this.id.split('view-');
        editRole(id[1]);
    });

    $('#roles-list').on("click", '[id^="remove-"]', function() {
        var id = this.id.split('remove-');
        $('#delete-id').val(id[1]);
        $('#delete-modal-label').html("Delete role?");
        $('#delete-modal').modal('show');
    });

    $('#delete-confirm').click(function() {
        deleteRole($('#delete-id').val());
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
                        '<td><a href="/views/role_members?id=' + item.pk + '">' + role.name + '</a></td>' +
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

function saveRole() {

    $('#required-fields-alert').hide();

    if($('#role-name').val()!="") {

        var id = null;
        if($('#role-id').val()!="") {
            id = $('#role-id').val();
            url = '/api/roles/update';
        }
        else {
            url = '/api/roles/add';
        }

        ecblockui();
        $.ajax({
            type: 'POST',
            url: url,
            dataType: 'json',
            data: {    id : id,
                       name : $('#role-name').val(),
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

function editRole(id) {

    clearRoleFields();
    $('#role-modal-label').html("Edit role");
    $('#role-modal').modal('show');
    ecblockui();
    $.ajax({
        type: 'GET',
        url: '/api/roles/getSingle',
        dataType: 'json',
        data: { id : id },
        success: function (data) {
            ecunblockui();
            var role = data[0];
            $('#role-id').val(role.pk);
            $('#role-name').val(role.fields.name);
            $('#role-description').val(role.fields.description);
        }
    });

}

function deleteRole(id) {

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

}

function clearRoleFields() {

    $('#role-id').val("");
    $('#role-name').val("");
    $('#role-description').val("");

}