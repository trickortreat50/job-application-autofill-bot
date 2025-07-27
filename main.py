"""
Main script for the Job Application Auto-Fill Bot.
Provides a simple interface to run the auto-fill functionality.
"""

import sys
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from form_filler import JobApplicationFiller
import config_manager as config
import threading
import time

class AutoFillGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Job Application Auto-Fill Bot")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Job Application Auto-Fill Bot", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # URL input
        ttk.Label(main_frame, text="Job Application URL:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.url_entry = ttk.Entry(main_frame, width=50)
        self.url_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        # Start button
        self.start_button = ttk.Button(button_frame, text="Start Auto-Fill", 
                                      command=self.start_auto_fill, style="Accent.TButton")
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        # Configure button
        self.config_button = ttk.Button(button_frame, text="Configure Info", 
                                       command=self.open_config)
        self.config_button.pack(side=tk.LEFT, padx=5)
        
        # Help button
        self.help_button = ttk.Button(button_frame, text="Help", 
                                     command=self.show_help)
        self.help_button.pack(side=tk.LEFT, padx=5)
        
        # Update button
        self.update_button = ttk.Button(button_frame, text="Check Updates", 
                                       command=self.check_updates)
        self.update_button.pack(side=tk.LEFT, padx=5)
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        status_frame.columnconfigure(0, weight=1)
        
        self.status_text = tk.Text(status_frame, height=15, width=70, wrap=tk.WORD)
        self.status_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for status text
        scrollbar = ttk.Scrollbar(status_frame, orient=tk.VERTICAL, command=self.status_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.status_text.configure(yscrollcommand=scrollbar.set)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Instructions
        instructions = """
INSTRUCTIONS:
1. Enter the URL of the job application page
2. Click "Start Auto-Fill" to begin
3. The bot will automatically fill out common fields
4. Review the filled form and submit manually
5. The browser will remain open for your review

NOTE: This bot will NOT submit the application automatically.
You must review and submit the form yourself.
        """
        
        instruction_label = ttk.Label(main_frame, text=instructions, 
                                     font=("Arial", 9), foreground="gray")
        instruction_label.grid(row=5, column=0, columnspan=2, pady=10)
        
        # Initial status
        self.log_status("Ready to start auto-fill...")
        
    def log_status(self, message):
        """Add a message to the status text area."""
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)
        self.root.update_idletasks()
        
    def start_auto_fill(self):
        """Start the auto-fill process."""
        url = self.url_entry.get().strip()
        
        if not url:
            messagebox.showerror("Error", "Please enter a job application URL.")
            return
            
        if not url.startswith(('http://', 'https://')):
            messagebox.showerror("Error", "Please enter a valid URL starting with http:// or https://")
            return
        
        # Disable buttons during processing
        self.start_button.config(state='disabled')
        self.config_button.config(state='disabled')
        self.help_button.config(state='disabled')
        self.update_button.config(state='disabled')
        
        # Start progress bar
        self.progress.start()
        
        # Start auto-fill in a separate thread
        import threading
        thread = threading.Thread(target=self.run_auto_fill, args=(url,))
        thread.daemon = True
        thread.start()
        
    def run_auto_fill(self, url):
        """Run the auto-fill process in a separate thread."""
        try:
            self.log_status(f"Starting auto-fill for: {url}")
            self.log_status("Initializing browser...")
            
            # Create filler instance
            filler = JobApplicationFiller()
            
            self.log_status("Browser initialized successfully")
            self.log_status("Navigating to application page...")
            
            # Run auto-fill
            fields_filled = filler.auto_fill_application(url)
            
            self.log_status(f"Auto-fill completed! Filled {fields_filled} fields.")
            self.log_status("Please review the form and submit manually.")
            self.log_status("Browser will remain open for your review.")
            
            # Show completion message
            self.root.after(0, lambda: messagebox.showinfo(
                "Auto-Fill Complete!",
                f"Job application auto-fill completed!\n\n"
                f"Filled {fields_filled} fields automatically.\n\n"
                f"Please review the form and submit manually.\n"
                f"The browser will remain open for your review."
            ))
            
        except Exception as e:
            error_msg = f"Error during auto-fill: {str(e)}"
            self.log_status(error_msg)
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
            
        finally:
            # Re-enable buttons
            self.root.after(0, self.enable_buttons)
    
    def check_updates(self):
        """Check for updates in a separate thread."""
        def update_check():
            try:
                self.log_status("Checking for updates...")
                
                # Import here to avoid circular imports
                from auto_updater import AutoUpdater
                updater = AutoUpdater()
                updates = updater.run_update_check(force=True)
                
                if updates:
                    self.log_status("Updates available!")
                    # Show update dialog
                    self.root.after(0, lambda: self.show_update_dialog(updates))
                else:
                    self.log_status("No updates available.")
                    self.root.after(0, lambda: messagebox.showinfo("Updates", "No updates available."))
                    
            except Exception as e:
                error_msg = f"Error checking updates: {str(e)}"
                self.log_status(error_msg)
                self.root.after(0, lambda: messagebox.showerror("Update Error", error_msg))
        
        # Run update check in separate thread
        thread = threading.Thread(target=update_check)
        thread.daemon = True
        thread.start()
    
    def show_update_dialog(self, updates):
        """Show dialog for available updates."""
        update_text = "Updates available:\n\n"
        for category, packages in updates.items():
            if packages:
                update_text += f"{category}:\n"
                for package, version in packages.items():
                    update_text += f"  - {package}: {version}\n"
                update_text += "\n"
        
        update_text += "Would you like to install these updates now?"
        
        result = messagebox.askyesno("Updates Available", update_text)
        
        if result:
            self.install_updates(updates)
    
    def install_updates(self, updates):
        """Install updates in a separate thread."""
        def install():
            try:
                self.log_status("Installing updates...")
                
                from auto_updater import AutoUpdater
                updater = AutoUpdater()
                updater.install_updates(updates)
                
                self.log_status("Updates installed successfully!")
                self.root.after(0, lambda: messagebox.showinfo("Update Complete", 
                                                              "All updates have been installed successfully!"))
                
            except Exception as e:
                error_msg = f"Error installing updates: {str(e)}"
                self.log_status(error_msg)
                self.root.after(0, lambda: messagebox.showerror("Update Error", error_msg))
        
        # Run installation in separate thread
        thread = threading.Thread(target=install)
        thread.daemon = True
        thread.start()
            
    def enable_buttons(self):
        """Re-enable all buttons."""
        self.start_button.config(state='normal')
        self.config_button.config(state='normal')
        self.help_button.config(state='normal')
        self.update_button.config(state='normal')
        self.progress.stop()
        
    def open_config(self):
        """Open configuration window."""
        # Show options for configuration
        import tkinter as tk
        from tkinter import messagebox
        
        config_choice = messagebox.askyesnocancel(
            "Configuration Options",
            "Choose configuration method:\n\n"
            "Yes = Interactive Configuration Manager (Command Line)\n"
            "No = GUI Configuration Window\n"
            "Cancel = Cancel"
        )
        
        if config_choice is True:
            # Launch interactive configuration manager
            self.launch_config_manager()
        elif config_choice is False:
            # Open GUI configuration window
            self.launch_gui_config()
        # If Cancel, do nothing
    
    def launch_config_manager(self):
        """Launch the interactive configuration manager."""
        import subprocess
        import sys
        import os
        
        try:
            # Show starting message
            self.log_status("Launching interactive configuration manager...")
            
            # Launch config_manager.py in a separate console window
            # This ensures the command-line interface is visible to the user
            if os.name == 'nt':  # Windows
                process = subprocess.Popen([sys.executable, "config_manager.py"], 
                                         creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:  # Unix/Linux/Mac
                process = subprocess.Popen([sys.executable, "config_manager.py"])
            
            # Don't wait for completion - let user interact with the console
            # Show a message that the configuration manager is running
            self.root.after(0, lambda: messagebox.showinfo(
                "Configuration Manager",
                "The interactive configuration manager has been launched in a separate window.\n\n"
                "Please complete your configuration in that window, then return here.\n\n"
                "The configuration will be automatically loaded when you restart the application."
            ))
            self.root.after(0, lambda: self.log_status("Configuration manager launched in separate window"))
                
        except Exception as e:
            error_msg = f"Error launching configuration manager: {str(e)}"
            self.root.after(0, lambda: messagebox.showerror("Configuration Error", error_msg))
            self.root.after(0, lambda: self.log_status(f"Configuration error: {str(e)}"))
    
    def launch_gui_config(self):
        """Launch the GUI configuration window."""
        try:
            from gui_config import GUIConfigWindow
            config_window = GUIConfigWindow(self.root)
            # The window will handle its own lifecycle
        except Exception as e:
            error_msg = f"Error launching GUI configuration: {str(e)}"
            messagebox.showerror("Configuration Error", error_msg)
        
    def show_help(self):
        """Show help information."""
        help_text = """
JOB APPLICATION AUTO-FILL BOT HELP

What this bot does:
- Automatically fills out common job application fields
- Saves you time on repetitive data entry
- Works with most job application websites
- Does NOT submit applications automatically

How to use:
1. Enter the URL of the job application page
2. Click "Start Auto-Fill"
3. Wait for the bot to fill the form
4. Review and submit manually

Supported fields:
- Personal information (name, email, phone, address)
- Work experience (company, position, dates, description)
- Education (degree, university, graduation year)
- Common questions (why interested, salary expectations, etc.)

Before using:
1. Configure your information using the "Configure Info" button:
   - Choose "Yes" for interactive command-line configuration
   - Choose "No" for GUI configuration window
2. Make sure you have Chrome browser installed
3. Test on a simple application first

Tips:
- The bot works best with standard application forms
- Some custom forms may not be fully compatible
- Always review the filled form before submitting
- Keep your information in config.py up to date

Troubleshooting:
- If fields aren't filled, the form may use custom field names
- Check the status log for detailed information
- Make sure the URL is correct and accessible
        """
        
        help_window = tk.Toplevel(self.root)
        help_window.title("Help")
        help_window.geometry("500x600")
        
        text_widget = tk.Text(help_window, wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert(tk.END, help_text)
        text_widget.config(state=tk.DISABLED)
        
        close_button = ttk.Button(help_window, text="Close", 
                                 command=help_window.destroy)
        close_button.pack(pady=10)
        
    def run(self):
        """Start the GUI application."""
        # Start auto-update check on startup
        self.start_auto_update_check()
        self.root.mainloop()
    
    def start_auto_update_check(self):
        """Start automatic update checking."""
        def auto_check():
            try:
                from auto_updater import AutoUpdater
                updater = AutoUpdater()
                updates = updater.run_update_check()
                
                if updates:
                    # Show update notification
                    self.root.after(0, lambda: self.show_update_dialog(updates))
                    
            except Exception as e:
                # Silently fail on startup - don't bother user
                pass
        
        # Run auto-check in separate thread after a delay
        thread = threading.Thread(target=auto_check)
        thread.daemon = True
        thread.start()

class ConfigWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Configure Personal Information")
        self.window.geometry("500x400")
        self.window.resizable(False, False)
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the configuration UI."""
        # Create notebook for tabs
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Personal info tab
        personal_frame = ttk.Frame(notebook)
        notebook.add(personal_frame, text="Personal Info")
        self.create_personal_info_tab(personal_frame)
        
        # Work experience tab
        work_frame = ttk.Frame(notebook)
        notebook.add(work_frame, text="Work Experience")
        self.create_work_experience_tab(work_frame)
        
        # Education tab
        education_frame = ttk.Frame(notebook)
        notebook.add(education_frame, text="Education")
        self.create_education_tab(education_frame)
        
        # Common answers tab
        answers_frame = ttk.Frame(notebook)
        notebook.add(answers_frame, text="Common Answers")
        self.create_common_answers_tab(answers_frame)
        
        # Buttons
        button_frame = ttk.Frame(self.window)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="Save", command=self.save_config).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.window.destroy).pack(side=tk.RIGHT, padx=5)
        
    def create_personal_info_tab(self, parent):
        """Create the personal information tab."""
        # This is a simplified version - you can expand this
        info_text = """
To configure your personal information, please edit the config.py file directly.

The following information is stored:
- Name, email, phone, address
- LinkedIn, GitHub links
- City, state, zip code, country

Open config.py in your text editor and update the PERSONAL_INFO dictionary.
        """
        
        text_widget = tk.Text(parent, wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert(tk.END, info_text)
        text_widget.config(state=tk.DISABLED)
        
    def create_work_experience_tab(self, parent):
        """Create the work experience tab."""
        info_text = """
To configure your work experience, please edit the config.py file directly.

Update the WORK_EXPERIENCE list with your job history:
- Company name
- Position/title
- Start and end dates
- Job description

Open config.py in your text editor and update the WORK_EXPERIENCE list.
        """
        
        text_widget = tk.Text(parent, wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert(tk.END, info_text)
        text_widget.config(state=tk.DISABLED)
        
    def create_education_tab(self, parent):
        """Create the education tab."""
        info_text = """
To configure your education, please edit the config.py file directly.

Update the EDUCATION dictionary with:
- Highest degree earned
- Field of study
- University name
- Graduation year
- GPA (optional)

Open config.py in your text editor and update the EDUCATION dictionary.
        """
        
        text_widget = tk.Text(parent, wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert(tk.END, info_text)
        text_widget.config(state=tk.DISABLED)
        
    def create_common_answers_tab(self, parent):
        """Create the common answers tab."""
        info_text = """
To configure common answers, please edit the config.py file directly.

Update the COMMON_ANSWERS dictionary with your responses to:
- Why are you interested in this position?
- What are your salary expectations?
- When are you available to start?
- Are you open to relocation?
- Work authorization status
- Notice period

Open config.py in your text editor and update the COMMON_ANSWERS dictionary.
        """
        
        text_widget = tk.Text(parent, wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert(tk.END, info_text)
        text_widget.config(state=tk.DISABLED)
        
    def save_config(self):
        """Save configuration (placeholder for now)."""
        messagebox.showinfo("Configuration", 
                           "Please edit config.py directly to update your information.\n\n"
                           "The configuration window will be enhanced in future versions.")
        self.window.destroy()

def main():
    """Main function to run the application."""
    print("Starting Job Application Auto-Fill Bot...")
    print("Make sure to configure your information in config.py before using!")
    
    # Check if running in GUI mode or command line
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        # Command line mode
        run_cli_mode()
    else:
        # GUI mode
        app = AutoFillGUI()
        app.run()

def run_cli_mode():
    """Run the application in command line mode."""
    print("\nCommand Line Mode")
    print("=" * 50)
    
    url = input("Enter job application URL: ").strip()
    
    if not url:
        print("No URL provided. Exiting.")
        return
        
    if not url.startswith(('http://', 'https://')):
        print("Invalid URL. Please enter a URL starting with http:// or https://")
        return
    
    print(f"\nStarting auto-fill for: {url}")
    print("Initializing browser...")
    
    try:
        filler = JobApplicationFiller()
        fields_filled = filler.auto_fill_application(url)
        
        print(f"\nAuto-fill completed! Filled {fields_filled} fields.")
        print("Please review the form and submit manually.")
        print("Browser will remain open for your review.")
        
        input("\nPress Enter to close the browser...")
        filler.close()
        
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main() 