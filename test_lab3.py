from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pytest
import time


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Для CI/CD без GUI
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


def test_open_page(driver):
    driver.get("https://the-internet.herokuapp.com/login")
    assert "The Internet" in driver.title
    print("Page opened successfully")


def test_login_success(driver):
    driver.get("https://the-internet.herokuapp.com/login")

    # Явные ожидания
    wait = WebDriverWait(driver, 10)

    username_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
    password_input = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')

    username_input.send_keys("tomsmith")
    password_input.send_keys("SuperSecretPassword!")
    login_button.click()

    # Ждем появления flash сообщения
    flash_message = wait.until(EC.presence_of_element_located((By.ID, "flash")))
    assert "You logged into a secure area!" in flash_message.text

    logout_button = driver.find_element(By.CSS_SELECTOR, 'a[href="/logout"]')
    assert logout_button.is_displayed()

    # Делаем скриншот для отчета
    driver.save_screenshot("login_success.png")
    print("Login test passed")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--html=report.html", "--self-contained-html"])s