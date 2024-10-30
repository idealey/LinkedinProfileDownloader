import winsound
from selenium import webdriver
import urllib.request
from getpass import getpass

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, InvalidArgumentException
import logging

from twocaptcha import TwoCaptcha

LINKEDIN_URL = 'https://www.linkedin.com/checkpoint/lg/sign-in-another-account'

solver = TwoCaptcha('API_KEY')


config = {
            'server':           '2captcha.com',
            'apiKey':           'API_KEY',
            'softId':            123,
            'callback':         'https://your.site/result-receiver',
            'defaultTimeout':    120,
            'recaptchaTimeout':  600,
            'pollingInterval':   10,
        }



logging.basicConfig(filename='out.log',
                    filemode='w',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


email = input('Login: ')
password = getpass('Password: ')

browser = webdriver.Chrome()


login_selector = '#username'
pass_selector = '#password'
accept_selector = '#organic-div > form > div.login__form_action_container > button'
link_to_profile_classname = 'profile-card-profile-picture-container'
target_photo_profile_classname = 'profile-photo-edit__preview'
checkpoint_btn_selector = '#home_children_button'

try:
    browser.get(LINKEDIN_URL)
    logging.info('Opening LinkedIn login page')
except InvalidArgumentException:
    logging.error('Page is not found')
    exit(1)

(WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, login_selector)))
    .send_keys(email))
logging.info('Entered email')
(WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, pass_selector)))
    .send_keys(password))
logging.info('Entered password')


WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, accept_selector))).click()
if browser.current_url == LINKEDIN_URL:
    logging.error('Wrong credential')
    exit(1)


if 'challenge' in browser.current_url:
    winsound.Beep(1000, 200)
    print('Pass the captcha manually')
    #Також можливо скористатися платним сервісом для виріщення капчі.
    # result = solver.funcaptcha(sitekey='3117BF26-4762-4F5A-8ED9-A85E69209A46', url=browser.current_url)
    # if 'code' in result:
    #         logging.info('Success, code:', result['code'])
    #     else:
    #         logging.error('Error:', result)

WebDriverWait(browser, 360).until(EC.visibility_of_element_located((By.CLASS_NAME, link_to_profile_classname))).click()
logging.info('Go to the profile')

logging.info('Searching for a photo...')
try:
    photo = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CLASS_NAME,
                                                                               target_photo_profile_classname)))
except NoSuchElementException:
    logging.error('Photo is not found')
    exit(1)

photo_url = photo.get_attribute(name='src')
logging.info('Receive a link to the photo...')
photo_alt = photo.get_attribute(name='alt')
logging.info('Receiving photo signature...')
logging.info('Downloading profile...')
urllib.request.urlretrieve(photo_url, f'./photo_profiles/{photo_alt}.jpg')


browser.quit()
logging.info('Browser quit')


