"""
Auto-Updater for Job Application Auto-Fill Bot
Automatically checks for and installs updates to dependencies and the bot.
"""

import subprocess
import sys
import os
import json
import requests
import time
from pathlib import Path
from packaging import version
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AutoUpdater:
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.config_file = self.project_dir / "update_config.json"
        self.last_check_file = self.project_dir / ".last_update_check"
        self.update_config = self.load_update_config()
        
    def load_update_config(self):
        """Load update configuration."""
        default_config = {
            "auto_check_updates": True,
            "check_interval_hours": 24,
            "auto_install_dependencies": True,
            "auto_install_bot_updates": False,
            "notify_on_updates": True,
            "backup_before_update": True,
            "excluded_packages": [],
            "update_channels": ["conda-forge", "defaults"]
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    for key, value in default_config.items():
                        if key not in config:
                            config[key] = value
                    return config
            except Exception as e:
                logger.warning(f"Could not load update config: {e}")
                return default_config
        else:
            # Create default config
            self.save_update_config(default_config)
            return default_config
    
    def save_update_config(self, config):
        """Save update configuration."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            logger.error(f"Could not save update config: {e}")
    
    def should_check_for_updates(self):
        """Check if it's time to look for updates."""
        if not self.update_config["auto_check_updates"]:
            return False
            
        if not self.last_check_file.exists():
            return True
            
        try:
            last_check = self.last_check_file.read_text().strip()
            last_check_time = float(last_check)
            current_time = time.time()
            hours_since_last_check = (current_time - last_check_time) / 3600
            
            return hours_since_last_check >= self.update_config["check_interval_hours"]
        except Exception as e:
            logger.warning(f"Could not read last check time: {e}")
            return True
    
    def mark_update_check(self):
        """Mark that an update check was performed."""
        try:
            self.last_check_file.write_text(str(time.time()))
        except Exception as e:
            logger.warning(f"Could not save update check time: {e}")
    
    def get_installed_packages(self):
        """Get list of installed packages with versions."""
        try:
            result = subprocess.run([sys.executable, "-m", "pip", "list", "--format=json"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                packages = json.loads(result.stdout)
                return {pkg["name"]: pkg["version"] for pkg in packages}
            else:
                logger.error(f"Failed to get installed packages: {result.stderr}")
                return {}
        except Exception as e:
            logger.error(f"Error getting installed packages: {e}")
            return {}
    
    def get_latest_versions(self, packages):
        """Get latest versions of packages from PyPI."""
        latest_versions = {}
        
        for package in packages:
            if package in self.update_config["excluded_packages"]:
                continue
                
            try:
                response = requests.get(f"https://pypi.org/pypi/{package}/json", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    latest_version = data["info"]["version"]
                    latest_versions[package] = latest_version
                else:
                    logger.warning(f"Could not get version for {package}")
            except Exception as e:
                logger.warning(f"Error checking version for {package}: {e}")
        
        return latest_versions
    
    def check_conda_updates(self):
        """Check for conda package updates."""
        try:
            # Check if conda is available
            result = subprocess.run(["conda", "--version"], capture_output=True, text=True)
            if result.returncode != 0:
                logger.info("Conda not available, skipping conda updates")
                return {}
            
            # Get conda package list
            result = subprocess.run(["conda", "list", "--json"], capture_output=True, text=True)
            if result.returncode == 0:
                packages = json.loads(result.stdout)
                conda_packages = {pkg["name"]: pkg["version"] for pkg in packages}
                
                # Check for updates
                result = subprocess.run(["conda", "list", "--updatable", "--json"], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    updatable = json.loads(result.stdout)
                    return {pkg["name"]: pkg["version"] for pkg in updatable}
                else:
                    logger.warning("Could not check conda updates")
                    return {}
            else:
                logger.warning("Could not get conda package list")
                return {}
                
        except Exception as e:
            logger.warning(f"Error checking conda updates: {e}")
            return {}
    
    def backup_config(self):
        """Create backup of configuration files."""
        if not self.update_config["backup_before_update"]:
            return
            
        try:
            backup_dir = self.project_dir / "backups" / time.strftime("%Y%m%d_%H%M%S")
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            # Backup important files
            important_files = ["config.py", "update_config.json"]
            for file_name in important_files:
                file_path = self.project_dir / file_name
                if file_path.exists():
                    backup_path = backup_dir / file_name
                    backup_path.write_text(file_path.read_text())
            
            logger.info(f"Backup created at: {backup_dir}")
            return backup_dir
        except Exception as e:
            logger.error(f"Failed to create backup: {e}")
            return None
    
    def update_pip_packages(self, outdated_packages):
        """Update pip packages."""
        if not outdated_packages:
            return True
            
        if not self.update_config["auto_install_dependencies"]:
            logger.info("Auto-install disabled, skipping pip updates")
            return False
        
        try:
            logger.info(f"Updating {len(outdated_packages)} pip packages...")
            
            for package, latest_version in outdated_packages.items():
                logger.info(f"Updating {package} to {latest_version}")
                result = subprocess.run([sys.executable, "-m", "pip", "install", 
                                       f"{package}=={latest_version}", "--upgrade"], 
                                      capture_output=True, text=True)
                
                if result.returncode != 0:
                    logger.error(f"Failed to update {package}: {result.stderr}")
                    return False
                else:
                    logger.info(f"Successfully updated {package}")
            
            return True
        except Exception as e:
            logger.error(f"Error updating pip packages: {e}")
            return False
    
    def update_conda_packages(self, outdated_packages):
        """Update conda packages."""
        if not outdated_packages:
            return True
            
        if not self.update_config["auto_install_dependencies"]:
            logger.info("Auto-install disabled, skipping conda updates")
            return False
        
        try:
            logger.info(f"Updating {len(outdated_packages)} conda packages...")
            
            # Update all packages at once
            packages_to_update = list(outdated_packages.keys())
            result = subprocess.run(["conda", "update", "-y"] + packages_to_update, 
                                  capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.error(f"Failed to update conda packages: {result.stderr}")
                return False
            else:
                logger.info("Successfully updated conda packages")
                return True
                
        except Exception as e:
            logger.error(f"Error updating conda packages: {e}")
            return False
    
    def check_bot_updates(self):
        """Check for bot updates (placeholder for future implementation)."""
        # This would check for updates to the bot itself
        # For now, just return False (no updates available)
        return False
    
    def update_bot(self):
        """Update the bot itself (placeholder for future implementation)."""
        if not self.update_config["auto_install_bot_updates"]:
            logger.info("Auto-install bot updates disabled")
            return False
        
        # This would download and install bot updates
        # For now, just return True (no updates to install)
        return True
    
    def notify_updates(self, updates):
        """Notify user about available updates."""
        if not self.update_config["notify_on_updates"]:
            return
        
        if not updates:
            return
        
        try:
            import tkinter as tk
            from tkinter import messagebox
            
            root = tk.Tk()
            root.withdraw()
            
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
            
            root.destroy()
            
        except Exception as e:
            logger.warning(f"Could not show update notification: {e}")
            print(f"\nUpdates available: {updates}")
    
    def install_updates(self, updates):
        """Install all available updates."""
        logger.info("Installing updates...")
        
        # Create backup
        backup_dir = self.backup_config()
        
        success = True
        
        # Update pip packages
        if "pip" in updates and updates["pip"]:
            success &= self.update_pip_packages(updates["pip"])
        
        # Update conda packages
        if "conda" in updates and updates["conda"]:
            success &= self.update_conda_packages(updates["conda"])
        
        # Update bot
        if "bot" in updates and updates["bot"]:
            success &= self.update_bot()
        
        if success:
            logger.info("All updates installed successfully!")
            if self.update_config["notify_on_updates"]:
                try:
                    import tkinter as tk
                    from tkinter import messagebox
                    root = tk.Tk()
                    root.withdraw()
                    messagebox.showinfo("Update Complete", "All updates have been installed successfully!")
                    root.destroy()
                except:
                    print("Updates installed successfully!")
        else:
            logger.error("Some updates failed to install")
            if backup_dir:
                logger.info(f"Backup available at: {backup_dir}")
    
    def run_update_check(self, force=False):
        """Run a complete update check."""
        if not force and not self.should_check_for_updates():
            logger.info("No update check needed")
            return
        
        logger.info("Checking for updates...")
        
        updates = {}
        
        # Check pip packages
        try:
            installed_packages = self.get_installed_packages()
            latest_versions = self.get_latest_versions(installed_packages.keys())
            
            pip_updates = {}
            for package, current_version in installed_packages.items():
                if package in latest_versions:
                    latest_version = latest_versions[package]
                    if version.parse(latest_version) > version.parse(current_version):
                        pip_updates[package] = latest_version
            
            if pip_updates:
                updates["pip"] = pip_updates
                logger.info(f"Found {len(pip_updates)} pip package updates")
        except Exception as e:
            logger.error(f"Error checking pip updates: {e}")
        
        # Check conda packages
        try:
            conda_updates = self.check_conda_updates()
            if conda_updates:
                updates["conda"] = conda_updates
                logger.info(f"Found {len(conda_updates)} conda package updates")
        except Exception as e:
            logger.error(f"Error checking conda updates: {e}")
        
        # Check bot updates
        try:
            bot_updates = self.check_bot_updates()
            if bot_updates:
                updates["bot"] = bot_updates
                logger.info("Bot updates available")
        except Exception as e:
            logger.error(f"Error checking bot updates: {e}")
        
        # Mark check as completed
        self.mark_update_check()
        
        # Notify user if updates are available
        if updates:
            self.notify_updates(updates)
        else:
            logger.info("No updates available")
        
        return updates
    
    def configure_auto_update(self):
        """Configure auto-update settings."""
        print("\n" + "="*50)
        print("AUTO-UPDATE CONFIGURATION")
        print("="*50)
        
        print("\nCurrent settings:")
        for key, value in self.update_config.items():
            print(f"  {key}: {value}")
        
        print("\nConfigure auto-update settings:")
        print("1. Enable/disable auto-check for updates")
        print("2. Set check interval")
        print("3. Enable/disable auto-install")
        print("4. Enable/disable notifications")
        print("5. Enable/disable backups")
        print("6. Exit")
        
        while True:
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == "1":
                current = self.update_config["auto_check_updates"]
                new_value = input(f"Auto-check updates (currently {current})? (y/n): ").strip().lower()
                self.update_config["auto_check_updates"] = new_value == "y"
                
            elif choice == "2":
                current = self.update_config["check_interval_hours"]
                new_value = input(f"Check interval in hours (currently {current})? ").strip()
                try:
                    self.update_config["check_interval_hours"] = int(new_value)
                except ValueError:
                    print("Invalid number")
                    
            elif choice == "3":
                current = self.update_config["auto_install_dependencies"]
                new_value = input(f"Auto-install dependencies (currently {current})? (y/n): ").strip().lower()
                self.update_config["auto_install_dependencies"] = new_value == "y"
                
            elif choice == "4":
                current = self.update_config["notify_on_updates"]
                new_value = input(f"Show notifications (currently {current})? (y/n): ").strip().lower()
                self.update_config["notify_on_updates"] = new_value == "y"
                
            elif choice == "5":
                current = self.update_config["backup_before_update"]
                new_value = input(f"Create backups (currently {current})? (y/n): ").strip().lower()
                self.update_config["backup_before_update"] = new_value == "y"
                
            elif choice == "6":
                break
                
            else:
                print("Invalid choice")
        
        # Save configuration
        self.save_update_config(self.update_config)
        print("Configuration saved!")

def main():
    """Main function for auto-updater."""
    updater = AutoUpdater()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "check":
            updater.run_update_check(force=True)
        elif command == "install":
            updates = updater.run_update_check(force=True)
            if updates:
                updater.install_updates(updates)
        elif command == "config":
            updater.configure_auto_update()
        else:
            print("Unknown command. Use: check, install, or config")
    else:
        # Interactive mode
        print("Auto-Updater for Job Application Auto-Fill Bot")
        print("1. Check for updates")
        print("2. Install updates")
        print("3. Configure auto-update")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            updater.run_update_check(force=True)
        elif choice == "2":
            updates = updater.run_update_check(force=True)
            if updates:
                updater.install_updates(updates)
        elif choice == "3":
            updater.configure_auto_update()
        elif choice == "4":
            print("Goodbye!")
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main() 