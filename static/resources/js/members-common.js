function loadAddresses() {
    ecblockui();
    $("#address-select").html("");

    $.ajax({
        type: 'GET',
        url: '/api/addresses/getAll',
        dataType: 'json',
        async: false,
        success: function (data) {
            ecunblockui();
            var options = '';
            $.each(data, function(i, item) {
                options += '<option value="' + htmlEntities(data[i].pk) + '">' + htmlEntities(data[i].fields.number) + ' ' + htmlEntities(data[i].fields.street) +
                 ' ' + htmlEntities(data[i].fields.locality) + ', ' + htmlEntities(data[i].fields.city) + ', ' + htmlEntities(data[i].fields.post_code) + '</option> ';
            });
            $("#address-select").append(options);
            $("#address-select").select2('val', 1);
        }
    });

}

function loadMembershipTypes() {
    ecblockui();
    $("#membership-type-select").html("");
    $.ajax({
        type: 'GET',
        url: '/api/membership/getTypes',
        dataType: 'json',
        async: false,
        success: function (data) {
            ecunblockui();
            var options = '';
            $.each(data, function(i, item) {
                options += '<option value="' + htmlEntities(data[i].pk) + '">' + htmlEntities(data[i].fields.name) + '</option> ';
            });
            $("#membership-type-select").append(options);
            $("#membership-type-select").select2('val', 1);
        }
    });
}

function loadChurchRoles() {
    var results = null;
    ecblockui();
    $("#church-role-select").html("");
    $.ajax({
        type: 'GET',
        url: '/api/roles/getAll',
        dataType: 'json',
        async: false,
        success: function (data) {
            results = data;
            ecunblockui();
            var options = '';
            $.each(data, function(i, item) {
                options += '<option value="' + htmlEntities(data[i].pk) + '">' + htmlEntities(data[i].fields.name) + '</option> ';
            });
            $("#church-role-select").append(options);
            $("#church-role-select").select2('val', 1);
        }
    });

    return results;
}

function getRoleName(data, key) {

    for (i = 0; i < data.length; i++) {
        if(data[i].pk === key){
            return data[i].fields.name;
        }
    }

}

function addMember(members_table) {

    new_address = false;

    if($('select[name=address-select]').val()==null && $('#member-id').val()=="") {
        new_address = true;
        if($('#street').val()=="" || $('#city').val()=="" || $('#post_code').val()=="") {

           $('#required-fields-alert').show();
        }
    }

    if($('#first_name').val()=="" || $('#last_name').val()=="" || $('select[name=church-role-select]').val()==null || $('#date_of_birth').val()==""){
        $('#required-fields-alert').show();

    }
    else if(!dateFormatValidator($('#date_of_birth').val())){
        $('#date-format-alert').show();

    }
    else {

        if(new_address || $('#post_code').val()!="") {
            submitAddress(members_table);
        }

        else {
            submitMember(members_table, null);
        }

    }

}

function submitAddress(members_table) {

    url = '/api/addresses/add';

    var posting = $.post( url, {
                  number    : $('#number').val(),
                  street    : $('#street').val(),
                  locality  : $('#locality').val(),
                  city      : $('#city').val(),
                  post_code : $('#post_code').val(),
                  csrfmiddlewaretoken : getCookie('csrftoken')
    });

        posting.done(function( data ) {
        if(data.address) {
            submitMember(members_table, data.address);
            loadAddresses();
        }

    });

}

