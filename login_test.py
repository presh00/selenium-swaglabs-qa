from selenium import webdriver
from selenium.webdriver.common.by import By
import time

print("Running Selenium tests...")

# Reusable login function
def login(driver, username, password):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()
    time.sleep(1)

# Test 1: Valid login
def test_valid_login():
    driver = webdriver.Chrome()
    try:
        print("Testing: Valid login")
        login(driver, "standard_user", "secret_sauce")
        assert "inventory" in driver.current_url
        print("✅ Successful login")
    finally:
        driver.quit()

# Test 2: Locked-out user login
def test_invalid_login():
    driver = webdriver.Chrome()
    try:
        print("Testing: Locked out user login")
        login(driver, "locked_out_user", "secret_sauce")
        error_msg = driver.find_element(By.CLASS_NAME, "error-message-container").text
        assert "locked out" in error_msg.lower()
        print("✅ Locked out user message displayed")
    finally:
        driver.quit()

# Test 3: Invalid username and password
def test_invalid_username_password():
    driver = webdriver.Chrome()
    try:
        print("Testing: Invalid username and password")
        login(driver, "wrong_user", "wrong_pass")
        error = driver.find_element(By.CLASS_NAME, "error-message-container").text
        assert "username and password do not match" in error.lower() or "epic sadface" in error.lower()
        print("✅ Error message displayed for invalid credentials")
    finally:
        driver.quit()

#Test 4: Empty username and password fields
def test_empty_username_password():
    driver = webdriver.Chrome()
    try:
        print("Testing: Empty username and password")
        login(driver, "", "")
        error = driver.find_element(By.CLASS_NAME, "error-message-container").text
        assert "username and password do not match" in error.lower() or "epic sadface" in error.lower()
        print("✅ Error message displayed for invalid credentials")
    finally:
        driver.quit()


if __name__ == "__main__":
    test_valid_login()
    test_invalid_login()
    test_invalid_username_password()
    test_empty_username_password()
