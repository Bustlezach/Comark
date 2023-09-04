// location.js

document.addEventListener("DOMContentLoaded", function () {
    const getLocationButton = document.querySelector(".form-btn");

    getLocationButton.addEventListener("click", () => {
        if ("geolocation" in navigator) {
            navigator.geolocation.getCurrentPosition(function (position) {
                const latitude = position.coords.latitude;
                const longitude = position.coords.longitude;

                sendToFlask(latitude, longitude);
            }, function (error) {
                console.error("Error getting geolocation:", error.message);
            });
        } else {
            console.error("Geolocation is not available in this browser.");
        }
    });

    // Function to send latitude and longitude to the Flask app
    function sendToFlask(latitude, longitude) {
        const data = { latitude: latitude, longitude: longitude }; // Create a JSON object with latitude and longitude
        const headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        };
        $.ajax({
            url: "/search",
            type: 'POST',
            dataType: 'json',
            headers: headers,
            data: JSON.stringify(data),
            success: function (response) {
                console.log("Data sent to Flask app:", data);
                console.log("Response from Flask app:", response);
            },
            error: function (error) {
                console.error("Error sending data to Flask app:", error);
            }
        });
    }
});
