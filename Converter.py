"""
Unified OnCall Schedule Converter - Streamlit Web App
=====================================================
A web-based system for converting department-specific Excel schedules 
to standardized CSV/Excel import format.
"""

import streamlit as st
import openpyxl
import csv
import calendar
import re
import io
from datetime import datetime, timedelta
from pathlib import Path
from abc import ABC, abstractmethod
import importlib.util
import pandas as pd
import tempfile
import os

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="OnCall Schedule Converter",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# EMPLOYEE MAPPING
# ============================================================================

EMPLOYEE_MAP = {
    # Radiology Department
    'allwo0f': {'emp_initials': 'AK', 'emp_roles': ['1056'], 'emp_name': 'Dr. Allison Livingston', 'department': 'Radiology'},
    'audr95t': {'emp_initials': 'AO', 'emp_roles': ['1056'], 'emp_name': 'Dr. Audrey Randy', 'department': 'Radiology'},
    'ellias4': {'emp_initials': 'AS', 'emp_roles': ['1056'], 'emp_name': 'Dr. Ankur Simran Ellison', 'department': 'Radiology'},
    'lotta3': {'emp_initials': 'AT', 'emp_roles': ['1056'], 'emp_name': 'Dr. Angela Lotti', 'department': 'Radiology'},
    'figeftr': {'emp_initials': 'FT', 'emp_roles': ['1056'], 'emp_name': 'Dr. Fernando Figer', 'department': 'Radiology'},
    'hauser4': {'emp_initials': 'IG', 'emp_roles': ['1056'], 'emp_name': 'Dr. Irvin Garrett Hauser', 'department': 'Radiology'},
    'kaisbam': {'emp_initials': 'LK', 'emp_roles': ['1056'], 'emp_name': 'Dr. Barry Midland Kaiser', 'department': 'Radiology'},
    'bellam5': {'emp_initials': 'MB', 'emp_roles': ['1056'], 'emp_name': 'Dr. Monica Bella', 'department': 'Radiology'},
    'chengme': {'emp_initials': 'MC', 'emp_roles': ['1056'], 'emp_name': 'Dr. Milkha Chengi', 'department': 'Radiology'},
    'fakma0e': {'emp_initials': 'MF', 'emp_roles': ['1056'], 'emp_name': 'Dr. Maria Nargis', 'department': 'Radiology'},
    'mumir4': {'emp_initials': 'MM', 'emp_roles': ['1056'], 'emp_name': 'Dr. Mir Miranda', 'department': 'Radiology'},
    'nilanin': {'emp_initials': 'NN', 'emp_roles': ['1056'], 'emp_name': 'Dr. Nayan Nilani', 'department': 'Radiology'},
    'hernapat': {'emp_initials': 'PR', 'emp_roles': ['1056'], 'emp_name': 'Dr. Paul Hernandez', 'department': 'Radiology'},
    'gonzsa2': {'emp_initials': 'SG', 'emp_roles': ['1056'], 'emp_name': 'Dr. Gonzales, Salem', 'department': 'Radiology'},
    'alitar3b': {'emp_initials': 'TA', 'emp_roles': ['1056'], 'emp_name': 'Dr. Tarzan Ali', 'department': 'Radiology'},
    'ignaro5w': {'emp_initials': 'RI', 'emp_roles': ['1056'], 'emp_name': 'Dr. Roberta Ignatius', 'department': 'Radiology'},
    
    # Cardiology Department
    'qulfi6e': {'emp_initials': 'Q', 'emp_roles': ['3042457'], 'emp_name': 'Qureshi', 'department': 'Cardiology'},
    'salam0c': {'emp_initials': 'S', 'emp_roles': ['3042457'], 'emp_name': 'Salami', 'department': 'Cardiology'},
    'mehndo4e': {'emp_initials': 'M', 'emp_roles': ['3042457'], 'emp_name': 'M. Enadi', 'department': 'Cardiology'},
    'lipar45': {'emp_initials': 'L', 'emp_roles': ['3042457'], 'emp_name': 'L. Parivar', 'department': 'Cardiology'},
    'alsind34': {'emp_initials': 'AS', 'emp_roles': ['3042457'], 'emp_name': 'Le Sindapur', 'department': 'Cardiology'},
    'formi57r': {'emp_initials': 'F99', 'emp_roles': ['3042457'], 'emp_name': 'Fox Machar', 'department': 'Cardiology'},
    'purita5': {'emp_initials': 'P99', 'emp_roles': ['72'], 'emp_name': 'P Bhajra', 'department': 'Cardiology'},
    'konasje': {'emp_initials': 'K99', 'emp_roles': ['72'], 'emp_name': 'Konsa', 'department': 'Cardiology'},
    'bhenjt4': {'emp_initials': 'B99', 'emp_roles': ['72'], 'emp_name': 'Ben Ji', 'department': 'Cardiology'},
    'maskirt3': {'emp_initials': 'Q99', 'emp_roles': ['72'], 'emp_name': 'Mesquita N', 'department': 'Cardiology'},
    'vahard3g': {'emp_initials': 'V99', 'emp_roles': ['72'], 'emp_name': 'Vaha Robert', 'department': 'Cardiology'},
    'lukolnd': {'emp_initials': 'L99', 'emp_roles': ['72'], 'emp_name': 'Lu K. Olna', 'department': 'Cardiology'},
    'sponset5': {'emp_initials': 'S99', 'emp_roles': ['72'], 'emp_name': 'Sp F Sed', 'department': 'Cardiology'},
    'tamasho': {'emp_initials': 'T99', 'emp_roles': ['72'], 'emp_name': 'Tamhane', 'department': 'Cardiology'},
    'fouza64w': {'emp_initials': 'F992', 'emp_roles': ['47'], 'emp_name': 'F Ouza Wik', 'department': 'Cardiology'},
    'dosa0b': {'emp_initials': 'AG', 'emp_roles': ['2001'], 'emp_name': 'Anita Gunda', 'department': 'Cardiology'},
    'ghas4g': {'emp_initials': 'GS', 'emp_roles': ['84', '2001'], 'emp_name': 'Ghaitani S', 'department': 'Cardiology'},
    'abherq': {'emp_initials': 'AE', 'emp_roles': ['84'], 'emp_name': 'Abe E M', 'department': 'Cardiology'},
    'villfh': {'emp_initials': 'VL', 'emp_roles': ['84'], 'emp_name': 'Village Lomba', 'department': 'Cardiology'},
}

