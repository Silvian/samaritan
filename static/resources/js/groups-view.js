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
                $('#group-name').html(htmlEntities(group.fields.name));

                //enable the powerful data table sorting, pagination and searching controls
                var group_members_table = $('#group-members-list').DataTable({
                'ajax': {
                    "type"   : "GET",
                    "url"    : '/api/groups/getMembers?id='+id+'',
                    "dataSrc": ""
                },
                    'columns': [
                        {"mRender": function(data, type, row) {
                            return htmlEntities(row.fields.first_name);
                                    }
                        },
                        {"mRender": function(data, type, row) {
                                        return htmlEntities(row.fields.last_name);
                                    }
                        },
                        {"mRender": function(data, type, row) {
                                        return htmlEntities(row.fields.telephone);
                                    }
                        },
                        {"mRender": function(data, type, row) {
                                        return getEmailLink(htmlEntities(row.fields.email));
                                    }
                        },
                        {"mRender": function (data, type, row) {
                                        return '<button type="button" class="btn btn-danger btn-sm" id="remove-'+ htmlEntities(row.pk)
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

                $('#email-group-members').click(function(event) {
                    $('#email-modal-label').html("Send email to all "+htmlEntities(group.fields.name)+" group members");
                    $('#email-modal').modal('show');
                });

                $('#send-email').click(function(event) {
                    sendGroupEmail(id);
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

function sendGroupEmail(group_id) {

    $('#email-required-fields-alert').hide();

    if($('#email-subject').val()!="" && $('#email-message').val()!="") {

        $('#email-modal').modal('hide');
        $('#email-sending').show();
        $.ajax({
            type: 'POST',
            url: '/email/send/group',
            dataType: 'json',
            data: {id     : group_id,
                   subject: $('#email-subject').val(),
                   message: $('#email-message').val(),
                   csrfmiddlewaretoken : getCookie('csrftoken')
                   },
            success: function (data) {
                $('#email-sending').hide();
                if(data.success) {
                    $('#email-success').show();
                    setTimeout(function () {
                        $('#email-success').hide();
                    }, 3000);
                }
                else {
                    $('#email-error').val(data.error);
                    $('#email-error').show();
                    setTimeout(function () {
                        $('#email-error').hide();
                    }, 3000);
                }
            }
        });

    }

    else {
        $('#email-required-fields-alert').show();
    }

}