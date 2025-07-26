"""
Configuration Manager for Job Application Auto-Fill Bot
Provides interactive prompts for updating user information.
"""

import json
import os
from pathlib import Path
import config

class ConfigManager:
    def __init__(self):
        self.config_file = Path("config.py")
        
    def update_personal_info(self):
        """Update personal information interactively."""
        print("\n" + "="*50)
        print("PERSONAL INFORMATION")
        print("="*50)
        
        personal_info = config.PERSONAL_INFO.copy()
        
        print("\nCurrent personal information:")
        for key, value in personal_info.items():
            print(f"  {key}: {value}")
        
        print("\nUpdate personal information (press Enter to keep current value):")
        
        # Basic info
        personal_info["first_name"] = input(f"First Name ({personal_info['first_name']}): ").strip() or personal_info["first_name"]
        personal_info["last_name"] = input(f"Last Name ({personal_info['last_name']}): ").strip() or personal_info["last_name"]
        personal_info["email"] = input(f"Email ({personal_info['email']}): ").strip() or personal_info["email"]
        personal_info["phone"] = input(f"Phone ({personal_info['phone']}): ").strip() or personal_info["phone"]
        
        # Address
        personal_info["address"] = input(f"Address ({personal_info['address']}): ").strip() or personal_info["address"]
        personal_info["city"] = input(f"City ({personal_info['city']}): ").strip() or personal_info["city"]
        personal_info["state"] = input(f"State ({personal_info['state']}): ").strip() or personal_info["state"]
        personal_info["zip_code"] = input(f"Zip Code ({personal_info['zip_code']}): ").strip() or personal_info["zip_code"]
        personal_info["country"] = input(f"Country ({personal_info['country']}): ").strip() or personal_info["country"]
        
        # Online profiles
        personal_info["linkedin"] = input(f"LinkedIn URL ({personal_info['linkedin']}): ").strip() or personal_info["linkedin"]

        personal_info["github"] = input(f"GitHub URL ({personal_info['github']}): ").strip() or personal_info["github"]
        
        return personal_info
    
    def update_education(self):
        """Update education information interactively."""
        print("\n" + "="*50)
        print("EDUCATION INFORMATION")
        print("="*50)
        
        education_list = config.EDUCATION.copy()
        
        print(f"\nYou currently have {len(education_list)} degree(s):")
        for i, edu in enumerate(education_list, 1):
            print(f"  {i}. {edu['degree']} in {edu['field_of_study']} from {edu['university']} ({edu['graduation_year']})")
        
        while True:
            print("\nEducation options:")
            print("1. Add new degree")
            print("2. Edit existing degree")
            print("3. Remove degree")
            print("4. Mark highest degree")
            print("5. Done with education")
            
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == "1":
                education_list.append(self.add_degree())
            elif choice == "2":
                self.edit_degree(education_list)
            elif choice == "3":
                self.remove_degree(education_list)
            elif choice == "4":
                self.mark_highest_degree(education_list)
            elif choice == "5":
                break
            else:
                print("Invalid choice!")
        
        return education_list
    
    def add_degree(self):
        """Add a new degree."""
        print("\nAdding new degree:")
        
        degree = input("Degree (e.g., Bachelor's, Master's, PhD): ").strip()
        field_of_study = input("Field of Study: ").strip()
        university = input("University: ").strip()
        graduation_year = input("Graduation Year: ").strip()
        gpa = input("GPA (optional): ").strip() or "N/A"
        is_highest = input("Is this your highest degree? (y/n): ").strip().lower() == "y"
        
        return {
            "degree": degree,
            "field_of_study": field_of_study,
            "university": university,
            "graduation_year": graduation_year,
            "gpa": gpa,
            "is_highest": is_highest
        }
    
    def edit_degree(self, education_list):
        """Edit an existing degree."""
        if not education_list:
            print("No degrees to edit!")
            return
        
        print("\nSelect degree to edit:")
        for i, edu in enumerate(education_list, 1):
            print(f"  {i}. {edu['degree']} in {edu['field_of_study']} from {edu['university']}")
        
        try:
            index = int(input("Enter degree number: ").strip()) - 1
            if 0 <= index < len(education_list):
                edu = education_list[index]
                print(f"\nEditing: {edu['degree']} in {edu['field_of_study']}")
                
                edu["degree"] = input(f"Degree ({edu['degree']}): ").strip() or edu["degree"]
                edu["field_of_study"] = input(f"Field of Study ({edu['field_of_study']}): ").strip() or edu["field_of_study"]
                edu["university"] = input(f"University ({edu['university']}): ").strip() or edu["university"]
                edu["graduation_year"] = input(f"Graduation Year ({edu['graduation_year']}): ").strip() or edu["graduation_year"]
                edu["gpa"] = input(f"GPA ({edu['gpa']}): ").strip() or edu["gpa"]
                edu["is_highest"] = input(f"Is highest degree? ({edu['is_highest']}) (y/n): ").strip().lower() == "y"
            else:
                print("Invalid degree number!")
        except ValueError:
            print("Invalid input!")
    
    def remove_degree(self, education_list):
        """Remove a degree."""
        if not education_list:
            print("No degrees to remove!")
            return
        
        print("\nSelect degree to remove:")
        for i, edu in enumerate(education_list, 1):
            print(f"  {i}. {edu['degree']} in {edu['field_of_study']} from {edu['university']}")
        
        try:
            index = int(input("Enter degree number: ").strip()) - 1
            if 0 <= index < len(education_list):
                removed = education_list.pop(index)
                print(f"Removed: {removed['degree']} in {removed['field_of_study']}")
            else:
                print("Invalid degree number!")
        except ValueError:
            print("Invalid input!")
    
    def mark_highest_degree(self, education_list):
        """Mark the highest degree."""
        if not education_list:
            print("No degrees to mark!")
            return
        
        # Clear all highest degree flags
        for edu in education_list:
            edu["is_highest"] = False
        
        print("\nSelect your highest degree:")
        for i, edu in enumerate(education_list, 1):
            print(f"  {i}. {edu['degree']} in {edu['field_of_study']} from {edu['university']}")
        
        try:
            index = int(input("Enter degree number: ").strip()) - 1
            if 0 <= index < len(education_list):
                education_list[index]["is_highest"] = True
                print(f"Marked as highest: {education_list[index]['degree']}")
            else:
                print("Invalid degree number!")
        except ValueError:
            print("Invalid input!")
    
    def update_work_experience(self):
        """Update work experience interactively."""
        print("\n" + "="*50)
        print("WORK EXPERIENCE")
        print("="*50)
        
        work_experience = config.WORK_EXPERIENCE.copy()
        
        print(f"\nYou currently have {len(work_experience)} job(s):")
        for i, job in enumerate(work_experience, 1):
            print(f"  {i}. {job['position']} at {job['company']} ({job['start_date']} - {job['end_date']})")
        
        while True:
            print("\nWork experience options:")
            print("1. Add new job")
            print("2. Edit existing job")
            print("3. Remove job")
            print("4. Reorder jobs")
            print("5. Done with work experience")
            
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == "1":
                work_experience.append(self.add_job())
            elif choice == "2":
                self.edit_job(work_experience)
            elif choice == "3":
                self.remove_job(work_experience)
            elif choice == "4":
                self.reorder_jobs(work_experience)
            elif choice == "5":
                break
            else:
                print("Invalid choice!")
        
        return work_experience
    
    def add_job(self):
        """Add a new job."""
        print("\nAdding new job:")
        
        company = input("Company Name: ").strip()
        position = input("Position/Title: ").strip()
        start_date = input("Start Date (MM/YYYY): ").strip()
        end_date = input("End Date (MM/YYYY or 'Present'): ").strip()
        description = input("Job Description: ").strip()
        
        return {
            "company": company,
            "position": position,
            "start_date": start_date,
            "end_date": end_date,
            "description": description
        }
    
    def edit_job(self, work_experience):
        """Edit an existing job."""
        if not work_experience:
            print("No jobs to edit!")
            return
        
        print("\nSelect job to edit:")
        for i, job in enumerate(work_experience, 1):
            print(f"  {i}. {job['position']} at {job['company']}")
        
        try:
            index = int(input("Enter job number: ").strip()) - 1
            if 0 <= index < len(work_experience):
                job = work_experience[index]
                print(f"\nEditing: {job['position']} at {job['company']}")
                
                job["company"] = input(f"Company ({job['company']}): ").strip() or job["company"]
                job["position"] = input(f"Position ({job['position']}): ").strip() or job["position"]
                job["start_date"] = input(f"Start Date ({job['start_date']}): ").strip() or job["start_date"]
                job["end_date"] = input(f"End Date ({job['end_date']}): ").strip() or job["end_date"]
                job["description"] = input(f"Description ({job['description'][:50]}...): ").strip() or job["description"]
            else:
                print("Invalid job number!")
        except ValueError:
            print("Invalid input!")
    
    def remove_job(self, work_experience):
        """Remove a job."""
        if not work_experience:
            print("No jobs to remove!")
            return
        
        print("\nSelect job to remove:")
        for i, job in enumerate(work_experience, 1):
            print(f"  {i}. {job['position']} at {job['company']}")
        
        try:
            index = int(input("Enter job number: ").strip()) - 1
            if 0 <= index < len(work_experience):
                removed = work_experience.pop(index)
                print(f"Removed: {removed['position']} at {removed['company']}")
            else:
                print("Invalid job number!")
        except ValueError:
            print("Invalid input!")
    
    def reorder_jobs(self, work_experience):
        """Reorder jobs (most recent first)."""
        if len(work_experience) < 2:
            print("Need at least 2 jobs to reorder!")
            return
        
        print("\nCurrent order (most recent first):")
        for i, job in enumerate(work_experience, 1):
            print(f"  {i}. {job['position']} at {job['company']}")
        
        print("\nTo reorder, enter the new order (e.g., '3 1 2' to move job 3 to position 1):")
        try:
            new_order = input("New order: ").strip().split()
            new_order = [int(x) - 1 for x in new_order]
            
            if len(new_order) == len(work_experience) and all(0 <= x < len(work_experience) for x in new_order):
                work_experience[:] = [work_experience[i] for i in new_order]
                print("Jobs reordered successfully!")
            else:
                print("Invalid order!")
        except (ValueError, IndexError):
            print("Invalid input!")
    
    def update_skills(self):
        """Update skills interactively."""
        print("\n" + "="*50)
        print("SKILLS")
        print("="*50)
        
        skills = config.SKILLS.copy()
        
        print(f"\nCurrent skills ({len(skills)}):")
        for i, skill in enumerate(skills, 1):
            print(f"  {i}. {skill}")
        
        while True:
            print("\nSkills options:")
            print("1. Add skill")
            print("2. Remove skill")
            print("3. Edit skill")
            print("4. Clear all skills")
            print("5. Done with skills")
            
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == "1":
                skill = input("Enter new skill: ").strip()
                if skill:
                    skills.append(skill)
                    print(f"Added: {skill}")
            elif choice == "2":
                self.remove_skill(skills)
            elif choice == "3":
                self.edit_skill(skills)
            elif choice == "4":
                if input("Clear all skills? (y/n): ").strip().lower() == "y":
                    skills.clear()
                    print("All skills cleared!")
            elif choice == "5":
                break
            else:
                print("Invalid choice!")
        
        return skills
    
    def remove_skill(self, skills):
        """Remove a skill."""
        if not skills:
            print("No skills to remove!")
            return
        
        print("\nSelect skill to remove:")
        for i, skill in enumerate(skills, 1):
            print(f"  {i}. {skill}")
        
        try:
            index = int(input("Enter skill number: ").strip()) - 1
            if 0 <= index < len(skills):
                removed = skills.pop(index)
                print(f"Removed: {removed}")
            else:
                print("Invalid skill number!")
        except ValueError:
            print("Invalid input!")
    
    def edit_skill(self, skills):
        """Edit a skill."""
        if not skills:
            print("No skills to edit!")
            return
        
        print("\nSelect skill to edit:")
        for i, skill in enumerate(skills, 1):
            print(f"  {i}. {skill}")
        
        try:
            index = int(input("Enter skill number: ").strip()) - 1
            if 0 <= index < len(skills):
                new_skill = input(f"New skill name ({skills[index]}): ").strip()
                if new_skill:
                    skills[index] = new_skill
                    print(f"Updated: {new_skill}")
            else:
                print("Invalid skill number!")
        except ValueError:
            print("Invalid input!")
    
    def update_common_answers(self):
        """Update common answers interactively."""
        print("\n" + "="*50)
        print("COMMON APPLICATION ANSWERS")
        print("="*50)
        
        common_answers = config.COMMON_ANSWERS.copy()
        
        print("\nCurrent answers:")
        for key, value in common_answers.items():
            print(f"  {key}: {value[:50]}...")
        
        print("\nUpdate answers (press Enter to keep current value):")
        
        common_answers["why_interested"] = input(f"Why interested ({common_answers['why_interested'][:50]}...): ").strip() or common_answers["why_interested"]
        common_answers["salary_expectation"] = input(f"Salary expectation ({common_answers['salary_expectation'][:50]}...): ").strip() or common_answers["salary_expectation"]
        common_answers["availability"] = input(f"Availability ({common_answers['availability'][:50]}...): ").strip() or common_answers["availability"]
        common_answers["relocation"] = input(f"Relocation ({common_answers['relocation']}): ").strip() or common_answers["relocation"]
        common_answers["work_authorization"] = input(f"Work authorization ({common_answers['work_authorization']}): ").strip() or common_answers["work_authorization"]
        common_answers["notice_period"] = input(f"Notice period ({common_answers['notice_period']}): ").strip() or common_answers["notice_period"]
        
        return common_answers
    
    def save_config(self, personal_info, education, work_experience, skills, common_answers):
        """Save the updated configuration to config.py."""
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
        
        try:
            with open(self.config_file, 'w') as f:
                f.write(config_content)
            print(f"\n✅ Configuration saved to {self.config_file}")
            return True
        except Exception as e:
            print(f"❌ Error saving configuration: {e}")
            return False
    
    def run_interactive_update(self):
        """Run the complete interactive update process."""
        print("🔧 CONFIGURATION MANAGER")
        print("="*50)
        print("This will help you update your information interactively.")
        
        while True:
            print("\nWhat would you like to update?")
            print("1. Personal Information")
            print("2. Education (multiple degrees)")
            print("3. Work Experience")
            print("4. Skills")
            print("5. Common Answers")
            print("6. Update Everything")
            print("7. Exit")
            
            choice = input("\nEnter your choice (1-7): ").strip()
            
            if choice == "1":
                personal_info = self.update_personal_info()
                self.save_config(personal_info, config.EDUCATION, config.WORK_EXPERIENCE, config.SKILLS, config.COMMON_ANSWERS)
            elif choice == "2":
                education = self.update_education()
                self.save_config(config.PERSONAL_INFO, education, config.WORK_EXPERIENCE, config.SKILLS, config.COMMON_ANSWERS)
            elif choice == "3":
                work_experience = self.update_work_experience()
                self.save_config(config.PERSONAL_INFO, config.EDUCATION, work_experience, config.SKILLS, config.COMMON_ANSWERS)
            elif choice == "4":
                skills = self.update_skills()
                self.save_config(config.PERSONAL_INFO, config.EDUCATION, config.WORK_EXPERIENCE, skills, config.COMMON_ANSWERS)
            elif choice == "5":
                common_answers = self.update_common_answers()
                self.save_config(config.PERSONAL_INFO, config.EDUCATION, config.WORK_EXPERIENCE, config.SKILLS, common_answers)
            elif choice == "6":
                print("\nUpdating everything...")
                personal_info = self.update_personal_info()
                education = self.update_education()
                work_experience = self.update_work_experience()
                skills = self.update_skills()
                common_answers = self.update_common_answers()
                self.save_config(personal_info, education, work_experience, skills, common_answers)
            elif choice == "7":
                print("Goodbye!")
                break
            else:
                print("Invalid choice!")

def main():
    """Main function for configuration manager."""
    manager = ConfigManager()
    manager.run_interactive_update()

if __name__ == "__main__":
    main() 