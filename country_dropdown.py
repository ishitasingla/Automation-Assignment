from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random


driver = webdriver.Chrome() 
driver.get("https://idt.iion.io/dashboard") 


driver.maximize_window()


time.sleep(3)


try:
    dropdown = driver.find_element(By.CLASS_NAME, "ant-select-selector")
    dropdown.click()
    print("Dropdown clicked.")
except Exception as e:
    print("Failed to click dropdown:", str(e))
    driver.quit()
    exit()


WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".ant-select-item"))
)


country_elements = driver.find_elements(By.CSS_SELECTOR, ".ant-select-item")


if not country_elements:
    print("No countries found in the dropdown.")
    driver.quit()
    exit()


random_country = random.choice(country_elements)


driver.execute_script("arguments[0].scrollIntoView(true);", random_country)


actions = ActionChains(driver)
actions.move_to_element(random_country).click().perform()
driver.execute_script("window.scrollBy(0, -500);")  # Scrolls up 500 pixels
time.sleep(2)

print("Country selected.")


time.sleep(2)


selected_country = driver.find_element(By.CLASS_NAME, "ant-select-selection-item").text
assert selected_country != "All countries", f"Failed: The selected country is not updated. Current text: {selected_country}"

print("Dropdown text updated to the selected country.")


try:
    cross_button = driver.find_element(By.CSS_SELECTOR, ".ant-select-clear")
    cross_button.click()
    print("Cross button clicked, selection cleared.")
except Exception as e:
    print("Failed to click the cross button:", str(e))


time.sleep(2)

dropdown_text_after = driver.find_element(By.CLASS_NAME, "ant-select-selection-item").text
assert dropdown_text_after == "All countries", f"Failed: The dropdown text is not 'All countries'. Current text: {dropdown_text_after}"

print("Dropdown text reset to 'All countries'.")

# Close the browser
driver.quit()
