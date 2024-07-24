import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from urllib.parse import urlparse
import os
from dotenv import load_dotenv
load_dotenv() 

# source venv/Scripts/activate

# Set up the Selenium WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# # LinkedIn login credentials
linkedin_username = load_dotenv('LINKEDIN_USERNAME')
linkedin_password = load_dotenv('LINKEDIN_PASSWORD')

# Log in to LinkedIn
def login_to_linkedin():
    driver.get('https://www.linkedin.com/login')
    time.sleep(2)
    username_field = driver.find_element(By.ID, 'username')
    username_field.send_keys(linkedin_username)
    password_field = driver.find_element(By.ID, 'password')
    password_field.send_keys(linkedin_password)
    password_field.send_keys(Keys.RETURN)
    time.sleep(2)

# # import validators
# def send_connection_request(profile_url):
#     # Validate the profile URL
#     if profile_url and validators.url(profile_url):
#         try:
#             driver.get(profile_url)
#             time.sleep(5)

#         except Exception as e:
#             print(f"An error occurred while trying to navigate to {profile_url}: {e}")
#     else:
#         print(f"Invalid URL: {profile_url}")



def navigate_to_company_employees_section(company_page_url):
    company_page_url = str(company_page_url)
    # Check if the URL is valid
    parsed_url = urlparse(company_page_url)
    if not parsed_url.scheme or not parsed_url.netloc:
        print(f"Invalid URL: {company_page_url}")
        return

    try:
        driver.get(company_page_url)
        # Find and click the link to the employees section
        employees_link = driver.find_element(By.CSS_SELECTOR, "a[href*='currentCompany'][id^='ember']")

        # Extract the text from the located element
        employees_text = employees_link.click()
        wait = WebDriverWait(driver, 10)
        search_box = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "search-global-typeahead__input")))
        time.sleep(5)

        keys = ['team lead', 'hr',]
        for key in keys:
            search_box.clear()
            search_box.send_keys(key)
            search_box.send_keys(Keys.ENTER)
            
            wait = WebDriverWait(driver, 10)
            wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "entity-result__actions")))
        
            # Locate the "Connect" buttons for the profiles in the search results
            connect_buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//button[contains(@aria-label, 'Invite') and contains(@class, 'artdeco-button')]")))
            try:
                for button in connect_buttons[:5]:  # Limit to top 5 profiles
                    driver.execute_script("arguments[0].scrollIntoView();", button)

                    driver.execute_script("arguments[0].click();", button)
                    time.sleep(2)
                    # Next Step to find the connect button and click on it
                    send_without_note_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Send without a note')]")))
                    time.sleep(1)
                    driver.execute_script("arguments[0].click();", send_without_note_button)
                    time.sleep(2)
            except Exception as e:
                print(f"Error interacting with connect buttons: {e}")

    

        time.sleep(10) 
    except Exception as e:
        print(f"An error occurred while trying to navigate to {company_page_url}: {e}")

# def find_and_connect(role):
#     print(f"Searching for...")
#     try:
#     # Wait up to 10 seconds for the search box to be present
#         search_box = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, 'xpath_to_search_box'))
#         )
#         # Now you can interact with the search box, e.g., sending keys
#         search_box.send_keys(role)
#         search_box.send_keys(Keys.RETURN)
#     except TimeoutException:
#         print("Timed out waiting for the search box to be present.")


#     print(f"Searching for {role}...")
#     print(search_box)
#     print("Searching for {role}...")
#     time.sleep(2)  # Wait for search results to load





# Read the Excel sheet
df = pd.read_excel('Job_list.xlsx')

def main():
    login_to_linkedin()
    for profile_url in df['LinkedIn']:
        if pd.notna(profile_url) and isinstance(profile_url, str):
            navigate_to_company_employees_section(profile_url)
            
            


main()

