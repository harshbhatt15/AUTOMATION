# 🚀 LeetCode to Google Sheets Automation

This project automatically tracks my LeetCode submissions and updates a Google Sheet in real-time.

---

## 🔧 Features

- Detects new LeetCode submissions
- Updates daily progress in Google Sheets
- Automatically increments problem count
- Handles empty cells and invalid entries
- Works with custom sheet structure (date-based tracking)

---

## 🛠️ Tech Stack

- Python
- Google Sheets API
- LeetCode unofficial API
- Requests

---

## ⚙️ How It Works

1. Script runs continuously in the background  
2. Checks latest LeetCode submission every few seconds  
3. If submission is **Accepted ✅**:
   - Finds today's date row in Google Sheet  
   - Updates the count in the correct column  


---

## Author
-- Harsh bhatt
-- BCA 