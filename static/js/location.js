const search = document.querySelector(".search-input")

if (window.navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function (position) {
        const { latitude, longitude } = position.coords;
        console.log(latitude, longitude);

        function fun() {
            const xml = new XMLHttpRequest();
            xml.open("POST", "/search", true); 
            xml.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

            xml.onload = function () {
                if (xml.status === 200) {
                    const dataReply = JSON.parse(xml.responseText);
                    console.log(dataReply);
                } else {
                    console.error('Error:', xml.status, xml.statusText);
                }
                
            };

            const data = JSON.stringify({
                'latitude': latitude,
                'longitude': longitude
            });

            xml.send(data);
        }
        
        fun();  // Call the function to send the POST request
    });
} else {
    // Geolocation is not available in this browser
    console.log("Geolocation is not available in your browser.");
}