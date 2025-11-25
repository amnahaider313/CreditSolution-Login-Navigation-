from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize Chrome WebDriver
driver = webdriver.Chrome()
driver.maximize_window()
driver.get("http://192.168.4.239/credit_limit_solution/admin/Public/")

wait = WebDriverWait(driver, 10)

# --- Login ---
wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='text' and contains(@class, 'login-input')]"))) \
    .send_keys("root")
driver.find_element(By.XPATH, "//input[@type='password' and contains(@class, 'login-input')]") \
    .send_keys("Mercurial@786")
driver.find_element(By.ID, "loginbutton").click()

# --- Navigate to Customers > Add Customer ---
wait.until(EC.element_to_be_clickable((By.XPATH, "//strong[text()='CUSTOMERS']"))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='A2B_entity_card.php?section=1&atmenu=addsearch']"))) \
    .click()
wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Add Customer')]"))).click()

# --- Fill in Credit Field ---
credit_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='credit']")))
credit_input.clear()
credit_input.send_keys("100")

# Fill First Name
first_name = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='firstname']")))
first_name.send_keys("Amna")

# Fill Last Name
last_name = driver.find_element(By.XPATH, "//input[@name='lastname']")
last_name.send_keys("Qatester")

# Fill City
city = driver.find_element(By.XPATH, "//input[@name='city']")
city.send_keys("Lahore")


# --- Select Group from Dropdown ---
group_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, "//select[@name='id_group']")))
Select(group_dropdown).select_by_value("11")  # e.g., "qa testers grp"

# --- Enter Email ---
email_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='email']")))
email_input.send_keys("amna1@yopmail.com")

# Optional: Pause to observe before closing
time.sleep(2)

# Click the CONFIRM DATA button
confirm_button = driver.find_element(By.XPATH, "//a[contains(text(), 'CONFIRM DATA')]")
confirm_button.click()


expected_url = "http://192.168.4.239/credit_limit_solution/admin/Public/A2B_entity_card.php?section=1&id=556"
if driver.current_url == expected_url:
    print("✅ Form submitted successfully and redirected.")
else:
    print("❌ Still on same page, likely validation errors.")
time.sleep(2)
driver.quit()
