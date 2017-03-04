function redirectTo(url) {
    window.location = "".concat(url);
}

function clickElement(element) {
    element.click();
}

function runAutomation(automation_name) {
    passMessageToFlask(
        { "function": automation_name },
        (response) => { console.log(response) },
        (error) => { console.log(error) }
    )
}

function passElementValueToFlask(element) {
    passMessageToFlask(
        { "value": element.innerHTML, },
        (response) => { console.log(response) },
        (error) => { console.log(error) }
    )
}

function passMessageToFlask(message, onResponse, onError) {
    axios({
        method: "post",
        url: "http://127.0.0.1:5000/messages",
        message: message
    })
    .then((response) => {
        onResponse(response)
    })
    .catch((error) {
        onErorr(error)
    })
}
