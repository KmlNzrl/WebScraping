import time
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Path to ChromeDriver (update this based on your system)
chromedriver_path = "C:\Windows\chromedriver.exe"

# Set up Selenium WebDriver options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no UI)
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Start WebDriver
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open McDonald's location page
url = "https://www.mcdonalds.com.my/locate-us"
driver.get(url)
time.sleep(3)  # Wait for page to load

# Select "Kuala Lumpur" from the dropdown
state_dropdown = Select(driver.find_element(By.ID, "states"))
state_dropdown.select_by_value("Kuala Lumpur")
time.sleep(3)  # Wait for results to load

# Function to scrape JSON-LD data
def scrape_page():
    outlets = []
    results_div = driver.find_element(By.ID, "results")
    script_tags = results_div.find_elements(By.TAG_NAME, "script")

    for script in script_tags:
        script_content = script.get_attribute("innerText").strip()
        try:
            data = json.loads(script_content)
            if isinstance(data, dict) and data.get("@type") == "Restaurant":
                name = data.get("name", "N/A")
                address = data.get("address", "N/A")
                phone = data.get("telephone", "N/A")
                latitude = data["geo"]["latitude"] if "geo" in data else "N/A"
                longitude = data["geo"]["longitude"] if "geo" in data else "N/A"
                menu_url = data.get("menu", "N/A")
                waze_url = data.get("url", "N/A")

                outlets.append({
                    "Name": name,
                    "Address": address,
                    "Phone": phone,
                    "Latitude": latitude,
                    "Longitude": longitude,
                    "Menu URL": menu_url,
                    "Waze Link": waze_url
                })
        except json.JSONDecodeError:
            continue  # Skip if JSON is invalid

    return outlets

# Scrape first page
data = scrape_page()

# Handle pagination
while True:
    try:
        next_button = driver.find_element(By.LINK_TEXT, "Next")
        next_button.click()
        time.sleep(3)  # Wait for next page to load
        data.extend(scrape_page())
    except:
        break  # No more pages

# Convert to DataFrame & Save to Excel
df = pd.DataFrame(data)
df.to_excel("McDonalds_Kuala_Lumpur.xlsx", index=False)

# Close the WebDriver
driver.quit()

print("Scraping completed! Data saved as 'McDonalds_Kuala_Lumpur.xlsx'.")
