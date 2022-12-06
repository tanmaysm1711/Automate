import time
import os
import shutil
import pandas as pd
import eel
from selenium import webdriver
from selenium.common import NoSuchElementException, WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from config import CHROME_PROFILE_PATH, SAMPLE_LIST_PATH, DESIGN_FILES_DIRECTORY_PATH, CLIENT_DIRECTORY_PATH

# Information for Command Line
print("STARTING THE APPLICATION...")

# Initializing directory for GUI files
eel.init('web')

# Initializing list for samples with no images
samples_with_no_images = []
filtered_samples_with_no_images = []

# WhatsApp Web URL
URL = 'https://web.whatsapp.com/'

# Initializing the buttons, input fields present on the WhatsApp Web UI
PHONE_NUMBER_INPUT = "//*[@id='side']/div[1]/div/div/div[2]/div/div[2]"
MESSAGE_INPUT = "//*[@id='main']/footer/div[1]/div/span[2]/div/div[2]/div[1]/div"
ATTACHMENT_BUTTON = "//*[@id='main']/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div"
IMAGE_BUTTON = "//*[@id='main']/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div/div/ul/li[1]/button/input"
SEND_BUTTON = "//*[@id='app']/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]/div/div[1]"

# Declaring variables for Chrome Driver
driver = ""
waiter = ""
options = ""

# List to store filtered file paths which will further be used when sending image files on WhatsApp
file_paths = []

# Declaring a variable to store Merged File Paths
merged_file_path = ""


# Function to check whether the Chrome WebDriver is alive or not
def is_webdriver_alive():
    # || print('Checking whether the driver is alive')
    try:
        # Returns an int if dead and None if alive
        assert (driver.service.process.poll() is None)

        # Throws a WebDriverException if dead
        driver.service.assert_process_still_running()

        # Throws a NoSuchElementException if dead
        driver.find_element_by_tag_name('html')

        # || print('The driver appears to be alive')

        return True
    except (NoSuchElementException, WebDriverException, AssertionError):
        # || print('The driver appears to be dead')
        return False
    except Exception as ex:
        print('Encountered an unexpected exception type ({}) while checking the driver status'.format(type(ex)))
        return False


def initialize_chrome_webdriver():
    global driver
    global waiter
    global options

    # Initializing options to create a session during the initial setup of the software
    options = webdriver.ChromeOptions()
    options.add_argument(CHROME_PROFILE_PATH)

    # Initializing the Chrome Driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(10)
    waiter = WebDriverWait(driver, 60)

    # Opening WhatsApp Web
    driver.get(URL)
    waiter.until(EC.title_is("WhatsApp"))


# Function to concatenate paths of filtered sample images
def concatenate_file_paths():
    global merged_file_path
    merged_file_path = "\n".join(file_paths[0:30])


def send_whatsapp_message(filters):
    time.sleep(2)

    while 1:
        try:
            if driver.find_element('xpath', "//canvas[@aria-label='Scan me!']"):
                waiter.until(EC.presence_of_element_located((By.XPATH, "//canvas[@aria-label='Scan me!']")))
        except:
            break

    # Using the PHONE_NUMBER_INPUT, search for the given phone number
    waiter.until(EC.presence_of_element_located((By.XPATH, PHONE_NUMBER_INPUT)))
    driver.find_element('xpath', PHONE_NUMBER_INPUT).send_keys(filters["clientPhoneNumber"])

    # Open the chat for the given PHONE_NUMBER
    driver.find_element('xpath', PHONE_NUMBER_INPUT).send_keys(Keys.ENTER)
    time.sleep(5)

    while len(file_paths) != 0:
        # Concatenating all the file paths
        concatenate_file_paths()
        del file_paths[0:30]

        # Click the ATTACHMENT_BUTTON on the chat window
        try:
            driver.find_element('xpath', ATTACHMENT_BUTTON).click()
        except NoSuchElementException:
            # print("Contact Does Not Exist!")
            eel.handleErrorsAndSuccess("Contact Does Not Exist")
            return
        time.sleep(5)

        # Click the Image/Video button and send the image file path to be sent
        driver.find_element('xpath', IMAGE_BUTTON).send_keys(merged_file_path)
        waiter.until(EC.presence_of_element_located((By.XPATH, SEND_BUTTON)))

        # Click the send button to send the selected image(s)
        driver.find_element('xpath', SEND_BUTTON).click()
        time.sleep(10)

    eel.handleErrorsAndSuccess("Image Files Sent!")


# Function to send filtered sample images via whatsapp
def send_on_whatsapp(filters):
    # Checking whether the chrome webdriver is alive or not
    if not is_webdriver_alive():
        initialize_chrome_webdriver()

    # Send whatsapp message
    send_whatsapp_message(filters)

    # Close chromedriver
    driver.close()


