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

function standardDate(date_string) {

    if(date_string != "") {

        var date = date_string.split("/");
        var day = date[0];
        var month = date[1];
        var year = date[2];
        var standard = year+"-"+month+"-"+day;

        return standard;
    }
}

function europeanDate(date_string) {

    if(date_string != null) {

        date = new Date(date_string);

        function pad(s) {
            return (s < 10) ? '0' + s : s;
        }

        return [pad(date.getDate()), pad(date.getMonth()+1), date.getFullYear()].join('/');
    }

}

function getEmailLink(email) {
    return '<a href="mailto:'+email+'">'+email+'</a>';
}

function getGDPR(gdpr) {
    if(gdpr) {
        return 'Yes';
    }
    else {
        return 'No';
    }
}

// function to protect against cross site scripting by escaping html entities
function htmlEntities(str) {
    var formatted = "";

    if(str) {
        formatted = String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }
    return formatted;
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

function setCheckbox(checkboxId, value) {

     if(value) {
        $(checkboxId).prop('checked', true);
     }

     else {
        $(checkboxId).prop('checked', false);
     }

}

// function to retrieve any parameter directly from URL, simply call function and specify parameter name you wish to retrieve.
function getURLParameter(sParam){

	var sPageURL = window.location.search.substring(1);
	var sURLVariables = sPageURL.split('&');

	for(var i = 0; i < sURLVariables.length; i++){

		var sParameterName = sURLVariables[i].split('=');

		if(sParameterName[0] == sParam){

			return sParameterName[1];
		}
	}
}

// function to see if a date is inserted in a valid format

function dateFormatValidator(date){
    patt = /\d\d.\d\d.\d\d\d\d/i;
    if (date.search(patt) == -1){

        return false;
    }
    else{

        return true;
    }
}
