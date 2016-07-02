$(document).ready(function(){
    var id = getURLParameter("id");

    if(id != null) {
        ecblockui();
        $.ajax({
            type: 'GET',
            url: '/api/groups/getSingle',
            dataType: 'json',
            data: { id: id},
            success: function (data) {
                ecunblockui();
                var group=data[0];
                $('#group-name').html(group.fields.name);

                //enable the powerful data table sorting, pagination and searching controls
                var group_members_table = $('#group-members-list').DataTable({
                'ajax': {
                    "type"   : "GET",
                    "url"    : '/api/groups/getMembers?id='+id+'',
                    "dataSrc": ""
                },
                    'columns': [
                        {"data" : "fields.first_name"},
                        {"data" : "fields.last_name"},
                        {"data" : "fields.telephone"},
                        {"mRender": function(data, type, row) {
                                        return getEmailLink(row.fields.email);
                                    }
                        },
                        {"mRender": function (data, type, row) {
                                        return '<button type="button" class="btn btn-danger btn-sm" id="remove-'+ row.pk
                                        +'"><i class="fa fa-trash fa-fw"></i></td>';
                                    }
                        },

                    ],

                });

                $('#add-group-members').click(function() {
                     window.location = '/views/group_add?id='+id+'';
                });

                $('#group-members-list').on("click", '[id^="remove-"]', function() {
                    var id = this.id.split('remove-');
                    $('#delete-id').val(id[1]);
                    $('#delete-modal-label').html("Remove member from this group?");
                    $('#delete-modal').modal('show');
                });

                $('#delete-confirm').click(function() {
                    deleteGroupMember($('#delete-id').val(), id, group_members_table);
                });

            }
        });

    }

});

function deleteGroupMember(member_id, group_id, group_members_table) {

    $('#delete-modal').modal('hide');

    ecblockui();
    $.ajax({
        type: 'POST',
        url: '/api/groups/memberDelete',
        dataType: 'json',
        data: {    member_id : member_id,
                   group_id  : group_id,
                   csrfmiddlewaretoken : getCookie('csrftoken')
                },
        success: function (data) {
            ecunblockui();
            group_members_table.ajax.reload();
        }
    });

}