# Function to move the files from No Stock to Stock
def move_to_stock(file_name):
    # || print(file_name)
    if file_name.find('\\NoStock') != -1:
        destination = file_name.replace("NoStock", "Stock")
    else:
        destination = file_name

    try:
        if os.path.exists(destination):
            # || print(f'{file_name} already exists!')
            pass
        else:
            os.replace(file_name, destination)
            # || print("Source file moved to specified destination")
    except FileNotFoundError:
        print(file_name + " File Not Found")


# Function to move the files from Stock to No Stock
def move_from_stock_to_no_stock(file_name):
    # || print(file_name)
    if file_name.find('\\Stock') != -1:
        destination = file_name.replace("Stock", "NoStock")
    else:
        destination = file_name

    try:
        if os.path.exists(destination):
            pass
            # print(f'{file_name} already exists!')
        else:
            os.replace(file_name, destination)
            # print("Source file was moved to specified destination")
    except FileNotFoundError:
        print(file_name + " File Not Found")


# Function to create a separate folder and copy the filtered sample images
def separate_filtered_samples_images(file_path, file_name):
    destination = CLIENT_DIRECTORY_PATH
    # || print(destination)
    if not os.path.exists(destination):
        # || print("Created A New One!")
        os.mkdir(destination)

    destination = os.path.join(destination, file_name)
    os.system(f'copy "{file_path}" "{destination}"')
    file_paths.append(destination)


# Function to create an Excel File for Samples with No Images
def create_excel_sheet_of_samples_with_no_images():
    no_images = pd.DataFrame(samples_with_no_images, columns=['DESIGN_NAME'])
    # || print(no_images)
    with pd.ExcelWriter('C:\\Users\\hp\\Documents\\AviraFashions\\NO_IMAGES.xlsx') as writer:
        no_images.to_excel(writer)


# Function to create an Excel File for Filtered Samples with No Images
def create_excel_sheet_of_filtered_samples_with_no_images():
    no_images = pd.DataFrame(filtered_samples_with_no_images, columns=['DESIGN_NAME'])
    if not os.path.exists(CLIENT_DIRECTORY_PATH):
        # || print("Directory Non-Existent")
        os.mkdir(CLIENT_DIRECTORY_PATH)

    if os.path.exists(f'{CLIENT_DIRECTORY_PATH}\\NO_IMAGES.xlsx'):
        print("Excel file exists")
        os.remove(f'{CLIENT_DIRECTORY_PATH}\\NO_IMAGES.xlsx')

    with pd.ExcelWriter(f'{CLIENT_DIRECTORY_PATH}\\NO_IMAGES.xlsx') as writer:
        no_images.to_excel(writer)


# Function to separate filtered samples with and without images
def create_filtered_sample_images_folder(filtered_samples):
    # print("Filtering Samples and Separating Images!")
    global filtered_samples_with_no_images
    global file_paths

    filtered_samples_with_no_images = []
    file_paths = []

    # Declaring difference for separation of samples
    difference = 0
    for index, sample in filtered_samples.iterrows():
        # Initializing the file to be searched for
        file_to_search = sample['DESIGN_NAME'] + '.jpg'
        file_found = False

        if sample['Width'] == '36':
            difference = 30
        elif sample['Width'] == '58':
            difference = 20

        if sample['Difference'] >= difference:
            # print(f'{sample["DESIGN_NAME"]} IN STOCK')

            # Searching for files in the directory
            for relative_path, dirs, files in os.walk(DESIGN_FILES_DIRECTORY_PATH):

                # Checking whether file exists or not
                if file_to_search in files:
                    file_found = True
                    # print(f'{file_to_search} found in {relative_path}')
                    separate_filtered_samples_images(f'{relative_path}\\{file_to_search}', file_to_search)

            if not file_found:
                filtered_samples_with_no_images.append(sample['DESIGN_NAME'])

    create_excel_sheet_of_filtered_samples_with_no_images()


# Function to separate samples into Stock and No Stock
def separate_stock_no_stock(samples_list):
    # || print("No Filter Given | Separating in Stock & No Stock")

    # Declaring net_difference for separation of samples into Stock | No Stock
    net_difference = 0
    for index, sample in samples_list.iterrows():

        # Initializing the file to be searched for
        file_to_search = sample['DESIGN_NAME'] + '.jpg'
        file_found = False

        # Searching for files in the directory
        for relative_path, dirs, files in os.walk(DESIGN_FILES_DIRECTORY_PATH):
            if relative_path.find("36_inches") != -1:
                net_difference = 30
            elif relative_path.find("58_inches") != -1:
                net_difference = 20

            # Checking whether file exists or not
            if file_to_search in files:
                file_found = True

                # Checking whether stock exists or not
                if sample['Difference'] < net_difference:
                    # || print(f'{file_to_search} found in {relative_path}')
                    move_from_stock_to_no_stock(f'{relative_path}\\{file_to_search}')
                else:
                    move_to_stock(f'{relative_path}\\{file_to_search}')

        if not file_found:
            samples_with_no_images.append(sample['DESIGN_NAME'])

    create_excel_sheet_of_samples_with_no_images()
    eel.handleErrorsAndSuccess("Samples Separated into Stock & No Stock!")


