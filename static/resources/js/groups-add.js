$(document).ready(function(){
    var id = getURLParameter("id");

    if(id != null) {

        $('#back-group-members').click(function() {
            window.location = '/views/group_members?id='+id+'';
        });

        //enable the powerful data table sorting, pagination and searching controls
        var add_members_table = $('#add-members-list').DataTable({
        'ajax': {
            "type"   : "GET",
            "url"    : '/api/groups/membersToAdd?id='+id+'',
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
                                return '<button type="button" class="btn btn-success btn-sm" id="add-'+ htmlEntities(row.pk)
                                +'"><i class="fa fa-plus-square fa-fw"></i></td>';
                            }
                },

            ],

        });

        $('#add-members-list').on("click", '[id^="add-"]', function() {
            var member_id = this.id.split('add-');
            addGroupMember(member_id[1], id, add_members_table);
        });

    }
});

function addGroupMember(member_id, group_id, add_members_table) {

    ecblockui();
    $.ajax({
        type: 'POST',
        url: '/api/groups/memberAdd',
        dataType: 'json',
        data: {    member_id : member_id,
                   group_id  : group_id,
                   csrfmiddlewaretoken : getCookie('csrftoken')
                },
        success: function (data) {
            ecunblockui();
            add_members_table.ajax.reload();
        }
    });

}
