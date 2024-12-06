from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time
import random

# Initialize the WebDriver
driver = webdriver.Chrome()  # Ensure the ChromeDriver matches your browser version
driver.get("https://idt.iion.io/dashboard")
time.sleep(3)  # Replace with the correct URL

# Maximize the browser window
driver.maximize_window()

# Wait for the page to fully load
time.sleep(5)

# Click on the MAU tab using the provided XPath
try:
    mau_tab = driver.find_element(By.XPATH, "//div[@id='rc-tabs-1-tab-2']")
    mau_tab.click()
    time.sleep(2)
    mau_tab2 = driver.find_element(By.XPATH, "//div[@id='rc-tabs-0-tab-2']")
    mau_tab2.click()
    driver.execute_script("window.scrollBy(0, 500);")  # Scrolls down 500 pixels
    time.sleep(2)
    
    mau_tab3 = driver.find_element(By.XPATH, "//div[@id='rc-tabs-2-tab-2']")
    mau_tab3.click()
    time.sleep(2)
    driver.execute_script("window.scrollBy(0, -500);")  # Scrolls up 500 pixels
    time.sleep(2)
    
    print("Clicked on the MAU tab.")
    time.sleep(3)  # Wait for the content to load
except Exception as e:
    print("Failed to click on the MAU tab:", str(e))
    driver.quit()
    exit()

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

# Wait for the tooltip to appear (adjust the time if necessary)
time.sleep(2)

# Extract the tooltip text for MAU count
try:
    tooltip_element = driver.find_element(By.CLASS_NAME, "__react_component_tooltip")
    tooltip_text = tooltip_element.text
    print("Tooltip text:", tooltip_text)

    # Extract MAU count from tooltip
    if "MAU" in tooltip_text:
        mau_line = [line for line in tooltip_text.split("\n") if "MAU" in line][0]
        tooltip_mau_count = int(mau_line.split("(")[1].split(")")[0].replace(",", ""))
        print("Tooltip MAU Count:", tooltip_mau_count)
    else:
        print("Tooltip text does not contain 'MAU'.")
        tooltip_mau_count = 0  # Default to 0 if not found
except Exception as e:
    print("Tooltip not found or failed to load:", str(e))
    tooltip_mau_count = 0  # Default to 0 if error occurs
    driver.quit()
    exit()

# Extract MAU values for the three categories on the page
try:
    # Around the Game MAU
    try:
        around_game_mau = int(''.join(filter(str.isdigit, driver.find_element(By.XPATH, '//*[@id="rc-tabs-1-panel-2"]').text)))
    except Exception:
        around_game_mau = 0
        print("Around the Game MAU not found. Defaulting to 0.")

    # In Game MAU
    try:
        in_game_mau = int(''.join(filter(str.isdigit, driver.find_element(By.XPATH, '//*[@id="rc-tabs-0-panel-2"]').text)))
    except Exception:
        in_game_mau = 0
        print("In Game MAU not found. Defaulting to 0.")

    # Away from Game MAU
    try:
        away_from_game_mau = int(''.join(filter(str.isdigit, driver.find_element(By.XPATH, '//*[@id="rc-tabs-2-panel-2"]').text)))
    except Exception:
        away_from_game_mau = 0
        print("Away from Game MAU not found. Defaulting to 0.")

    print("Around the Game MAU:", around_game_mau)
    print("In Game MAU:", in_game_mau)
    print("Away from Game MAU:", away_from_game_mau)

    # Calculate the total sum of MAUs
    total_mau_count = around_game_mau + in_game_mau + away_from_game_mau
    print("Total MAU (Sum of all):", total_mau_count)

    # Compare the total with the tooltip value
    if total_mau_count == tooltip_mau_count:
        print("The sum of MAU matches the tooltip value!")
    else:
        print("Mismatch! The sum of MAU does NOT match the tooltip value.")
except Exception as e:
    print("Error extracting MAU values from the page:", str(e))
    driver.quit()
    exit()

# Wait to observe the results
time.sleep(5)

# Close the browser
driver.quit()
