$(document).ready(function(){

    //enable the powerful data table sorting, pagination and searching controls
    var historical_table = $('#historical-list').DataTable({
    'ajax': {
        "type"   : "GET",
        "url"    : '/api/history/getRecords',

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
            {"mRender": function (data, type, row) {
                            return '<button type="button" class="btn btn-default btn-sm" id="edit-'+ row.pk
                            +'"><i class="fa fa-pencil-square-o fa-fw"></i></td>';
                        }
            },
        ],

    });

    loadAddresses();

    loadMembershipTypes();

    loadChurchRoles();

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

    $('#reinstate-member').click(function() {
        $.ajax({
            type: 'POST',
            url: '/api/history/reinstate',
            dataType: 'json',
            data: { id: $('#member-id').val(),
                    csrfmiddlewaretoken : getCookie('csrftoken')
                    },
            success: function (data) {
                $("#add-member-modal").modal('hide');
                historical_table.ajax.reload();
            }
        });
    });

});