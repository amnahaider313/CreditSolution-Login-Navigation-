import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

@pytest.mark.selenium
def test_add_customer_credit_limit():
    # --- Setup Chrome in headless mode ---
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    driver.get("http://192.168.4.239/credit_limit_solution/admin/Public/")

    wait = WebDriverWait(driver, 15)  # Increased timeout for slower pages

    try:
        # --- Login ---
        wait.until(EC.presence_of_element_located(
            (By.XPATH, "//input[@type='text' and contains(@class, 'login-input')]")
        )).send_keys("root")
        driver.find_element(By.XPATH, "//input[@type='password' and contains(@class, 'login-input')]") \
            .send_keys("Mercurial@786")
        driver.find_element(By.ID, "loginbutton").click()

        # --- Navigate to Customers > Add Customer ---
        wait.until(EC.element_to_be_clickable((By.XPATH, "//strong[text()='CUSTOMERS']"))).click()
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[@href='A2B_entity_card.php?section=1&atmenu=addsearch']")
        )).click()
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[contains(text(), 'Add Customer')]")
        )).click()

        # --- Fill in Form Fields ---
        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='credit']"))).send_keys("100")
        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='firstname']"))).send_keys("Amna")
        driver.find_element(By.XPATH, "//input[@name='lastname']").send_keys("Qatester")
        driver.find_element(By.XPATH, "//input[@name='city']").send_keys("Lahore")

        # --- Select Group ---
        group_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, "//select[@name='id_group']")))
        Select(group_dropdown).select_by_value("11")

        # --- Enter Unique Email ---
        unique_email = f"amna{int(time.time())}@yopmail.com"
        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='email']"))).send_keys(unique_email)

        # --- Submit Form ---
        confirm_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[contains(text(), 'CONFIRM DATA')]")
        ))
        driver.execute_script("arguments[0].scrollIntoView(true);", confirm_button)
        driver.execute_script("arguments[0].click();", confirm_button)  # JS click to avoid interception

        # --- Wait for URL change after submission ---
        wait.until(lambda d: "A2B_entity_card.php?section=1&id=" in d.current_url)
        current_url = driver.current_url
        print("Redirected URL:", current_url)
        assert "A2B_entity_card.php?section=1&id=" in current_url, "❌ Form submission failed or validation errors"

    except Exception as e:
        # Capture screenshot if test fails
        driver.save_screenshot("form_submission_error.png")
        raise e

    finally:
        driver.quit()
