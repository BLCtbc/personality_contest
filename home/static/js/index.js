window.addEventListener("load", function(e) {
	eventHandlers();
	window.setTimeout(function() {
		console.log("loaded")
	}, 250)
});



function eventHandlers() {
    var mailingList = document.querySelector("#mailing_list")
	mailingList.addEventListener("submit", emailSignup)
}

function emailSignup(e) {
    e.preventDefault()
    var request = new XMLHttpRequest(),
        fd = new FormData(document.querySelector("#mailing_list"));

    request.addEventListener("load", requestSuccess)
    request.addEventListener("error", requestError)
    request.addEventListener("abort", requestAborted)

    request.open("POST", "/mailing_list")
    // request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded'); // tells server what format to expect request data in
    // request.setRequestHeader('X-CSRFToken', getCookie('csrftoken')) // only necessary if {% csrf_token %} not set
    request.setRequestHeader('X-Requested-With', 'XMLHttpRequest')
    request.send(fd);

}

function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = cookies[i].trim();
			if (cookie.substring(0, name.length + 1) === (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}

function requestSuccess() {
    var response = JSON.parse(this.responseText)
    window.alert(`successfully added ${response.email} to mailing list!`)
}

function requestError() {
    console.log('error: ', this.responseText)
}

function requestAborted() {
    // do stuff
    console.log('aborted: ', this.responseText)

}
