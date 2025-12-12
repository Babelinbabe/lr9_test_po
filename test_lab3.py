from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pytest

@pytest.fixture
def driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()

def test_open_page(driver):
    driver.get("https://the-internet.herokuapp.com/login")
    assert "The Internet" in driver.title

def test_login_success(driver):
    driver.get("https://the-internet.herokuapp.com/login")
    username_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')

    username_input.send_keys("tomsmith")
    password_input.send_keys("SuperSecretPassword!")
    login_button.click()

    flash_message = driver.find_element(By.ID, "flash")
    assert "You logged into a secure area!" in flash_message.text

    logout_button = driver.find_element(By.CSS_SELECTOR, 'a[href="/logout"]')
    assert logout_button.is_displayed()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])