from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
# to check for alerts:
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
# some essential python libraries 
import os
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
import random
import time
import rename

def draw_map():
    """
    returns world_map: a Basemap object that contains the entire world. This will tell us whether or not a random GPS coordinate is on land
    """
    bottomlat = -89.0
    toplat = 89.0
    bottomlong = -170.0
    toplong =  170.0
    gridsize = 0.1
    world_map = Basemap(projection="merc", resolution='c', area_thresh=0.1, llcrnrlon=bottomlong, llcrnrlat=bottomlat, urcrnrlon=toplong, urcrnrlat=toplat)
    world_map.drawcoastlines(color='black')
    return world_map

def is_unvaried_image(image_path, threshold=10):
    """
    Check if the image is unvaried based on the standard deviation of pixel values.
    """
    img = plt.imread(image_path)
    std_deviation = np.std(img)
    return std_deviation < threshold

def main():
    # To prevent download dialog
    options = Options()
    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.download.folderList', 2)  
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.download.alwaysOpenPanel', False)
    profile.set_preference('browser.download.dir', '/tmp')
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')
    profile.set_preference("browser.download.dir", "C:\\Users\\Vedanth\\OneDrive\\Desktop\\Procedural Environment Dataset 2\\")
    profile.set_preference("browser.download.useDownloadDir", True)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "zip")

    profile.update_preferences()
    options.profile = profile

    driver = webdriver.Firefox(options=options)

    # navigate to the web page to acquire data
    driver.get("https://heightmap.skydark.pl/")
    alert = Alert(driver)
    print(alert.text)
    alert.accept()

    save_button = driver.find_element(By.CSS_SELECTOR, '.fa-file-image')
    locator = driver.find_element(By.CSS_SELECTOR, ".fa-map-marker-alt")

    # instantiate map object
    world_map = draw_map()
    print("map is drawn")

    # attempt to acquire 40000 images
    for i in range(40000):
        for attempt in range(3):  # Limit the number of attempts to avoid infinite loops
            # generate a random point
            lon, lat = random.uniform(-179, 179), random.uniform(-89, 89)
            xpt, ypt = world_map(lon, lat)

            # Check if the point is on land
            if world_map.is_land(xpt, ypt):
                name = "map_lon{:4.2f}_lat{:4.2f}".format(lon, lat)
                print(name)
                print("\n")

                try:
                    locator.click()  # click the search button on terrain.party
                    print("adding new location")
                    lat_input = driver.find_element(By.ID, 'latInput')
                    lng_input = driver.find_element(By.ID, 'lngInput')
                    apply = driver.find_element(By.CSS_SELECTOR, 'i.fa-check:nth-child(1)')
                    clear = driver.find_element(By.CSS_SELECTOR, 'button.outline:nth-child(3)')
                    # enter gps coordinate string of land coordinates
                    clear.click()
                    print('clicked clear')
                    lat_input.send_keys("{}".format(lat))
                    lng_input.send_keys("{}".format(lon))
                    # click apply
                    apply.click()
                    time.sleep(random.uniform(3, 5))  # Increase sleep time

                    try:
                        WebDriverWait(driver, 5).until(EC.alert_is_present(),
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
                    print('saved')
                    driver.switch_to.default_content()
                    # enter name to save to in the popup
                    name = "map_lon{:4.2f}_lat{:4.2f}".format(lon, lat) 
                    rename(name + '.png')

                    time.sleep(random.uniform(3, 7))  # Increase sleep time

                    # check if there is a problem saving
                    try:
                        WebDriverWait(driver, 5).until(EC.alert_is_present(),
                                                       'Timed out waiting for PA creation ' +
                                                       'confirmation popup to appear.')
                        alert = driver.switch_to.alert
                        alert.accept()
                        continue
                    except TimeoutException:
                        pass

                    # Check if the downloaded image is unvaried
                    downloaded_image_path = os.path.join("C:\\Users\\Vedanth\\OneDrive\\Desktop\\Procedural Environment Generation Dataset\\", name + '.png')
                    if is_unvaried_image(downloaded_image_path):
                        print("Detected unvaried image. Retrying...")
                        continue

                except Exception as e:
                    print(f"Error occurred: {e}. Retrying with new coordinates.")
                    continue

                break  
            else:
                print(f"Generated coordinates {lon}, {lat} are not on land. Retrying...")
                continue

if __name__ == "__main__":
    main()

