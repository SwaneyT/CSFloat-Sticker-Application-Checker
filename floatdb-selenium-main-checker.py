from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
import chromedriver_autoinstaller
import getpass
import contextlib
import re
import json
import datetime
import winsound
import math
import numpy
import time
import pwinput
import os
import random
import sys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.firefox.service import Service
from subprocess import CREATE_NO_WINDOW
import undetected_chromedriver as uc
from DrissionPage import ChromiumPage


with open(sys.argv[1], 'r') as f:
    json_data = f.read()
print(json_data)

stickers = json.loads(json_data)

chrome_options = uc.ChromeOptions()
chrome_options.add_argument("--disable-popup-blocking")

driver = uc.Chrome(options=chrome_options)

url = 'https://csfloat.com/'
driver.get(url)
driver.maximize_window()

# from seleniumbase import Driver
# import time

# driver = Driver(uc=True)
# driver.get("https://nowsecure.nl/#relax")
# time.sleep(8)
# driver.quit()


################# CHROME WITH LOCALHOST PROXY (POSSIBLY BEST ROUTE?? CANT GET IT TO CONNECT THO)
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
# #Change chrome driver path accordingly
# chrome_service = ChromeService(ChromeDriverManager().install())
# driver = webdriver.Chrome(options=chrome_options,service=chrome_service)
# print("Initialized?")
# print(driver.title)
# driver.get("https://csfloat.com")



##############FIREFOX WITH LOCALHOST PROXY (DOESNT WORK RN)
# profile = webdriver.FirefoxProfile(r'C:\Users\icysh\AppData\Roaming\Mozilla\Firefox\Profiles\334aipxs.default-release')

# PROXY_HOST = "12.12.12.123"
# PROXY_PORT = "1234"
# profile.set_preference("network.proxy.type", 1)
# profile.set_preference("network.proxy.http", PROXY_HOST)
# profile.set_preference("network.proxy.http_port", int(PROXY_PORT))
# profile.set_preference("dom.webdriver.enabled", False)
# profile.set_preference('useAutomationExtension', False)
# profile.update_preferences()
# desired = DesiredCapabilities.FIREFOX

# driver = webdriver.Firefox(service=profile, options=desired)

#all_rmr_ids = [4701, 4702, 4703, 4704, 4705, 4706, 4707, 4708, 4709, 4710, 4711, 4712, 4713, 4714, 4715, 4716, 4717, 4718, 4719, 4720, 4721, 4722, 4723, 4724, 4725, 4726, 4727, 4728, 4729, 4730, 4731, 4732, 4733, 4734, 4735, 4736, 4737, 4738, 4739, 4740, 4741, 4742, 4743, 4744, 4745, 4746, 4747, 4748, 4749, 4750, 4751, 4752, 4753, 4754, 4755, 4756, 4757, 4758, 4759, 4760, 4761, 4762, 4763, 4764, 4765, 4766, 4767, 4768, 4769, 4770, 4771, 4772, 4773, 4774, 4775, 4776, 4777, 4778, 4779, 4780, 4781, 4782, 4783, 4784, 4785, 4786, 4787, 4788, 4789, 4790, 4791, 4792, 4793, 4794, 4795, 4796]

################## DrissionPage Implementation, Success on "https://nowsecure.nl/" and should be on CSFloat

results = []

delay = 1800
delay2 = 25

def getCount(driver,timeout_timer,data1,float1,float2,isRunningGold,category):
    print("Loading Page...")
    try:
        url = f"https://csgofloat.com/db?category={category}&min={float1}&max={float2}&stickers={data1}"
        driver.set_page_load_timeout(timeout_timer) # arbitrary time to prevent infinite loading
        driver.get(url)
        time.sleep(0.1) # not necessary
        driver.execute_script(f"window.open('{url}', '_blank')")

        time.sleep(10)

        all_handles = driver.window_handles

        first_tab_handle = all_handles[0]
        driver.switch_to.window(first_tab_handle)
        driver.close()

        second_tab_handle = all_handles[1]
        driver.switch_to.window(second_tab_handle)

    except Exception as e:
        print(f"Error while getting page or switching tab... seems driver is closed? error: {e}")
    try:
        myElem1 = WebDriverWait(driver, timeout_timer).until(EC.presence_of_element_located((By.XPATH, "//div[@class='count ng-star-inserted']")))
        print(myElem1.text)
        extracted_count = int(re.findall(r'\d+(?:,\d{3})*', myElem1.text)[0].replace(",",""))

        search_div = driver.find_element(By.XPATH, "//div[@class='container dense-input ng-untouched ng-pristine ng-valid']")
        all_inputs = search_div.find_elements(By.XPATH, "//input[contains(@class, 'mat-mdc-input-element') and contains(@class, 'mat-mdc-autocomplete-trigger')]") #mat-mdc-input-element mat-mdc-autocomplete-trigger
        first_item_search_value = all_inputs[1].get_attribute("value") #value 0 is just empty? not exactly sure lol
        print(first_item_search_value)
        if " (Gold)" in first_item_search_value and souvenirGoldsInput.lower() == "yes" and isRunningGold == False: #and total>0, and if souvenirs can be gold == yes       #(By.XPATH, "//div[@class='search']//*[contains(text(),'(Gold)')]"):
            print("Gold sticker that can appear on souvenirs detected.")
            return "gold"
        else:
            print("Gold not found, or is already in split search.")
        print("Found:",extracted_count)
        return extracted_count
    
    except TimeoutException:
        try:
            time.sleep(5)
            if "Found No Items" in driver.page_source:
                print("Found no items. Returning 0")
                extracted_count = 0
                return extracted_count
            myElem2 = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h3.ng-star-inserted'))) #this checked if no items were found in old UI, but now it just forces a timeoutexception
        
        except TimeoutException:
            if "Woah, you've been making a lot of searches lately and will need to wait a bit." in driver.page_source:
                print("Too many requests. Trying again.")
            elif "failed to verify recaptcha" in driver.page_source:
                print("Unable to verify recaptcha. Trying again.")
            elif "turnstile error" in driver.page_source:
                print("CloudFlare Turnstile error.")
            else:
                print("Unknown status on page, or page did not finish loading.")
            return "Fail"
    except Exception as error:
        print(f"Unknown Error, retrying... EXCEPTION: {error}")
        getCount(driver,300,data1,0,1,False,0)
    
