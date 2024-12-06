from selenium import webdriver
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Set up WebDriver (e.g., Chrome)
driver = webdriver.Chrome() # Update with the path to your driver

# Open a webpage
driver.get("https://idt.iion.io/dashboard")
time.sleep(5)
driver.maximize_window()

dropdown = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div/div/section/section/div[2]/section/div/div/div[1]/div[2]/span/div/div/span[2]')
dropdown.click()
time.sleep(2)
option = driver.find_element(By.XPATH, '//*[@title="In Game"]') 
option.click() # Use the title attribute for selection
selected_option = driver.find_element(By.XPATH, "//h3[contains(text(), 'In Game')]")  # Replace with the element showing the selected option
try:
    assert "In Game" in selected_option.text
    print("Assertion passed! The text matches.")
except AssertionError as e:
    print(f"Assertion failed! {e}")


time.sleep(3)
countrydropdown = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div/div/section/section/div[2]/section/div/div/div[1]/div[1]/span[2]/div/div/span[2]')
countrydropdown.click()
search_input = driver.find_element(By.XPATH, "//span[@class='ant-select-selection-search']/input[@type='search']")
search_input.send_keys("China") 
time.sleep(2) # Type China into the input field

# Optionally, you can wait for the dropdown to update and select the country if necessary
search_input.send_keys(Keys.RETURN)
time.sleep(5)
        

# china_path = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div/div/section/section/div[2]/section/div/div/div[2]/svg/g/path[32]')
# highlighted_fill_color = china_path.get_attribute("fill")
# try:
#     assert highlighted_fill_color == "#00f", "China is not highlighted correctly on the map."
        
#     print("Test passed: china is highlighted correctly on the map.")
# except AssertionError as e:
#     print(f"Assertion failed! {e}")
selected_item = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div/div/section/section/div[2]/section/div/div/div[1]/div[1]/span[2]/div/div/span[2]')
selected_text = selected_item.text.strip()  # Get the text of the selected item and remove any surrounding spaces

# Assert if "China" is selected
assert selected_text == "China", f"Expected 'China', but got {selected_text}"
print("China is successfully selected!")
time.sleep(3)

reset_filters_button = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div/div/section/section/div[2]/section/div/div/div[1]/div[3]')
reset_filters_button.click()
time.sleep(4)
optionincategories = driver.find_element(By.XPATH, "//span[@class='ant-select-selection-item' and @title='All categories']") 
selected_optioningames = driver.find_element(By.XPATH, "//h3[contains(text(), 'In Game')]")
selected_optionaround=driver.find_element(By.XPATH, "//h3[contains(text(), 'Around the Game')]")
selected_optionaway=driver.find_element(By.XPATH, "//h3[contains(text(), 'Away from Game')]")
countries=driver.find_element(By.XPATH, "//span[@class='ant-select-selection-item' and @title='All countries']")
try:
 assert "All categories" in optionincategories.text.strip() and \
           "In Game" in selected_optioningames.text.strip() and \
           "Around the Game" in selected_optionaround.text.strip() and \
           'Away from Game' in selected_optionaway.text.strip() and \
           'All countries' in countries.text.strip()    
 print("Reset button is working fine")
except AssertionError as e:
    print(f"Assertion failed! {e}")

time.sleep(2)


def check_and_click_button(driver, locator, timeout=10):
    """
    Check if a button is displayed, ensure it's clickable, and click it.

    :param driver: WebDriver instance
    :param locator: Tuple (By.<method>, "value") for locating the button
    :param timeout: Time in seconds to wait for the button to be clickable
    """
    try:
        # Locate the button and check if it is displayed
        button = WebDriverWait(driver, timeout).until(
            lambda d: d.find_element(*locator)
        )
        assert button.is_displayed(), "The button is not displayed on the page."

        # Wait for the button to be clickable
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))

        # Click the button
        button.click()
        time.sleep(2)
        print("Button clicked successfully.")
    except (TimeoutException, NoSuchElementException, AssertionError) as e:
        print(f"Failed to click the button: {e}")
        
button_locator = (By.XPATH, "//a[@href='/inventory']")
check_and_click_button(driver, button_locator)
print("Assertion passed: The button is clickable and displayed.")
popup_locator = (By.CLASS_NAME, "ant-modal-body")

WebDriverWait(driver, 20).until(EC.visibility_of_element_located(popup_locator))
driver.switch_to.frame("hs-form-iframe-0")

