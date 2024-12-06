from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time
import random

# Initialize the WebDriver
driver = webdriver.Chrome()  # Ensure the ChromeDriver matches your browser version
driver.get("https://idt.iion.io/dashboard")  # Replace with the correct URL

# Maximize the browser window
driver.maximize_window()

# Wait for the page to fully load
time.sleep(5)

# Locate all countries (or paths) within the SVG map
country_elements = driver.find_elements(By.CSS_SELECTOR, ".rsm-svg path")  # Adjust selector if needed

# Check if we found any countries
if not country_elements:
    print("No clickable countries found inside the SVG map.")
    driver.quit()
    exit()

# Randomly select one country element
random_country = random.choice(country_elements)

# Scroll the map into view to ensure visibility
driver.execute_script("arguments[0].scrollIntoView(true);", random_country)

# Highlight the selected country (optional debugging step)
driver.execute_script("arguments[0].setAttribute('style', 'stroke: red; stroke-width: 2;')", random_country)

# Move to the selected country and click
actions = ActionChains(driver)
actions.move_to_element(random_country).click().perform()

# Wait for the tooltip to appear
time.sleep(2)

# Extract the tooltip text
try:
    tooltip_element = driver.find_element(By.CLASS_NAME, "__react_component_tooltip")
    tooltip_text = tooltip_element.text
    print("Tooltip text:", tooltip_text)

    # Extract Ad Request value from tooltip text
    if "Ad Request" in tooltip_text:
        ad_request_line = [line for line in tooltip_text.split("\n") if "Ad Request" in line][0]
        tooltip_ad_request = int(ad_request_line.split("(")[1].split(")")[0].replace(",", ""))
        print("Tooltip Ad Request Value:", tooltip_ad_request)
    else:
        print("Tooltip text does not contain 'Ad Request'.")
        tooltip_ad_request = 0  # Default to 0 if not found
except Exception as e:
    print("Tooltip not found or failed to load:", str(e))
    driver.quit()
    exit()

# Extract Ad Request values for the three categories on the page
try:
    # Around the Game Ad Request
    try:
        around_game_element = driver.find_element(By.XPATH, '//*[@id="rc-tabs-2-panel-1"]')
        around_game_ad_request = int(''.join(filter(str.isdigit, around_game_element.text)))
    except Exception:
        around_game_ad_request = 0
        print("Around the Game Ad Request not found. Defaulting to 0.")

    # In Game Ad Request
    try:
        in_game_element = driver.find_element(By.XPATH, '//*[@id="rc-tabs-0-panel-1"]')
        in_game_ad_request = int(''.join(filter(str.isdigit, in_game_element.text)))
    except Exception:
        in_game_ad_request = 0
        print("In Game Ad Request not found. Defaulting to 0.")

    # Away from Game Ad Request
    try:
        away_from_game_element = driver.find_element(By.XPATH, '//*[@id="rc-tabs-1-panel-1"]')
        away_from_game_ad_request = int(''.join(filter(str.isdigit, away_from_game_element.text)))
    except Exception:
        away_from_game_ad_request = 0
        print("Away from Game Ad Request not found. Defaulting to 0.")

    # Print Ad Request values
    print("Around the Game Ad Request:", around_game_ad_request)
    print("In Game Ad Request:", in_game_ad_request)
    print("Away from Game Ad Request:", away_from_game_ad_request)

    # Calculate the total sum of Ad Requests
    total_ad_request = around_game_ad_request + in_game_ad_request + away_from_game_ad_request
    print("Total Ad Request (Sum of all):", total_ad_request)

    # Compare the total with the tooltip value
    if total_ad_request == tooltip_ad_request:
        print("The sum of Ad Requests matches the tooltip value!")
    else:
        print("Mismatch! The sum of Ad Requests does NOT match the tooltip value.")
except Exception as e:
    print("Error extracting Ad Request values from the page:", str(e))
    driver.quit()
    exit()

# Wait to observe the results
time.sleep(5)

# Close the browser
driver.quit()
