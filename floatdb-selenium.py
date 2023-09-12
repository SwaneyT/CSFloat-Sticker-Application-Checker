from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import chromedriver_autoinstaller
import getpass
import contextlib
import re
import json
import datetime
import winsound
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

stickers = {
    "rmr2020_team_vita": 4701,
    "rmr2020_team_vita_holo": 4702,
    "rmr2020_team_vita_foil": 4703,
    "rmr2020_team_vita_gold": 4704,
}

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get("https://csfloat.com/db")
driver.delete_all_cookies()

#all_rmr_ids = [4701, 4702, 4703, 4704, 4705, 4706, 4707, 4708, 4709, 4710, 4711, 4712, 4713, 4714, 4715, 4716, 4717, 4718, 4719, 4720, 4721, 4722, 4723, 4724, 4725, 4726, 4727, 4728, 4729, 4730, 4731, 4732, 4733, 4734, 4735, 4736, 4737, 4738, 4739, 4740, 4741, 4742, 4743, 4744, 4745, 4746, 4747, 4748, 4749, 4750, 4751, 4752, 4753, 4754, 4755, 4756, 4757, 4758, 4759, 4760, 4761, 4762, 4763, 4764, 4765, 4766, 4767, 4768, 4769, 4770, 4771, 4772, 4773, 4774, 4775, 4776, 4777, 4778, 4779, 4780, 4781, 4782, 4783, 4784, 4785, 4786, 4787, 4788, 4789, 4790, 4791, 4792, 4793, 4794, 4795, 4796]
sticker_ids = [4701, 4702, 4703]
results = []

delay = 1800
delay2 = 45


def getCount(driver,delay2,data1):
    print("Trying...")
    driver.get(f"https://csgofloat.com/db?min=0&max=1&stickers={data1}")
    try:
        myElem1 = WebDriverWait(driver, delay2).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'mat-card.count')))
        extracted_count = int(re.findall(r'\d+(?:,\d{3})*', myElem1.text)[0].replace(",",""))
        print("Found:",extracted_count)
        return extracted_count
    
    except TimeoutException:
        try:
            myElem2 = WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h3.ng-star-inserted')))
            extracted_count = 0
            return extracted_count
        
        except TimeoutException:
            print("Too many requests...")
            return "Fail"
    except Exception as error:
        print("UNKNOWN ERROR!!!!!")
        getCount(driver,300,data1)
    
    # except Exception as error:
    #     print("UNKNOWN ERROR!!!!!",error)
    #     getCount(driver,300,data1)

WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH, "//img[@src='assets/login-steam.png']"))).click()
WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'avatar')))
print("Session Ready!")
for name,sticker in stickers.items():
    total_applied=0
    for i in range(5,0,-1):
        data=[]
        count=None
        myElem2=None
        for z in range(i):
            data.append(json.loads(f"{{\"i\":\"{sticker}\"}}"))
        
        data1=str(data).replace("'","\"")

        extracted_count = getCount(driver,delay2,data1)

        while extracted_count == "Fail":
            print("Too many requests.")
            extracted_count = getCount(driver,120,data1) #False means too many requests, this will make it retry for as long as its "false"
        
        if total_applied>0:
            print("Deducting",deduct_amount)
            extracted_count = extracted_count - deduct_amount
        
        print("Adding to total:",(extracted_count * i),"sticker applications")
        total_applied = total_applied + (extracted_count * i)
        deduct_amount = extracted_count
        print("Total applications:",total_applied)
    results.append([name,total_applied])
    print(results)
        #Login session is now verified, main code here


now = datetime.datetime.now()
name = now.strftime("%x")+"-"+now.strftime("%X")
filename = name.replace("/","_").replace(":","_")

file = open(filename+".txt","w")
file.write(str(results))

winsound.Beep(500,750)
print("Complete!")

while True:
    pass
