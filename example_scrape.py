import time
import random
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import csv

# Load the CSV with ZIP codes
zip_data = pd.read_csv('uszips.csv')  # Replace 'uszips.csv' with your CSV filename

# Choose headless or head mode
headless_mode = True  # Set to False for head mode (visible browser)

# Set up Chrome options
chrome_options = Options()
if headless_mode:
    chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)  # Make sure ChromeDriver is in PATH

# URL of the page to scrape
url = 'https://www.9marks.org/church-search/'  # Replace with the actual URL
driver.get(url)

# Load previous progress if exists
output_file = 'church_data_output2.csv'
try:
    all_church_data = pd.read_csv(output_file).to_dict('records')
    print("Loaded existing progress from CSV.")
except FileNotFoundError:
    all_church_data = []
    print("No existing progress found, starting fresh.")

# Keep track of processed ZIP codes to avoid re-scraping if the script is resumed
processed_zips = set([record['ZIP Code'] for record in all_church_data])

# Iterate over each ZIP code in the CSV
for index, zip_code in enumerate(zip_data['zip'][23000:23020], start=23000):
    if zip_code in processed_zips:
        print(f"Skipping ZIP code {zip_code} (already processed).")
        continue
    
    try:
        # Find the search field, clear it, and enter the ZIP code
        search_field = driver.find_element("id", "address")
        search_field.clear()
        search_field.send_keys(str(zip_code))
        search_field.send_keys(Keys.RETURN)

        # Wait for the page to load results
        time.sleep(random.uniform(3, 7))  # Random delay between 3 and 7 seconds

        # Parse the page content with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        church_items = soup.find_all('div', class_='item hentry church')

        # Check if no results are found and skip if so
        if not church_items:
            print(f"No data found for ZIP code {zip_code}")
            continue

        # Extract details for each church
        for item in church_items:
            # Use conditional checks to handle missing elements gracefully
            church_name = item.find('h6', class_='title')
            church_name = church_name.get_text(strip=True) if church_name else 'N/A'

            address_link = item.find('h6', class_='title').find('a') if item.find('h6', class_='title') else None
            address = address_link['href'] if address_link else 'N/A'

            location_links = item.find('div', class_='location-links')
            phone_number = location_links.find('p').get_text(strip=True).split(' • ')[0] if location_links else 'N/A'

            email_tag = item.find('a', href=lambda href: href and 'mailto:' in href)
            email = email_tag['href'].replace('mailto:', '') if email_tag else 'N/A'

            website_tag = item.find('a', href=lambda href: href and href.startswith('http'))
            website_url = website_tag['href'] if website_tag else 'N/A'

            directions_tag = item.find('a', href=lambda href: href and 'maps.google.com' in href)
            directions_link = directions_tag['href'] if directions_tag else 'N/A'

            description_tag = item.find('div', class_='content')
            description = description_tag.get_text(strip=True) if description_tag else 'N/A'

            # Append the data to the list
            all_church_data.append({
                'ZIP Code': zip_code,
                'Church Name': church_name,
                'Address': address,
                'Phone Number': phone_number,
                'Email': email,
                'Website URL': website_url,
                'Directions Link': directions_link,
                'Description': description
            })

        # Periodically save the data to CSV every 10 ZIP codes
        if (index + 1) % 10 == 0:
            # Remove duplicates and set an ID column as index
            df = pd.DataFrame(all_church_data).drop_duplicates().reset_index(drop=True)
            df.index += 1  # Start the ID index from 1
            df.index.name = 'ID'
            df.to_csv(output_file, index=True)
            print(f"Progress saved at ZIP code {zip_code}")

    except Exception as e:
        print(f"An error occurred for ZIP code {zip_code}: {e}")

# Close the browser
driver.quit()

# Final save after all ZIP codes are processed
# Remove duplicates and set an ID column as index
df = pd.DataFrame(all_church_data).drop_duplicates().reset_index(drop=True)
df.index += 1  # Start the ID index from 1
df.index.name = 'ID'
df.to_csv(output_file, index=True)
print(f"Final data saved to {output_file}")

# After your final save of data, add this code:
excel_output_file = 'church_data_output2.xlsx'
df.to_excel(excel_output_file, index=True)  # Save as Excel file
print(f"Final data saved to {output_file} and {excel_output_file}")
