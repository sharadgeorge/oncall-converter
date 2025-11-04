# OnCall Schedule Converter - Streamlit Web App

A web-based system for converting department-specific Excel schedules to standardized CSV/Excel import format for Epic OnCall system.

## Features

- ✅ **Single Landing Page** - One unified interface for all departments
- 📁 **Multi-Department Support** - Radiology, Cardiology, and easily extensible for new departments
- 📤 **File Upload** - Simple drag-and-drop Excel file upload
- 🔄 **Automatic Processing** - Converts schedules with validation and error checking
- 📥 **Dual Output Formats** - Download results as CSV or Excel
- ⚠️ **Smart Warnings** - Alerts for unknown names, initials, and missing entries
- 🎨 **Clean UI** - Professional, easy-to-use interface

## File Structure

```
oncall_converter/
├── app.py                          # Main Streamlit application
├── department_configs/             # Backend department configurations
│   ├── cardiology_config.py       # Cardiology schedule logic
│   ├── radiology_config.py        # Radiology schedule logic
│   └── template_config.py         # Template for new departments
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## Deployment to Streamlit Community Cloud

### Prerequisites

1. GitHub account
2. Streamlit Community Cloud account (free at [share.streamlit.io](https://share.streamlit.io))

### Step-by-Step Deployment

1. **Create a GitHub Repository**
   - Go to GitHub and create a new repository (e.g., `oncall-converter`)
   - Make it private if the employee data is sensitive

2. **Upload Files**
   - Upload all files maintaining the folder structure:
     ```
     - app.py
     - requirements.txt
     - README.md
     - department_configs/
       - cardiology_config.py
       - radiology_config.py
       - template_config.py
     ```

3. **Deploy to Streamlit Community Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Connect your GitHub account
   - Select your repository
   - Set main file path: `app.py`
   - Click "Deploy"

4. **Wait for Deployment**
   - Streamlit will install dependencies and launch your app
   - Usually takes 2-3 minutes

5. **Share Your App**
   - You'll get a URL like: `https://your-app-name.streamlit.app`
   - Share this with your team

## Local Development

To run locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## Adding a New Department

1. **Create Configuration File**
   - Copy `department_configs/template_config.py`
   - Rename to `your_department_config.py`

2. **Customize Configuration**
   - Update class name (e.g., `YourDepartmentConfig`)
   - Implement required methods:
     - `get_department_name()`
     - `get_file_requirements()`
     - `get_team_abbr_map()`
     - `validate_and_configure()`
     - `extract_schedule_data()`

3. **Add Employees**
   - Update `EMPLOYEE_MAP` in `app.py` with your department's staff

4. **Deploy**
   - Commit and push to GitHub
   - Streamlit will auto-redeploy

## Usage Guide

1. **Select Department**
   - Choose your department from the dropdown

2. **Upload Files**
   - Upload Excel schedule files in the required order
   - Files are processed in memory (not stored on server)

3. **Configure Month/Year**
   - Auto-detection from filename
   - Manual override available

4. **Convert Schedule**
   - Click "Convert Schedule" button
   - View statistics and sample entries

5. **Download Results**
   - Download CSV for system import
   - Download Excel for review/backup

## Employee Map

The employee mapping connects schedule identifiers (initials/names) to system usernames. Update `EMPLOYEE_MAP` in `app.py`:

```python
EMPLOYEE_MAP = {
    'username1': {
        'emp_initials': 'AB',
        'emp_roles': ['1056'],
        'emp_name': 'Dr. Name',
        'department': 'Radiology'
    },
    # Add more employees...
}
```

## Troubleshooting

### "No department configurations found"
- Ensure `department_configs/` folder exists with config files
- Check file names end with `_config.py`

### "Module not found" errors
- Verify `requirements.txt` is in the root directory
- Check Python version compatibility (3.9+)

### Unknown names/initials warnings
- Add missing employees to `EMPLOYEE_MAP`
- Check for typos in schedule files

### Deployment fails
- Check GitHub repository structure matches file structure above
- Verify all files are committed
- Check Streamlit Community Cloud logs for specific errors

## Security Notes

- **No Data Storage**: Files are processed in memory only
- **Private Deployment**: Consider making GitHub repo private
- **Access Control**: Use Streamlit's built-in authentication if needed
- **Employee Data**: Review `EMPLOYEE_MAP` before deploying publicly

## Support

For issues or questions:
1. Check the warnings/errors displayed in the app
2. Review the debug information in expanded sections
3. Verify schedule file format matches department requirements

## License

Internal use only. Please ensure compliance with your organization's policies regarding employee data.
