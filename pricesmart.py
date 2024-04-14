from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import os


def CheckElement(driver, ElementID):
    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, ElementID)))
    except:
        for i in range(3):
            try:
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, ElementID)))
                break
            except:
                if i == 2:
                    
                    return False
    return True

def CheckElementByClass(driver, ElementName):
    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, ElementName)))
    except:
        for i in range(3):
            try:
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, ElementName)))
                break
            except:
                if i == 2:
                    
                    return False
    return True

def CheckElementByXPATH(driver, ElementName):
    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, ElementName)))
    except:
        for i in range(3):
            try:
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, ElementName)))
                break
            except:
                if i == 2:
                    
                    return False
    return True


def initCall(userId):

    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=chrome_options)

    driver.maximize_window()
    driver.get("https://www.pricesmart.com/site/jm/en")

    CheckElement(driver,"dropdownMenuButton")
    next_element = driver.find_element(By.ID, "dropdownMenuButton")
    next_element.click()

    CheckElement(driver,"login-button")
    next_element = driver.find_element(By.ID, "login-button")
    next_element.click()

    CheckElement(driver,"username")
    next_element = driver.find_element(By.ID, "username")
    next_element.send_keys(userId)

    CheckElement(driver,"marketplace-login-btn")
    next_element = driver.find_element(By.ID, "marketplace-login-btn")
    next_element.click()

    if CheckElement(driver,"btnValidate") == False:
        return driver
    else:
        driver.quit()
        return initCall(userId)


def initial_process(tmp):
    location = tmp[1]
    user, pw = tmp[3], tmp[4]

    driver = initCall(user)

    CheckElement(driver, "password")
    next_element = driver.find_element(By.ID, "password")
    next_element.send_keys(pw)

    CheckElement(driver, "kc-login")
    next_element = driver.find_element(By.ID, "kc-login")
    next_element.click()

    # for changing location
    if CheckElement(driver, "club-name"):
        if driver.find_element(By.ID, "club-name").text != location:
            next_element = driver.find_element(By.ID, "club-name")
            next_element.click()

        if CheckElementByXPATH(driver, ".//a[contains(@onclick, 'clubChangeAlertContinue()')]"):
            next_element = driver.find_element(By.XPATH, ".//a[contains(@onclick, 'clubChangeAlertContinue()')]")
            next_element.click()

        CheckElement(driver, "select-club")
        next_element = driver.find_element(By.ID, "select-club")
        next_element.click()

    return driver


def order_process(driver, pDF, tmp, bool="false"):
    productUrl = 'https://www.pricesmart.com/site/jm/en/pdp/'

    use = 'item_sku'
    for index, row in pDF.iterrows():
        if bool == "true":
            if pDF.loc[index, "output_status"] == "Added":
                continue
        pDF.loc[index, "membership"] = "'" + str(tmp[3])
        pDF.loc[index, "date_processed"] = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        driver.get(productUrl + str(row[use]))
        isValid = CheckElementByClass(driver, "input-group-prepend")

        try:
            if isValid:
                CheckElement(driver, "product-price")
                next_element = driver.find_element(By.ID, "product-price")
                pDF.loc[index, "source_cost"] = next_element.text

                CheckElement(driver, "customValue")
                next_element = driver.find_element(By.ID, "customValue")
                next_element.send_keys(Keys.CONTROL + "a")
                next_element.send_keys(row['qty_ordered'])

                CheckElement(driver, "btn-add-to-cart")
                next_element = driver.find_element(By.ID, "btn-add-to-cart")
                next_element.click()

                if driver.current_url == 'https://www.pricesmart.com/site/jm/en/cart' or 'https://www.pricesmart.com/site/jm/es/carrito':
                    pDF.loc[index, "output_status"] = "Added"
                    pDF.loc[index, "source"] = "Price Smart"
                    pDF.loc[index, "location"] = tmp[1]
                else:
                    pDF.loc[index, "output_status"] = "Not Added"
                    pDF.loc[index, "source"] = "Price Smart"

            else:
                pDF.loc[index, "output_status"] = "Not Added"
                pDF.loc[index, "source"] = "Price Smart"

        except Exception as e:
            print(e)
            pDF.loc[index, "output_status"] = "Not Added"
            pDF.loc[index, "source"] = "Price Smart"
    
    driver.quit()

    return pDF


def process_config(con):
    
    userconfig = con.split("/")
    primary = userconfig[0].split("-")
    order_numbers = userconfig[1].split(",")

    if not os.path.exists("./input/" + primary[2]):
        print("\033[91m File exists in the input directory but not in the userconfig, filename :- " + str(primary[2]) + "\033[0m")
        # continue
    
    pDF = pd.read_csv("./input/" + primary[2])

    if order_numbers != ['']:
        pDF["order_number"] = pDF["order_number"].astype(str)
        pDF = pDF[pDF['order_number'].isin(order_numbers)]
    if 'source_cost' not in pDF.columns:
        pDF.insert(len(pDF.columns), column='source_cost', value='')
    if 'output_status' not in pDF.columns:
        pDF.insert(len(pDF.columns), column='output_status', value='')
    if 'membership' not in pDF.columns:
        pDF.insert(len(pDF.columns), column='membership', value='')
    if 'date_processed' not in pDF.columns:
        pDF.insert(len(pDF.columns), column='date_processed', value='')
    if 'source' not in pDF.columns:
        pDF.insert(len(pDF.columns), column='source', value='')
    if 'location' not in pDF.columns:
        pDF.insert(len(pDF.columns), column='location', value='')

    driver = initial_process(primary)


    cartUrl = 'https://www.pricesmart.com/site/jm/en/cart'
    driver.get(cartUrl)

    while CheckElement(driver, "remove-item"):
        next_element = driver.find_element(By.ID, "remove-item")
        next_element.click()

    order_process(driver, pDF, primary)

    if os.path.isfile("output.csv"):
        file_path = 'output.csv'
        prevDf = pd.read_csv(file_path)
        pd.concat([prevDf, pDF]).to_csv('output.csv', index=False)
    else:
        pDF.to_csv('output.csv', index=False)