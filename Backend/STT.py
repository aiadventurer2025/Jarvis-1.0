from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

# Suppress ChromeDriver logs
os.environ['WDM_LOG_LEVEL'] = '0'

class SpeechRecognizer:
    def __init__(self):
        self.is_active = False
        self.driver = self._initialize_driver()
        self._load_html()
        self._click_start()

    def _initialize_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--use-fake-ui-for-media-stream")
        chrome_options.add_argument("--use-fake-device-for-media-stream")
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        service = Service(ChromeDriverManager().install(), log_path=None)
        return webdriver.Chrome(service=service, options=chrome_options)

    def _load_html(self):
        html_path = f"file:///{os.getcwd()}/Backend/Data/voice.html"
        self.driver.get(html_path)

    def _click_start(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "start"))
            ).click()
        except Exception as e:
            print(f"Error starting recognition: {e}")
            self._restart_driver()

    def _clear_output(self):
        try:
            self.driver.execute_script("document.getElementById('output').textContent = '';")
        except Exception as e:
            print(f"Error clearing output: {e}")
            self._restart_driver()

    def _get_text(self):
        try:
            return self.driver.find_element(By.ID, "output").text.strip()
        except Exception as e:
            print(f"Error getting text: {e}")
            self._restart_driver()
            return ""

    def _restart_driver(self):
        """Restart the WebDriver instance to recover from errors."""
        try:
            self.driver.quit()
        except:
            pass
        self.driver = self._initialize_driver()
        self._load_html()
        self._click_start()

    def listen(self):
        while True:
            try:
                text = self._get_text()
                if not text:
                    continue

                # Handle activation
                if not self.is_active:
                    if "jarvis" in text.lower():
                        self.is_active = True
                        command = text.lower().split("jarvis", 1)[-1].strip()
                        self._clear_output()
                        if command:
                            return command

                # Handle deactivation
                if self.is_active and "exit" in text.lower():
                    self.is_active = False
                    self._clear_output()
                    return None

                # Handle normal commands
                if self.is_active:
                    self._clear_output()
                    return text

            except Exception as e:
                print(f"Error in listen loop: {e}")
                self._restart_driver()
# Singleton instance
recognizer = SpeechRecognizer()

def SpeechRecognition():
    return recognizer.listen()