function submitMember(members_table, addressId) {

    ecblockui();

    id = $('#member-id').val();

    if(id == "") {
        id = null;
        url = '/api/members/add';
    }

    else {
        url = '/api/members/update';
    }

    var address;

    if(addressId != null) {
        address = addressId;
    }

    else if ($('select[name=address-select]').val() != null){
       address = $('select[name=address-select]').val();
    }

    else if($('#address-id').val()!="") {
        address = $('#address-id').val();
    }

    var is_member = false;

    if($('#is_member').prop("checked") == true){
        is_member = true;
    }

    var is_baptised = false;

    if($('#is_baptised').prop("checked") == true){
         is_baptised = true;
    }

    var gdpr = false;

    if($('#gdpr').prop("checked") == true){
         gdpr = true;
    }

    /* Send the data using post */
    var posting = $.post( url, {
                      id              : id,
                      first_name      : $('#first_name').val(),
                      last_name       : $('#last_name').val(),
                      date_of_birth   : standardDate($('#date_of_birth').val()),
                      telephone       : $('#telephone').val(),
                      email           : $('#email').val(),
                      address         : address,
                      details         : $('#details').val(),
                      is_baptised     : is_baptised,
                      baptismal_date  : standardDate($('#baptismal_date').val()),
                      baptismal_place : $('#baptismal_place').val(),
                      is_member       : is_member,
                      membership_type : $('select[name=membership-type-select]').val(),
                      membership_date : standardDate($('#membership_date').val()),
                      church_role     : $('select[name=church-role-select]').val(),
                      gdpr            : gdpr,
                      is_active       : true,
                      csrfmiddlewaretoken : getCookie('csrftoken')
    });

    /* Alerts the results */
    posting.done(function( data ) {
        if(data.success) {
            ecunblockui();
            $("#add-member-modal").modal('hide');
            members_table.ajax.reload();
        }

    });

}

function editMember(id, members_table, title) {
    ecblockui();
    $.ajax({
	    type: 'GET',
	    url: '/api/members/getMember',
	    dataType: 'json',
	    data: { id: id},
	    success: function (data) {
	         ecunblockui();
	         var member = data[0];

             $('#member-id').val(member.pk);
             $('#first_name').val(member.fields.first_name);
             $('#last_name').val(member.fields.last_name);
             $('#date_of_birth').val(europeanDate(member.fields.date_of_birth));
             $('#telephone').val(member.fields.telephone);
             $('#email').val(member.fields.email);
             $('#address-id').val(member.fields.address);
             editAddress(member.fields.address);

             $('#details').val(member.fields.details);

             setCheckbox('#is_member', member.fields.is_member);
             setCheckbox('#is_baptised', member.fields.is_baptised);
             setCheckbox('#gdpr', member.fields.gdpr);
             $('#baptismal_place').val(member.fields.baptismal_place);

             if (!dateFormatValidator($('#baptismal_date').val())){
                $('date-format-alert').show();
            }
            else{
               $('#baptismal_date').val(europeanDate(member.fields.baptismal_date));
            }

            if (!dateFormatValidator($('#membership_date').val())){
                 $('date-format-alert').show();
             }
            else{
                $('#membership_date').val(europeanDate(member.fields.membership_date));
             }
             editMembershipType(member.fields.membership_type);

             editRole(member.fields.church_role);

             if($('#is_baptised').prop("checked") == true){
                 $('#baptismal_details').show();
             }
             else if($('#is_baptised').prop("checked") == false){
                 $('#baptismal_details').hide();
             }

             if($('#is_member').prop("checked") == true){
                 $('#membership_details').show();
             }
             else if($('#is_member').prop("checked") == false){
                 $('#membership_details').hide();
             }

             $('#additional-notes').val(member.fields.notes);

             $('#required-fields-alert').hide();
             $('#date-format-alert').hide();
             $('#member-modal-label').html(title);
             $('#terminate-member').show();
             $("#add-member-modal").modal('show');
	    }
	});

}

function editAddress(address_id) {
    ecblockui();
    $.ajax({
	    type: 'GET',
	    url: '/api/addresses/getAddress',
	    dataType: 'json',
	    data: { id: address_id},
	    success: function (data) {
	        ecunblockui();
	        var address=data[0];
	        var address_string = htmlEntities(address.fields.number)+' '+htmlEntities(address.fields.street)+' '+htmlEntities(address.fields.locality)+' '
                                    +htmlEntities(address.fields.city)+' '+htmlEntities(address.fields.post_code);
            var map = '<i class="fa fa-map-marker" aria-hidden="true"></i> ';
            $('#address').html(map + address_string);
            $('#address').attr('href','http://google.co.uk/maps/place/'+address_string);
            $('#address').attr('target','_');
            $('#address-group').show();
	    }
    });

}

