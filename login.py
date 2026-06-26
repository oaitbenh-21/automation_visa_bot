from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from image_process import base64_to_image, solve_captcha_image
import re

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

# Wait for the challenge text to appear
challenge = wait.until(
    EC.visibility_of_element_located(
        (By.XPATH, "//div[contains(text(),'Please select all boxes with number')]")
    )
)

text = challenge.text
print("Challenge:", text)

# Extract the number
match = re.search(r"\d+", text)
if match:
    number = match.group(0)
    print("Number:", number)
else:
    print("No number found.")

import re

# Wait until the captcha images are loaded
images = wait.until(
    EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "img.captcha-img")
    )
)

captcha_images = []

for i, img in enumerate(images, start=1):
    src = img.get_attribute("src")

    if src.startswith("data:image"):
        base64_data = src.split(",", 1)[1]

        image = base64_to_image(base64_data)

        processed = preprocess(image)

        text = solve_captcha_image(processed)

        print(f"Image {i} -> OCR: {text}")
