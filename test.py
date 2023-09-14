
"""Make a request to the ipinfo.io API"""
response = requests.get("https://ipinfo.io/json")
ip_address = response.json()["ip"]
response_ip = requests.get(f"https://ipinfo.io/{ip_address}/json")
data_ip = response_ip.json()

# Extract the latitude and longitude
latitude, longitude = data_ip["loc"].split(",")

# Print the latitude and longitude
print(f"Latitude: {latitude}, Longitude: {longitude}")

"""Make a request to the ipgeolocation.abstractapi.com API"""

url = "https://ipgeolocation.abstractapi.com/v1/?api_key=9fabc1053c684dc49448caeb978652ab"
resp = requests.request("GET", url)
data = resp.json()
city = data.get('city')

