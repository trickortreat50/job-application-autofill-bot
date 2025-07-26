# Job Application Auto-Fill Bot

A Python application that automatically fills out job application forms to save you time during your job search. The bot fills common fields but **does not submit applications automatically** - you must review and submit manually.

## Features

- **Automatic Form Filling**: Fills personal information, work experience, education, and common questions
- **Smart Field Detection**: Uses multiple selectors to find form fields across different job sites
- **User-Friendly Interface**: Both GUI and command-line modes available
- **Safe Operation**: Never submits applications automatically - you remain in control
- **Notification System**: Alerts you when auto-fill is complete
- **Configurable**: Easy to update your personal information
- **Auto-Update System**: Automatically checks for and installs updates to dependencies and the bot

## What It Fills

### Personal Information
- First and last name
- Email address
- Phone number
- Address (street, city, state, zip code)
- LinkedIn, portfolio, and GitHub links

### Work Experience
- Company name
- Job title/position
- Start and end dates
- Job description

### Education
- Degree type
- Field of study
- University name
- Graduation year
- GPA

### Common Questions
- Why are you interested in this position?
- Salary expectations
- Availability to start
- Relocation willingness
- Work authorization status
- Notice period

## Installation

### Prerequisites
- Python 3.8 or higher (or Anaconda/Miniconda)
- Google Chrome browser
- Windows, macOS, or Linux

### Quick Start (Recommended)