submit = driver.find_element(By.XPATH, "//input[@value='Submit']")
submit.click()
errormessage=driver.find_element(By.XPATH, "//label[@class='hs-error-msg hs-main-font-element' and text()='Please complete this required field.']")
errormessage2=driver.find_element(By.XPATH, "//label[@class='hs-main-font-element' and text()='Please complete all required fields.']")
assert errormessage2.is_displayed() and errormessage.is_displayed(),"Error message for empty form is not displayed"
print("Error message for empty form is displayed correctly on both the required field and on empty submission")


emailfield = driver.find_element(By.ID, 'email-4b87b19b-0cb4-4159-a394-2eff153274d3')

def test_invalid_email_submission(email):
    # Clear the email field and input the invalid email
    emailfield.clear()
    emailfield.send_keys(email)
    
    
   
    
    # Wait for the form submission to complete (adjust the time as necessary)
    time.sleep(3)
    
    # Assert error message for invalid email format
    try:
        if "@" not in email or len(email.split('@')[1].split('.')[-1]) < 2:
            error_message = driver.find_element(By.XPATH, "//label[@class='hs-error-msg hs-main-font-element' and text()='Please enter a valid email address.']")
            assert error_message.is_displayed(), f"Expected 'Please enter a valid email address.' but got: {error_message.text}"
            print(f"Correct error message for invalid email '{email}': {error_message.text}")
        else:
            error_message = driver.find_element(By.XPATH, "//label[@class='hs-error-msg hs-main-font-element' and text()='Email must be formatted correctly.']")
            assert error_message.is_displayed(), f"Expected 'Email must be formatted correctly.' but got: {error_message.text}"
            print(f"Correct error message for invalid email '{email}': {error_message.text}")
    except Exception as e:
        print(f"Failed to assert error message for email '{email}': {str(e)}")

# Run the test for each invalid email
invalid_emails = [
    "invalid_email.com",  # Missing '@' and domain
    "test@domain",         # Missing domain extension
    "user@domain..com",    # Double dot in domain
    "@nodomain.com",       # Missing username
]
for email in invalid_emails:
    test_invalid_email_submission(email)

firstname=WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, '//*[@id="firstname-4b87b19b-0cb4-4159-a394-2eff153274d3"]'))
)

assert firstname.is_displayed() and firstname.is_enabled(), "Firstname field is not interactable."
print("Firstname field is interactable")
firstname.send_keys("Ishita")
assert firstname.get_attribute("value") == "Ishita", "Firstname field was not filled correctly."
print("Firstname field is filled properly as expected")

# Fill the 'lastname' field
lastname = driver.find_element(By.ID, 'lastname-4b87b19b-0cb4-4159-a394-2eff153274d3')
assert lastname.is_displayed() and lastname.is_enabled(), "Lastname field is not interactable."
print("lastname field is interactable")
lastname.send_keys("Singla")
assert lastname.get_attribute("value") == "Singla", "Lastname field was not filled correctly."
print("lastname field is filled properly as expected")

# Fill the 'email' field
email = driver.find_element(By.ID, 'email-4b87b19b-0cb4-4159-a394-2eff153274d3')
assert email.is_displayed() and email.is_enabled(), "Email field is not interactable."
print("email field is interactable")
email.clear()
email.send_keys("ishitasingla123@gmail.com")
assert email.get_attribute("value") == "ishitasingla123@gmail.com", "Email field was not filled correctly."
print("email field is filled properly as expected")

# Fill the 'company' field
company = driver.find_element(By.ID, 'company-4b87b19b-0cb4-4159-a394-2eff153274d3')
assert company.is_displayed() and company.is_enabled(), "Company field is not interactable."
print("company name field is interactable")
company.send_keys("XYZ")
assert company.get_attribute("value") == "XYZ", "Company field was not filled correctly."
print("company name field is filled properly as expected")
submit = driver.find_element(By.XPATH, "//input[@value='Submit']")
submit.click()
try:
    success_message = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//strong[normalize-space()='Thank you for your interest!']"))
    )
    success_message2=WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'’ll be in touch soon. Keep an')]"))
    )
    # Assert the message is displayed
    assert success_message.is_displayed() and success_message2.is_displayed(), "Form submission failed!"
    print("Form submitted successfully!")

except Exception as e:
    print(f"Error: {e}")
time.sleep(2)
driver.switch_to.default_content()
close_form = driver.find_element(By.XPATH, "//a[@href='/dashboard' and text()='X']")
close_form.click()
time.sleep(6)
dashboard_tab = driver.find_element(By.XPATH, "//a[@href='/dashboard']")
assert dashboard_tab.get_attribute("id") == "activeNavLink", "Dashboard tab is not active, navigation may have failed."
print("Dashboard tab is active. Navigation successful.")
driver.quit()
