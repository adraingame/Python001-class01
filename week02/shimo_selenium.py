from selenium import webdriver
import time

try:
    browser = webdriver.Chrome()
    
    browser.get('https://shimo.im/login?from=home')
    time.sleep(1)


    browser.find_element_by_xpath('//input[@name="mobileOrEmail"]').send_keys('raingame@163.com')
    browser.find_element_by_xpath('//input[@name="password"]').send_keys('liuhedong123')
    time.sleep(5)
    browser.find_element_by_xpath('//button[@type="black"]').click()
    time.sleep(15)

    cookies = browser.get_cookies() # 获取cookies
    print(cookies)
    time.sleep(3)

except Exception as e:
    print(e)
finally:    
    browser.close()