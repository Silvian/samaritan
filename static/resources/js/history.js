$(document).ready(function(){

    var rolesData = loadChurchRoles();

    if(rolesData) {

        //enable the powerful data table sorting, pagination and searching controls
        var historical_table = $('#historical-list').DataTable({
        'ajax': {
            "type"   : "GET",
            "url"    : '/api/history/getRecords',

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
                {"mRender": function(data, type, row) {
                                return getGDPR(htmlEntities(row.fields.gdpr));
                            }
                },
                {"mRender": function(data, type, row) {
                                return htmlEntities(getRoleName(rolesData, row.fields.church_role));
                            }
                },
                {"mRender": function (data, type, row) {
                                return '<button type="button" class="btn btn-default btn-sm" id="edit-'+ htmlEntities(row.pk)
                                +'"><i class="fa fa-pencil-square-o fa-fw"></i></td>';
                            }
                },
            ],

        });
    }

    $('#is_baptised').click(function() {
        $('#baptismal_details')[this.checked ? "show" : "hide"]();
    });

    $('#is_member').click(function() {
        $('#membership_details')[this.checked ? "show" : "hide"]();
    });

    $('#historical-list').on("click", 'button', function() {
        clearFields();
        var id = this.id.split('edit-');
        editMember(id[1], historical_table, "Person details");
    });

    $('#delete-member').click(function () {
        $('#delete-modal-label').html("Delete this record permanently?");
        $('#delete-modal').modal('show');
    });

    $('#reinstate-member').click(function() {
        ecblockui();
        $.ajax({
            type: 'POST',
            url: '/api/members/reinstate',
            dataType: 'json',
            data: { id: $('#member-id').val(),
                    csrfmiddlewaretoken : getCookie('csrftoken')
                    },
            success: function (data) {
                ecunblockui();
                $("#add-member-modal").modal('hide');
                historical_table.ajax.reload();
            }
        });
    });

    $('#delete-confirm').click(function () {
        ecblockui();
        $.ajax({
            type: 'POST',
            url: '/api/members/delete',
            dataType: 'json',
            data: {id : $('#member-id').val(),
                   csrfmiddlewaretoken : getCookie('csrftoken')
                   },
            success: function (data) {
                ecunblockui();
                $('#delete-modal').modal('hide');
                $("#add-member-modal").modal('hide');
                historical_table.ajax.reload();
            }
        });
    });

    detailsToggle();

});