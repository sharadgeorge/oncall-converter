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
- **Private Deployment**: GitHub repo is private
- **Access Control**: Use Streamlit's built-in authentication if needed

## Support

For issues or questions:
1. Check the warnings/errors displayed in the app
2. Review the debug information in expanded sections
3. Verify schedule file format matches department requirements

## License

Internal use only.
