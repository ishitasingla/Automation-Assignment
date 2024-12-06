from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


# Function to initialize the WebDriver and open the page
def initialize_driver(url):
    driver = webdriver.Chrome()  # Update with the path to your driver
    driver.get(url)
    driver.maximize_window()
    time.sleep(5)
    return driver


# Function to select a dropdown option by its visible text
def select_dropdown_option(driver, dropdown_xpath, option_xpath):
    dropdown = driver.find_element(By.XPATH, dropdown_xpath)
    dropdown.click()
    time.sleep(2)
    option = driver.find_element(By.XPATH, option_xpath)
    option.click()


# Function to assert the selected option from a dropdown
def assert_selected_option(driver, selected_xpath, expected_text):
    selected_option = driver.find_element(By.XPATH, selected_xpath)
    try:
        assert expected_text in selected_option.text
        print(f"Assertion passed! The text matches: {expected_text}")
    except AssertionError as e:
        print(f"Assertion failed! {e}")


# Function to select a country from a dropdown by searching
def select_country(driver, country_xpath, search_xpath, country_name):
    countrydropdown = driver.find_element(By.XPATH, country_xpath)
    countrydropdown.click()
    search_input = driver.find_element(By.XPATH, search_xpath)
    search_input.send_keys(country_name)
    time.sleep(2)
    search_input.send_keys(Keys.RETURN)
    time.sleep(5)


# Function to reset filters and assert the initial state
def reset_filters_and_assert(driver):
    reset_filters_button = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div/div/section/section/div[2]/section/div/div/div[1]/div[3]')
    reset_filters_button.click()
    time.sleep(4)
    optionincategories = driver.find_element(By.XPATH, "//span[@class='ant-select-selection-item' and @title='All categories']")
    selected_optioningames = driver.find_element(By.XPATH, "//h3[contains(text(), 'In Game')]")
    selected_optionaround = driver.find_element(By.XPATH, "//h3[contains(text(), 'Around the Game')]")
    selected_optionaway = driver.find_element(By.XPATH, "//h3[contains(text(), 'Away from Game')]")
    countries = driver.find_element(By.XPATH, "//span[@class='ant-select-selection-item' and @title='All countries']")
    
    try:
        assert "All categories" in optionincategories.text.strip() and \
               "In Game" in selected_optioningames.text.strip() and \
               "Around the Game" in selected_optionaround.text.strip() and \
               'Away from Game' in selected_optionaway.text.strip() and \
               'All countries' in countries.text.strip()
        print("Reset button is working fine")
    except AssertionError as e:
        print(f"Assertion failed! {e}")


# Function to check if a button is clickable and click it
def check_and_click_button(driver, locator, timeout=10):
    try:
        button = WebDriverWait(driver, timeout).until(lambda d: d.find_element(*locator))
        assert button.is_displayed(), "The button is not displayed on the page."
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))
        button.click()
        time.sleep(2)
        print("Button clicked successfully.")
    except (TimeoutException, NoSuchElementException, AssertionError) as e:
        print(f"Failed to click the button: {e}")

def fill_with_invalid_inputs(driver):
     invalid_input='<>'
     first_name_field = driver.find_element(By.ID, 'firstname-4b87b19b-0cb4-4159-a394-2eff153274d3')
     
    
     last_name_field = driver.find_element(By.ID, 'lastname-4b87b19b-0cb4-4159-a394-2eff153274d3')
    
     company_field = driver.find_element(By.ID, 'company-4b87b19b-0cb4-4159-a394-2eff153274d3')
    
     try:
        first_name_field.clear()
        first_name_field.send_keys(invalid_input)
        assert invalid_input not in first_name_field.get_attribute("value"), "Invalid characters were accepted in First Name!"
        print("First Name test passed: Invalid characters '<>' were not accepted.")
     except AssertionError as e:
        print(f"First Name test failed: {e}")
     except Exception as e:
        print(f"An error occurred while testing First Name field: {e}")

    # Test for Last Name Field
     try:
        last_name_field.clear()
        last_name_field.send_keys(invalid_input)
        assert invalid_input not in last_name_field.get_attribute("value"), "Invalid characters were accepted in Last Name!"
        print("Last Name test passed: Invalid characters '<>' were not accepted.")
     except AssertionError as e:
        print(f"Last Name test failed: {e}")
     except Exception as e:
        print(f"An error occurred while testing Last Name field: {e}")

    # Test for Company Field
     try:
        company_field.clear()
        company_field.send_keys(invalid_input)
        assert invalid_input not in company_field.get_attribute("value"), "Invalid characters were accepted in Company!"
        print("Company test passed: Invalid characters '<>' were not accepted.")
     except AssertionError as e:
        print(f"Company test failed: {e}")
     except Exception as e:
        print(f"An error occurred while testing Company field: {e}")



# Function to handle email validation for submission
def test_invalid_email_submission(driver, email):
    emailfield = driver.find_element(By.ID, 'email-4b87b19b-0cb4-4159-a394-2eff153274d3')
    emailfield.clear()
    
    emailfield.send_keys(email)
    time.sleep(3)
    
    try:
        
        error_message = driver.find_element(By.XPATH, "//label[@class='hs-error-msg hs-main-font-element' and text()='Email must be formatted correctly.']")
        assert error_message.is_displayed(), f"Expected 'Email must be formatted correctly.' but got: {error_message.text}"
        print(f"Correct error message for invalid email '{email}': {error_message.text}")
    except Exception as e:
        print(f"Failed to assert error message for email '{email}': {str(e)}")
    emailfield.clear()


