# Quick Deployment Guide

## 🚀 Deploy to Streamlit Community Cloud in 5 Minutes

### Step 1: Prepare GitHub Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click the "+" icon → "New repository"
3. Name it: `oncall-converter` (or your preferred name)
4. Choose "Private" if employee data is sensitive
5. Click "Create repository"

### Step 2: Upload Files

You can upload files via GitHub web interface:

1. Click "uploading an existing file"
2. Drag and drop the entire `oncall_converter` folder
3. Or upload files one by one maintaining this structure:
   ```
   oncall-converter/
   ├── app.py
   ├── requirements.txt
   ├── README.md
   ├── .gitignore
   ├── .streamlit/
   │   └── config.toml
   └── department_configs/
       ├── cardiology_config.py
       ├── radiology_config.py
       └── template_config.py
   ```

### Step 3: Deploy to Streamlit

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub (authorize the connection)
3. Click **"New app"**
4. Fill in the form:
   - **Repository**: Select `your-username/oncall-converter`
   - **Branch**: `main` (or `master`)
   - **Main file path**: `app.py`
5. Click **"Deploy!"**

### Step 4: Wait for Deployment

- Streamlit will install dependencies (takes 2-3 minutes)
- You'll see logs in real-time
- Once complete, you'll get a URL like: `https://oncall-converter.streamlit.app`

### Step 5: Test Your App

1. Click the URL to open your app
2. Select a department
3. Upload a test schedule file
4. Verify the conversion works

### Step 6: Share with Team

- Share the Streamlit URL with your team
- Bookmark it for easy access
- Consider adding password protection if needed

---

## 🔧 Alternative: Deploy via Git (for developers)

If you're comfortable with Git:

```bash
# 1. Initialize git in your folder
cd oncall_converter
git init

# 2. Add all files
git add .

# 3. Commit
git commit -m "Initial commit"

# 4. Link to GitHub
git remote add origin https://github.com/your-username/oncall-converter.git

# 5. Push to GitHub
git branch -M main
git push -u origin main

# 6. Then follow Step 3 above to deploy on Streamlit
```

---

## 📝 Post-Deployment Configuration

### Update Employee Map

If you need to add/modify employees:

1. Edit `app.py` on GitHub
2. Find the `EMPLOYEE_MAP` section
3. Add your employees following the format
4. Commit changes
5. Streamlit will automatically redeploy (takes 1-2 minutes)

### Add New Department

1. Create new config file in `department_configs/`
2. Copy from `template_config.py`
3. Customize for your department
4. Update `EMPLOYEE_MAP` in `app.py`
5. Commit and push
6. Auto-redeploys!

---

## 🔒 Security & Privacy

### Recommended Settings:

1. **Make GitHub Repo Private**
   - Go to repo Settings → Danger Zone → Change visibility → Private

2. **Add Password Protection** (optional)
   - In Streamlit app settings
   - Share password only with authorized users

3. **Review Employee Data**
   - Ensure no sensitive info in `EMPLOYEE_MAP`
   - Use employee IDs, not personal identifiers

---

## ❓ Troubleshooting

### "Application error" on Streamlit
- Check the logs in Streamlit dashboard
- Verify all files are uploaded correctly
- Ensure `requirements.txt` is present

### Files not appearing
- Check folder structure matches exactly
- Department configs must be in `department_configs/` folder
- File names must end with `_config.py`

### "Module not found"
- Verify `requirements.txt` contains all dependencies
- Try redeploying the app from Streamlit dashboard

### Need Help?
- Check Streamlit logs for detailed error messages
- Review the main README.md for detailed documentation
- Test locally first with `streamlit run app.py`

---

## 🎉 You're Done!

Your OnCall Schedule Converter is now live and accessible from anywhere!

**Next Steps:**
- Test with real schedule files
- Share URL with your team
- Monitor for any warnings/errors
- Customize as needed
