const search = document.querySelector('#search');

function successCallback(position) {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;
    sendRequest(latitude, longitude);
}

const errorCallback = (error) => {
    console.log(error);
}

const get_coords = () => {
    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(successCallback, errorCallback);
    }
}

const sendRequest = (latitude, longitude) => {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/receive_coordinates", true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status !== 200) {
                console.log("Request failed:", xhr.statusText);
            } else {
                console.log("Request successful:", xhr.responseText);
            }
        }
    };
    xhr.send(JSON.stringify({ latitude: latitude, longitude: longitude }));
};

search.addEventListener("click", get_coords);