1. **Download the project**:
   - Download the latest release from [GitHub Releases](https://github.com/yourusername/job-application-autofill-bot/releases)
   - Or clone the repository: `git clone https://github.com/yourusername/job-application-autofill-bot.git`

2. **Run the installer**:
   ```bash
   python install.py
   ```

3. **Start the application**:
   ```bash
   python main.py
   ```

### Option 1: Using Conda (Advanced)

1. **Clone or download this project**
   ```bash
   git clone https://github.com/yourusername/job-application-autofill-bot.git
   cd job-application-autofill-bot
   ```

2. **Create and activate conda environment**
   ```bash
   conda env create -f environment.yml
   conda activate job-auto-fill
   ```

3. **Configure your information**
   - Open `config.py` in a text editor
   - Update all the placeholder information with your actual details
   - Save the file

### Option 2: Using pip

1. **Clone or download this project**
   ```bash
   git clone https://github.com/yourusername/job-application-autofill-bot.git
   cd job-application-autofill-bot
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your information**
   - Open `config.py` in a text editor
   - Update all the placeholder information with your actual details
   - Save the file

### Option 3: Install via pip (from PyPI)

```bash
pip install job-application-autofill-bot
job-autofill  # Start the GUI
job-autofill-cli  # Start the command-line interface
```

**Note:** For detailed conda setup instructions, see `setup_conda.md`.

## Usage

### GUI Mode (Recommended)
```bash
# If using conda environment
conda activate job-auto-fill
python main.py

# If using pip
python main.py
```

1. Enter the job application URL
2. Click "Start Auto-Fill"
3. Wait for the bot to complete
4. Review the filled form
5. Submit manually

### Command Line Mode
```bash
# If using conda environment
conda activate job-auto-fill
python main.py --cli

# If using pip
python main.py --cli
```

Follow the prompts to enter the URL and start auto-fill.

### Application Tracker
```bash
python application_tracker.py
```

Track all your job applications, interviews, and follow-ups.

### Configuration Manager
```bash
python config_manager.py
```

Interactive tool to update your personal information, including multiple degrees and work experience.

### Auto-Update System
```bash
# Check for updates
python auto_updater.py check

# Install available updates
python auto_updater.py install

# Configure auto-update settings
python auto_updater.py config

# Interactive mode
python auto_updater.py
```

## Auto-Update Features

The bot includes a comprehensive auto-update system that:

- **Automatic Checks**: Checks for updates every 24 hours (configurable)
- **Dependency Updates**: Updates Python packages and conda packages
- **Safe Installation**: Creates backups before installing updates
- **User Notifications**: Shows update notifications with options to install
- **Configurable Settings**: Control update frequency, auto-install, and notifications

### Auto-Update Configuration

The auto-update system can be configured with these settings:

- **Auto-check updates**: Enable/disable automatic update checking
- **Check interval**: How often to check for updates (in hours)
- **Auto-install dependencies**: Automatically install package updates
- **Auto-install bot updates**: Automatically install bot updates (future feature)
- **Notifications**: Show update notifications
- **Backups**: Create backups before installing updates

## Configuration

Edit `config.py` to update your information:

```python
# Personal Information
PERSONAL_INFO = {
    "first_name": "Your First Name",
    "last_name": "Your Last Name",
    "email": "your.email@example.com",
    "phone": "(555) 123-4567",
    # ... more fields
}

# Work Experience
WORK_EXPERIENCE = [
    {
        "company": "Current Company",
        "position": "Software Developer",
        "start_date": "01/2022",
        "end_date": "Present",
        "description": "Developed web applications..."
    }
    # ... more jobs
]

# Education
EDUCATION = {
    "highest_degree": "Bachelor's Degree",
    "field_of_study": "Computer Science",
    "university": "Your University",
    "graduation_year": "2020"
}

# Common Answers
COMMON_ANSWERS = {
    "why_interested": "I am passionate about technology...",
    "salary_expectation": "I'm looking for a competitive salary...",
    # ... more answers
}
```

## How It Works

1. **Browser Automation**: Uses Selenium WebDriver to control Chrome browser
2. **Smart Field Detection**: Tries multiple CSS selectors to find form fields
3. **Safe Filling**: Clears existing content before filling new data
4. **Error Handling**: Gracefully handles missing fields or errors
5. **User Control**: Keeps browser open for manual review and submission
6. **Auto-Updates**: Automatically maintains the bot and dependencies

## Supported Job Sites

The bot works with most standard job application forms, including:
- LinkedIn Easy Apply
- Indeed applications
- Company career pages
- ATS (Applicant Tracking System) forms
- Custom application forms

## Safety Features

- **No Auto-Submission**: Never submits applications automatically
- **Manual Review Required**: Browser stays open for your review
- **Error Logging**: Detailed logs of what was filled and any issues
- **Graceful Failures**: Continues working even if some fields can't be found
- **Backup System**: Creates backups before installing updates
- **Safe Updates**: Validates updates before installation

## Troubleshooting

### Common Issues

1. **Fields not being filled**
   - The form may use custom field names
   - Check the status log for details
   - Some forms may require manual intervention

2. **Browser not starting**
   - Make sure Chrome is installed
   - Check that all dependencies are installed
   - Try running with `--cli` flag for command line mode

3. **Slow performance**
   - Some forms load slowly
   - The bot includes delays to ensure stability
   - Be patient during the filling process

4. **Update issues**
   - Check your internet connection
   - Ensure you have write permissions to the project directory
   - Try running the updater manually: `python auto_updater.py check`

### Getting Help

1. Check the status log in the GUI for detailed information
2. Review the console output for error messages
3. Make sure your information in `config.py` is correct
4. Test with a simple application first
5. Check for updates: `python auto_updater.py check`

## Tips for Best Results

1. **Update your information regularly** in `config.py`
2. **Test on simple applications first** before using on important ones
3. **Always review the filled form** before submitting
4. **Keep your answers professional** and tailored to each position
5. **Use the bot as a time-saver**, not a replacement for careful review
6. **Keep the bot updated** using the auto-update system
7. **Use the application tracker** to stay organized

## Legal and Ethical Considerations

- This tool is for personal use only
- Always review applications before submitting
- Respect website terms of service
- Use responsibly and ethically
- The bot does not bypass any security measures

## Contributing

Feel free to improve this project by:
- Adding support for more field types
- Improving field detection algorithms
- Enhancing the user interface
- Adding more configuration options
- Improving the auto-update system

## License

This project is for educational and personal use. Please use responsibly and in accordance with website terms of service.

## Disclaimer

This tool is provided as-is for educational purposes. Users are responsible for ensuring their use complies with applicable laws and website terms of service. The developers are not responsible for any misuse or consequences of using this tool. 