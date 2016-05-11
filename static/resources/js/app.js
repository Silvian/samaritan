$(document).ready(function(){
	
	//enable the powerful data table sorting, pagination and searching controls
    var members_table = $('#members-list').DataTable({
    'ajax': {
        "type"   : "GET",
        "url"    : 'api/members/getActive',

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

    loadAddresses();

    loadChurchRoles();

    $("#address-select").select2({
        dropdownAutoWidth: true,
        width: '100%',
        placeholder: "Select an existing address",
        allowClear: true,
    });

    $("#church-role-select").select2({
        dropdownAutoWidth: true,
        width: '100%',
        placeholder: "Select a church role",
        allowClear: true,
    });

    $('.datepicker').datepicker();

    $("#add-member-button").click(function(event) {
        $('#new-address').hide();
        $('#required-fields-alert').hide();
        $("#add-member-modal").modal('show');
    });

    $("#create-address").click(function(event) {
        $('#new-address').show();
    });

    $("#save-member").click(function(event) {
        addMember(members_table);
    });


});

function loadAddresses() {
    ecblockui();
    $("#address-select").html("");

    $.ajax({
        type: 'GET',
        url: 'api/addresses/get',
        dataType: 'json',
        success: function (data) {
            ecunblockui();
            var options = '';
            $.each(data, function(i, item) {
                options += '<option value="' + data[i].pk + '">' + data[i].fields.number + ' ' + data[i].fields.street + ' ' + data[i].fields.locality + ', ' + data[i].fields.city + ', ' + data[i].fields.post_code + '</option> ';
            });
            $("#address-select").append(options);
            $("#address-select").select2('val', 1);
        }
    });

}

function loadChurchRoles() {
    ecblockui();
    $.ajax({
        type: 'GET',
        url: 'api/roles',
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

    if($('select[name=address-select]').val()==null) {
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

        if(new_address) {
            submitAddAddress(members_table);
        }

        else {
            submitAddMember(members_table, null);
        }

    }

}

function submitAddAddress(members_table) {

    url = 'api/addresses/add';

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
            submitAddMember(members_table, data.address);
            loadAddresses();
        }

    });

}

function submitAddMember(members_table, addressId) {

    url = 'api/members/add';

    var address;

    if(addressId != null) {
        address = addressId;
    }

    else {
       address = $('select[name=address-select]').val();
    }

    /* Send the data using post */
    var posting = $.post( url, {
                      first_name     : $('#first_name').val(),
                      last_name      : $('#last_name').val(),
                      date_of_birth  : $('#date_of_birth').val(),
                      telephone      : $('#telephone').val(),
                      email          : $('#email').val(),
                      address        : address,
                      is_baptised    : $('#is_baptised').val(),
                      baptismal_date : $('#baptismal_date').val(),
                      is_member      : $('#is_member').val(),
                      church_role    : $('select[name=church-role-select]').val(),
                      is_active      : true,
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

function getFormattedDate(date) {
    var month = date.getMonth() + 1;
    var day = date.getDate();
    var year = date.getFullYear();
    var input = month + "/" + day + "/" + year;

    var pattern=/(.*?)\/(.*?)\/(.*?)$/;
    var result = input.replace(pattern, function(match, p1, p2, p3) {
        var months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
        return (p2<10?"0"+p2:p2)+" "+months[(p1-1)]+" "+p3;
    });

    return result;
}

function getEmailLink(email) {
    return '<a href="mailto:'+email+'">'+email+'</a>';
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }

    return cookieValue;
}

function ecblockui() {

    $.blockUI({ message: '', baseZ: 2000});
    $.fancybox.showLoading();

}

function ecunblockui() {

    $.unblockUI();
    $.fancybox.hideLoading();

}