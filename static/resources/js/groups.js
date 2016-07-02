$(document).ready(function(){

    $('#groups-error').hide();

    getGroups();

    $('#add-group-button').click(function() {
        clearGroupFields();
        $('#group-modal-label').html("Add a new group");
        $('#required-fields-alert').hide();
        $('#group-modal').modal('show');
    });

    $('#save-group').click(function() {
        saveGroup();
    });

    $('#groups-list').on("click", '[id^="view-"]', function() {
        var id = this.id.split('view-');
        editGroup(id[1]);
    });

    $('#groups-list').on("click", '[id^="remove-"]', function() {
        var id = this.id.split('remove-');
        $('#delete-id').val(id[1]);
        $('#delete-modal-label').html("Delete group?");
        $('#delete-modal').modal('show');
    });

    $('#delete-confirm').click(function() {
        deleteGroup($('#delete-id').val());
    });

});

function getGroups() {

    ecblockui();
    $('#groups-empty').hide();
    $('#groups-list tbody').html("");

    $.ajax({
        type: 'GET',
        url: '/api/groups/getAll',
        dataType: 'json',
        success: function (data) {
            ecunblockui();
            if(data && data.length > 0) {
                $('#groups-list tbody').html("");

                $.each(data, function(i, item) {
                    var group = item.fields;
                    $('#groups-list tbody').append('<tr>' +
                        '<td><a href="/views/group_members?id=' + item.pk + '">' + group.name + '</a></td>' +
                        '<td>' + group.description + '</td>' +
                        '<td><button type="button" class="btn btn-default btn-sm" id="view-'+ item.pk +'"><i class="fa fa-edit fa-fw"></i></td>' +
                        '<td><button type="button" class="btn btn-danger btn-sm" id="remove-'+ item.pk +'"><i class="fa fa-trash fa-fw"></i></td>' +
                    '</tr>');
                });

            }

            else {
                $('#groups-empty').show();
            }

        }
    });

}

function saveGroup() {

    $('#required-fields-alert').hide();

    if($('#group-name').val()!="") {

        var id = null;
        if($('#group-id').val()!="") {
            id = $('#group-id').val();
            url = '/api/groups/update';
        }
        else {
            url = '/api/groups/add';
        }

        ecblockui();
        $.ajax({
            type: 'POST',
            url: url,
            dataType: 'json',
            data: {    id : id,
                       name : $('#group-name').val(),
                       description : $('#group-description').val(),
                       csrfmiddlewaretoken : getCookie('csrftoken')
                    },
            success: function (data) {
                ecunblockui();
                $("#group-modal").modal('hide');
                getGroups();
            }
        });

    }

    else {
       $('#required-fields-alert').show();
    }

}

function editGroup(id) {

    clearGroupFields();
    $('#group-modal-label').html("Edit group");
    $('#group-modal').modal('show');
    ecblockui();
    $.ajax({
        type: 'GET',
        url: '/api/groups/getSingle',
        dataType: 'json',
        data: { id : id },
        success: function (data) {
            ecunblockui();
            var group = data[0];
            $('#group-id').val(group.pk);
            $('#group-name').val(group.fields.name);
            $('#group-description').val(group.fields.description);
        }
    });

}

function deleteGroup(id) {

    $('#delete-modal').modal('hide');

    ecblockui();
    $.ajax({
        type: 'POST',
        url: '/api/groups/delete',
        dataType: 'json',
        data: {    id : id,
                   csrfmiddlewaretoken : getCookie('csrftoken')
                },
        success: function (data) {
            ecunblockui();
            if(data.success) {
                getGroups();
            }
            else {
                $('#error-msg').html(data.error);
                $('#groups-error').show();
                setTimeout(function () {
                    $('#groups-error').hide();
                }, 3000);
            }
        }
    });

}

function clearGroupFields() {

    $('#group-id').val("");
    $('#group-name').val("");
    $('#group-description').val("");

}