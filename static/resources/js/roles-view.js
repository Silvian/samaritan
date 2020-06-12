$(document).ready(function(){

    $("#address-select").select2({
        dropdownAutoWidth: true,
        width: '100%',
        placeholder: "Select an existing address",
        allowClear: true,
    });

    $("#membership-type-select").select2({
        dropdownAutoWidth: true,
        width: '100%',
        placeholder: "Select membership type",
        allowClear: true,
    });

    $("#church-role-select").select2({
        dropdownAutoWidth: true,
        width: '100%',
        placeholder: "Select a church role",
        allowClear: true,
    });

    $('.datepicker').datepicker({
        format: 'dd/mm/yyyy'
    });

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
                                if(row.fields.date_of_birth){
                                    return getFormattedDate(new Date(htmlEntities(row.fields.date_of_birth)));
                                }
                                else{
                                    return "";
                                }
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
                                        return '<button type="button" class="btn btn-default btn-sm" id="edit-'+ htmlEntities(row.pk)
                                        +'"><i class="fa fa-pencil-square-o fa-fw"></i></td>';
                                    }
                        },

                    ],

                });

                $('#is_baptised').click(function() {
                    $('#baptismal_details')[this.checked ? "show" : "hide"]();
                });

                $('#is_member').click(function() {
                    $('#membership_details')[this.checked ? "show" : "hide"]();
                });

                $("#create-address").click(function(event) {
                    $('#new-address').show();
                });

                $("#clear-member").click(function(event) {
                    clearFields();
                });

                $("#terminate-member").click(function(event) {
                    terminateMember(role_members_table);
                });

                $("#save-member").click(function(event) {
                    addMember(role_members_table);
                });

                $('#role-members-list').on("click", 'button', function() {
                    clearFields();
                    var id = this.id.split('edit-');
                    editMember(id[1], role_members_table, "Person details");
                });

                $('#download-role-members').click(function() {
                    location.href="/export/download/role/excel?id="+id;
                });

                loadAddresses();

                loadMembershipTypes();

                detailsToggle();

            }
        });

    }

});
