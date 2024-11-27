import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Go to the login page and attempt to log in if cookies are not available
def login(driver):
    try:
        driver.get("https://17fit.com/account?show_fb=1&success_url=https://17fit.com/authorization/jwt?success_url=https://17fit.com/&fail_url=https://17fit.com/&cancel_url=https://17fit.com/")

        # Go to login page if no cookies are available
        goToLoginPageButton = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/div[4]/div/div[2]/button"))
        )
        goToLoginPageButton.click()

        # Input gmail
        gmail_input = WebDriverWait(driver, 2).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input.st-mb-0.st-text-black.st-p-3.st-w-full.st-border-none.st-bg-transparent"))
        )
        gmail_input.clear()
        gmail_input.send_keys("weihong609193@gmail.com")

        next_button = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'st-bg-primary') and contains(., '下一步')]"))
        )
        next_button.click()

        # Input password
        password_input = WebDriverWait(driver, 2).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
        )
        password_input.clear()
        password_input.send_keys("Hong609193")  

        login_button = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'st-bg-primary') and contains(., '登入')]"))
        )

        login_button.click()
        WebDriverWait(driver, 2).until(
            EC.visibility_of_element_located((By.XPATH, "//a[contains(text(), '我的帳戶')]"))  # Use "我的帳戶" text to confirm login
        )
        print("Login successful.")
    except Exception as e:
        print("Error during login process:", e)

# Go to the appointment page and start booking
def appointment(driver):
    try:
        # Go to the appointment page
        driver.get("https://17fit.com/NCUsportscenter/01?tab=appointments")
        print("Navigated to the appointment page.")
        
        # Click the reservation button
        reservation_button = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'btn--black') and text()='預約']"))
        )
        reservation_button.click()
        print("Clicked on reservation button.")

        # Select the court
        court_name = "桌球場01"
        court_item = WebDriverWait(driver, 2).until(
            EC.visibility_of_element_located((By.XPATH, f"//h6[text()='{court_name}']/.."))
        )
        print(f"Found court: {court_name}")

        select_button = WebDriverWait(court_item, 2).until(
            EC.element_to_be_clickable((By.XPATH, ".//ancestor::div[contains(@class, 'staff_box')]//a[contains(@class, 'price')]"))
        )
        select_button.click()

        # Select the date
        retries = 0
        date_str = "11/29"
        while retries < 3:  # Retry 3 times before giving up
            try:
                date_button = WebDriverWait(driver, 2).until(
                    EC.element_to_be_clickable((By.XPATH, f"//div[@data-date='2024/{date_str}']"))
                )
                date_button.click()  
                print(f"Clicked on date: {date_str}.")
                break  

            except Exception as e:
                print(f"Date {date_str} button not found, trying to click next button ({retries + 1}/3):", e)
                click_next_button(driver)  # Retry by clicking the next button
                retries += 1
        
        # Check if the date was successfully selected
        if retries == 3:
            print(f"Could not find the date {date_str} after multiple attempts.")
            return  # Exit the function if the date is not available

        # Select the time
        time_str = "09:00"
        time_elements = WebDriverWait(driver, 2).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "stime"))
        )

        print(f"Found {len(time_elements)} time elements.")
        time_found = False
        for time_element in time_elements:
            if time_element.text.strip() == time_str:
                print(f"Found time: {time_str}")
                # Locate the corresponding "Select" button and click
                select_button = time_element.find_element(By.XPATH, "./following-sibling::a[contains(@class, 'select_time_in')]")
                select_button.click()
                print(f"Clicked on select button for time: {time_str}.")
                time_found = True
                break
        
        if not time_found:
            print(f"Time {time_str} not found.")
            return  # Exit if the time is not available

    except Exception as e:
        print(f"Error during appointment selection: {e}")

# Click next button if required
def click_next_button(driver):
    try:
        next_button = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, "//i[contains(@class, 'btn-right')]"))
        )
        next_button.click()
        print("Clicked the next button.")
        time.sleep(1)
    except Exception as e:
        print("Error: Unable to find the next button:", e)

# Confirm the appointment
def confirm_appointment(driver):
    try:
        confirm_button = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'booking-btn') and contains(@class, 'primary-business-color-background') and text()='確認預約']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", confirm_button)
        time.sleep(1)
        confirm_button.click()
        print("Confirmed the appointment.")

        # Wait for confirmation
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), '預約成功') or contains(text(), '預約確認')]"))
        )
        print("Appointment confirmed successfully.")
    except Exception as e:
        print(f"Error during appointment confirmation: {e}")

# Main execution function
def main():
    try:
        chrome_options = Options()
        driver = webdriver.Chrome(options=chrome_options)
        
        # First, attempt to log in using cookies if available
        login(driver)

        # Proceed with the appointment process
        appointment(driver)

        # Confirm the appointment
        confirm_appointment(driver)
        
    except Exception as e:
        print(f"Error during execution: {e}")
    finally:
        driver.quit()  # Always close the browser

if __name__ == "__main__":
    main()
