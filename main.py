import requests
from bs4 import BeautifulSoup

# URL of the McDonald's Malaysia locations page
url = "https://www.mcdonalds.com.my/locate-us"

# Send a request to fetch the webpage
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}
response = requests.get(url, headers=headers)

# Check if request is successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, "lxml")

    # Find all store locations (modify selector based on webpage structure)
    locations = soup.find_all("div", class_="location-name")  # Example class (check actual HTML)

    # Filter only Kuala Lumpur locations
    kl_locations = [loc.text.strip() for loc in locations if "Kuala Lumpur" in loc.text]

    # Print Kuala Lumpur locations
    for loc in kl_locations:
        print(loc)
else:
    print(f"Failed to fetch page. Status Code: {response.status_code}")
