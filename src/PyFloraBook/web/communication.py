from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import time

timeout = 10  # seconds

def wait_for_load(browser, attribute, class_to_look_for):
    try:
        element_present = EC.presence_of_element_located(
            (getattr(By, attribute), class_to_look_for)
            )
        WebDriverWait(browser, timeout).until(element_present)
        time.sleep(.5)
    except TimeoutException:
        pass

