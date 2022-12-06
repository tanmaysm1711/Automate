import os

# Path for storing the WhatsApp session
CHROME_PROFILE_PATH = f'user-data-dir=C:\\Users\\{os.getlogin()}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Automate'

# Path to Excel file which is to be worked upon
SAMPLE_LIST_PATH = f"{os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')}DESIGN_STATUS.xlsm"

# Path to folder containing image files for the records present in Excel file
DESIGN_FILES_DIRECTORY_PATH = f"{os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')}\\Designs"

# Path to folder which will contain the images of filtered samples
CLIENT_DIRECTORY_PATH = f"{os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')}\\Client"
