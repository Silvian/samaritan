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

    var rolesData = loadChurchRoles();

    if(rolesData) {

        //enable the powerful data table sorting, pagination and searching controls
        var members_table = $('#members-list').DataTable({
        'ajax': {
            "type"   : "GET",
            "url"    : '/api/members/getActive',

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

    $("#add-member-button").click(function(event) {
        clearFields();
        $('#member-id').val("");
        $('#address-id').val("");
        $('#create-address').show();
        $('#required-fields-alert').hide();
        $('#date-format-alert').hide();
        $('#member-modal-label').html("Add new member");
        $('#is_member').prop('checked', true);
        $('#terminate-member').hide();
        $('#membership_details').show();
        $("#add-member-modal").modal('show');
        get_profile_image($('#member-id').val());
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
        terminateMember(members_table);
    });

    $("#save-member").click(function(event) {
        addMember(members_table);
    });

    $('#members-list').on("click", 'button', function() {
        clearFields();
        var id = this.id.split('edit-');
        editMember(id[1], members_table, "Member details");
    });

    $('#email-members').click(function(event) {
        $('#email-modal-label').html("Send email to all members");
        $('#email-modal').modal('show');
    });

    $('#send-email').click(function(event) {
        sendEmail('/email/send/members');
    });

    loadAddresses();

    loadMembershipTypes();

    detailsToggle();

});