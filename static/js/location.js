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
        fetch("/search", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            position: JSON.stringify({ latitude, longitude }),
        })
        .then(response => response.json())
        .then(data => {
            console.log("Data sent to Flask app:", data);
        })
        .catch(error => {
            console.error("Error sending data to Flask app:", error);
        });
    }
});
