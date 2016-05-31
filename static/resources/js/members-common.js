function loadAddresses() {
    ecblockui();
    $("#address-select").html("");

    $.ajax({
        type: 'GET',
        url: '/api/addresses/getAll',
        dataType: 'json',
        success: function (data) {
            ecunblockui();
            var options = '';
            $.each(data, function(i, item) {
                options += '<option value="' + data[i].pk + '">' + data[i].fields.number + ' ' + data[i].fields.street +
                 ' ' + data[i].fields.locality + ', ' + data[i].fields.city + ', ' + data[i].fields.post_code + '</option> ';
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
        success: function (data) {
            ecunblockui();
            var options = '';
            $.each(data, function(i, item) {
                options += '<option value="' + data[i].pk + '">' + data[i].fields.name + '</option> ';
            });
            $("#membership-type-select").append(options);
            $("#membership-type-select").select2('val', 1);
        }
    });
}

function loadChurchRoles() {
    ecblockui();
    $("#church-role-select").html("");
    $.ajax({
        type: 'GET',
        url: '/api/roles/getAll',
        dataType: 'json',
        success: function (data) {
            ecunblockui();
            var options = '';
            $.each(data, function(i, item) {
                options += '<option value="' + data[i].pk + '">' + data[i].fields.name + '</option> ';
            });
            $("#church-role-select").append(options);
            $("#church-role-select").select2('val', 1);
        }
    });

}

function addMember(members_table) {

    new_address = false;

    if($('select[name=address-select]').val()==null && $('#member-id').val()=="") {
        new_address = true;
        if($('#street').val()=="" || $('#city').val()=="" || $('#post_code').val()=="") {

           $('#required-fields-alert').show();
        }
    }

    if($('#first_name').val()=="" || $('#last_name').val()=="" || $('#date_of_birth').val()=="" ||
         $('select[name=church-role-select]').val()==null) {

        $('#required-fields-alert').show();

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

    /* Send the data using post */
    var posting = $.post( url, {
                      id              : id,
                      first_name      : $('#first_name').val(),
                      last_name       : $('#last_name').val(),
                      date_of_birth   : standardDate($('#date_of_birth').val()),
                      telephone       : $('#telephone').val(),
                      email           : $('#email').val(),
                      address         : address,
                      is_baptised     : is_baptised,
                      baptismal_date  : standardDate($('#baptismal_date').val()),
                      baptismal_place : $('#baptismal_place').val(),
                      is_member       : is_member,
                      membership_type : $('select[name=membership-type-select]').val(),
                      membership_date : standardDate($('#membership_date').val()),
                      church_role     : $('select[name=church-role-select]').val(),
                      is_active       : true,
                      csrfmiddlewaretoken : getCookie('csrftoken')
    });

    /* Alerts the results */
    posting.done(function( data ) {
        if(data.success) {
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

             setCheckbox('#is_member', member.fields.is_member);
             setCheckbox('#is_baptised', member.fields.is_baptised);
             $('#baptismal_place').val(member.fields.baptismal_place);
             $('#baptismal_date').val(europeanDate(member.fields.baptismal_date));
             $('#membership_date').val(europeanDate(member.fields.membership_date));

             editMembershipType(member.fields.membership_type);

             editRole(member.fields.church_role);

             if($('#is_baptised').prop("checked") == true){
                 $('#baptismal_details').show();
             }
             else if($('#is_baptised').prop("checked") == false){
                 $('#baptismal_details').hide();
             }

             $('#required-fields-alert').hide();
             $('#member-modal-label').html(title);
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
	        var address_string = address.fields.number+' '+address.fields.street+' '+address.fields.locality+' '
                                    +address.fields.city+' '+address.fields.post_code;
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
	        $('#membership-type').html(membershipType.fields.name);

            $('select[name=membership-type-select] option:selected').attr("selected", null);
            $('select[name=membership-type-select] option[value="'+membershipType.pk+'"]').attr("selected","selected");

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
	        $('#church-role').html(role.fields.name);

            $('select[name=church-role-select] option:selected').attr("selected", null);
            $('select[name=church-role-select] option[value="'+role.pk+'"]').attr("selected","selected");

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
   $('#is_baptised').prop('checked', false);
   $('#baptismal_date').val("");
   $('#baptismal_place').val("");
   $('#church-role').html("");
   $('#membership-type').html("");
   $('#membership_date').val("");
   $('#baptismal_details').hide();



}