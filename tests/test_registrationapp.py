import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

options = Options()
options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
options.add_argument("--headless=new") 

@pytest.fixture
def setup_teardown():
    """Setup and teardown for Selenium WebDriver."""
    # Initialize WebDriver with correct Chrome binary and driver version
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)

    # Provide driver to test
    yield driver

    # Quit driver after test
    driver.quit()


def get_alert_text(driver):
    """Helper function to get and accept alert text."""
    alert = Alert(driver)
    text = alert.text
    alert.accept()
    return text


# ===============================
#        Test Cases
# ===============================

def test_empty_username(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5001/")
    driver.find_element(By.NAME, "username").clear()
    driver.find_element(By.NAME, "pwd").send_keys("Password123")
    driver.find_element(By.NAME, "sb").click()
    time.sleep(1)
    alert_text = get_alert_text(driver)
    assert alert_text == "Username cannot be empty."


def test_empty_password(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5001/")
    driver.find_element(By.NAME, "username").send_keys("Pravalika")
    driver.find_element(By.NAME, "pwd").clear()
    driver.find_element(By.NAME, "sb").click()
    time.sleep(1)
    alert_text = get_alert_text(driver)
    assert alert_text == "Password cannot be empty."


def test_short_password(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5001/")
    driver.find_element(By.NAME, "username").send_keys("Meena")
    driver.find_element(By.NAME, "pwd").send_keys("abc1")
    driver.find_element(By.NAME, "sb").click()
    time.sleep(1)
    alert_text = get_alert_text(driver)
    assert alert_text == "Password must be at least 6 characters long."


def test_valid_input(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5001/")
    driver.find_element(By.NAME, "username").send_keys("Pravalika")
    driver.find_element(By.NAME, "pwd").send_keys("abc123")
    driver.find_element(By.NAME, "sb").click()
    time.sleep(2)

    current_url = driver.current_url
    assert "/submit" in current_url

    body_text = driver.find_element(By.TAG_NAME, "body").text
    assert "Hello, Pravalika! Welcome to the website" in body_text