# ============================================================================
# UTILITY CLASSES AND FUNCTIONS
# ============================================================================

class DebugTracker:
    """Tracks debugging information across schedule processing"""
    
    def __init__(self, department_name=""):
        self.department_name = department_name
        self.unknown_names = set()
        self.unknown_initials = set()
        self.expected_entries = []
        
    def add_unknown_name(self, name):
        self.unknown_names.add(name)
    
    def add_unknown_initials(self, initials):
        self.unknown_initials.add(initials)
    
    def add_expected_entry(self, team_name, day, start_time, end_time, source, employee=None):
        self.expected_entries.append({
            'team': team_name,
            'day': day,
            'start_time': start_time,
            'end_time': end_time,
            'source': source,
            'employee': employee,
            'generated': False
        })
    
    def mark_entry_generated(self, team_name, day, start_time, end_time):
        for entry in self.expected_entries:
            if (entry['team'] == team_name and 
                entry['day'] == day and 
                entry['start_time'] == start_time and 
                entry['end_time'] == end_time and
                not entry['generated']):
                entry['generated'] = True
                break
    
    def get_missing_entries(self):
        return [entry for entry in self.expected_entries if not entry['generated']]
    
    def get_warnings_summary(self):
        """Return warnings as a dictionary for Streamlit display"""
        warnings = {}
        if self.unknown_names:
            warnings['unknown_names'] = sorted(self.unknown_names)
        if self.unknown_initials:
            warnings['unknown_initials'] = sorted(self.unknown_initials)
        missing = self.get_missing_entries()
        if missing:
            warnings['missing_entries'] = missing
        return warnings

class DepartmentConfig(ABC):
    """Base class for department configurations"""
    
    def __init__(self, employee_map):
        self.employee_map = employee_map
        self.debug_tracker = DebugTracker(self.get_department_name())
    
    @abstractmethod
    def get_department_name(self):
        pass
    
    @abstractmethod
    def get_file_requirements(self):
        pass
    
    @abstractmethod
    def get_team_abbr_map(self):
        pass
    
    @abstractmethod
    def validate_and_configure(self, files, month, year):
        pass
    
    @abstractmethod
    def extract_schedule_data(self, workbooks, config, month, year):
        pass

def col_letter_to_index(letter):
    """Convert column letter (A, B, AA, etc.) to 1-based index"""
    letter = letter.upper()
    result = 0
    for char in letter:
        result = result * 26 + (ord(char) - ord('A') + 1)
    return result

def is_weekday(date):
    """Check if date is a weekday (Sunday=0 to Thursday=4 in Saudi Arabia)"""
    return date.weekday() in [6, 0, 1, 2, 3]