def f(x):
    return round((x**3)/100,4)

def multiple_weighted_average(floats,weights,n):

  floats_output = []

  for outer_loop_i in range(n,0,-1):
    per_search_num = round((sum(weights) / n) * outer_loop_i,2)
    current_added_weighted = 0

    for i in range(len(weights)):
      current_added_weighted += weights[i]
      if current_added_weighted >= per_search_num: #stops the for loop when current_added_weighted is bigger than the original per_search_num given to it
        corresponding_float_number_for_weighting = floats[i]
        floats_output.append(floats[i])
        break

    #print(f"iteration: {outer_loop_i}, per_search_num: {per_search_num}, current_added_weighted: {current_added_weighted}, number of i loops completed: {i}, float value output: {floats[i]}")
  floats_output.reverse()
  return floats_output


def handleSouvenirGolds(driver,data1):
    #In this function, if "gold" is returned from getCount(), split search into "Normal" category and "StatTrak" category (id 1 and 2 respectively), then return the combined total of count into "extracted_count" variable.
    print("Handling Gold Sticker.")
    extracted_count = getCount(driver,30,data1,0,1,True,1)

    while extracted_count == "Fail":
        print("Sleeping 25 - 45 seconds")
        time.sleep(round(random.uniform(25,45),8))
        extracted_count = getCount(driver,30,data1,0,1,True,1) #False means too many requests, this will make it retry for as long as its "false"
        #50 is the time that it waits for the page to load
    
    extracted_count2 = getCount(driver,30,data1,0,1,True,2)

    while extracted_count2 == "Fail":
        print("Sleeping 25 - 45 seconds")
        time.sleep(round(random.uniform(25,45),8))
        extracted_count2 = getCount(driver,30,data1,0,1,True,2) #False means too many requests, this will make it retry for as long as its "false"
        #50 is the time that it waits for the page to load

    extracted_count = extracted_count + extracted_count2

    print(f"Gold sticker split search complete! Found: {extracted_count}")
    return extracted_count