@eel.expose
def rename_files():
    # Searching for files
    for relative_path, dirs, files in os.walk(DESIGN_FILES_DIRECTORY_PATH):
        for file in files:
            if file.find('.jpg') != -1:
                filename = file.replace('.jpg', '')
            elif file.find('.JPG') != -1:
                filename = file.replace('.JPG', '')
            elif file.find('.jpeg') != -1:
                filename = file.replace('.jpeg', '')
            elif file.find('.png') != -1:
                filename = file.replace('.png', '')

            try:
                os.rename(f'{relative_path}\\{file}', f'{relative_path}\\{filename.upper()}.jpg')
            except FileNotFoundError:
                print(f'{file} not found!')
            except FileExistsError:
                print(f"{file} - File with same name already exists!")

    # Information for Command Line
    print('Files Renamed Successfully!')
    eel.handleErrorsAndSuccess('Files Renamed Successfully!')


@eel.expose
def initialize_and_get_categories():
    # Information for Command Line
    print("GETTING THE CATEGORIES FROM EXCEL SHEET...")

    # Initializing the Excel file
    samples_list = pd.read_excel(SAMPLE_LIST_PATH)

    # Finding all the unique categories from the DESCR column
    category_list = [category for category in list(samples_list['DESCR'].unique()) if str(category) != 'nan']

    # Information for Command Line
    print("FOUND THE CATEGORIES FROM EXCEL SHEET!")

    return category_list


@eel.expose
def exchange_filters(data):
    # Deleting the Client directory if it already exists
    if os.path.exists(CLIENT_DIRECTORY_PATH):
        shutil.rmtree(CLIENT_DIRECTORY_PATH)

    filters = data

    # || print(filters)

    samples_list = pd.read_excel(SAMPLE_LIST_PATH)
    filtered_samples = samples_list

    # Information for Command Line
    print("\nWORKING ON FILTERS...")

    if filters["category"]:
        filtered_samples = samples_list[samples_list['DESCR'].isin(filters["category"])]
        # || print("Category given")
    # || else:
        # || print("Category not given...")

    if filters["length"]:
        filtered_samples = filtered_samples.loc[filtered_samples['Difference'] >= filters["length"]]
        # || print("Length given")
    # || else:
        # || print("Length not given...")

    if filters["width"]:
        filtered_samples = filtered_samples.loc[filtered_samples['Width'] == filters["width"]]
        # || print("Width given")
    # || else:
        # || print("Width not given...")

    if (not filters["category"]) and (not filters["length"]) and (not filters["width"]):

        # Information for Command Line
        print("NO FILTERS GIVEN, THEREFORE SEPARATING SAMPLES INTO Stock & No Stock FOLDER...")
        eel.handleErrorsAndSuccess("Separating Samples into Stock & No Stock!")
        separate_stock_no_stock(samples_list)

        # Information for Command Line
        print("SEPARATION COMPLETED!")

        # Opens the folder containing images for all samples
        os.system(f'start {DESIGN_FILES_DIRECTORY_PATH}')
    else:
        # Information for Command Line
        print("CREATING A SEPARATE FOLDER FOR FILTERED SAMPLES...")
        create_filtered_sample_images_folder(filtered_samples)

        # Information for Command Line
        print("CREATED A SEPARATE FOLDER FOR FILTERED SAMPLES!")

        # || print(filters)

        # Opens the folder containing images of filtered samples
        os.system(f'start {CLIENT_DIRECTORY_PATH}')

        if filters["clientPhoneNumber"] and file_paths:

            # Information for Command Line
            print("GETTING THE CLIENT PHONE NUMBER AND SENDING FILES VIA WHATSAPP...")

            send_on_whatsapp(filters)
            print("FILES SENT SUCCESSFULLY!")
        else:
            # print(file_paths)
            if file_paths:
                eel.handleErrorsAndSuccess("Images Files Generated!")
            else:
                eel.handleErrorsAndSuccess("Image Files Do Not Exist!")

    # print(filtered_samples)
    return "You've reached python!"


eel.start("index.html")
