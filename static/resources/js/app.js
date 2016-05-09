$(document).ready(function(){
	
	//enable the powerful data table sorting, pagination and searching controls
    var members_table = $('#members-list').DataTable({
    'ajax': {
        "type"   : "GET",
        "url"    : 'api/members',

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
        $('#required-fields-alert').hide();
        $("#add-member-modal").modal('show');
    });

    $("#save-member").click(function(event) {
        submitAddMember(members_table);
    });


});

function loadAddresses() {
    ecblockui();
    $.ajax({
        type: 'GET',
        url: 'api/addresses',
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

function submitAddMember(members_table) {

    if($('#first_name').val()=="" || $('#last_name').val()=="" || $('#date_of_birth').val()=="" ||
        $('select[name=address-select]').val()=="" || $('select[name=church-role-select]').val()=="") {

        $('#required-fields-alert').show();

    }

    else {

        $('#required-fields-alert').hide();
        url = 'api/addMember';

        /* Send the data using post */
        var posting = $.post( url, {
                          first_name     : $('#first_name').val(),
                          last_name      : $('#last_name').val(),
                          date_of_birth  : $('#date_of_birth').val(),
                          telephone      : $('#telephone').val(),
                          email          : $('#email').val(),
                          address        : $('select[name=address-select]').val(),
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