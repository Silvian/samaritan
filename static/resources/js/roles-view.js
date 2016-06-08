$(document).ready(function(){

    var id = getURLParameter("id");

    if(id != null) {
        ecblockui();
        $.ajax({
            type: 'GET',
            url: '/api/roles/getSingle',
            dataType: 'json',
            data: { id: id},
            success: function (data) {
                ecunblockui();
                var role=data[0];
                $('#role-name').html(role.fields.name);

                //enable the powerful data table sorting, pagination and searching controls
                var role_members_table = $('#role-members-list').DataTable({
                'ajax': {
                    "type"   : "GET",
                    "url"    : '/api/roles/getMembers?id='+id+'',
                    "dataSrc": ""
                },
                    'columns': [
                        {"data" : "fields.first_name"},
                        {"data" : "fields.last_name"},
                        {"mRender": function(data, type, row) {
                                        return getFormattedDate(new Date(row.fields.date_of_birth));
                                    }
                        },
                        {"data" : "fields.telephone"},
                        {"mRender": function(data, type, row) {
                                        return getEmailLink(row.fields.email);
                                    }
                        },

                    ],

                });

            }
        });

    }

});