import tkinter as tk
from tkinter import messagebox
import time
import matplotlib.pyplot as plt
import psutil
import win32process
import win32gui
from datetime import datetime
import os

class AppTracker:
    def __init__(self):
        self.app_usage = {}
        self.current_app = None
        self.start_time = None
        self.total_time = {}
        self.usage_frequency = {}
        self.categories = {
            'Productivity': [
                'notepad.exe', 'winword.exe', 'excel.exe', 'powerpnt.exe', 'outlook.exe', 
                'onenote.exe', 'mspub.exe', 'access.exe', 'teams.exe', 'slack.exe', 
                'evernote.exe', 'todo.exe', 'microsoft edge.exe', 'zoom.exe', 
                'google docs.exe', 'notion.exe', 'trello.exe', 'basecamp.exe', 
                'coda.exe', 'figma.exe', 'illustrator.exe', 'photoshop.exe'
            ],
            'Games': [
                'valorant.exe', 'csgo.exe', 'dota2.exe', 'fortnite.exe', 'apex.exe', 
                'leagueoflegends.exe', 'rainbowsix.exe', 'overwatch.exe', 'minecraft.exe', 
                'gta5.exe', 'pubg.exe', 'rocketleague.exe', 'battlefield.exe', 
                'wow.exe', 'starcraft.exe', 'hearthstone.exe', 'crysis.exe', 
                'assassinscreed.exe', 'skyrim.exe', 'fallout4.exe', 'cyberpunk2077.exe'
            ],
            'Social Media': [
                'chrome.exe', 'firefox.exe', 'msedge.exe', 'opera.exe', 'discord.exe', 
                'whatsapp.exe', 'telegram.exe', 'facebook.exe', 'instagram.exe', 
                'twitter.exe', 'reddit.exe', 'tiktok.exe', 'snapchat.exe', 
                'linkedin.exe', 'pinterest.exe', 'tumblr.exe', 'weibo.exe'
            ],
            'Streaming': [
                'obs64.exe', 'vlc.exe', 'spotify.exe', 'itunes.exe', 'windows media player.exe', 
                'apple music.exe', 'twitch.exe', 'netflix.exe', 'hulu.exe', 
                'disney+.exe', 'youtube.exe', 'steam.exe', 'gog.exe', 
                'epicgameslauncher.exe', 'blizzard.exe', 'plex.exe', 'kodi.exe'
            ],
            'Development': [
                'pycharm.exe', 'vscode.exe', 'eclipse.exe', 'netbeans.exe', 'intellij.exe', 
                'sublime_text.exe', 'notepad++.exe', 'docker.exe', 'git.exe', 
                'postman.exe', 'xampp-control.exe', 'android studio.exe', 'unity.exe', 
                'visual studio.exe', 'rstudio.exe', 'webstorm.exe'
            ],
            'Utilities': [
                'taskmgr.exe', 'control.exe', 'cmd.exe', 'powershell.exe', 'explorer.exe', 
                'defender.exe', 'windows update.exe', 'teamviewer.exe', 'anydesk.exe', 
                'ccleaner.exe', 'winrar.exe', 'zip.exe', 'malwarebytes.exe'
            ],
            'Web Browsers': [
                'chrome.exe', 'firefox.exe', 'msedge.exe', 'opera.exe', 'brave.exe', 
                'safari.exe', 'vivaldi.exe', 'internet explorer.exe'
            ],
            'Communication': [
                'skype.exe', 'zoom.exe', 'teams.exe', 'discord.exe', 'slack.exe', 
                'whatsapp.exe', 'telegram.exe', 'signal.exe', 'facetime.exe', 
                'line.exe', 'wechat.exe', 'hangouts.exe'
            ],
            'Design': [
                'illustrator.exe', 'photoshop.exe', 'indesign.exe', 'coreldraw.exe', 
                'gimp.exe', 'sketch.exe', 'canva.exe', 'figma.exe', 'autocad.exe'
            ],

        }

        self.category_usage = {cat: 0 for cat in self.categories}
        self.last_reset_time = datetime.now()

        self.load_total_time()

    def start_tracking(self, app_name):
        if app_name not in self.app_usage:
            self.app_usage[app_name] = 0
            self.usage_frequency[app_name] = 0  

        self.current_app = app_name
        self.start_time = time.time()

    def stop_tracking(self):
        if self.current_app and self.start_time:
            elapsed_time = time.time() - self.start_time
            self.app_usage[self.current_app] += elapsed_time
            self.total_time[self.current_app] = self.total_time.get(self.current_app, 0) + elapsed_time  
            self.usage_frequency[self.current_app] += 1  
            self.start_time = None
            self.current_app = None

    def get_category(self, app_name):
        """Return the category of the app based on the predefined categories."""
        for category, apps in self.categories.items():
            if app_name in apps:
                return category
        return None  

    def reset_usage(self):
        self.app_usage.clear()
        self.current_app = None
        self.start_time = None
        self.category_usage = {cat: 0 for cat in self.categories}  
        self.last_reset_time = datetime.now()  

    def get_total_summary(self):
        return self.total_time  

    def get_summary(self):
        """Return a summary of the current app usage."""
        return {app: time_spent for app, time_spent in self.app_usage.items() if time_spent > 0}

    def display_daily_summary(self):
        """Show daily summary in a bar graph."""
        apps = list(self.total_time.keys())
        total_times = list(self.total_time.values())
        frequencies = [self.usage_frequency.get(app, 0) for app in apps]  

        fig, ax1 = plt.subplots()

        ax2 = ax1.twinx()
        ax1.bar(apps, total_times, color='g', alpha=0.6, label='Total Time (seconds)')
        ax2.plot(apps, frequencies, color='b', marker='o', label='Usage Frequency', linestyle='--')

        ax1.set_xlabel('Applications')
        ax1.set_ylabel('Total Time (seconds)', color='g')
        ax2.set_ylabel('Usage Frequency', color='b')
        plt.title('Daily App Usage Summary')
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')

        plt.savefig('daily_summary.png')
        plt.show()

    def get_most_used_category(self):
        """Determine the most used category based on total time."""
        for app, total in self.total_time.items():
            category = self.get_category(app)
            if category:
                self.category_usage[category] += total

        most_used_category = max(self.category_usage, key=self.category_usage.get)
        return most_used_category, self.category_usage[most_used_category]

    def load_total_time(self):
        """Load the lifetime total time from a file."""
        if os.path.exists('total_time.txt'):
            with open('total_time.txt', 'r') as f:
                for line in f:
                    app, time_spent = line.strip().split(':')
                    self.total_time[app] = float(time_spent)

    def save_data(self):
        """Save the current session data and graph to a text file."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H_%M_%S")  
        filename = f"app_usage_summary_{timestamp}.txt"

        with open(filename, 'w') as f:
            f.write(f"Summary for {timestamp}:\n")
            f.write("Current App Usage:\n")
            for app, time_spent in self.get_summary().items():
                f.write(f"{app}: {time_spent:.2f} seconds\n")

            f.write("\nLifetime Total Time:\n")
            for app, time_spent in self.total_time.items():
                f.write(f"{app}: {time_spent:.2f} seconds\n")

        plt.savefig(f"app_usage_graph_{timestamp}.png")  
        print(f"Session data saved to {filename} and graph to app_usage_graph_{timestamp}.png")

class AppTrackerGUI:
    def __init__(self, master):
        self.master = master
        self.tracker = AppTracker()
        self.create_widgets()
        self.update_live_data()  

    def create_widgets(self):

        self.summary_text = tk.Text(self.master, height=10, width=50, state='disabled')  
        self.summary_text.pack()

        self.show_graph_button = tk.Button(self.master, text="Show App Usage Graph", command=self.display_app_pie_chart)
        self.show_graph_button.pack()

        self.total_summary_button = tk.Button(self.master, text="Show Total Time Summary", command=self.display_total_summary)
        self.total_summary_button.pack()

        self.daily_summary_button = tk.Button(self.master, text="Show Daily Summary", command=self.tracker.display_daily_summary)
        self.daily_summary_button.pack()

        self.most_used_category_button = tk.Button(self.master, text="Show Most Used Category", command=self.display_most_used_category)
        self.most_used_category_button.pack()

        self.reset_button = tk.Button(self.master, text="Reset Data", command=self.reset_data)
        self.reset_button.pack()

    def display_total_summary(self):
        """Display the total time spent on each application."""
        summary = self.tracker.get_total_summary()

        message = "Total Time Summary:\n"
        for app, time_spent in summary.items():
            message += f"{app}: {time_spent:.2f} seconds\n"

        messagebox.showinfo("Total Time Summary", message)

    def reset_data(self):
        """Reset all data and inform the user."""
        self.tracker.reset_usage()
        messagebox.showinfo("Reset", "All data has been reset.")

    def update_live_data(self):
        active_window = win32gui.GetForegroundWindow()  
        app_name = self.get_executable_name(active_window)  

        if app_name:
            if self.tracker.current_app != app_name:
                self.tracker.stop_tracking()  
                self.tracker.start_tracking(app_name)  
            else:

                self.tracker.stop_tracking()  
                self.tracker.start_tracking(app_name)  

            self.update_summary_display()  

        self.master.after(3000, self.update_live_data)  

    def get_executable_name(self, hwnd):
        try:
            _, pid = win32process.GetWindowThreadProcessId(hwnd)  
            process = psutil.Process(pid)  
            return process.name()  
        except Exception as e:
            print(f"Error retrieving process name: {e}")
            return None

    def update_summary_display(self):
        self.summary_text.config(state='normal')
        self.summary_text.delete(1.0, tk.END)  
        summary = self.tracker.get_summary()  
        for app, time_spent in summary.items():
            self.summary_text.insert(tk.END, f"{app}: {time_spent:.2f} seconds\n")  
        self.summary_text.config(state='disabled')  

    def display_app_pie_chart(self):
        summary = self.tracker.get_summary()
        labels = summary.keys()
        sizes = summary.values()
        plt.figure(figsize=(8, 8))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        plt.title("App Usage Distribution")
        plt.show()

    def display_most_used_category(self):
        """Display the most used application category along with detailed information."""
        category, time_spent = self.tracker.get_most_used_category()

        total_usage_time = sum(self.tracker.total_time.values())

        percentage = (time_spent / total_usage_time * 100) if total_usage_time > 0 else 0

        message = (
            f"Most Used Category: {category}\n"
            f"Time Spent: {time_spent:.2f} seconds\n"
            f"Percentage of Total Usage: {percentage:.2f}%\n"
            f"Total Time Across All Categories: {total_usage_time:.2f} seconds"
        )

        messagebox.showinfo("Most Used Category", message)

    def display_most_used_category(self):
        category, time_spent = self.tracker.get_most_used_category()
        messagebox.showinfo("Most Used Category", f"{category}: {time_spent:.2f} seconds")

    def on_closing(self):
        """Handle the window closing event."""
        self.tracker.save_data()  
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("App Tracker")
    app = AppTrackerGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)  
    root.mainloop()