floats = [0, 0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.007, 0.008, 0.009, 0.01, 0.011, 0.012, 0.013, 0.014, 0.015, 0.016, 0.017, 0.018, 0.019, 0.02, 0.021, 0.022, 0.023, 0.024, 0.025, 0.026, 0.027, 0.028, 0.029, 0.03, 0.031, 0.032, 0.033, 0.034, 0.035, 0.036, 0.037, 0.038, 0.039, 0.04, 0.041, 0.042, 0.043, 0.044, 0.045, 0.046, 0.047, 0.048, 0.049, 0.05, 0.051, 0.052, 0.053, 0.054, 0.055, 0.056, 0.057, 0.058, 0.059, 0.06, 0.061, 0.062, 0.063, 0.064, 0.065, 0.066, 0.067, 0.068, 0.069, 0.07, 0.071, 0.072, 0.073, 0.074, 0.075, 0.076, 0.077, 0.078, 0.079, 0.08, 0.081, 0.082, 0.083, 0.084, 0.085, 0.086, 0.087, 0.088, 0.089, 0.09, 0.091, 0.092, 0.093, 0.094, 0.095, 0.096, 0.097, 0.098, 0.099, 0.1, 0.101, 0.102, 0.103, 0.104, 0.105, 0.106, 0.107, 0.108, 0.109, 0.11, 0.111, 0.112, 0.113, 0.114, 0.115, 0.116, 0.117, 0.118, 0.119, 0.12, 0.121, 0.122, 0.123, 0.124, 0.125, 0.126, 0.127, 0.128, 0.129, 0.13, 0.131, 0.132, 0.133, 0.134, 0.135, 0.136, 0.137, 0.138, 0.139, 0.14, 0.141, 0.142, 0.143, 0.144, 0.145, 0.146, 0.147, 0.148, 0.149, 0.15, 0.151, 0.152, 0.153, 0.154, 0.155, 0.156, 0.157, 0.158, 0.159, 0.16, 0.161, 0.162, 0.163, 0.164, 0.165, 0.166, 0.167, 0.168, 0.169, 0.17, 0.171, 0.172, 0.173, 0.174, 0.175, 0.176, 0.177, 0.178, 0.179, 0.18, 0.181, 0.182, 0.183, 0.184, 0.185, 0.186, 0.187, 0.188, 0.189, 0.19, 0.191, 0.192, 0.193, 0.194, 0.195, 0.196, 0.197, 0.198, 0.199, 0.2, 0.201, 0.202, 0.203, 0.204, 0.205, 0.206, 0.207, 0.208, 0.209, 0.21, 0.211, 0.212, 0.213, 0.214, 0.215, 0.216, 0.217, 0.218, 0.219, 0.22, 0.221, 0.222, 0.223, 0.224, 0.225, 0.226, 0.227, 0.228, 0.229, 0.23, 0.231, 0.232, 0.233, 0.234, 0.235, 0.236, 0.237, 0.238, 0.239, 0.24, 0.241, 0.242, 0.243, 0.244, 0.245, 0.246, 0.247, 0.248, 0.249, 0.25, 0.251, 0.252, 0.253, 0.254, 0.255, 0.256, 0.257, 0.258, 0.259, 0.26, 0.261, 0.262, 0.263, 0.264, 0.265, 0.266, 0.267, 0.268, 0.269, 0.27, 0.271, 0.272, 0.273, 0.274, 0.275, 0.276, 0.277, 0.278, 0.279, 0.28, 0.281, 0.282, 0.283, 0.284, 0.285, 0.286, 0.287, 0.288, 0.289, 0.29, 0.291, 0.292, 0.293, 0.294, 0.295, 0.296, 0.297, 0.298, 0.299, 0.3, 0.301, 0.302, 0.303, 0.304, 0.305, 0.306, 0.307, 0.308, 0.309, 0.31, 0.311, 0.312, 0.313, 0.314, 0.315, 0.316, 0.317, 0.318, 0.319, 0.32, 0.321, 0.322, 0.323, 0.324, 0.325, 0.326, 0.327, 0.328, 0.329, 0.33, 0.331, 0.332, 0.333, 0.334, 0.335, 0.336, 0.337, 0.338, 0.339, 0.34, 0.341, 0.342, 0.343, 0.344, 0.345, 0.346, 0.347, 0.348, 0.349, 0.35, 0.351, 0.352, 0.353, 0.354, 0.355, 0.356, 0.357, 0.358, 0.359, 0.36, 0.361, 0.362, 0.363, 0.364, 0.365, 0.366, 0.367, 0.368, 0.369, 0.37, 0.371, 0.372, 0.373, 0.374, 0.375, 0.376, 0.377, 0.378, 0.379, 0.38, 0.381, 0.382, 0.383, 0.384, 0.385, 0.386, 0.387, 0.388, 0.389, 0.39, 0.391, 0.392, 0.393, 0.394, 0.395, 0.396, 0.397, 0.398, 0.399, 0.4, 0.401, 0.402, 0.403, 0.404, 0.405, 0.406, 0.407, 0.408, 0.409, 0.41, 0.411, 0.412, 0.413, 0.414, 0.415, 0.416, 0.417, 0.418, 0.419, 0.42, 0.421, 0.422, 0.423, 0.424, 0.425, 0.426, 0.427, 0.428, 0.429, 0.43, 0.431, 0.432, 0.433, 0.434, 0.435, 0.436, 0.437, 0.438, 0.439, 0.44, 0.441, 0.442, 0.443, 0.444, 0.445, 0.446, 0.447, 0.448, 0.449, 0.45, 0.451, 0.452, 0.453, 0.454, 0.455, 0.456, 0.457, 0.458, 0.459, 0.46, 0.461, 0.462, 0.463, 0.464, 0.465, 0.466, 0.467, 0.468, 0.469, 0.47, 0.471, 0.472, 0.473, 0.474, 0.475, 0.476, 0.477, 0.478, 0.479, 0.48, 0.481, 0.482, 0.483, 0.484, 0.485, 0.486, 0.487, 0.488, 0.489, 0.49, 0.491, 0.492, 0.493, 0.494, 0.495, 0.496, 0.497, 0.498, 0.499, 0.5, 0.501, 0.502, 0.503, 0.504, 0.505, 0.506, 0.507, 0.508, 0.509, 0.51, 0.511, 0.512, 0.513, 0.514, 0.515, 0.516, 0.517, 0.518, 0.519, 0.52, 0.521, 0.522, 0.523, 0.524, 0.525, 0.526, 0.527, 0.528, 0.529, 0.53, 0.531, 0.532, 0.533, 0.534, 0.535, 0.536, 0.537, 0.538, 0.539, 0.54, 0.541, 0.542, 0.543, 0.544, 0.545, 0.546, 0.547, 0.548, 0.549, 0.55, 0.551, 0.552, 0.553, 0.554, 0.555, 0.556, 0.557, 0.558, 0.559, 0.56, 0.561, 0.562, 0.563, 0.564, 0.565, 0.566, 0.567, 0.568, 0.569, 0.57, 0.571, 0.572, 0.573, 0.574, 0.575, 0.576, 0.577, 0.578, 0.579, 0.58, 0.581, 0.582, 0.583, 0.584, 0.585, 0.586, 0.587, 0.588, 0.589, 0.59, 0.591, 0.592, 0.593, 0.594, 0.595, 0.596, 0.597, 0.598, 0.599, 0.6, 0.601, 0.602, 0.603, 0.604, 0.605, 0.606, 0.607, 0.608, 0.609, 0.61, 0.611, 0.612, 0.613, 0.614, 0.615, 0.616, 0.617, 0.618, 0.619, 0.62, 0.621, 0.622, 0.623, 0.624, 0.625, 0.626, 0.627, 0.628, 0.629, 0.63, 0.631, 0.632, 0.633, 0.634, 0.635, 0.636, 0.637, 0.638, 0.639, 0.64, 0.641, 0.642, 0.643, 0.644, 0.645, 0.646, 0.647, 0.648, 0.649, 0.65, 0.651, 0.652, 0.653, 0.654, 0.655, 0.656, 0.657, 0.658, 0.659, 0.66, 0.661, 0.662, 0.663, 0.664, 0.665, 0.666, 0.667, 0.668, 0.669, 0.67, 0.671, 0.672, 0.673, 0.674, 0.675, 0.676, 0.677, 0.678, 0.679, 0.68, 0.681, 0.682, 0.683, 0.684, 0.685, 0.686, 0.687, 0.688, 0.689, 0.69, 0.691, 0.692, 0.693, 0.694, 0.695, 0.696, 0.697, 0.698, 0.699, 0.7, 0.701, 0.702, 0.703, 0.704, 0.705, 0.706, 0.707, 0.708, 0.709, 0.71, 0.711, 0.712, 0.713, 0.714, 0.715, 0.716, 0.717, 0.718, 0.719, 0.72, 0.721, 0.722, 0.723, 0.724, 0.725, 0.726, 0.727, 0.728, 0.729, 0.73, 0.731, 0.732, 0.733, 0.734, 0.735, 0.736, 0.737, 0.738, 0.739, 0.74, 0.741, 0.742, 0.743, 0.744, 0.745, 0.746, 0.747, 0.748, 0.749, 0.75, 0.751, 0.752, 0.753, 0.754, 0.755, 0.756, 0.757, 0.758, 0.759, 0.76, 0.761, 0.762, 0.763, 0.764, 0.765, 0.766, 0.767, 0.768, 0.769, 0.77, 0.771, 0.772, 0.773, 0.774, 0.775, 0.776, 0.777, 0.778, 0.779, 0.78, 0.781, 0.782, 0.783, 0.784, 0.785, 0.786, 0.787, 0.788, 0.789, 0.79, 0.791, 0.792, 0.793, 0.794, 0.795, 0.796, 0.797, 0.798, 0.799, 0.8, 0.801, 0.802, 0.803, 0.804, 0.805, 0.806, 0.807, 0.808, 0.809, 0.81, 0.811, 0.812, 0.813, 0.814, 0.815, 0.816, 0.817, 0.818, 0.819, 0.82, 0.821, 0.822, 0.823, 0.824, 0.825, 0.826, 0.827, 0.828, 0.829, 0.83, 0.831, 0.832, 0.833, 0.834, 0.835, 0.836, 0.837, 0.838, 0.839, 0.84, 0.841, 0.842, 0.843, 0.844, 0.845, 0.846, 0.847, 0.848, 0.849, 0.85, 0.851, 0.852, 0.853, 0.854, 0.855, 0.856, 0.857, 0.858, 0.859, 0.86, 0.861, 0.862, 0.863, 0.864, 0.865, 0.866, 0.867, 0.868, 0.869, 0.87, 0.871, 0.872, 0.873, 0.874, 0.875, 0.876, 0.877, 0.878, 0.879, 0.88, 0.881, 0.882, 0.883, 0.884, 0.885, 0.886, 0.887, 0.888, 0.889, 0.89, 0.891, 0.892, 0.893, 0.894, 0.895, 0.896, 0.897, 0.898, 0.899, 0.9, 0.901, 0.902, 0.903, 0.904, 0.905, 0.906, 0.907, 0.908, 0.909, 0.91, 0.911, 0.912, 0.913, 0.914, 0.915, 0.916, 0.917, 0.918, 0.919, 0.92, 0.921, 0.922, 0.923, 0.924, 0.925, 0.926, 0.927, 0.928, 0.929, 0.93, 0.931, 0.932, 0.933, 0.934, 0.935, 0.936, 0.937, 0.938, 0.939, 0.94, 0.941, 0.942, 0.943, 0.944, 0.945, 0.946, 0.947, 0.948, 0.949, 0.95, 0.951, 0.952, 0.953, 0.954, 0.955, 0.956, 0.957, 0.958, 0.959, 0.96, 0.961, 0.962, 0.963, 0.964, 0.965, 0.966, 0.967, 0.968, 0.969, 0.97, 0.971, 0.972, 0.973, 0.974, 0.975, 0.976, 0.977, 0.978, 0.979, 0.98, 0.981, 0.982, 0.983, 0.984, 0.985, 0.986, 0.987, 0.988, 0.989, 0.99, 0.991, 0.992, 0.993, 0.994, 0.995, 0.996, 0.997, 0.998, 0.999, 1]
weights = [0.0, 1074.7, 2149.4, 3224.1, 4298.8, 5373.5, 6448.2, 7522.9, 8597.6, 9672.3, 10747.0, 11259.5, 11772.0, 12284.5, 12797.0, 13309.5, 13822.0, 14334.5, 14847.0, 15359.5, 15872.0, 16404.9, 16937.8, 17470.7, 18003.6, 18536.5, 19069.4, 19602.3, 20135.2, 20668.1, 21201.0, 21482.0, 21763.0, 22044.0, 22325.0, 22606.0, 22887.0, 23168.0, 23449.0, 23730.0, 24011.0, 24290.0, 24569.0, 24848.0, 25127.0, 25406.0, 25685.0, 25964.0, 26243.0, 26522.0, 26801.0, 27211.9, 27622.8, 28033.7, 28444.6, 28855.5, 29266.4, 29677.3, 30088.2, 30499.1, 30910.0, 32034.4, 33158.8, 34283.2, 35407.6, 36532.0, 37656.4, 38780.8, 39905.2, 41029.6, 42154.0, 40901.7, 39649.4, 38397.1, 37144.8, 35892.5, 34640.2, 33387.9, 32135.6, 30883.3, 29631.0, 31367.9, 33104.8, 34841.7, 36578.6, 38315.5, 40052.4, 41789.3, 43526.2, 45263.1, 47000.0, 47500.0, 48000.0, 48500.0, 49000.0, 49500.0, 50000.0, 50500.0, 51000.0, 51500.0, 52000.0, 50900.0, 49800.0, 48700.0, 47600.0, 46500.0, 45400.0, 44300.0, 43200.0, 42100.0, 41000.0, 41715.3, 42430.6, 43145.9, 43861.2, 44576.5, 45291.8, 46007.1, 46722.4, 47437.7, 48153.0, 48737.7, 49322.4, 49907.1, 50491.8, 51076.5, 51661.2, 52245.9, 52830.6, 53415.3, 54000.0, 53100.0, 52200.0, 51300.0, 50400.0, 49500.0, 48600.0, 47700.0, 46800.0, 45900.0, 45000.0, 46600.0, 48200.0, 49800.0, 51400.0, 53000.0, 54600.0, 56200.0, 57800.0, 59400.0, 61000.0, 58160.1, 55320.2, 52480.3, 49640.4, 46800.5, 43960.6, 41120.7, 38280.8, 35440.9, 32601.0, 32510.0, 32419.0, 32328.0, 32237.0, 32146.0, 32055.0, 31964.0, 31873.0, 31782.0, 31691.0, 31431.0, 31171.0, 30911.0, 30651.0, 30391.0, 30131.0, 29871.0, 29611.0, 29351.0, 29091.0, 29180.8, 29270.6, 29360.4, 29450.2, 29540.0, 29629.8, 29719.6, 29809.4, 29899.2, 29989.0, 30111.5, 30234.0, 30356.5, 30479.0, 30601.5, 30724.0, 30846.5, 30969.0, 31091.5, 31214.0, 31443.8, 31673.6, 31903.4, 32133.2, 32363.0, 32592.8, 32822.6, 33052.4, 33282.2, 33512.0, 33536.9, 33561.8, 33586.7, 33611.6, 33636.5, 33661.4, 33686.3, 33711.2, 33736.1, 33761.0, 33483.5, 33206.0, 32928.5, 32651.0, 32373.5, 32096.0, 31818.5, 31541.0, 31263.5, 30986.0, 30775.4, 30564.8, 30354.2, 30143.6, 29933.0, 29722.4, 29511.8, 29301.2, 29090.6, 28880.0, 29037.1, 29194.2, 29351.3, 29508.4, 29665.5, 29822.6, 29979.7, 30136.8, 30293.9, 30451.0, 30439.8, 30428.6, 30417.4, 30406.2, 30395.0, 30383.8, 30372.6, 30361.4, 30350.2, 30339.0, 30311.9, 30284.8, 30257.7, 30230.6, 30203.5, 30176.4, 30149.3, 30122.2, 30095.1, 30068.0, 29764.4, 29460.8, 29157.2, 28853.6, 28550.0, 28246.4, 27942.8, 27639.2, 27335.6, 27032.0, 26976.2, 26920.4, 26864.6, 26808.8, 26753.0, 26697.2, 26641.4, 26585.6, 26529.8, 26474.0, 26422.5, 26371.0, 26319.5, 26268.0, 26216.5, 26165.0, 26113.5, 26062.0, 26010.5, 25959.0, 25966.7, 25974.4, 25982.1, 25989.8, 25997.5, 26005.2, 26012.9, 26020.6, 26028.3, 26036.0, 26194.3, 26352.6, 26510.9, 26669.2, 26827.5, 26985.8, 27144.1, 27302.4, 27460.7, 27619.0, 27511.6, 27404.2, 27296.8, 27189.4, 27082.0, 26974.6, 26867.2, 26759.8, 26652.4, 26545.0, 26471.1, 26397.2, 26323.3, 26249.4, 26175.5, 26101.6, 26027.7, 25953.8, 25879.9, 25806.0, 25143.3, 24480.6, 23817.9, 23155.2, 22492.5, 21829.8, 21167.1, 20504.4, 19841.7, 19179.0, 19611.5, 20044.0, 20476.5, 20909.0, 21341.5, 21774.0, 22206.5, 22639.0, 23071.5, 23504.0, 23092.4, 22680.8, 22269.2, 21857.6, 21446.0, 21034.4, 20622.8, 20211.2, 19799.6, 19388.0, 19313.4, 19238.8, 19164.2, 19089.6, 19015.0, 18940.4, 18865.8, 18791.2, 18716.6, 18642.0, 18451.6, 18261.2, 18070.8, 17880.4, 17690.0, 17499.6, 17309.2, 17118.8, 16928.4, 16738.0, 18116.8, 19495.6, 20874.4, 22253.2, 23632.0, 25010.8, 26389.6, 27768.4, 29147.2, 30526.0, 30206.2, 29886.4, 29566.6, 29246.8, 28927.0, 28607.2, 28287.4, 27967.6, 27647.8, 27328.0, 27266.6, 27205.2, 27143.8, 27082.4, 27021.0, 26959.6, 26898.2, 26836.8, 26775.4, 26714.0, 26708.9, 26703.8, 26698.7, 26693.6, 26688.5, 26683.4, 26678.3, 26673.2, 26668.1, 26663.0, 26625.3, 26587.6, 26549.9, 26512.2, 26474.5, 26436.8, 26399.1, 26361.4, 26323.7, 26286.0, 26178.3, 26070.6, 25962.9, 25855.2, 25747.5, 25639.8, 25532.1, 25424.4, 25316.7, 25209.0, 23069.1, 20929.2, 18789.3, 16649.4, 14509.5, 12369.6, 10229.7, 8089.8, 5949.9, 3810.0, 3914.5, 4019.0, 4123.5, 4228.0, 4332.5, 4437.0, 4541.5, 4646.0, 4750.5, 4855.0, 4851.5, 4848.0, 4844.5, 4841.0, 4837.5, 4834.0, 4830.5, 4827.0, 4823.5, 4820.0, 4802.9, 4785.8, 4768.7, 4751.6, 4734.5, 4717.4, 4700.3, 4683.2, 4666.1, 4649.0, 4625.7, 4602.4, 4579.1, 4555.8, 4532.5, 4509.2, 4485.9, 4462.6, 4439.3, 4416.0, 4365.6, 4315.2, 4264.8, 4214.4, 4164.0, 4113.6, 4063.2, 4012.8, 3962.4, 3912.0, 3896.2, 3880.4, 3864.6, 3848.8, 3833.0, 3817.2, 3801.4, 3785.6, 3769.8, 3754.0, 3759.4, 3764.8, 3770.2, 3775.6, 3781.0, 3786.4, 3791.8, 3797.2, 3802.6, 3808.0, 3782.6, 3757.2, 3731.8, 3706.4, 3681.0, 3655.6, 3630.2, 3604.8, 3579.4, 3554.0, 3564.1, 3574.2, 3584.3, 3594.4, 3604.5, 3614.6, 3624.7, 3634.8, 3644.9, 3655.0, 3636.3, 3617.6, 3598.9, 3580.2, 3561.5, 3542.8, 3524.1, 3505.4, 3486.7, 3468.0, 3452.8, 3437.6, 3422.4, 3407.2, 3392.0, 3376.8, 3361.6, 3346.4, 3331.2, 3316.0, 3327.8, 3339.6, 3351.4, 3363.2, 3375.0, 3386.8, 3398.6, 3410.4, 3422.2, 3434.0, 3421.1, 3408.2, 3395.3, 3382.4, 3369.5, 3356.6, 3343.7, 3330.8, 3317.9, 3305.0, 3301.6, 3298.2, 3294.8, 3291.4, 3288.0, 3284.6, 3281.2, 3277.8, 3274.4, 3271.0, 3250.3, 3229.6, 3208.9, 3188.2, 3167.5, 3146.8, 3126.1, 3105.4, 3084.7, 3064.0, 3068.8, 3073.6, 3078.4, 3083.2, 3088.0, 3092.8, 3097.6, 3102.4, 3107.2, 3112.0, 3114.8, 3117.6, 3120.4, 3123.2, 3126.0, 3128.8, 3131.6, 3134.4, 3137.2, 3140.0, 3128.6, 3117.2, 3105.8, 3094.4, 3083.0, 3071.6, 3060.2, 3048.8, 3037.4, 3026.0, 3010.5, 2995.0, 2979.5, 2964.0, 2948.5, 2933.0, 2917.5, 2902.0, 2886.5, 2871.0, 2869.9, 2868.8, 2867.7, 2866.6, 2865.5, 2864.4, 2863.3, 2862.2, 2861.1, 2860.0, 2853.4, 2846.8, 2840.2, 2833.6, 2827.0, 2820.4, 2813.8, 2807.2, 2800.6, 2794.0, 2794.2, 2794.4, 2794.6, 2794.8, 2795.0, 2795.2, 2795.4, 2795.6, 2795.8, 2796.0, 2795.3, 2794.6, 2793.9, 2793.2, 2792.5, 2791.8, 2791.1, 2790.4, 2789.7, 2789.0, 2794.1, 2799.2, 2804.3, 2809.4, 2814.5, 2819.6, 2824.7, 2829.8, 2834.9, 2840.0, 2808.8, 2777.6, 2746.4, 2715.2, 2684.0, 2652.8, 2621.6, 2590.4, 2559.2, 2528.0, 2513.7, 2499.4, 2485.1, 2470.8, 2456.5, 2442.2, 2427.9, 2413.6, 2399.3, 2385.0, 2385.1, 2385.2, 2385.3, 2385.4, 2385.5, 2385.6, 2385.7, 2385.8, 2385.9, 2386.0, 2389.7, 2393.4, 2397.1, 2400.8, 2404.5, 2408.2, 2411.9, 2415.6, 2419.3, 2423.0, 2417.2, 2411.4, 2405.6, 2399.8, 2394.0, 2388.2, 2382.4, 2376.6, 2370.8, 2365.0, 2336.4, 2307.8, 2279.2, 2250.6, 2222.0, 2193.4, 2164.8, 2136.2, 2107.6, 2079.0, 2082.9, 2086.8, 2090.7, 2094.6, 2098.5, 2102.4, 2106.3, 2110.2, 2114.1, 2118.0, 2106.8, 2095.6, 2084.4, 2073.2, 2062.0, 2050.8, 2039.6, 2028.4, 2017.2, 2006.0, 1999.2, 1992.4, 1985.6, 1978.8, 1972.0, 1965.2, 1958.4, 1951.6, 1944.8, 1938.0, 1946.6, 1955.2, 1963.8, 1972.4, 1981.0, 1989.6, 1998.2, 2006.8, 2015.4, 2024.0, 1962.8, 1901.6, 1840.4, 1779.2, 1718.0, 1656.8, 1595.6, 1534.4, 1473.2, 1412.0, 1412.0, 1412.0, 1412.0, 1412.0, 1412.0, 1412.0, 1412.0, 1412.0, 1412.0, 1412.0, 1406.8, 1401.6, 1396.4, 1391.2, 1386.0, 1380.8, 1375.6, 1370.4, 1365.2, 1360.0, 1369.5, 1379.0, 1388.5, 1398.0, 1407.5, 1417.0, 1426.5, 1436.0, 1445.5, 1455.0, 1447.7, 1440.4, 1433.1, 1425.8, 1418.5, 1411.2, 1403.9, 1396.6, 1389.3, 1382.0, 1380.0, 1378.0, 1376.0, 1374.0, 1372.0, 1370.0, 1368.0, 1366.0, 1364.0, 1362.0, 1351.3, 1340.6, 1329.9, 1319.2, 1308.5, 1297.8, 1287.1, 1276.4, 1265.7, 1255.0, 1259.3, 1263.6, 1267.9, 1272.2, 1276.5, 1280.8, 1285.1, 1289.4, 1293.7, 1298.0, 1295.1, 1292.2, 1289.3, 1286.4, 1283.5, 1280.6, 1277.7, 1274.8, 1271.9, 1269.0, 1260.1, 1251.2, 1242.3, 1233.4, 1224.5, 1215.6, 1206.7, 1197.8, 1188.9, 1180.0, 1177.7, 1175.4, 1173.1, 1170.8, 1168.5, 1166.2, 1163.9, 1161.6, 1159.3, 1157.0, 1153.4, 1149.8, 1146.2, 1142.6, 1139.0, 1135.4, 1131.8, 1128.2, 1124.6, 1121.0, 1119.9, 1118.8, 1117.7, 1116.6, 1115.5, 1114.4, 1113.3, 1112.2, 1111.1, 1110.0, 1106.6, 1103.2, 1099.8, 1096.4, 1093.0, 1089.6, 1086.2, 1082.8, 1079.4, 1076.0, 1073.2, 1070.4, 1067.6, 1064.8, 1062.0, 1059.2, 1056.4, 1053.6, 1050.8, 1048.0, 1055.0, 1062.0, 1069.0, 1076.0, 1083.0, 1090.0, 1097.0, 1104.0, 1111.0, 1118.0, 1110.1, 1102.2, 1094.3, 1086.4, 1078.5, 1070.6, 1062.7, 1054.8, 1046.9, 1039.0, 1042.2, 1045.4, 1048.6, 1051.8, 1055.0, 1058.2, 1061.4, 1064.6, 1067.8, 1071.0, 1060.3, 1049.6, 1038.9, 1028.2, 1017.5, 1006.8, 996.1, 985.4, 974.7, 964.0, 965.1, 966.2, 967.3, 968.4, 969.5, 970.6, 971.7, 972.8, 973.9, 975]


WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.CLASS_NAME, "login"))).click()

usernameInput = input("Enter Username - ")
passwordInput = pwinput.pwinput("Enter Password - ")

username_field = driver.find_element("xpath","//input[@type='text']")
password_field = driver.find_element("xpath","//input[@type='password']")
username_field.send_keys(usernameInput)
password_field.send_keys(passwordInput)
password_field.send_keys(Keys.ENTER)
print("Waiting for Steam confirmation...")
WebDriverWait(driver, 1200).until(EC.presence_of_element_located((By.CLASS_NAME, "btn_green_white_innerfade")))
driver.find_element("xpath","//input[@type='submit']").click()
print("Logged in.")
WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'avatar')))

print("Session Ready!")

souvenirGoldsInput = input("Golds can be souvenir? This will split the check into Normal & StatTrak categories (YES or NO) - ")
#split it by running the check, then if the sticker contains gold in the name, close the check out, return the fact that it's a gold, then run two separate checks with categories included

now = datetime.datetime.now()
name = now.strftime("%x")+"-"+now.strftime("%X")
filename = name.replace("/","_").replace(":","_")

for name,sticker in stickers.items():
    total_applied=0
    deduct_amount=0
    for i in range(5,0,-1):

        search_num1 = 0
        search_num2 = 0

        data=[]
        count=None
        myElem2=None
        for z in range(i):
            data.append(json.loads(f"{{\"i\":\"{sticker}\"}}"))
        
        data1=str(data).replace("'","\"")

        extracted_count = getCount(driver,30,data1,0,1,False,0) #30 is the time that it waits for the page to load

        while extracted_count == "Fail":
            print("Sleeping 25 - 45 seconds")
            time.sleep(round(random.uniform(25,45),8))
            extracted_count = getCount(driver,30,data1,0,1,False,0) #False means too many requests, this will make it retry for as long as its "false"
            #50 is the time that it waits for the page to load

        if extracted_count == "gold": #Souvenir capable gold detected, running split in two search
            extracted_count = handleSouvenirGolds(driver,data1)
            

            
        if extracted_count != "gold":
            if extracted_count > 40000:
                splitted_total = 0

                number_of_searches = math.ceil((extracted_count / 40000) * 1.44) #1.47 is arbitrary, experiment with it
                #Calculate. (Maybe count / 40k ) * 1.3 (always rounded up)

                all_search_nums = multiple_weighted_average(floats,weights,number_of_searches)

                print(f"Count above 40,000, splitting into {number_of_searches} searches instead, search numbers: {all_search_nums}.")

                for i2 in numpy.arange(0,number_of_searches,1):
                    
                    if search_num2 == 0:
                        search_num2 = all_search_nums[i2]
                    else:
                        search_num1 = search_num2
                        search_num2 = all_search_nums[i2]

                    #print(f"Search Number 1: {search_num1}, Search Number 2: {search_num2}")
                
                    print(f"Search_num1: {search_num1}, Search_num2: {search_num2}")
                    splitted_result = getCount(driver,30,data1,search_num1,search_num2,False,0) #50 is the time that it waits for the page to load


                    while splitted_result == "Fail":
                        print("Sleeping 25 - 45 seconds")
                        time.sleep(round(random.uniform(25,45),8))
                        splitted_result = getCount(driver,30,data1,search_num1,search_num2,False,0) #False means too many requests, this will make it retry for as long as its "false"
                        #50 is the time that it waits for the page to load

                    print(f"Splitted Result: {splitted_result}")

                    if isinstance(splitted_result,int) == True:
                        if splitted_result > 40000:
                            print("OVER 40K.... RUNNING TWICE AGAIN AND NOT COUNTING PREVIOUS RESULT")
                            splitted_result = 0
                            old_search_num2 = search_num2
                            search_num2 = round((search_num1 + search_num2) / 2,4)
                            print(f"Search_num1: {search_num1}, Search_num2: {search_num2}")
                            splitted_result = getCount(driver,30,data1,search_num1,search_num2,False,0)
                            while splitted_result == "Fail":
                                print("Sleeping 25 - 45 seconds")
                                time.sleep(round(random.uniform(25,45),8))
                                splitted_result = getCount(driver,30,data1,search_num1,search_num2,False,0) #False means too many requests, this will make it retry for as long as its "false"
                            search_num1 = search_num2
                            search_num2 = old_search_num2
                            print(f"Search_num1: {search_num1}, Search_num2: {search_num2}")
                            splitted_result2 = getCount(driver,30,data1,search_num1,search_num2,False,0)
                            while splitted_result2 == "Fail":
                                print("Sleeping 25 - 45 seconds")
                                time.sleep(round(random.uniform(25,45),8))
                                splitted_result2 = getCount(driver,30,data1,search_num1,search_num2,False,0) #False means too many requests, this will make it retry for as long as its "false"
                            
                            splitted_result += splitted_result2
                            
                            #cancer code don't look please... it's a bandaid solution to a minor problem that doesn't need that much time
                            print(f"SPLIT IN TWO RUN COMPLETE, RESULT FOUND TOTAL: {splitted_result}")

                    splitted_total += splitted_result

                    print(f"Splitted total: {splitted_total}")

                extracted_count = splitted_total
                print(f"Split up search complete. {extracted_count}")



        if total_applied>0:
            print("Deducting",deduct_amount)
        
        print("Adding to total:",((extracted_count - deduct_amount) * i),"sticker applications")
        total_applied = total_applied + ((extracted_count - deduct_amount) * i)
        deduct_amount = extracted_count
        print("Total applications:",total_applied)
    time_completed = datetime.datetime.now().strftime("%D:%H:%M:%S")
    result = [name,total_applied,time_completed]
    results.append(result)
    file = open(filename+".txt","a")
    file.write(str(result)+", ")
    file.close()
    print(results)


winsound.Beep(500,750)
print("Complete!")

while True:
    pass