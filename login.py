from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

email = "saidoizna3@gmail.com"

# Firefox
driver = webdriver.Firefox()

driver.get("https://www.blsspainmorocco.net/MAR/account/login")

wait = WebDriverWait(driver, 20)

# Find the visible email field
email_inputs = wait.until(
    EC.presence_of_all_elements_located(
        (By.XPATH, "//label[contains(normalize-space(),'Email')]/following-sibling::input")
    )
)

for field in email_inputs:
    if field.is_displayed() and field.is_enabled():
        field.clear()
        field.send_keys(email)
        break

# Click Verify
verify_button = wait.until(
    EC.element_to_be_clickable((By.ID, "btnVerify"))
)
verify_button.click()
