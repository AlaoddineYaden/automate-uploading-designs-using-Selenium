import pickle
import os
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
from selenium.webdriver.support.wait import WebDriverWait
from openpyxl import load_workbook
from selenium_stealth import stealth
from user_agent import generate_user_agent

os.environ['PATH'] += r";C:/SeleniumDrivers"
userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'

if __name__ == "__main__":
    class upload_complet_check(object):

        def __init__(self, locator, text):
            self.locator = locator
            self.text = text

        def __call__(self, driver):
            # Finding the referenced element
            element = driver.find_element(*self.locator)
            if self.text == element.get_attribute("data-value").title():
                return True
            else:
                return False

    copy_settings_url = 'https://www.redbubble.com/portfolio/images/122233479-aries-zodiac-the-aries-astrology-new-design/duplicate'

    try:
        # reading file from ./

        try:
            book = load_workbook('book.xlsx')
            sheet = book.active
            rows = sheet.rows

            headers = [cell.value for cell in next(rows)]

            all_rows = []

            for row in rows:
                data = {}
                for title, cell in zip(headers, row):
                    data[title] = cell.value
                all_rows.append(data)
        except Exception as e:
            print('file exeption ' + e)
        finally:
            print('end reading file')

        # ua = UserAgent(use_cache_server=False)
        # userAgent = ua.random

        options = webdriver.ChromeOptions()

        options.add_argument('--no-sandbox')
        options.add_argument('--start-maximized')
        options.add_argument('--single-process')
        options.add_argument("--disable-xss-auditor")
        # options.add_argument("--disable-web-security")
        # options.add_argument("--allow-running-insecure-content")
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("disable-infobars")
        user_agent = generate_user_agent(navigator='chrome')
        options.add_argument(f'user-agent={userAgent}')
        options.add_argument("--lang=en")
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        # options.headless = True

        driver = webdriver.Chrome(options=options)
        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                run_on_insecure_origins=True
                )
        # load cookies
        print('loeading cookies')
        driver.get("https://www.redbubble.com/auth/login")
        WebDriverWait(driver, 60).until(
            EC.text_to_be_present_in_element(
                (By.XPATH,
                 '//*[@id="RB_React_Component_LoginFormContainer_0"]/div/form/span/button/span/span'),
                'Log In')
        )
        original_window = driver.current_window_handle
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            cookie['domaine'] = '.redbubble.com'
            try:
                driver.add_cookie(cookie)
            except Exception as e:
                print(e)
        print('done loading cookies')
        time.sleep(1)
        x = 0

        for r in all_rows:
            title_text = r['titre']
            tags_text = r['tags']
            description_text = r['description']
            image_path = r['path']

            try:
                driver.switch_to.new_window('tab')

                WebDriverWait(driver, 30).until(EC.number_of_windows_to_be(2))

                driver.get(copy_settings_url)
                
                # time.sleep(20)

                WebDriverWait(driver, 60).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, '//*[@id="add-new-work"]'))
                )
                if x == 0:
                    WebDriverWait(driver, 120).until(
                        EC.presence_of_all_elements_located(
                            (By.XPATH, '/html/body/div[52]/iframe'))
                    )
                    time.sleep(5)
                    iframe = driver.find_element(
                        By.XPATH, '/html/body/div[52]/iframe')
                    driver.switch_to.frame(iframe)
                    time.sleep(5)

                    driver.find_element(By.ID, 'button2').send_keys(Keys.ENTER)
                    time.sleep(1)
                    driver.switch_to.default_content()
                    time.sleep(1)

                title = driver.find_element(
                    By.XPATH, '//*[@id="work_title_en"]')
                title.clear()
                title.send_keys(title_text)
                time.sleep(1)

                tags = driver.find_element(
                    By.XPATH, '//*[@id="work_tag_field_en"]')
                tags.clear()
                tags.send_keys(tags_text)
                time.sleep(1)

                discription = driver.find_element(By.XPATH,
                                                  '/html/body/div[1]/div[5]/div[2]/form/div/div[2]/div/div/div['
                                                  '1]/div/div[3]/textarea')
                discription.clear()
                discription.send_keys(description_text)
                time.sleep(1)

                replaceAllImagesBtn = driver.find_element(
                    By.CSS_SELECTOR, '#select-image-base')
                replaceAllImagesBtn.send_keys(image_path)

                WebDriverWait(driver, 120).until(
                    upload_complet_check(
                        (By.XPATH, '//*[@id="add-new-work"]/div/div[1]/div[1]/div[1]'), '100')
                )

                time.sleep(1)

                agree = driver.find_element(
                    By.XPATH, '/html/body/div[1]/div[5]/div[2]/form/section[2]/div[3]/input')
                agree.click()

                time.sleep(1)

                save_work = driver.find_element(
                    By.XPATH, '//*[@id="submit-work"]')
                save_work.click()

                WebDriverWait(driver, 120).until(
                    EC.text_to_be_present_in_element(
                        (By.XPATH,
                         '//*[@id="app"]/div/div[1]/div[2]/div/div/div/div[2]/div[2]/div[1]/div[1]/h1'),
                        title_text)
                )
                x = x + 1
                time.sleep(1)
            except Exception as e:
                print(e)
            finally:
                print(f'done process {x}')
                driver.close()
                driver.switch_to.window(original_window)
        time.sleep(1)

    except Exception as e:
        print(e)
    finally:
        print('end')
        driver.close()
        driver.quit()
