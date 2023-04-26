
import pickle
import sys
import os

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from selenium_stealth import stealth


os.environ['PATH'] += r";C:/SeleniumDrivers"
user = 'alaodine'
mdp = 'poi098Aa@'

userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'


if __name__ == "__main__":
    try:
        # ua = UserAgent(use_cache_server=False)
        # userAgent = ua['google chrome'].random

        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--start-maximized')
        options.add_argument('--single-process')
        options.add_argument("--disable-xss-auditor")
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument('--disable-dev-shm-usage')
        # options.add_argument("--incognito")
        # options.add_argument("--disable-popup-blocking")
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument("disable-infobars")
        options.add_argument(f'user-agent={userAgent}')
        options.add_argument("--lang=en");

        # options.headless = True

        driver = webdriver.Chrome(options=options)
        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                run_on_insecure_origins= True
                )
        
        # driver.get("https://bot.sannysoft.com/")
        # time.sleep(10)
        driver.get("https://www.redbubble.com/auth/login")
        # time.sleep(5)

        WebDriverWait(driver, 30).until(
            EC.text_to_be_present_in_element(
                (By.XPATH, '//*[@id="RB_React_Component_LoginFormContainer_0"]/div/form/span/button/span/span'),
                'Log In')
        )
        name = driver.find_element(By.ID, "ReduxFormInput1")
        name.send_keys(user)
        pwd = driver.find_element(By.ID, "ReduxFormInput2")
        pwd.send_keys(mdp)
        logIn = driver.find_element(By.XPATH, '//*[@id="RB_React_Component_LoginFormContainer_0"]/div/form/span/button')
        logIn.click()

        WebDriverWait(driver, 90).until(
            EC.text_to_be_present_in_element(
                (By.XPATH, '//*[@id="app"]/div[1]/div/footer/div[5]/div/ul/li/span/span'),
                '© Redbubble. All Rights Reserved')
        )
        cookies = driver.get_cookies()
        pickle.dump(cookies, open("cookies.pkl", "wb"))
        print(cookies)
        time.sleep(20)

        print("done")
    except Exception as e:
        print(e)
    finally:
        driver.close()
        driver.quit()


