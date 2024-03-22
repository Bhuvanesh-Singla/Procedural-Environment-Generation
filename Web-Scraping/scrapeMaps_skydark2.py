"""
scrapeMaps.py
Retrieve map data automatically

note that the selenium webdriver for mozilla is required to be in the project folder.

Download a copy at https://github.com/mozilla/geckodriver/releases
"""

# Selenium is a web driver wrapper
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
# to check for alerts:
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
# some essential python libraries to make it chooch
import os
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
import random
import time
from rename import rename


def draw_map():
    """
    returns world_map: a Basemap object that contains the entire world. This will tell us whether or not a random GPS coordinate is on land
    """
    bottomlat = -89.0
    toplat = 89.0
    bottomlong = -170.0
    toplong =  170.0
    gridsize = 0.1
    world_map = Basemap(projection="merc", resolution = 'c', area_thresh = 0.1,llcrnrlon=bottomlong, llcrnrlat=bottomlat, urcrnrlon=toplong, urcrnrlat=toplat)
    world_map.drawcoastlines(color='black')
    return world_map


def main():



    # To prevent download dialog
    def initialize():
        options = Options()
        profile = webdriver.FirefoxProfile()
        profile.set_preference('browser.download.folderList', 2) # custom location
        profile.set_preference('browser.download.manager.showWhenStarting', False)
        profile.set_preference('browser.download.alwaysOpenPanel', False)
        profile.set_preference('browser.download.dir', '/tmp')
        profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')
        profile.set_preference("browser.download.dir", "C:\\Users\\singl\\Desktop\\Bhuvanesh\\NITK\\Procedural Environment Generation\\Dataset\\skydark\\trial3\\")
        profile.set_preference("browser.download.useDownloadDir", True)
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "zip")

        profile.update_preferences()
        options.profile = profile

        driver=webdriver.Firefox(options=options)
        # driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)

        # capture the screen
        # driver.get_screenshot_as_file("capture.png")

        # navigate to the page you want to acquire data from
        driver.get("https://heightmap.skydark.pl/")
        alert = Alert(driver)
        print(alert.text)
        alert.accept()


        # save_button = driver.find_element(By.CSS_SELECTOR, ".fa-file-image")
        save_button = driver.find_element(By.CSS_SELECTOR, '.fa-file-image')
        locator = driver.find_element(By.CSS_SELECTOR, ".fa-map-marker-alt")

        # instantiate map object
        world_map=draw_map()
        print("map is drawn")

        
        return world_map,driver, save_button, locator
    
    world_map,driver, save_button, locator = initialize()

    # try to acquire 50000 images
    # for i in range(5):
    retry = False
    error = 0
    i = 9901
    while i<10000:
        if not retry:
            while True:
                # # generate a random point that is on land
                lon, lat = random.uniform(-175,175), random.uniform(-80, 80)
                xpt, ypt = world_map( lon, lat ) # convert to projection map

                # Check if that point is on the map
                if world_map.is_land(xpt,ypt):
                    # if it is on the map, print the name and break
                    name="map_lon{:4.2f}_lat{:4.2f}".format(lon, lat) # note that the precision can be changed here.
                    print(name)
                    # print("\n")
                    break

        try:
            print(f"iter: {i}")
            wait = WebDriverWait(driver, 2)
            locator.click() # click the search button on terrain.party
            # print("clicked locator")
            lat_input = driver.find_element(By.ID, 'latInput')
            lng_input = driver.find_element(By.ID, 'lngInput')
            # print('input activated')
            # apply = driver.find_element(By.CSS_SELECTOR, 'i.fa-check:nth-child(1)')
            # clear = driver.find_element(By.CSS_SELECTOR, 'button.outline:nth-child(3)')
            clear = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.outline:nth-child(3)')))
            # print('clr button found')
            clear.click()
            # print('clicked clear')
            lat_input.send_keys("{}".format(lat))
            lng_input.send_keys("{}".format(lon))
            # print("sent coords")

            
            apply = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'i.fa-check:nth-child(1)')))

            # click apply
            apply.click()
            time.sleep(3) # data should be pulled slowly

            # check if it can find that location
            try:
                WebDriverWait(driver, 1).until(EC.alert_is_present(),
                                               'Timed out waiting for PA creation ' +
                                               'confirmation popup to appear.')
                alert = driver.switch_to.alert
                alert.accept()
                continue
            except TimeoutException:
                # if it doesn't find the location we can continue
                pass

            # save the data to a zip folder by clicking the save button
            save_button.click()
            time.sleep(6)
            print('saved')
            driver.switch_to.default_content()
            # enter name to save to in the popup
            name="map_lon{:4.2f}_lat{:4.2f}".format(lon, lat) # the precision can be saved here
            try:
                ren = rename(name + '.png')
                if not ren:
                    raise Exception("unsuccessful renaming")
                print('renamed to map coords\n')
                retry = False
                error = 0
            except Exception as e:
                error = error+1
                print(str(e))
                retry= True
                i = i-1
                if(error == 5):#thrice it got error, means the site stopped working
                    driver.quit()
                    world_map,driver, save_button, locator = initialize()
                    error = 0


            time.sleep(2) # again.... download time is the holdup in this script
            i = i+1

            # check if there is a problem saving
            try:
                WebDriverWait(driver, 1).until(EC.alert_is_present(),
                                               'Timed out waiting for PA creation ' +
                                               'confirmation popup to appear.')
                alert = driver.switch_to.alert
                # print(alert.text)
                alert.accept()
                continue
            except TimeoutException:
                # print("no alert")
                pass
        except Exception as e:
            print(f"Exception: {type(e).__name__}")
            print("retrying...\n")
            error = error+1
            retry = True
            if(error == 5): #thrice it got error, means the site stopped working
                driver.quit()
                world_map,driver, save_button, locator = initialize()
                error = 0
            
            
    
    driver.quit()




if __name__=="__main__":
    main()
