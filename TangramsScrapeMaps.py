from selenium import webdriver
# import urllib.request
import random, math, time
import keyboard
# Set up the Selenium webdriver
#'C:\Users\N Nagabhushanam\Downloads\msedgedriver.exe')
driver = webdriver.Edge()
# Navigate to the URL
t=1000
while(t):
    time.sleep(0.5)
    
    x=(random.uniform(9,44))
    y=(random.uniform(77,87))
    # v=(x-17)*math.sin(1.2)+(y-88.6)*math.cos(1.2)
    # u=(x-17)*math.cos(1.2)-(y-88.6)*math.sin(1.2)
    while(not((10/13)(x-9)>=(y-77) and (-5/19)(x-9)<=(y-77) and (5/16)(x-28)<=(y-72) and (-10/22)(x-22)>=(y-87))):
        x=(random.uniform(9,44))
        y=(random.uniform(77,87))
    #     v=(x-17)*math.sin(1.2)+(y-88.6)*math.cos(1.2)
    #     u=(x-17)*math.cos(1.2)-(y-88.6)*math.sin(1.2)
    url = r"https://tangrams.github.io/heightmapper/#12/{}/{}".format(x,y)
    print(url)
    driver.get(url)
    
    print("got website")
    # button=driver.find_element(by="xpath",value="//li[11]/div/div/div")
    time.sleep(6)
    try:
        button=driver.find_element(webdriver.common.by.By.XPATH, '//li[8]//div/span[@class="property-name"]')
        print("got element") 
        button.click()
        print("clicked")
        time.sleep(1)
    except :
        driver.back()
        continue
    
    # driver.save_screenshot(r"C:\Users\N Nagabhushanam\Downloads\{}.png".format(t))
    
    driver.back()
    t-=1