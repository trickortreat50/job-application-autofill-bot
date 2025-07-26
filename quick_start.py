"""
Quick Start Script for Job Application Auto-Fill Bot
Helps you set up your configuration and test the bot quickly.
"""

import os
import sys
import json
from pathlib import Path

def check_conda_environment():
    """Check if conda environment is activated."""
    conda_env = os.environ.get('CONDA_DEFAULT_ENV')
    if conda_env and conda_env != 'base':
        print(f"✅ Conda environment '{conda_env}' is activated")
        return True
    else:
        print("⚠️  Conda environment not detected")
        print("   Run: conda activate job-auto-fill")
        return False

def check_dependencies():
    """Check if required packages are installed."""
    required_packages = ['selenium', 'webdriver-manager']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Install them with: pip install -r requirements.txt")
        return False
    
    return True

def check_config():
    """Check if config.py has been updated with real information."""
    try:
        import config
        
        # Check if personal info still has placeholder values
        placeholder_indicators = [
            "Your First Name", "Your Last Name", "your.email@example.com",
            "Your City", "Your State", "Your University"
        ]
        
        has_placeholders = False
        for indicator in placeholder_indicators:
            if indicator in str(config.PERSONAL_INFO.values()):
                has_placeholders = True
                break
        
        if has_placeholders:
            print("❌ config.py still contains placeholder information")
            print("   Please edit config.py with your actual details")
            return False
        else:
            print("✅ config.py has been configured with your information")
            return True
            
    except ImportError:
        print("❌ config.py not found")
        return False

def create_sample_config():
    """Create a sample configuration with prompts."""
    print("\n" + "="*50)
    print("SETTING UP YOUR CONFIGURATION")
    print("="*50)
    
    print("\nPlease provide your information (press Enter to skip any field):")
    
    personal_info = {}
    
    # Basic personal info
    personal_info["first_name"] = input("First Name: ").strip() or "Your First Name"
    personal_info["last_name"] = input("Last Name: ").strip() or "Your Last Name"
    personal_info["email"] = input("Email: ").strip() or "your.email@example.com"
    personal_info["phone"] = input("Phone: ").strip() or "(555) 123-4567"
    
    # Address
    personal_info["address"] = input("Address: ").strip() or "123 Main Street"
    personal_info["city"] = input("City: ").strip() or "Your City"
    personal_info["state"] = input("State: ").strip() or "Your State"
    personal_info["zip_code"] = input("Zip Code: ").strip() or "12345"
    personal_info["country"] = input("Country: ").strip() or "United States"
    
    # Online profiles
    personal_info["linkedin"] = input("LinkedIn URL: ").strip() or "https://linkedin.com/in/yourprofile"
    
    personal_info["github"] = input("GitHub URL: ").strip() or "https://github.com/yourusername"
    
    # Education
    education = {}
    education["highest_degree"] = input("Highest Degree: ").strip() or "Bachelor's Degree"
    education["field_of_study"] = input("Field of Study: ").strip() or "Computer Science"
    education["university"] = input("University: ").strip() or "Your University"
    education["graduation_year"] = input("Graduation Year: ").strip() or "2020"
    education["gpa"] = input("GPA (optional): ").strip() or "3.8"
    
    # Work experience
    print("\nWork Experience (most recent job):")
    work_experience = []
    
    company = input("Company Name: ").strip()
    if company:
        position = input("Position/Title: ").strip() or "Software Developer"
        start_date = input("Start Date (MM/YYYY): ").strip() or "01/2022"
        end_date = input("End Date (MM/YYYY or 'Present'): ").strip() or "Present"
        description = input("Job Description: ").strip() or "Developed web applications using Python and JavaScript."
        
        work_experience.append({
            "company": company,
            "position": position,
            "start_date": start_date,
            "end_date": end_date,
            "description": description
        })
    
    # Skills
    print("\nSkills (comma-separated):")
    skills_input = input("Skills: ").strip()
    if skills_input:
        skills = [skill.strip() for skill in skills_input.split(",")]
    else:
        skills = ["Python", "JavaScript", "HTML", "CSS", "SQL", "Git"]
    
    # Common answers
    print("\nCommon Application Answers:")
    common_answers = {}
    common_answers["why_interested"] = input("Why are you interested in this position? (or press Enter for default): ").strip()
    if not common_answers["why_interested"]:
        common_answers["why_interested"] = "I am passionate about technology and innovation. I believe my skills and experience align well with this role."
    
    common_answers["salary_expectation"] = input("Salary expectations? (or press Enter for default): ").strip()
    if not common_answers["salary_expectation"]:
        common_answers["salary_expectation"] = "I'm looking for a competitive salary commensurate with my experience."
    
    common_answers["availability"] = input("When are you available to start? (or press Enter for default): ").strip()
    if not common_answers["availability"]:
        common_answers["availability"] = "I am available to start within 2 weeks of receiving an offer."
    
    # Generate config.py content
    config_content = f'''"""
Configuration file for storing personal information used in job applications.
Edit this file with your actual information.
"""

# Personal Information
PERSONAL_INFO = {json.dumps(personal_info, indent=4)}

# Education Information
EDUCATION = {json.dumps(education, indent=4)}

# Work Experience (most recent first)
WORK_EXPERIENCE = {json.dumps(work_experience, indent=4)}

# Skills
SKILLS = {json.dumps(skills, indent=4)}

# Common Application Questions and Answers
COMMON_ANSWERS = {json.dumps(common_answers, indent=4)}

# Browser Settings
BROWSER_SETTINGS = {{
    "headless": False,  # Set to True to run browser in background
    "implicit_wait": 10,  # Seconds to wait for elements
    "page_load_timeout": 30  # Seconds to wait for page load
}}
'''
    
    # Write to config.py
    with open("config.py", "w") as f:
        f.write(config_content)
    
    print(f"\n✅ Configuration saved to config.py")
    print("You can edit this file anytime to update your information.")

