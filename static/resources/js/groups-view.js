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

                $('#sms-group-members').click(function(event) {
                    $('#sms-modal-label').html("Send sms to all "+htmlEntities(group.fields.name)+" group members");
                    $('#sms-modal').modal('show');
                });

                $('#send-sms').click(function (event) { 
                    sendGroupSMS(id);
                 });

                fileSizeCheck();
                 
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

        var formData = new FormData();
        formData.append("id", group_id);
        formData.append("subject", $('#email-subject').val());
        formData.append("message", $('#email-message').val());
        formData.append("attachment", $('#file-attachment')[0].files[0]);
        formData.append("csrfmiddlewaretoken", getCookie('csrftoken'));

        $.ajax({
            type: 'POST',
            url: '/email/send/group',
            dataType: 'json',
            data: formData,
            processData: false,
            contentType: false,
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

function sendGroupSMS(group_id) {
    $('#sms-required-fields-alert').hide();
    if($('#sms-message').val() != "") {
        $('#sms-modal').modal('hide');
        $('#sms-sending').show();
        $.ajax({
            type: 'POST',
            url: '/message/send/group',
            dataType: 'JSON',
            data: {
                id: group_id,
                message: $('#sms-message').val(),
                csrfmiddlewaretoken : getCookie('csrftoken')
            },
            success: function (data) { 
                $('#sms-sending').hide();
                if(data.success) {
                    $('#sms-success').show();
                    setTimeout(function () { 
                        $('#sms-success').hide();
                     }, 3000);
                }
                else {
                    $('#sms-error').val(data.error);
                    $('#sms-error').show();
                    setTimeout(function () {
                        $('#sms-error').hide();
                    }, 3000);
                }
             }
        });

    }
    else {
        $('#sms-required-fields-alert').show();
    }
}
