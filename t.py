import os
from selenium import webdriver
from selenium_stealth import stealth
from user_agent import generate_user_agent

os.environ['PATH'] += r";C:/SeleniumDrivers"
userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'

if __name__ == "__main__":

    try:
        options = webdriver.ChromeOptions()

        options.add_argument('--no-sandbox')
        options.add_argument('--start-maximized')
        options.add_argument('--single-process')
        options.add_argument("--disable-xss-auditor")
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-running-insecure-content")
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

        driver.get("https://www.redbubble.com/auth/login")
    except Exception as e:
        print(e)
    finally:
        print('end')
        driver.close()
        driver.quit()
