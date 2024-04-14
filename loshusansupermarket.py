from selenium import webdriver
from datetime import datetime
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
import os

def CheckElement(driver, ElementID):
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, ElementID)))
    except:
        for i in range(3):
            try:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, ElementID)))
                break
            except:
                if i == 2:
                    # print("Page did not load correctly")
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
                    # print("Page did not load correctly")
                    return False
    return True

def CheckElementByXPATH(driver, ElementName):
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, ElementName)))
    except:
        for i in range(3):
            try:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, ElementName)))
                break
            except:
                if i == 2:
                    # print("Page did not load correctly")
                    return False
    return True

def CheckElementByname(driver, ElementName):
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, ElementName)))
    except:
        for i in range(3):
            try:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, ElementName)))
                break
            except:
                if i == 3:
                    # print("Page did not load correctly")
                    return False
    return True

def CheckElementByCSS_SELECTOR(driver, ElementName):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ElementName)))
    except:
        for i in range(3):
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ElementName)))
                break
            except:
                if i == 3:
                    # print("Page did not load correctly")
                    return False
    return True

def CheckElementByCSS_SELECTOR_(driver, ElementName):
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ElementName)))
    except:
        for i in range(3):
            try:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ElementName)))
                break
            except:
                if i == 3:
                    # print("Page did not load correctly")
                    return False
    return True

def AddtoCart(con):
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument("window-size=1100,1400")

    userconfig = con.split("/")
    tmp = userconfig[0].split("-")
    order_numbers = userconfig[1].split(",")

    pDF = pd.read_csv( "./input/" + tmp[2])

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
    if 'currentStock' not in pDF.columns:   # 
        pDF.insert(len(pDF.columns), column='currentStock', value='')  


    driver = webdriver.Chrome(options=chrome_options)

    # driver.maximize_window()
    driver.get("https://loshusansupermarket.com/login.php?setCurrencyId=2")
    # print(CheckElement(driver,"login_email"))
    CheckElement(driver,"login_email")
    next_element = driver.find_element(By.ID, "login_email")
    next_element.send_keys(tmp[3])

    CheckElement(driver,"login_pass")
    next_element = driver.find_element(By.ID, "login_pass")
    next_element.send_keys(tmp[4])

    CheckElement(driver,"LoginButton")
    next_element = driver.find_element(By.ID, "LoginButton")
    next_element.click()

    CheckElement(driver,"login_auth_method_email")
    next_element = driver.find_element(By.ID, "login_auth_method_email")
    next_element.click()

    CheckElement(driver,"send_login_auth_code_btn")
    next_element = driver.find_element(By.ID, "send_login_auth_code_btn")
    next_element.click()


    input("Hit Enter after clicking otp confirm button")

    add_to_cart(driver, pDF, tmp)