function editMembershipType(membership_type_id) {
    loadMembershipTypes();
    $.ajax({
	    type: 'GET',
	    url: '/api/membership/getSingle',
	    dataType: 'json',
	    data: { id: membership_type_id},
	    success: function (data) {
	        var membershipType=data[0];
	        $('#membership-type').html(htmlEntities(membershipType.fields.name));

            $('select[name=membership-type-select] option:selected').attr("selected", null);
            $('select[name=membership-type-select] option[value="'+htmlEntities(membershipType.pk)+'"]').attr("selected","selected");

            $("#membership-type-select").select2({
                val: membershipType.pk,
                dropdownAutoWidth: true,
                width: '100%',
                placeholder: "Select membership type",
                allowClear: true,
            });

	    }
    });

}

function editRole(role_id) {
    loadChurchRoles();
    $.ajax({
	    type: 'GET',
	    url: '/api/roles/getSingle',
	    dataType: 'json',
	    data: { id: role_id},
	    success: function (data) {
	        var role=data[0];
	        $('#church-role').html(htmlEntities(role.fields.name));

            $('select[name=church-role-select] option:selected').attr("selected", null);
            $('select[name=church-role-select] option[value="'+htmlEntities(role.pk)+'"]').attr("selected","selected");

            $("#church-role-select").select2({
                val: role.pk,
                dropdownAutoWidth: true,
                width: '100%',
                placeholder: "Select a church role",
                allowClear: true,
            });

	    }
    });

}

function terminateMember(members_table) {

    $("#terminate-member-modal-label").html("Confirm termination?");
    $("#terminate-member-modal").modal('show');

    url = '/api/members/terminate';
    id = $('#member-id').val();

    $("#terminate-member-confirm").click(function(event) {
        notes = $('#additional-notes').val();
        /* Send the data using post */
        ecblockui();
        var posting = $.post( url, {
                          id    : id,
                          notes : notes,
                          csrfmiddlewaretoken : getCookie('csrftoken')
        });

        /* Alerts the results */
        posting.done(function( data ) {
            if(data.success) {
                ecunblockui();
                $("#terminate-member-modal").modal('hide');
                $("#add-member-modal").modal('hide');
                members_table.ajax.reload();
            }

        });

    });

}

function clearFields() {

   $('#new-address').hide();
   $('#address-group').hide();
   $('#first_name').val("");
   $('#last_name').val("");
   $('#date_of_birth').val("");
   $('#telephone').val("");
   $('#email').val("");
   $('#address').html("");
   $('#number').val("");
   $('#street').val("");
   $('#locality').val("");
   $('#city').val("");
   $('#post_code').val("");
   $('#details').val("");
   $('#is_baptised').prop('checked', false);
   $('#gdpr').prop('checked', false);
   $('#baptismal_date').val("");
   $('#baptismal_place').val("");
   $('#church-role').html("");
   $('#membership-type').html("");
   $('#membership_date').val("");
   $('#baptismal_details').hide();


}

//toggle between open and closed details
function detailsToggle() {

    //hide/show details open/closed
    $("[id^=toggle-]").click(function(event) {
        $('#details-area').toggle();

        $(this).html($(this).html() == '<i class="fa fa-minus-circle fa-fw"></i> Hide' ? '<i class="fa fa-plus-circle fa-fw"></i> Show' : '<i class="fa fa-minus-circle fa-fw"></i> Hide');

    });

}

function sendEmail(url) {

    $('#email-required-fields-alert').hide();

    if($('#email-subject').val()!="" && $('#email-message').val()!="") {

        $('#email-modal').modal('hide');
        $('#email-sending').show();
        $.ajax({
            type: 'POST',
            url: url,
            dataType: 'json',
            data: {subject: $('#email-subject').val(),
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
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                $('#email-error').val("Internal server error! Emails could not be sent.");
                $('#email-error').show();
                setTimeout(function () {
                    $('#email-error').hide();
                }, 3000);
            }
        });

    }

    else {
        $('#email-required-fields-alert').show();
    }

}