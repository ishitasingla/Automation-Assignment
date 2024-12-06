from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up WebDriver (make sure to use the correct WebDriver for your browser)
driver = webdriver.Chrome()  # Update path to your WebDriver

# Open the webpage
driver.get('https://idt.iion.io/dashboard')  # Replace with your page URL

# Wait for the dropdown (All categories) to be clickable
wait = WebDriverWait(driver, 10)  # Adjust the timeout as necessary

# Locate the dropdown initially (All categories)
dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='ant-select-selection-item'][contains(text(), 'All categories')]")))

# Iterate through the options
options = ['In Game', 'Around the Game', 'Away from Game']  # List of options to select

for option_name in options:
    # Click the dropdown to open it
    dropdown.click()

    # Wait for the options to be visible
    wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='ant-select-item-option-content']")))

    # Locate the specific option by text and click it
    option = driver.find_element(By.XPATH, f"//div[@class='ant-select-item-option-content'][contains(text(), '{option_name}')]")
    option.click()
    
    # Wait for the selection to update (you can adjust the sleep time as necessary)
    time.sleep(2)  # Wait for the page to reflect the selection
    
    # Check if the dropdown title has been updated with the selected option
    dropdown_title = driver.find_element(By.XPATH, "//span[@class='ant-select-selection-item']").text
    if dropdown_title == option_name:
        print(f"Option '{option_name}' is successfully selected. Dropdown title is updated to: '{dropdown_title}'")
    else:
        print(f"Option '{option_name}' was not correctly selected. Current dropdown title: '{dropdown_title}'")

# Close the browser after the actions are done
driver.quit()
