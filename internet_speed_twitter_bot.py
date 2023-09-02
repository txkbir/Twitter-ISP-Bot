import secrets
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class InternetSpeedTwitterBot:
    def __init__(self):
        self.down: int
        self.up: int

        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.get("https://twitter.com/home")
        self.driver.maximize_window()

        time.sleep(1)
        username_entry = self.driver.find_element(By.CSS_SELECTOR, value="input")
        username_entry.send_keys(secrets.TWITTER_EMAIL)

        next_button = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/'
                                                         'div/div[2]/div[2]/div/div/div/div[6]/div/span/span')
        next_button.click()
        time.sleep(3)

        try:
            verify_input = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]'
                                                              '/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/'
                                                              'div[2]/div/input')
            verify_input.send_keys(secrets.USERNAME)
            continue_button = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div'
                                                                 '[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div')
            continue_button.click()
        except NoSuchElementException:
            pass

        time.sleep(3)
        password_entry = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/'
                                                            'div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/'
                                                            'div[2]/div[1]/input')
        password_entry.send_keys(secrets.TWITTER_PASSWORD)

        log_in_button = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div'
                                                           '/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div')
        log_in_button.click()

        self.get_internet_speed()

    def get_internet_speed(self):
        time.sleep(3)
        self.driver.get("https://www.speedtest.net/")
        time.sleep(10)
        start_button = self.driver.find_element(By.CSS_SELECTOR, value="a .start-text")
        start_button.click()

        time.sleep(60)

        download_speed = self.driver.find_element(By.CLASS_NAME, value="download-speed")
        self.down = float(download_speed.text)

        upload_speed = self.driver.find_element(By.CLASS_NAME, value="upload-speed")
        self.up = float(upload_speed.text)

        self.tweet_at_provider()

    def tweet_at_provider(self):
        if self.down < secrets.PROMISED_DOWN or self.up < secrets.PROMISED_UP:
            self.driver.get("https://twitter.com/home")
            time.sleep(5)
            tweet_button = self.driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/header/div/div/div/'
                                                              'div[1]/div[3]/a/div')
            tweet_button.click()
            time.sleep(1)
            tweet = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/'
                                                       'div/div/div[3]/div[2]/div[1]/div/div/div/div[1]/div[2]/div/div/'
                                                       'div/div/div/div/div[2]/div/div/div/div/label/div[1]/div/div/div'
                                                       '/div/div/div[2]/div/div/div/div')
            tweet.send_keys(
                f'Hey @CharterCom, why is my internet speed {self.down}down/{self.up}up when I pay for '
                f'{secrets.PROMISED_DOWN}down/{secrets.PROMISED_UP}up?'
            )

            send_tweet = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]'
                                                            '/div/div/div/div[3]/div[2]/div[1]/div/div/div/div[2]/'
                                                            'div[2]/div/div/div[2]/div[4]/div')
            send_tweet.click()
