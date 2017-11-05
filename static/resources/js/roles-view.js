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
                $('#role-name').html(htmlEntities(role.fields.name));

                //enable the powerful data table sorting, pagination and searching controls
                var role_members_table = $('#role-members-list').DataTable({
                'ajax': {
                    "type"   : "GET",
                    "url"    : '/api/roles/getMembers?id='+id+'',
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
                                        return getFormattedDate(new Date(htmlEntities(row.fields.date_of_birth)));
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

                    ],

                });

            }
        });

        $('#download-role-members').click(function() {
            location.href="/export/download/role/excel?id="+id;
        });

    }

});