def test_bot():
    """Test the bot with a sample URL."""
    print("\n" + "="*50)
    print("TESTING THE BOT")
    print("="*50)
    
    print("\nTo test the bot, you can:")
    print("1. Use a real job application URL")
    print("2. Use a test form (like Google Forms)")
    print("3. Skip testing for now")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        url = input("Enter job application URL: ").strip()
        if url:
            print(f"\nStarting test with: {url}")
            try:
                from form_filler import JobApplicationFiller
                filler = JobApplicationFiller()
                fields_filled = filler.auto_fill_application(url)
                print(f"✅ Test completed! Filled {fields_filled} fields.")
                print("Please review the form and close the browser when done.")
            except Exception as e:
                print(f"❌ Test failed: {e}")
    
    elif choice == "2":
        print("\nYou can create a test form at: https://forms.google.com")
        print("Then use the bot to fill it out as a test.")
    
    else:
        print("Skipping test. You can test later by running: python main.py")

    def show_next_steps():
        """Show what to do next."""
        print("\n" + "="*50)
        print("NEXT STEPS")
        print("="*50)
        
        print("\n1. 🚀 Start using the bot:")
        print("   python main.py")
        
        print("\n2. 📊 Track your applications:")
        print("   python application_tracker.py")
        
        print("\n3. 🔧 Update your information anytime:")
        print("   python config_manager.py - Interactive configuration")
        print("   Edit config.py - Manual editing")
        
        print("\n4. 🔄 Auto-update system:")
        print("   python auto_updater.py - Check for updates")
        print("   python auto_updater.py config - Configure auto-update")
        
        print("\n5. 📚 Read the documentation:")
        print("   README.md - Complete usage guide")
        print("   setup_conda.md - Conda environment setup")
        
        print("\n6. 🎯 Tips for success:")
        print("   - Test on simple applications first")
        print("   - Always review filled forms before submitting")
        print("   - Keep your information in config.py up to date")
        print("   - Use the application tracker to stay organized")
        print("   - The bot will automatically check for updates")

def main():
    """Main quick start function."""
    print("🚀 JOB APPLICATION AUTO-FILL BOT - QUICK START")
    print("="*50)
    
    # Check environment
    env_ok = check_conda_environment()
    deps_ok = check_dependencies()
    config_ok = check_config()
    
    print("\n" + "="*50)
    print("SETUP STATUS")
    print("="*50)
    
    if not env_ok:
        print("❌ Please activate the conda environment first")
        print("   conda activate job-auto-fill")
        return
    
    if not deps_ok:
        print("❌ Please install missing dependencies")
        print("   pip install -r requirements.txt")
        return
    
    if not config_ok:
        print("❌ Configuration needs to be set up")
        setup_choice = input("Would you like to set up your configuration now? (y/n): ").strip().lower()
        if setup_choice == 'y':
            create_sample_config()
            config_ok = True
        else:
            print("Please edit config.py manually before using the bot.")
            return
    
    if env_ok and deps_ok and config_ok:
        print("✅ Everything is set up correctly!")
        
        test_choice = input("\nWould you like to test the bot now? (y/n): ").strip().lower()
        if test_choice == 'y':
            test_bot()
    
    show_next_steps()

if __name__ == "__main__":
    main() 