// location.js


const searchForm = document.querySelector("#search-form");
const getLocationButton = document.querySelector(".form-btn");
searchForm.addEventListener("submit", function (event) {
    event.preventDefault();
})

const successCallback = (position) => {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;
    let searchInput = document.querySelector(".search-input");
    // const searched = searchInput.value
    sendToFlask(latitude, longitude);
    // console.log(`Latitude: ${latitude}, Longitude: ${longitude}, search for: ${searched}`);
    
    // searchInput.value = "";
};

const errorCallback = (error) => {
    console.error(error);
}

getLocationButton.addEventListener(
    "click", 
    function(){
        navigator.geolocation.getCurrentPosition(successCallback, errorCallback);
    }
);

// Function to send latitude and longitude to the Flask app
function sendToFlask(latitude, longitude) {
    const data = { latitude: latitude, longitude: longitude }; // Create a JSON object with latitude and longitude
   const headers = {
       'Content-Type': 'application/json',
       'Accept': 'application/json', 
    //    'latitude': latitude,
    //    'longitude': longitude,
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
};