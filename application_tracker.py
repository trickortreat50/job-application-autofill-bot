"""
Job Application Tracker
Helps you keep track of all your job applications, interviews, and follow-ups.
"""

import json
import datetime
from pathlib import Path
from typing import Dict, List, Optional

class ApplicationTracker:
    def __init__(self, data_file: str = "applications.json"):
        self.data_file = Path(data_file)
        self.applications = self.load_applications()
    
    def load_applications(self) -> List[Dict]:
        """Load applications from JSON file."""
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("Warning: Corrupted applications file. Starting fresh.")
                return []
        return []
    
    def save_applications(self):
        """Save applications to JSON file."""
        with open(self.data_file, 'w') as f:
            json.dump(self.applications, f, indent=2, default=str)
    
    def add_application(self, company: str, position: str, url: str = "", 
                       applied_date: str = None, status: str = "Applied") -> Dict:
        """Add a new job application."""
        if applied_date is None:
            applied_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        application = {
            "id": len(self.applications) + 1,
            "company": company,
            "position": position,
            "url": url,
            "applied_date": applied_date,
            "status": status,
            "notes": "",
            "follow_up_date": None,
            "interviews": [],
            "created_at": datetime.datetime.now().isoformat()
        }
        
        self.applications.append(application)
        self.save_applications()
        return application
    
    def update_status(self, app_id: int, status: str, notes: str = ""):
        """Update application status."""
        for app in self.applications:
            if app["id"] == app_id:
                app["status"] = status
                if notes:
                    app["notes"] = notes
                app["updated_at"] = datetime.datetime.now().isoformat()
                break
        self.save_applications()
    
    def add_interview(self, app_id: int, interview_date: str, 
                     interview_type: str = "Phone", notes: str = ""):
        """Add an interview to an application."""
        for app in self.applications:
            if app["id"] == app_id:
                interview = {
                    "date": interview_date,
                    "type": interview_type,
                    "notes": notes,
                    "created_at": datetime.datetime.now().isoformat()
                }
                app["interviews"].append(interview)
                app["status"] = f"Interview - {interview_type}"
                break
        self.save_applications()
    
    def set_follow_up(self, app_id: int, follow_up_date: str):
        """Set a follow-up date for an application."""
        for app in self.applications:
            if app["id"] == app_id:
                app["follow_up_date"] = follow_up_date
                break
        self.save_applications()
    
    def get_applications_by_status(self, status: str = None) -> List[Dict]:
        """Get applications filtered by status."""
        if status is None:
            return self.applications
        return [app for app in self.applications if app["status"] == status]
    
    def get_applications_needing_follow_up(self) -> List[Dict]:
        """Get applications that need follow-up."""
        today = datetime.datetime.now().date()
        follow_ups = []
        
        for app in self.applications:
            if app["follow_up_date"]:
                try:
                    follow_up_date = datetime.datetime.strptime(
                        app["follow_up_date"], "%Y-%m-%d"
                    ).date()
                    if follow_up_date <= today:
                        follow_ups.append(app)
                except ValueError:
                    continue
        
        return follow_ups
    
    def get_statistics(self) -> Dict:
        """Get application statistics."""
        total = len(self.applications)
        if total == 0:
            return {"total": 0, "status_counts": {}, "response_rate": 0}
        
        status_counts = {}
        for app in self.applications:
            status = app["status"]
            status_counts[status] = status_counts.get(status, 0) + 1
        
        # Calculate response rate (any status other than "Applied")
        responses = sum(1 for app in self.applications if app["status"] != "Applied")
        response_rate = (responses / total) * 100 if total > 0 else 0
        
        return {
            "total": total,
            "status_counts": status_counts,
            "response_rate": round(response_rate, 1)
        }
    
    def export_to_csv(self, filename: str = "applications.csv"):
        """Export applications to CSV file."""
        import csv
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            if not self.applications:
                return
            
            # Get all possible fields
            fieldnames = set()
            for app in self.applications:
                fieldnames.update(app.keys())
            
            writer = csv.DictWriter(f, fieldnames=sorted(fieldnames))
            writer.writeheader()
            
            for app in self.applications:
                # Flatten interviews list
                app_copy = app.copy()
                if app_copy.get("interviews"):
                    app_copy["interviews"] = "; ".join([
                        f"{i['date']} - {i['type']}" for i in app_copy["interviews"]
                    ])
                writer.writerow(app_copy)
        
        print(f"Applications exported to {filename}")
    
    def print_summary(self):
        """Print a summary of all applications."""
        stats = self.get_statistics()
        
        print("\n" + "="*50)
        print("JOB APPLICATION SUMMARY")
        print("="*50)
        print(f"Total Applications: {stats['total']}")
        print(f"Response Rate: {stats['response_rate']}%")
        print("\nStatus Breakdown:")
        
        for status, count in stats['status_counts'].items():
            percentage = (count / stats['total']) * 100 if stats['total'] > 0 else 0
            print(f"  {status}: {count} ({percentage:.1f}%)")
        
        # Show recent applications
        recent_apps = sorted(self.applications, 
                           key=lambda x: x.get('applied_date', ''), 
                           reverse=True)[:5]
        
        if recent_apps:
            print(f"\nRecent Applications (Last 5):")
            for app in recent_apps:
                print(f"  {app['company']} - {app['position']} ({app['status']})")
        
        # Show follow-ups needed
        follow_ups = self.get_applications_needing_follow_up()
        if follow_ups:
            print(f"\nFollow-ups Needed:")
            for app in follow_ups:
                print(f"  {app['company']} - {app['position']} (Due: {app['follow_up_date']})")
        
        print("="*50)

def main():
    """Simple command-line interface for the tracker."""
    tracker = ApplicationTracker()
    
    while True:
        print("\nJob Application Tracker")
        print("1. Add new application")
        print("2. Update application status")
        print("3. Add interview")
        print("4. View summary")
        print("5. Export to CSV")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == "1":
            company = input("Company name: ").strip()
            position = input("Position: ").strip()
            url = input("Application URL (optional): ").strip()
            
            if company and position:
                app = tracker.add_application(company, position, url)
                print(f"Added application #{app['id']} for {company}")
            else:
                print("Company and position are required!")
        
        elif choice == "2":
            tracker.print_summary()
            try:
                app_id = int(input("Enter application ID: "))
                print("Status options: Applied, Interview, Rejected, Accepted, Withdrawn")
                status = input("New status: ").strip()
                notes = input("Notes (optional): ").strip()
                
                tracker.update_status(app_id, status, notes)
                print("Status updated!")
            except ValueError:
                print("Invalid application ID!")
        
        elif choice == "3":
            tracker.print_summary()
            try:
                app_id = int(input("Enter application ID: "))
                interview_date = input("Interview date (YYYY-MM-DD): ").strip()
                interview_type = input("Interview type (Phone/Video/On-site): ").strip()
                notes = input("Notes (optional): ").strip()
                
                tracker.add_interview(app_id, interview_date, interview_type, notes)
                print("Interview added!")
            except ValueError:
                print("Invalid application ID!")
        
        elif choice == "4":
            tracker.print_summary()
        
        elif choice == "5":
            filename = input("CSV filename (default: applications.csv): ").strip()
            if not filename:
                filename = "applications.csv"
            tracker.export_to_csv(filename)
        
        elif choice == "6":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main() 