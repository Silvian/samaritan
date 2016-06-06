$(document).ready(function(){

    getRoles();

    $('#add-role-button').click(function() {
        $('#role-modal-label').html("Add a new role");
        $('#required-fields-alert').hide();
        $('#role-modal').modal('show');
    });

    $('#save-role').click(function() {
        addRole();
    })

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