def extract_month_year_from_filename(filename):
    """Extract month and year from filename"""
    filename_lower = filename.lower()
    
    month_patterns = {
        1: ['january', 'jan'], 2: ['february', 'feb'], 3: ['march', 'mar'],
        4: ['april', 'apr'], 5: ['may'], 6: ['june', 'jun'],
        7: ['july', 'jul'], 8: ['august', 'aug'], 9: ['september', 'sep'],
        10: ['october', 'oct'], 11: ['november', 'nov'], 12: ['december', 'dec']
    }
    
    detected_month = None
    for month_num, patterns in month_patterns.items():
        for pattern in patterns:
            if pattern in filename_lower:
                detected_month = month_num
                break
        if detected_month:
            break
    
    year_match = re.search(r'20\d{2}', filename)
    detected_year = int(year_match.group()) if year_match else datetime.now().year
    
    return detected_month, detected_year

def create_schedule_entry(username, team_id, start_date, start_time, end_date, end_time, role):
    """Create a standardized schedule entry"""
    return {
        'EMPLOYEE': username,
        'TEAM': team_id,
        'STARTDATE': start_date.strftime('%m/%d/%Y'),
        'STARTTIME': start_time,
        'ENDDATE': end_date.strftime('%m/%d/%Y'),
        'ENDTIME': end_time,
        'ROLE': role,
        'NOTES': ''
    }

def write_output_files(output_data, year, month):
    """Write output data to CSV and Excel files in memory"""
    dept_name = "SCHEDULE"
    filename_prefix = f"EpicOnCall_Import_{dept_name}"
    
    # Create CSV in memory
    csv_buffer = io.StringIO()
    fieldnames = ['EMPLOYEE', 'TEAM', 'STARTDATE', 'STARTTIME', 'ENDDATE', 'ENDTIME', 'ROLE', 'NOTES']
    writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(output_data)
    csv_data = csv_buffer.getvalue()
    
    # Create Excel in memory
    df = pd.DataFrame(output_data)
    excel_buffer = io.BytesIO()
    df.to_excel(excel_buffer, index=False, engine='openpyxl')
    excel_data = excel_buffer.getvalue()
    
    csv_filename = f"{filename_prefix}_{year}_{calendar.month_name[month]}.csv"
    xlsx_filename = f"{filename_prefix}_{year}_{calendar.month_name[month]}.xlsx"
    
    return csv_data, excel_data, csv_filename, xlsx_filename

# ============================================================================
# DEPARTMENT CONFIG LOADER
# ============================================================================

def load_department_configs():
    """Load all department configuration classes"""
    configs = {}
    config_dir = Path(__file__).parent / 'department_configs'
    
    if not config_dir.exists():
        return configs
    
    for config_file in config_dir.glob('*_config.py'):
        try:
            spec = importlib.util.spec_from_file_location(config_file.stem, config_file)
            module = importlib.util.module_from_spec(spec)
            
            # Inject utilities
            module.DepartmentConfig = DepartmentConfig
            module.col_letter_to_index = col_letter_to_index
            module.is_weekday = is_weekday
            module.extract_month_year_from_filename = extract_month_year_from_filename
            module.create_schedule_entry = create_schedule_entry
            module.DebugTracker = DebugTracker
            
            spec.loader.exec_module(module)
            
            # Find DepartmentConfig subclasses
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (isinstance(attr, type) and 
                    issubclass(attr, DepartmentConfig) and 
                    attr is not DepartmentConfig):
                    try:
                        instance = attr(EMPLOYEE_MAP)
                        dept_name = instance.get_department_name().lower()
                        configs[dept_name] = attr
                    except Exception as e:
                        st.warning(f"Could not load {attr_name}: {e}")
        except Exception as e:
            st.warning(f"Could not load {config_file.name}: {e}")
    
    return configs

# ============================================================================
# STREAMLIT APP
# ============================================================================

