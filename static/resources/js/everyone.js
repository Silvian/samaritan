$(document).ready(function(){

    //enable the powerful data table sorting, pagination and searching controls
    var everyone_table = $('#everyone-list').DataTable({
    'ajax': {
        "type"   : "GET",
        "url"    : '/api/everyone/getActive',

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

    $("#add-person-button").click(function(event) {
        clearFields();
        $('#member-id').val("");
        $('#address-id').val("");
        $('#create-address').show();
        $('#required-fields-alert').hide();
        $('#member-modal-label').html("Add new person");
        $('#is_member').prop('checked', false);
        $('#terminate-member').hide();
        $("#add-member-modal").modal('show');
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
        terminateMember(everyone_table);
    });

    $("#save-member").click(function(event) {
        addMember(everyone_table);
    });

    $('#everyone-list').on("click", 'button', function() {
        clearFields();
        var id = this.id.split('edit-');
        editMember(id[1], everyone_table, "Person details");
    });

});