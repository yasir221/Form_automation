import os
from selenium import webdriver
from selenium.webdriver.common.by import By

os.environ['PATH'] += r"D:/SeleniumDrivers"
driver = webdriver.Chrome()


driver.get('https://www.w3schools.com/html/html_forms.asp')

driver.implicitly_wait(5)

sum1 = driver.find_element(By.ID,'fname')

sum2 = driver.find_element(By.ID,'lname')
print(sum1.text)
print(sum2.text)
# sum1.send_keys(15)
# sum2.send_keys(15)