def main():
    st.title("📅 OnCall Schedule Converter")
    st.markdown("---")
    
    # Load department configurations
    AVAILABLE_DEPARTMENTS = load_department_configs()
    
    if not AVAILABLE_DEPARTMENTS:
        st.error("⚠️ No department configurations found!")
        st.info("Please ensure department configuration files are in the `department_configs/` folder.")
        return
    
    # Department Selection
    st.header("1. Select Department")
    dept_names = list(AVAILABLE_DEPARTMENTS.keys())
    selected_dept = st.selectbox(
        "Choose your department:",
        options=dept_names,
        format_func=lambda x: x.capitalize()
    )
    
    if not selected_dept:
        return
    
    # Initialize department config
    dept_config = AVAILABLE_DEPARTMENTS[selected_dept](EMPLOYEE_MAP)
    file_reqs = dept_config.get_file_requirements()
    
    st.success(f"✓ Selected: {dept_config.get_department_name()}")
    st.markdown("---")
    
    # File Upload
    st.header("2. Upload Schedule Files")
    st.info(f"**Required files for {dept_config.get_department_name()}:**")
    for i, req in enumerate(file_reqs, 1):
        st.markdown(f"   {i}. {req}")
    
    uploaded_files = st.file_uploader(
        "Upload your Excel files:",
        type=['xlsx', 'xls'],
        accept_multiple_files=True,
        help="Upload files in the order specified above"
    )
    
    if not uploaded_files or len(uploaded_files) < len([r for r in file_reqs if 'optional' not in r.lower()]):
        st.warning(f"Please upload at least {len([r for r in file_reqs if 'optional' not in r.lower()])} file(s)")
        return
    
    st.markdown("---")
    
    # Month/Year Configuration
    st.header("3. Configure Month & Year")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Try to detect from first filename
        detected_month, detected_year = extract_month_year_from_filename(uploaded_files[0].name)
        
        month_options = {i: calendar.month_name[i] for i in range(1, 13)}
        default_month = detected_month if detected_month else datetime.now().month
        
        selected_month = st.selectbox(
            "Select Month:",
            options=list(month_options.keys()),
            format_func=lambda x: month_options[x],
            index=default_month - 1
        )
    
    with col2:
        default_year = detected_year if detected_year else datetime.now().year
        selected_year = st.number_input(
            "Select Year:",
            min_value=2020,
            max_value=2030,
            value=default_year,
            step=1
        )
    
    if detected_month and detected_year:
        st.info(f"📅 Auto-detected: {calendar.month_name[detected_month]} {detected_year}")
    
    st.markdown("---")
    
    # Process Button
    st.header("4. Process Schedule")
    
    if st.button("🚀 Convert Schedule", type="primary", use_container_width=True):
        try:
            with st.spinner("Processing schedule files..."):
                # Save uploaded files to temp directory
                temp_dir = tempfile.mkdtemp()
                file_paths = []
                
                for uploaded_file in uploaded_files:
                    temp_path = Path(temp_dir) / uploaded_file.name
                    with open(temp_path, 'wb') as f:
                        f.write(uploaded_file.getbuffer())
                    file_paths.append(temp_path)
                
                # Validate and configure
                workbooks, config = dept_config.validate_and_configure(
                    file_paths, 
                    selected_month, 
                    selected_year
                )
                
                # Extract schedule data
                output_data = dept_config.extract_schedule_data(
                    workbooks, 
                    config, 
                    selected_month, 
                    selected_year
                )
                
                # Display results
                st.success(f"✅ Successfully generated {len(output_data)} schedule entries!")
                
                # Statistics
                expected_count = len(dept_config.debug_tracker.expected_entries)
                actual_count = len(output_data)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Expected Entries", expected_count)
                with col2:
                    st.metric("Generated Entries", actual_count)
                with col3:
                    completion = (actual_count / expected_count * 100) if expected_count > 0 else 0
                    st.metric("Completion", f"{completion:.1f}%")
                
                # Show sample data
                if output_data:
                    st.subheader("📊 Sample Entries (first 5)")
                    df_sample = pd.DataFrame(output_data[:5])
                    st.dataframe(df_sample, use_container_width=True)
                
                # Download buttons
                st.subheader("📥 Download Results")
                
                csv_data, excel_data, csv_filename, xlsx_filename = write_output_files(
                    output_data, 
                    selected_year, 
                    selected_month
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        label="📄 Download CSV",
                        data=csv_data,
                        file_name=csv_filename,
                        mime="text/csv",
                        use_container_width=True
                    )
                
                with col2:
                    st.download_button(
                        label="📊 Download Excel",
                        data=excel_data,
                        file_name=xlsx_filename,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                
                # Display warnings if any
                warnings = dept_config.debug_tracker.get_warnings_summary()
                if warnings:
                    st.markdown("---")
                    st.subheader("⚠️ Warnings & Issues")
                    
                    if 'unknown_names' in warnings:
                        with st.expander("Unknown Names Found", expanded=True):
                            st.warning(f"The following names were not found in the {dept_config.get_department_name()} employee list:")
                            for name in warnings['unknown_names']:
                                st.markdown(f"- {name}")
                    
                    if 'unknown_initials' in warnings:
                        with st.expander("Unknown Initials Found", expanded=True):
                            st.warning(f"The following initials were not found in the {dept_config.get_department_name()} employee list:")
                            for initials in warnings['unknown_initials']:
                                st.markdown(f"- {initials}")
                    
                    if 'missing_entries' in warnings:
                        missing_count = len(warnings['missing_entries'])
                        with st.expander(f"Missing Entries ({missing_count})", expanded=True):
                            st.warning(f"{missing_count} expected entries were not generated")
                            for entry in warnings['missing_entries'][:10]:  # Show first 10
                                st.markdown(f"- Day {entry['day']}: {entry['team']} ({entry['start_time']}-{entry['end_time']})")
                
        except Exception as e:
            st.error(f"❌ Error during processing: {str(e)}")
            st.exception(e)

if __name__ == "__main__":
    main()
