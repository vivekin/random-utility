import time
from PIL import Image
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ocrapi import solve_captcha

var_consumerno=''
var_phone=''

print("Script running ...")

now = datetime.now()
formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
print(f"Date: {formatted_time}")

# Creating an instance webdriver
browser = webdriver.Firefox()
wait = WebDriverWait(browser, 10)

loggedin=False
while(loggedin==False):
    browser.get("https://wss.kseb.in/selfservices/quickpay")
    consumerno = browser.find_element(By.XPATH,'//*[@id="ConsumerNo"]',)
    consumerno.send_keys(Keys.CONTROL + 'a', Keys.BACKSPACE)
    consumerno.send_keys(var_consumerno)
    phone = browser.find_element(By.XPATH,'//*[@id="phoneNum"]',)
    phone.send_keys(Keys.CONTROL + 'a', Keys.BACKSPACE)
    phone.send_keys(var_phone)

    time.sleep(2)
    captcha_img = browser.find_element(By.XPATH, '//*[@id="Vimage"]')
    image_bytes = captcha_img.screenshot_as_png

    with open("temp_captcha.png", "wb") as f:
        f.write(image_bytes)
    captcha_text = solve_captcha("temp_captcha.png")
    time.sleep(1)

    captcha = browser.find_element(By.XPATH,'//*[@id="code"]',)
    captcha.send_keys(Keys.CONTROL + 'a', Keys.BACKSPACE)
    captcha.send_keys(captcha_text)
    time.sleep(10)
    submit = browser.find_element(By.XPATH, '//*[@id="see-bill-due"]')
    submit.click()
    try:
        toast = WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/form[1]/div[1]/div/div[4]/div/div[2]")))
        print(f"error: {toast.text}")
        # if ("Please" in toast.text):
        #     print("Invalid captcha message")
        print("Login failed ...")
        # captcha_refresh = browser.find_element(By.XPATH, '//*[@id="refreshButton"]')
        # captcha_refresh.click()
    except:
        print("Login succedded ...")
        loggedin=True
time.sleep(3)

print("=========================================")
print(f"Consumer No: {var_consumerno}")
cname = browser.find_element(By.XPATH, "/html/body/div[3]/form[2]/div/div[1]/div/div[3]/div[1]/div[2]/input[1]")
print(f"Consumer Name: {cname.get_attribute('value')}")
sname = browser.find_element(By.XPATH, "/html/body/div[3]/form[2]/div/div[1]/div/div[3]/div[2]/div[2]/input")
print(f"Section Name: : {sname.get_attribute('value')}")
tcode = browser.find_element(By.XPATH, "/html/body/div[3]/form[2]/div/div[1]/div/div[4]/div[1]/div[2]/input")
print(f"Tariff Code: : {tcode.get_attribute('value')}")
bamt = browser.find_element(By.XPATH, "/html/body/div[3]/form[2]/div/div[1]/div/div[4]/div[2]/div[2]/div/input")
print(f"Bill Amount: {bamt.get_attribute('value')}")
duedate = browser.find_element(By.XPATH, "/html/body/div[3]/form[2]/div/div[1]/div/div[5]/div[1]/div[2]/input")
print(f"Due Date: {duedate.get_attribute('value')}")
ddate = browser.find_element(By.XPATH, "/html/body/div[3]/form[2]/div/div[1]/div/div[5]/div[2]/div[2]/input")
print(f"Disconnection Date: : {ddate.get_attribute('value')}")
damt = browser.find_element(By.XPATH, "/html/body/div[3]/form[2]/div/div[1]/div/div[6]/div[1]/div[2]/input")
print(f"Due Amount: {damt.get_attribute('value')}")
pamt = browser.find_element(By.XPATH, '//*[@id="paymentamount"]')
print(f"Payment Amount(Rs.): {pamt.get_attribute('value')}")
email = browser.find_element(By.XPATH, "/html/body/div[3]/form[2]/div/div[1]/div/div[7]/div[1]/div[2]/input")
print(f"Email Id: : {email.get_attribute('value')}")
mob = browser.find_element(By.XPATH, "/html/body/div[3]/form[2]/div/div[1]/div/div[7]/div[2]/div[2]/input")
print(f"Mobile Number: : {mob.get_attribute('value')}")
print("=========================================")

time.sleep(2)
browser.close()
print("Script exiting ...")
