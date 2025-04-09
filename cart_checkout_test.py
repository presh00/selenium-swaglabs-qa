from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Utility: Login user
def login(driver, username="standard_user", password="secret_sauce"):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()
    time.sleep(1)

# Test: Add product to cart
def test_add_to_cart():
    driver = webdriver.Chrome()
    try:
        print("Test: Add product to cart")
        login(driver)
        driver.find_element(By.CLASS_NAME, "btn_inventory").click()
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
        assert len(cart_items) == 1
        print("✅ Item successfully added to cart")
    finally:
        driver.quit()

# Test: Remove product from cart
def test_remove_from_cart():
    driver = webdriver.Chrome()
    try:
        print("Test: Remove product from cart")
        login(driver)
        driver.find_element(By.CLASS_NAME, "btn_inventory").click()
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        driver.find_element(By.CLASS_NAME, "cart_button").click()
        cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
        assert len(cart_items) == 0
        print("✅ Item removed successfully")
    finally:
        driver.quit()

#  Test: Complete checkout with valid data
def test_valid_checkout():
    driver = webdriver.Chrome()
    try:
        print("Test: Valid checkout")
        login(driver)
        driver.find_element(By.CLASS_NAME, "btn_inventory").click()
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        driver.find_element(By.ID, "checkout").click()
        driver.find_element(By.ID, "first-name").send_keys("John")
        driver.find_element(By.ID, "last-name").send_keys("Doe")
        driver.find_element(By.ID, "postal-code").send_keys("12345")
        driver.find_element(By.ID, "continue").click()
        driver.find_element(By.ID, "finish").click()
        complete_msg = driver.find_element(By.CLASS_NAME, "complete-header").text
        assert "THANK YOU" in complete_msg.upper()
        print("✅ Checkout completed successfully")
    finally:
        driver.quit()

# Test: Checkout with empty cart
def test_checkout_with_empty_cart():
    driver = webdriver.Chrome()
    try:
        print("Test: Checkout with empty cart")
        login(driver)
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        driver.get("https://www.saucedemo.com/checkout-step-one.html")
        page_title = driver.find_element(By.CLASS_NAME, "title").text
        assert "CHECKOUT" in page_title.upper()
        print("🟡 Reached checkout page with empty cart (no item to purchase)")
    finally:
        driver.quit()

# Test: Checkout with missing first name
def test_checkout_missing_first_name():
    driver = webdriver.Chrome()
    try:
        print("Test: Missing first name in checkout")
        login(driver)
        driver.find_element(By.CLASS_NAME, "btn_inventory").click()
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        driver.find_element(By.ID, "checkout").click()
        driver.find_element(By.ID, "last-name").send_keys("Doe")
        driver.find_element(By.ID, "postal-code").send_keys("12345")
        driver.find_element(By.ID, "continue").click()
        error = driver.find_element(By.CLASS_NAME, "error-message-container").text
        assert "first name is required" in error.lower()
        print("✅ Proper error for missing first name")
    finally:
        driver.quit()

# Test: Checkout with missing last name
def test_checkout_missing_last_name():
    driver = webdriver.Chrome()
    try:
        print("Test: Missing last name in checkout")
        login(driver)
        driver.find_element(By.CLASS_NAME, "btn_inventory").click()
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        driver.find_element(By.ID, "checkout").click()
        driver.find_element(By.ID, "first-name").send_keys("John")
        driver.find_element(By.ID, "postal-code").send_keys("12345")
        driver.find_element(By.ID, "continue").click()
        error = driver.find_element(By.CLASS_NAME, "error-message-container").text
        assert "last name is required" in error.lower()
        print("✅ Proper error for missing last name")
    finally:
        driver.quit()

# Test: Checkout with missing postal code
def test_checkout_missing_postal_code():
    driver = webdriver.Chrome()
    try:
        print("Test: Missing postal code in checkout")
        login(driver)
        driver.find_element(By.CLASS_NAME, "btn_inventory").click()
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        driver.find_element(By.ID, "checkout").click()
        driver.find_element(By.ID, "first-name").send_keys("John")
        driver.find_element(By.ID, "last-name").send_keys("Doe")
        driver.find_element(By.ID, "continue").click()
        error = driver.find_element(By.CLASS_NAME, "error-message-container").text
        assert "postal code is required" in error.lower()
        print("✅ Proper error for missing postal code")
    finally:
        driver.quit()

# Test: Invalid postal code (symbols)
def test_checkout_invalid_postal_code():
    driver = webdriver.Chrome()
    try:
        print("Test: Invalid postal code in checkout")
        login(driver)
        driver.find_element(By.CLASS_NAME, "btn_inventory").click()
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        driver.find_element(By.ID, "checkout").click()
        driver.find_element(By.ID, "first-name").send_keys("John")
        driver.find_element(By.ID, "last-name").send_keys("Doe")
        driver.find_element(By.ID, "postal-code").send_keys("!@#$%")
        driver.find_element(By.ID, "continue").click()
        # SauceDemo does not validate format, but good to document
        print(" No validation for invalid postal code (improvement area)")
    finally:
        driver.quit()

# Run all tests
if __name__ == "__main__":
    test_add_to_cart()
    test_remove_from_cart()
    test_valid_checkout()
    test_checkout_with_empty_cart()
    test_checkout_missing_first_name()
    test_checkout_missing_last_name()
    test_checkout_missing_postal_code()
    test_checkout_invalid_postal_code()
