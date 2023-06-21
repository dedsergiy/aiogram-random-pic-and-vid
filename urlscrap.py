from selenium import webdriver
import time
import os

os.environ['MOZ_HEADLESS'] = '1'
url = 'https://randomtube.xyz/'
driver = webdriver.Firefox()
driver.get(url=url)
time.sleep(2)

def take_url():
    vidurl = None
    while vidurl is None:
        driver.refresh()
        time.sleep(1)
        vidurl = driver.find_element(by='class name', value='player__video').get_attribute('src')
        if vidurl[-5:] == '.webm':
            vidurl = None
    return vidurl