# Function to handle form submission with proper input and validation
def fill_and_submit_form(driver, firstname, lastname, email, company):
    # Find the fields and fill them
    firstname_field = driver.find_element(By.ID, 'firstname-4b87b19b-0cb4-4159-a394-2eff153274d3')
    firstname_field.clear()
    assert firstname_field.is_displayed() and firstname_field.is_enabled(), "Firstname field is not interactable."
    print("Firstname field is interactable")
    firstname_field.send_keys(firstname)
    assert firstname_field.get_attribute("value") == firstname, f"Firstname field was not filled correctly. Expected: {firstname}, Found: {firstname_field.get_attribute('value')}"
    print(f"Firstname field is filled properly as expected: {firstname}")

    lastname_field = driver.find_element(By.ID, 'lastname-4b87b19b-0cb4-4159-a394-2eff153274d3')
    lastname_field.clear()
    assert lastname_field.is_displayed() and lastname_field.is_enabled(), "Lastname field is not interactable."
    print("lastname field is interactable")
    lastname_field.send_keys(lastname)
    assert lastname_field.get_attribute("value") == lastname, f"Lastname field was not filled correctly. Expected: {lastname}, Found: {lastname_field.get_attribute('value')}"
    print(f"Lastname field is filled properly as expected: {lastname}")

    email_field = driver.find_element(By.ID, 'email-4b87b19b-0cb4-4159-a394-2eff153274d3')
    email_field.clear()
    assert email_field.is_displayed() and email_field.is_enabled(), "Email field is not interactable."
    print("email field is interactable")
    email_field.send_keys(email)
    assert email_field.get_attribute("value") == email, f"Email field was not filled correctly. Expected: {email}, Found: {email_field.get_attribute('value')}"
    print(f"Email field is filled properly as expected: {email}")

    company_field = driver.find_element(By.ID, 'company-4b87b19b-0cb4-4159-a394-2eff153274d3')
    company_field.clear()
    assert company_field.is_displayed() and company_field.is_enabled(), "Company field is not interactable."
    print("company name field is interactable")
    company_field.send_keys(company)
    assert company_field.get_attribute("value") == company, f"Company field was not filled correctly. Expected: {company}, Found: {company_field.get_attribute('value')}"
    print(f"Company name field is filled properly as expected: {company}")

    # Optionally, you can also click the submit button here
    submit_button = driver.find_element(By.XPATH, "//input[@value='Submit']")
    submit_button.click()
    

    
    try:
        success_message = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//strong[normalize-space()='Thank you for your interest!']")))
        success_message2 = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'’ll be in touch soon. Keep an')]")))
        assert success_message.is_displayed() and success_message2.is_displayed(), "Form submission failed!"
        print("Form submitted successfully!")
    except Exception as e:
        print(f"Error: {e}")

def close_the_form(driver):
    driver.switch_to.default_content()
    close_form = driver.find_element(By.XPATH, "//a[@href='/dashboard' and text()='X']")
    close_form.click()
    time.sleep(6)
    dashboard_tab = driver.find_element(By.XPATH, "//a[@href='/dashboard']")
    assert dashboard_tab.get_attribute("id") == "activeNavLink", "Dashboard tab is not active, navigation may have failed."
    print("Dashboard tab is active. Navigation successful.")
# Main function to orchestrate the script
def main():
    driver = initialize_driver("https://idt.iion.io/dashboard")
    
    # Perform dropdown selection for "In Game"
    select_dropdown_option(driver, '//*[@id="__next"]/div/div[2]/div/div/section/section/div[2]/section/div/div/div[1]/div[2]/span/div/div/span[2]', '//*[@title="In Game"]')
    assert_selected_option(driver, "//h3[contains(text(), 'In Game')]", "In Game")

    select_dropdown_option(driver, '//*[@id="__next"]/div/div[2]/div/div/section/section/div[2]/section/div/div/div[1]/div[2]/span/div/div/span[2]', '//*[@title="Around the Game"]')
    assert_selected_option(driver, "//h3[contains(text(), 'In Game')]", "Around the Game")

    select_dropdown_option(driver, '//*[@id="__next"]/div/div[2]/div/div/section/section/div[2]/section/div/div/div[1]/div[2]/span/div/div/span[2]', '//*[@title="Away from Game"]')
    assert_selected_option(driver, "//h3[contains(text(), 'In Game')]", "Away from Game")

    
    # Select country China
    select_country(driver, '//*[@id="__next"]/div/div[2]/div/div/section/section/div[2]/section/div/div/div[1]/div[1]/span[2]/div/div/span[2]', "//span[@class='ant-select-selection-search']/input[@type='search']", "China")
    assert_selected_option(driver, '//*[@id="__next"]/div/div[2]/div/div/section/section/div[2]/section/div/div/div[1]/div[1]/span[2]/div/div/span[2]', "China")
    
    # Reset filters and check default state
    reset_filters_and_assert(driver)
    
    # Check and click a button
    check_and_click_button(driver, (By.XPATH, "//a[@href='/inventory']"))
    print("Assertion passed: The button is clickable and displayed.")
    popup_locator = (By.CLASS_NAME, "ant-modal-body")

    WebDriverWait(driver, 20).until(EC.visibility_of_element_located(popup_locator))
    driver.switch_to.frame("hs-form-iframe-0")
    try:
        fill_with_invalid_inputs(driver)
    except AssertionError as e:
        print(f"Invalid inputs test failed: {e}")
    
   
    # Test email validation
    invalid_emails = [
        "invalid_email.com",
        "test@domain",
        "user@domain..com",
        "@nodomain.com"
    ]
    for email in invalid_emails:
        test_invalid_email_submission(driver, email)
    
    # Fill the form and submit
    
    fill_and_submit_form(driver, "Ishita", "Singla", "ishitasingla123@gmail.com", "XYZ")
    close_the_form(driver)

    driver.quit()

if __name__ == "__main__":
    main()
