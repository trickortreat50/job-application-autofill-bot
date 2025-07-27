"""
Configuration file for Job Application Auto-Fill Bot
Contains default settings and user information.
"""

# Browser settings
BROWSER_SETTINGS = {
    "headless": False,
    "implicit_wait": 10,
    "page_load_timeout": 30
}

# Default personal information
PERSONAL_INFO = {
    "first_name": "",
    "last_name": "",
    "email": "",
    "phone": "",
    "address": "",
    "city": "",
    "state": "",
    "zip_code": "",
    "country": "United States",
    "linkedin": "",
    "github": ""
}

# Default education
EDUCATION = []

# Default work experience
WORK_EXPERIENCE = []

# Default skills
SKILLS = []

# Default common answers
COMMON_ANSWERS = {
    "why_join": "I am excited about the opportunity to contribute to [Company Name] and grow my career in [field/industry]. I believe my skills and experience align well with the role and I am eager to make a positive impact.",
    "salary_expectations": "I am open to discussing a competitive salary based on the role requirements and my experience.",
    "availability": "I am available to start immediately and can work flexible hours as needed.",
    "relocation": "I am open to relocation for the right opportunity.",
    "remote_work": "I am comfortable with both remote and in-office work arrangements."
} 