def add_to_cart(driver, pDF, tmp):
    for index, row in pDF.iterrows():
        pDF.loc[index, "membership"] = str(tmp[3])
        pDF.loc[index, "date_processed"] = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        name = ""
        name = row['item_name']
        if "vwt" in row['item_name']:
            name = row['item_name'].split("vwt")[0].strip() + " vwt"
        
        CheckElement(driver,"search_query")
        next_element = driver.find_element(By.ID, "search_query")
        next_element.send_keys(Keys.CONTROL, "a")
        next_element.send_keys(name)

        try:
            next_element.send_keys(Keys.ENTER)
            if CheckElementByCSS_SELECTOR(driver,".item_title"):
                next_element = driver.find_element(By.XPATH, '//*[@id="frmCompare"]/div[2]/ul/li/div[2]/div[2]/h1/a')
                time.sleep(1)
                next_element.click()

                if CheckElementByClass(driver,"VariationProductInventory"):
                    next_element = driver.find_element(By.CLASS_NAME, "VariationProductInventory").text
                    if int(float(next_element)) < int(float(row['qty_ordered'])): 
                        pDF.loc[index, "output_status"] = "Not Enough Stock"
                        pDF.loc[index, "source"] = "loshusansupermarket"
                        pDF.loc[index, "currentStock"] = int(float(next_element))
                        continue
                else : 
                    if CheckElementByClass(driver,"CurrentlySoldOut"):
                        pDF.loc[index, "output_status"] = "Sold Out"
                        pDF.loc[index, "source"] = "loshusansupermarket"
                        continue

                CheckElementByCSS_SELECTOR_(driver, "input.qtyInput.quantityInput")
                next_element = driver.find_element(By.CSS_SELECTOR, "input.qtyInput.quantityInput")
                time.sleep(1)
                next_element.click()
                next_element.clear()
                next_element.send_keys(str(row['qty_ordered']))

                next_element = driver.find_element(By.XPATH, '//*[@id="productDetailsAddToCartForm"]/div/div[3]/div/input[1]')
                next_element.click()

                CheckElement(driver,"myprodprice")
                next_element = driver.find_element(By.ID, "myprodprice")
                time.sleep(1)
                pDF.loc[index, "source_cost"] = next_element.text.replace("$", "").replace(" JMD", "")

                pDF.loc[index, "output_status"] = "Added"
                pDF.loc[index, "source"] = "loshusansupermarket"
                print(name, "Added")
            else: 
                pDF.loc[index, "output_status"] = "Not Added"
                pDF.loc[index, "source"] = "loshusansupermarket"
                print(name, "Not Added")
        except Exception:
            pDF.loc[index, "output_status"] = "Not Added"
            pDF.loc[index, "source"] = "loshusansupermarket"
            print(name, "Not Added")
            continue


    driver.get("https://loshusansupermarket.com/cart.php?setCurrencyId=2")

    CheckElementByCSS_SELECTOR(driver, 'tr.SubTotal.First')
    subtotal = driver.find_element(By.CSS_SELECTOR, 'tr.SubTotal.First').text
    subtotal = int(''.join(filter(str.isdigit, subtotal))) / 100
    print(subtotal)

    if subtotal >= 3000:
        try:
            driver.get("https://loshusansupermarket.com/checkout.php")

            CheckElementByCSS_SELECTOR(driver, '.col-12.col-md-6.address-item.mb-2')
            next_element = driver.find_element(By.CSS_SELECTOR, '.col-12.col-md-6.address-item.mb-2')
            time.sleep(1)
            next_element.click()

            CheckElementByCSS_SELECTOR_(driver, 'input[value="Bill to this Address"]')
            next_element = driver.find_element(By.CSS_SELECTOR, 'input[value="Bill to this Address"]')
            time.sleep(1)
            next_element.click()
            
            CheckElementByCSS_SELECTOR(driver, '.col-12.col-md-6.address-item.mb-2')
            next_element = driver.find_elements(By.CSS_SELECTOR, '.col-12.col-md-6.address-item.mb-2')[-1]
            time.sleep(1)
            next_element.click()

            CheckElementByCSS_SELECTOR_(driver, 'input[value="Ship to this address"]')
            next_element = driver.find_element(By.CSS_SELECTOR, 'input[value="Ship to this address"]')
            time.sleep(1)
            next_element.click()

            driver.execute_script("window.scrollBy(0, 100);")
            CheckElementByCSS_SELECTOR(driver, "ul.ShippingProviderList")
            ul = driver.find_element(By.CSS_SELECTOR, "ul.ShippingProviderList")
            lables = ul.find_elements(By.CSS_SELECTOR, "label")[1]
            time.sleep(1)
            lables.click()


            # 3rd step button
            CheckElementByCSS_SELECTOR(driver, 'div.ML20')
            next_element = driver.find_element(By.CSS_SELECTOR ,'div.ML20 > input[value="Continue"]')
            time.sleep(1)
            next_element.click()

            CheckElement(driver, "payment_options")
            next_element = driver.find_element(By.ID, "payment_options")
            actions = ActionChains(driver)
            actions.move_to_element(next_element).perform()
            driver.execute_script("window.scrollBy(0, 50);")
            time.sleep(1)


            els = driver.find_elements(By.NAME,"store_credit")
            for el in els:
                if "Pay using my reward points" == el.accessible_name:
                    el.click()

            next_element = driver.find_element(By.ID, "loyalty_checkout_provider_checkout_instore")
            actions.move_to_element(next_element).perform()
            driver.execute_script("window.scrollBy(0, 50);")
            time.sleep(1)
            next_element.click()

            CheckElementByCSS_SELECTOR(driver, 'textarea[name="ordercomments"]')
            driver.execute_script("window.scrollBy(0, 50);")
            next_element = driver.find_element(By.CSS_SELECTOR, 'textarea[name="ordercomments"]')
            time.sleep(1)
            next_element.click()
            next_element.send_keys(tmp[2])

            CheckElement(driver, "AgreeTermsAndConditions")
            next_element = driver.find_element(By.ID, "AgreeTermsAndConditions")
            actions.move_to_element(next_element).perform()
            time.sleep(1)
            next_element.click()

            # Last proceed to pay button
            next_element = driver.find_element(By.ID, "bottom_payment_button")
            actions.move_to_element(next_element).perform()
            # next_element.click()

        except Exception as e:
            print(e)
            pass
        

    else:
        pDF['output_status'] = "Not Added"
        print(f"\033[91m Your subtotal is ${subtotal}, which is lesser then $4000 \033[0m")

        print(f"Your subtotal is ${subtotal}, which is lesser then $4000")

    if os.path.isfile("output.csv"):
        file_path = 'output.csv'
        prevDf = pd.read_csv(file_path)
        pd.concat([prevDf, pDF]).to_csv('output.csv', index=False)
    else:
        pDF.to_csv('output.csv', index=False)

    input()

    driver.quit()
