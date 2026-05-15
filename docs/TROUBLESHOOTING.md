# Troubleshooting Guide

## Common Issues & Solutions

---

## ❌ Issue: Button Still Not Working on Home Page

**Problem:** Home page blue button still doesn't navigate

**Solution:**
1. Make sure you have `pages/report_form.py` file
2. Restart the Streamlit app
3. Clear browser cache (Ctrl+Shift+Delete)
4. Try: Click button again or use sidebar navigation

**Check:**
- ✅ `pages/report_form.py` exists in frontend folder
- ✅ File has `render_report_form()` function
- ✅ Main app.py has `st.switch_page("pages/report_form.py")`

---

## ❌ Issue: Cyber Laws Not Showing

**Problem:** Law guide page shows empty or no laws

**Solution:**
1. Make sure `frontend/data/cyber_laws.py` exists
2. Check file is not empty (17 laws should be there)
3. Restart app and try again

**Check:**
- ✅ `frontend/data/cyber_laws.py` file exists
- ✅ File contains CYBER_LAWS dictionary
- ✅ `frontend/pages/law_guide.py` imports from cyber_laws

**Manual Fix:**
```python
# Add to law_guide.py if needed
import sys
sys.path.append('data')
from cyber_laws import get_all_laws
laws_data = get_all_laws()
```

---

## ❌ Issue: Officer Login Page Doesn't Appear

**Problem:** Can't find officer login button

**Solution:**
1. Check sidebar has "🔐 Staff Area" section
2. Look for "👮 Officer Panel Login" button
3. Restart app

**Check:**
- ✅ Officer login code added to app.py sidebar
- ✅ `pages/officer_login.py` file exists
- ✅ File has `render_officer_login()` function

---

## ❌ Issue: Officer Registration Not Saving

**Problem:** Can't create officer account

**Solution:**
1. Enter all required fields (no blanks)
2. Password must be 6+ characters
3. Passwords must match exactly
4. Name will auto-generate Officer ID
5. Check `backend/data/` folder exists

**Check:**
- ✅ `backend/data/officers.json` file exists
- ✅ Folder structure: `backend/data/officers.json`
- ✅ JSON file is readable/writable

**Manual Fix:**
If officer won't save:
```bash
# Check file permissions
# Windows: Right-click → Properties → Security → Edit
# Make sure folder is writable
```

---

## ❌ Issue: Officer Panel Shows No Complaints

**Problem:** Officer sees "No pending reports" even after filing complaint

**Solution:**
1. File a complaint first (click home page button)
2. Save the Tracking ID shown
3. Wait a moment (app needs to save)
4. Go back to officer panel
5. Refresh the page (F5)

**Check:**
- ✅ `backend/data/complaints.json` file exists
- ✅ File contains complaint data (not empty `{}`)
- ✅ Officer is actually logged in

**Manual Debug:**
Open `backend/data/complaints.json` and check:
```json
{
  "CCRS-PK-2026-XXXXX": {
    "complaint_reason": "Hacking",
    ...
  }
}
```

---

## ❌ Issue: Complaint Tracking Not Working

**Problem:** Can't find complaint by Tracking ID

**Solution:**
1. Use exact Tracking ID (copy-paste, no typos)
2. Format should be: CCRS-PK-2026-XXXXXXXX
3. Make sure complaint was submitted successfully
4. Refresh the page

**Check:**
- ✅ Tracking ID copied correctly
- ✅ `backend/data/complaints.json` has the complaint
- ✅ No typos in ID

---

## ❌ Issue: Officer Decision Won't Submit

**Problem:** "Submit Decision" button doesn't work

**Solution:**
1. Make sure you entered investigation notes
2. Notes field cannot be empty
3. Choose either "Approve" or "Reject"
4. Click submit after filling notes

**Check:**
- ✅ Radio button selected (Approve or Reject)
- ✅ Notes text area not empty
- ✅ At least 1 character in notes

---

## ❌ Issue: Officer ID Format Wrong

**Problem:** "Invalid Officer ID" error

**Solution:**
Officer ID should be: **CYBER2026** + **YOUR NAME**

**Examples:**
- ✅ CYBER2026HAMZA (correct)
- ✅ CYBER2026ALI (correct)
- ❌ CYBER2026 HAMZA (wrong - has space)
- ❌ cyber2026hamza (wrong - lowercase)
- ❌ HAMZA (wrong - missing prefix)

