import gspread      #used to interact with Google Sheets using Python
from oauth2client.service_account import ServiceAccountCredentials  # used for authentication (login) with Google APIs
import requests # caalling APIs , Fetching data from websities
import time  # for time related operations 
from datetime import datetime #used for time and date handling
from dotenv import load_dotenv
import os
load_dotenv()


# ================= GOOGLE SHEET SETUP =================
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

spreadsheet = client.open_by_url(
    "https://docs.google.com/spreadsheets/d/1uMBhhz8nVKs8Pye8z6YzZHSG-C2JnMudq_ooFdpLdD4/edit?gid=0#gid=0"
)

sheet = spreadsheet.worksheet(" Leetcode")  

# ================= LEETCODE SETUP =================
url = "https://leetcode.com/api/submissions/"

cookies = {
    "LEETCODE_SESSION": os.getenv("LEETCODE_SESSION")
}


# ================= TRACK LAST SUBMISSION =================
last_submission_id = None

# ================= FUNCTION =================
def update_sheet():
    data = sheet.get_all_values()

    header_row_index = 3   # row 4 (names)
    date_col_index = 1     # column A (dates)

    # 🔍 find your column
    header = data[header_row_index]
    col_index = None

    for i, col_name in enumerate(header):
        if col_name.strip().upper() == "HARSH":
            col_index = i + 1
            break

    if col_index is None:
        print("❌ Name not found")
        return

    # 📅 get today's date (match format in sheet)
    today = datetime.now().strftime("%d/%m/%Y")

    # 🔍 find today's row
    row_index = None
    for i, row in enumerate(data):
        if len(row) > 0 and row[0].strip() == today:
            row_index = i + 1
            break

    if row_index is None:
        print("❌ Today's date not found")
        return

    # ➕ update value
    cell_value = sheet.cell(row_index, col_index).value

    if cell_value is None or cell_value == "":
        sheet.update_cell(row_index, col_index, 1)
    elif cell_value.isdigit():
        sheet.update_cell(row_index, col_index, int(cell_value) + 1)
    else:
        sheet.update_cell(row_index, col_index, 1)

    print("✅ Updated today's row!")

# ================= MAIN LOOP =================
print("🚀 Automation started...")

# Initialize last submission to avoid counting old ones
response = requests.get(url, cookies=cookies)
data = response.json()

if 'submissions_dump' in data and len(data['submissions_dump']) > 0:
    last_submission_id = data['submissions_dump'][0]['id']
else:
    print("❌ Could not fetch submissions. Check cookie.")
    last_submission_id = None


while True:
    try:
        response = requests.get(url, cookies=cookies)
        data = response.json()

        
        if 'submissions_dump' not in data or len(data['submissions_dump']) == 0:
            print("⚠️ No submission data (cookie issue)")
            time.sleep(10)
            continue

        latest = data['submissions_dump'][0]

        submission_id = latest['id']
        status = latest['status_display']

        submission_id = latest['id']
        status = latest['status_display']

        # 🔍 Check new submission
        if submission_id != last_submission_id:
            print("New submission detected:", status)

            if status == "Accepted":
                update_sheet()

            last_submission_id = submission_id

    except Exception as e:
        print("Error:", e)

    time.sleep(10) 