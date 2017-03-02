function redirectTo(url) {
    window.location = "".concat(url);
}

function clickElement(element) {
    element.click();
}

function passValueToFlask(elementID) {
    let el = document.getElementById(elementID);
    axios({
        method: "post",
        url: "http://127.0.0.1:5000/",
        data: {
            value: el.innerHTMLk
        }
    })
    .then((response) => {
        console.log(response)
    })
    .catch((error) {
        console.log(error)
    })

}