---

## ❌ Issue: Can't Login as Officer

**Problem:** Officer ID and password don't work

**Solution:**
1. Check Officer ID spelling (case-sensitive, no spaces)
2. Check password (case-sensitive)
3. Try demo account: ID=`CYBER2026DEMO`, Password=`demo123`
4. If still stuck, register a new officer

**Check:**
- ✅ Officer exists in `backend/data/officers.json`
- ✅ Password matches exactly
- ✅ No typos or extra spaces

---

## ❌ Issue: Form Shows Validation Error

**Problem:** "Please select complaint type" or similar errors

**Solution:**
1. **For complaint type:** Don't select "Select..." - choose actual crime type
2. **For description:** Type at least 10 characters
3. **For CNIC:** Must be exactly 13 digits (or leave blank)
4. **For name:** Type at least 2 characters (if not anonymous)
5. Fill all required fields before clicking Submit

**Checklist:**
- ✅ Complaint type selected (not "Select...")
- ✅ Description has 10+ characters
- ✅ CNIC is 13 digits OR checkbox says anonymous
- ✅ If not anonymous: name, phone fields filled

---

## ⚙️ Database Reset (If Needed)

**Problem:** Need to clear all data and start fresh

**Solution:**
1. Delete these files:
   - `backend/data/complaints.json`
   - `backend/data/officer_decisions.json`
   - `backend/data/officers.json`

2. Create fresh empty files:
   - Create empty `complaints.json` with `{}`
   - Create empty `officer_decisions.json` with `{}`
   - Create `officers.json` with demo officer:
   ```json
   {
     "CYBER2026DEMO": {
       "name": "Demo Officer",
       "designation": "Inspector",
       "email": "demo@police.gov.pk",
       "phone": "+92-300-0000000",
       "password": "demo123",
       "status": "active"
     }
   }
   ```

3. Restart app

---

## 🔍 Debug Mode

**Enable Debug Logging:**

Add to app.py:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Then use:
logger.debug(f"Complaint: {complaint_data}")
```

**Check Logs:**
- Look for `app.log` file in project root
- Shows all errors and debug messages

---

## 📱 Browser Issues

**Problem:** Page won't load or looks broken

**Solutions:**
1. **Clear cache:** Ctrl+Shift+Delete (or Cmd+Shift+Delete on Mac)
2. **Hard refresh:** Ctrl+F5 (or Cmd+Shift+R on Mac)
3. **Try different browser:** Chrome, Firefox, Edge
4. **Check console errors:** F12 → Console tab

---

## 🐍 Python Issues

**Error: "ModuleNotFoundError"**
- Make sure you're in correct directory
- Check file paths are correct
- Try: `pip install streamlit` if needed

**Error: "JSON decode error"**
- Check `backend/data/` JSON files are valid JSON
- Use JSON validator: https://jsonlint.com
- Backup and recreate files if corrupted

---

## 🚀 Performance Issues

**Problem:** App is slow or freezes

**Solutions:**
1. Close other applications
2. Restart Streamlit app
3. Check file sizes in `backend/data/`
4. Limit number of displayed records

**When to optimize:**
- If 1000+ complaints accumulated
- If page takes >5 seconds to load
- Move to proper database (PostgreSQL/MongoDB)

---

## 📞 Emergency Contacts

**If issue persists:**
1. Check all file paths are correct
2. Verify all files are created
3. Restart entire application
4. Clear all data and start fresh (see "Database Reset")
5. Re-read QUICK_REFERENCE.md
6. Contact system administrator

**System Admin Checklist:**
- ✅ All new files created
- ✅ All modified files updated
- ✅ Database folders exist
- ✅ File permissions correct
- ✅ No duplicate page definitions
- ✅ No circular imports

---

## ✅ Verification Checklist

Run through this to verify everything is working:

- [ ] Home button takes to complaint form
- [ ] Can file complaint and get Tracking ID
- [ ] Can view cyber laws with search
- [ ] Can click "Officer Panel Login"
- [ ] Can register officer with auto ID
- [ ] Officer can login
- [ ] Officer sees pending complaints
- [ ] Officer can review complaint
- [ ] Officer can approve/reject
- [ ] Can track complaint by ID
- [ ] See correct status (Pending/Approved/Rejected)
- [ ] Officer statistics show correct counts

---

**Last Updated:** May 14, 2026  
**Version:** 1.0
