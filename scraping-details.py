from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import os

# Set up the webdriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# List of car URLs (you can add more URLs to this list)
car_urls = all_links

# Check if the CSV file exists
csv_file = 'car_details.csv'
if os.path.exists(csv_file):
    # If file exists, read the existing data
    df_existing = pd.read_csv(csv_file)
else:
    # If file does not exist, create an empty dataframe with the required columns
    df_existing = pd.DataFrame(columns=["Price", "Car Model", "Year", "Kilometers", "Body Type", "Exterior Color", 
                                        "Doors", "Interior Color", "Fuel Type", "Horsepower", "No. of Cylinders", 
                                        "Transmission Type", "Warranty", "Target Market", "Seller type", "Steering Side", 
                                        "Seating Capacity", "Engine Capacity", "Car Link"])

# Loop through each car URL
for idx, url in enumerate(car_urls, start=1):
    print(f"Step {idx}: Processing {url}...")

    # Open the webpage
    driver.get(url)
    time.sleep(5)  # Wait for the page to load

    # Extract the first four important details (Price, Car Model, Year, Kilometers)
    elements1 = driver.find_elements(By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "mui-style-12h8crc", " " ))] | //*[contains(concat( " ", @class, " " ), concat( " ", "mui-style-1u8vfmp", " " ))] | //*[contains(concat( " ", @class, " " ), concat( " ", "mui-style-g5wj77", " " ))]')
    car_data = {}

    # Extract the first three pieces of information (Price, Model, Year)
    car_data["Price"] = elements1[0].text if len(elements1) > 0 else 'Not Found'
    car_data["Car Model"] = elements1[1].text if len(elements1) > 1 else 'Not Found'
    car_data["Year"] = elements1[2].text if len(elements1) > 2 else 'Not Found'
    car_data["Kilometers"] = elements1[3].text if len(elements1) > 3 else 'Not Found'

    print("Collected basic car details:", car_data)

    # Find all elements with the target class for other car details
    elements = driver.find_elements(By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "mui-style-1btz1yr", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "MuiTypography-root", " " ))]')

    # Define labels
    labels = [
        "Body Type", "Exterior Color", "Doors", "Interior Color", "Fuel Type",
        "Horsepower", "No. of Cylinders", "Transmission Type", "Warranty",
        "Target Market", "Seller type", "Steering Side", "Seating Capacity", "Engine Capacity"
    ]

    # Extract additional car details into car_data
    for i in range(0, len(elements), 2):  # Every two elements: label and value
        label = elements[i].text.strip()
        value = elements[i + 1].text.strip() if i + 1 < len(elements) else ''
        
        if label in labels:
            car_data[label] = value

    print("Collected additional car details:", car_data)

    # Add the link of the car
    car_data["Car Link"] = url

    # Check if the car already exists in the dataframe to avoid duplicates
    if not df_existing[df_existing["Car Link"] == url].empty:
        print(f"Car {url} already exists in the CSV. Skipping...")
        continue  # Skip if the car is already in the CSV

    # Convert car_data to a DataFrame and append to the existing dataframe
    df_new = pd.DataFrame([car_data])
    df_existing = pd.concat([df_existing, df_new], ignore_index=True)

    # Re-read the dataframe from the CSV file to minimize risk
    df_existing.to_csv(csv_file, index=False)
    df_existing = pd.read_csv(csv_file)

    print(f"Step {idx}: Data added for {url}\n")

# Final output
print("\nUpdated DataFrame:")
print(df_existing)

# Close the webdriver
driver.quit()

print("✅ Data saved to 'car_details.csv'")
