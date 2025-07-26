"""
GUI Configuration System for Job Application Auto-Fill Bot
Provides a fully functional graphical interface for updating user information.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import config
from pathlib import Path

class GUIConfigWindow:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("Configuration Manager")
        self.window.geometry("800x600")
        self.window.resizable(True, True)
        
        # Load current configuration
        self.load_current_config()
        
        # Setup UI
        self.setup_ui()
        
        # Center the window
        self.center_window()
        
    def center_window(self):
        """Center the window on screen."""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def load_current_config(self):
        """Load current configuration from config.py."""
        self.personal_info = config.PERSONAL_INFO.copy()
        self.education = config.EDUCATION.copy()
        self.work_experience = config.WORK_EXPERIENCE.copy()
        self.skills = config.SKILLS.copy()
        self.common_answers = config.COMMON_ANSWERS.copy()
    
    def setup_ui(self):
        """Set up the user interface."""
        # Main frame
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Configuration Manager", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Create tabs
        self.create_personal_info_tab()
        self.create_education_tab()
        self.create_work_experience_tab()
        self.create_skills_tab()
        self.create_common_answers_tab()
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Buttons
        ttk.Button(button_frame, text="Save Configuration", 
                  command=self.save_configuration).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Reset to Defaults", 
                  command=self.reset_to_defaults).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", 
                  command=self.window.destroy).pack(side=tk.RIGHT, padx=5)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready", foreground="gray")
        self.status_label.pack(pady=5)
    
    def create_personal_info_tab(self):
        """Create the personal information tab."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Personal Info")
        
        # Create scrollable frame
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Personal information fields
        fields = [
            ("first_name", "First Name"),
            ("last_name", "Last Name"),
            ("email", "Email"),
            ("phone", "Phone"),
            ("address", "Address"),
            ("city", "City"),
            ("state", "State"),
            ("zip_code", "Zip Code"),
            ("country", "Country"),
            ("linkedin", "LinkedIn URL"),
            ("github", "GitHub URL")
        ]
        
        self.personal_entries = {}
        
        for i, (key, label) in enumerate(fields):
            ttk.Label(scrollable_frame, text=f"{label}:").grid(row=i, column=0, sticky=tk.W, padx=5, pady=2)
            entry = ttk.Entry(scrollable_frame, width=50)
            entry.grid(row=i, column=1, sticky=(tk.W, tk.E), padx=5, pady=2)
            entry.insert(0, self.personal_info.get(key, ""))
            self.personal_entries[key] = entry
        
        # Configure grid weights
        scrollable_frame.columnconfigure(1, weight=1)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_education_tab(self):
        """Create the education tab."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Education")
        
        # Header
        header_frame = ttk.Frame(frame)
        header_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(header_frame, text="Education (Multiple Degrees Supported)", 
                 font=("Arial", 12, "bold")).pack(side=tk.LEFT)
        ttk.Button(header_frame, text="Add Degree", 
                  command=self.add_education_item).pack(side=tk.RIGHT, padx=5)
        
        # Education list frame
        self.education_frame = ttk.Frame(frame)
        self.education_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Load existing education
        self.education_widgets = []
        for edu in self.education:
            self.add_education_widget(edu)
    
    def add_education_item(self):
        """Add a new education item."""
        new_edu = {
            "degree": "",
            "field_of_study": "",
            "university": "",
            "graduation_year": "",
            "gpa": "",
            "is_highest": False
        }
        self.add_education_widget(new_edu)
    
    def add_education_widget(self, edu_data):
        """Add an education widget to the frame."""
        # Create frame for this education item
        edu_frame = ttk.LabelFrame(self.education_frame, text=f"Degree {len(self.education_widgets) + 1}")
        edu_frame.pack(fill=tk.X, pady=5, padx=5)
        
        # Fields
        fields = [
            ("degree", "Degree"),
            ("field_of_study", "Field of Study"),
            ("university", "University"),
            ("graduation_year", "Graduation Year"),
            ("gpa", "GPA")
        ]
        
        entries = {}
        for i, (key, label) in enumerate(fields):
            ttk.Label(edu_frame, text=f"{label}:").grid(row=i, column=0, sticky=tk.W, padx=5, pady=2)
            entry = ttk.Entry(edu_frame, width=40)
            entry.grid(row=i, column=1, sticky=(tk.W, tk.E), padx=5, pady=2)
            entry.insert(0, edu_data.get(key, ""))
            entries[key] = entry
        
        # Highest degree checkbox
        is_highest_var = tk.BooleanVar(value=edu_data.get("is_highest", False))
        ttk.Checkbutton(edu_frame, text="Highest Degree", 
                       variable=is_highest_var).grid(row=len(fields), column=0, columnspan=2, pady=5)
        
        # Remove button
        ttk.Button(edu_frame, text="Remove", 
                  command=lambda: self.remove_education_widget(edu_frame)).grid(row=len(fields)+1, column=1, pady=5)
        
        # Store widget data
        widget_data = {
            "frame": edu_frame,
            "entries": entries,
            "is_highest_var": is_highest_var
        }
        self.education_widgets.append(widget_data)
        
        # Configure grid weights
        edu_frame.columnconfigure(1, weight=1)
    
    def remove_education_widget(self, frame):
        """Remove an education widget."""
        frame.destroy()
        # Remove from widgets list
        self.education_widgets = [w for w in self.education_widgets if w["frame"] != frame]
    
    def create_work_experience_tab(self):
        """Create the work experience tab."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Work Experience")
        
        # Header
        header_frame = ttk.Frame(frame)
        header_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(header_frame, text="Work Experience (Most Recent First)", 
                 font=("Arial", 12, "bold")).pack(side=tk.LEFT)
        ttk.Button(header_frame, text="Add Job", 
                  command=self.add_work_item).pack(side=tk.RIGHT, padx=5)
        
        # Work experience list frame
        self.work_frame = ttk.Frame(frame)
        self.work_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Load existing work experience
        self.work_widgets = []
        for job in self.work_experience:
            self.add_work_widget(job)
    
    def add_work_item(self):
        """Add a new work experience item."""
        new_job = {
            "company": "",
            "position": "",
            "start_date": "",
            "end_date": "",
            "description": ""
        }
        self.add_work_widget(new_job)
    
    def add_work_widget(self, job_data):
        """Add a work experience widget to the frame."""
        # Create frame for this job
        job_frame = ttk.LabelFrame(self.work_frame, text=f"Job {len(self.work_widgets) + 1}")
        job_frame.pack(fill=tk.X, pady=5, padx=5)
        
        # Fields
        fields = [
            ("company", "Company"),
            ("position", "Position"),
            ("start_date", "Start Date (MM/YYYY)"),
            ("end_date", "End Date (MM/YYYY or Present)")
        ]
        
        entries = {}
        for i, (key, label) in enumerate(fields):
            ttk.Label(job_frame, text=f"{label}:").grid(row=i, column=0, sticky=tk.W, padx=5, pady=2)
            entry = ttk.Entry(job_frame, width=40)
            entry.grid(row=i, column=1, sticky=(tk.W, tk.E), padx=5, pady=2)
            entry.insert(0, job_data.get(key, ""))
            entries[key] = entry
        
        # Description (text area)
        ttk.Label(job_frame, text="Description:").grid(row=len(fields), column=0, sticky=tk.W, padx=5, pady=2)
        desc_text = tk.Text(job_frame, height=4, width=40)
        desc_text.grid(row=len(fields), column=1, sticky=(tk.W, tk.E), padx=5, pady=2)
        desc_text.insert("1.0", job_data.get("description", ""))
        
        # Remove button
        ttk.Button(job_frame, text="Remove", 
                  command=lambda: self.remove_work_widget(job_frame)).grid(row=len(fields)+1, column=1, pady=5)
        
        # Store widget data
        widget_data = {
            "frame": job_frame,
            "entries": entries,
            "desc_text": desc_text
        }
        self.work_widgets.append(widget_data)
        
        # Configure grid weights
        job_frame.columnconfigure(1, weight=1)
    
    def remove_work_widget(self, frame):
        """Remove a work experience widget."""
        frame.destroy()
        # Remove from widgets list
        self.work_widgets = [w for w in self.work_widgets if w["frame"] != frame]
    
    def create_skills_tab(self):
        """Create the skills tab."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Skills")
        
        # Header
        header_frame = ttk.Frame(frame)
        header_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(header_frame, text="Skills", font=("Arial", 12, "bold")).pack(side=tk.LEFT)
        
        # Skills entry frame
        skills_frame = ttk.Frame(frame)
        skills_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Add skill entry
        add_frame = ttk.Frame(skills_frame)
        add_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(add_frame, text="Add Skill:").pack(side=tk.LEFT, padx=5)
        self.skill_entry = ttk.Entry(add_frame, width=30)
        self.skill_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(add_frame, text="Add", command=self.add_skill).pack(side=tk.LEFT, padx=5)
        
        # Skills list
        list_frame = ttk.Frame(skills_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Listbox for skills
        self.skills_listbox = tk.Listbox(list_frame, height=15)
        self.skills_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar for listbox
        skills_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.skills_listbox.yview)
        skills_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.skills_listbox.configure(yscrollcommand=skills_scrollbar.set)
        
        # Buttons for skills
        skills_buttons_frame = ttk.Frame(skills_frame)
        skills_buttons_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(skills_buttons_frame, text="Remove Selected", 
                  command=self.remove_skill).pack(side=tk.LEFT, padx=5)
        ttk.Button(skills_buttons_frame, text="Clear All", 
                  command=self.clear_skills).pack(side=tk.LEFT, padx=5)
        
        # Load existing skills
        for skill in self.skills:
            self.skills_listbox.insert(tk.END, skill)
    
    def add_skill(self):
        """Add a skill to the list."""
        skill = self.skill_entry.get().strip()
        if skill and skill not in self.skills_listbox.get(0, tk.END):
            self.skills_listbox.insert(tk.END, skill)
            self.skill_entry.delete(0, tk.END)
    
    def remove_skill(self):
        """Remove selected skill from the list."""
        selection = self.skills_listbox.curselection()
        if selection:
            self.skills_listbox.delete(selection)
    
    def clear_skills(self):
        """Clear all skills."""
        if messagebox.askyesno("Clear Skills", "Are you sure you want to clear all skills?"):
            self.skills_listbox.delete(0, tk.END)
    
    def create_common_answers_tab(self):
        """Create the common answers tab."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Common Answers")
        
        # Create scrollable frame
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Common answers fields
        fields = [
            ("why_interested", "Why are you interested in this position?"),
            ("salary_expectation", "What are your salary expectations?"),
            ("availability", "When are you available to start?"),
            ("relocation", "Are you open to relocation?"),
            ("work_authorization", "What is your work authorization status?"),
            ("notice_period", "What is your notice period?")
        ]
        
        self.answers_entries = {}
        
        for i, (key, label) in enumerate(fields):
            ttk.Label(scrollable_frame, text=f"{label}:").grid(row=i, column=0, sticky=tk.W, padx=5, pady=5)
            text_widget = tk.Text(scrollable_frame, height=4, width=60)
            text_widget.grid(row=i, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
            text_widget.insert("1.0", self.common_answers.get(key, ""))
            self.answers_entries[key] = text_widget
        
        # Configure grid weights
        scrollable_frame.columnconfigure(1, weight=1)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def collect_personal_info(self):
        """Collect personal information from the form."""
        personal_info = {}
        for key, entry in self.personal_entries.items():
            personal_info[key] = entry.get().strip()
        return personal_info
    
    def collect_education(self):
        """Collect education information from the form."""
        education = []
        for widget in self.education_widgets:
            edu_data = {}
            for key, entry in widget["entries"].items():
                edu_data[key] = entry.get().strip()
            edu_data["is_highest"] = widget["is_highest_var"].get()
            education.append(edu_data)
        return education
    
    def collect_work_experience(self):
        """Collect work experience from the form."""
        work_experience = []
        for widget in self.work_widgets:
            job_data = {}
            for key, entry in widget["entries"].items():
                job_data[key] = entry.get().strip()
            job_data["description"] = widget["desc_text"].get("1.0", tk.END).strip()
            work_experience.append(job_data)
        return work_experience
    
    def collect_skills(self):
        """Collect skills from the form."""
        skills = list(self.skills_listbox.get(0, tk.END))
        return skills
    
    def collect_common_answers(self):
        """Collect common answers from the form."""
        common_answers = {}
        for key, text_widget in self.answers_entries.items():
            common_answers[key] = text_widget.get("1.0", tk.END).strip()
        return common_answers
    
    def save_configuration(self):
        """Save the configuration to config.py."""
        try:
            # Collect all data from the form
            personal_info = self.collect_personal_info()
            education = self.collect_education()
            work_experience = self.collect_work_experience()
            skills = self.collect_skills()
            common_answers = self.collect_common_answers()
            
            # Generate config.py content
            config_content = f'''"""
Configuration file for storing personal information used in job applications.
Edit this file with your actual information.
"""

# Personal Information
PERSONAL_INFO = {json.dumps(personal_info, indent=4)}

# Education Information (can have multiple degrees)
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
            
            # Update status
            self.status_label.config(text="Configuration saved successfully!", foreground="green")
            
            # Show success message
            messagebox.showinfo("Success", "Configuration has been saved successfully!")
            
            # Close window
            self.window.destroy()
            
        except Exception as e:
            error_msg = f"Error saving configuration: {str(e)}"
            self.status_label.config(text=error_msg, foreground="red")
            messagebox.showerror("Error", error_msg)
    
    def reset_to_defaults(self):
        """Reset configuration to default values."""
        if messagebox.askyesno("Reset Configuration", 
                              "Are you sure you want to reset to default values?\n"
                              "This will clear all your current information."):
            # Reset to default values
            self.personal_info = {
                "first_name": "Your First Name",
                "last_name": "Your Last Name",
                "email": "your.email@example.com",
                "phone": "(555) 123-4567",
                "address": "123 Main Street",
                "city": "Your City",
                "state": "Your State",
                "zip_code": "12345",
                "country": "United States",
                "linkedin": "https://linkedin.com/in/yourprofile",
                "github": "https://github.com/yourusername"
            }
            
            self.education = [{
                "degree": "Bachelor's Degree",
                "field_of_study": "Computer Science",
                "university": "Your University",
                "graduation_year": "2020",
                "gpa": "3.8",
                "is_highest": True
            }]
            
            self.work_experience = [{
                "company": "Current Company",
                "position": "Software Developer",
                "start_date": "01/2022",
                "end_date": "Present",
                "description": "Developed web applications using Python and JavaScript."
            }]
            
            self.skills = ["Python", "JavaScript", "HTML", "CSS", "SQL", "Git"]
            
            self.common_answers = {
                "why_interested": "I am passionate about technology and innovation.",
                "salary_expectation": "I'm looking for a competitive salary.",
                "availability": "I am available to start within 2 weeks.",
                "relocation": "I am open to relocation for the right opportunity.",
                "work_authorization": "I am authorized to work in the United States.",
                "notice_period": "I can provide 2 weeks notice to my current employer."
            }
            
            # Reload the UI
            self.window.destroy()
            self.__init__(self.parent)

def main():
    """Test the GUI configuration window."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    config_window = GUIConfigWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main() 