import os
import re
import shutil
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import ThemedStyle

def extract_date_from_filename(filename, pattern):
    pattern_mapping = {
        'yyyy': r"(?P<year>\d{4})",
        'yy': r"(?P<year>\d{2})",
        'mm': r"(?P<month>\d{2})",
        'dd': r"(?P<day>\d{2})",
        'hh': r"(?P<hour>\d{2})",
        'nn': r"(?P<minute>\d{2})",
        'ss': r"(?P<second>\d{2})"
    }

    for key, value in pattern_mapping.items():
        pattern = pattern.replace(key, value)

    # Add "?" to make missing date components optional
    pattern = pattern.replace('_', '_?')

    match = re.match(pattern, filename)
    if match:
        return match.groupdict()
    return None

def organize_files(folder_path, naming_format, organization_criteria, pattern):
    if not os.path.exists(folder_path):
        print("Folder not found.")
        return

    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)

        # Skip directories and non-files
        if not os.path.isfile(filepath):
            continue

        date_info = extract_date_from_filename(filename, pattern)
        if not date_info:
            print(f"Skipping file '{filename}' as it doesn't match the expected naming format.")
            continue

        year, month, day, hour, minute, second = (
            date_info.get('year', ''),
            date_info.get('month', ''),
            date_info.get('day', ''),
            date_info.get('hour', ''),
            date_info.get('minute', ''),
            date_info.get('second', '')
        )

        new_folder_name = naming_format.format(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            second=second,
            filename=filename
        )

        # Move the file to the corresponding folder
        new_folder_path = os.path.join(folder_path, new_folder_name)
        os.makedirs(new_folder_path, exist_ok=True)
        shutil.move(filepath, os.path.join(new_folder_path, filename))

def browse_folder():
    folder_path = filedialog.askdirectory()
    folder_path_entry.delete(0, tk.END)
    folder_path_entry.insert(0, folder_path)

def open_explorer():
    folder_path = folder_path_entry.get()
    if os.path.exists(folder_path):
        os.startfile(folder_path)

def show_tooltip(widget, text):
    tooltip = ttk.Label(root, text=text, background="#f0f0f0", relief="solid", borderwidth=1)
    tooltip.place(x=widget.winfo_rootx(), y=widget.winfo_rooty() - 30, relwidth=0.6)
    root.after(3000, lambda: tooltip.destroy())

def set_theme():
    selected_theme = theme_var.get()
    if selected_theme == 'dark':
        style.set_theme("equilux")
        root.config(background="#232323")  # Dark background color
        folder_path_entry.config(background="#404040", foreground="white")  # Dark themed folder path entry
        naming_format_entry.config(background="#404040", foreground="white")  # Dark themed naming format entry
        organization_criteria_entry.config(background="#404040", foreground="white")  # Dark themed organization criteria entry
        pattern_entry.config(background="#404040", foreground="white")  # Dark themed pattern entry
        for widget in label_widgets:
            widget.config(background="#232323", foreground="white")  # Dark themed labels
    else:
        style.set_theme("arc")
        root.config(background="#f0f0f0")  # Light background color
        folder_path_entry.config(background="white", foreground="black")  # Light themed folder path entry
        naming_format_entry.config(background="white", foreground="black")  # Light themed naming format entry
        organization_criteria_entry.config(background="white", foreground="black")  # Light themed organization criteria entry
        pattern_entry.config(background="white", foreground="black")  # Light themed pattern entry
        for widget in label_widgets:
            widget.config(background="#f0f0f0", foreground="black")  # Light themed labels



def organize_files_gui():
    folder_path = folder_path_entry.get()
    naming_format = naming_format_entry.get()
    organization_criteria = organization_criteria_entry.get()
    pattern = pattern_entry.get()

    organize_files(folder_path, naming_format, organization_criteria, pattern)
    status_label.config(text="File organization complete.")

# Create the main window
root = tk.Tk()
root.title("File Organizer")

# Configure the default theme
style = ThemedStyle(root)
style.set_theme("arc")  # Default theme
root.config(background="#f0f0f0")  # Light background color



# Custom fonts and colors
root.option_add("*Font", "Helvetica 10 bold")
root.option_add("*Button.font", "Helvetica 10 bold")
root.option_add("*Entry.font", "Helvetica 10")
root.option_add("*Label.font", "Helvetica 10")
root.option_add("*Label.foreground", "#333333")
root.option_add("*Label.background", "#f0f0f0")

# Folder Path
folder_path_label = tk.Label(root, text="Folder Path:")
folder_path_label.grid(row=0, column=0)
folder_path_entry = tk.Entry(root, width=50)
folder_path_entry.grid(row=0, column=1)
browse_button = ttk.Button(root, text="Browse", command=browse_folder)
browse_button.grid(row=0, column=2)

# Open Explorer Button
open_explorer_button = ttk.Button(root, text="Open Explorer", command=open_explorer)
open_explorer_button.grid(row=0, column=3)

# Naming Format
naming_format_label = tk.Label(root, text="Naming Format: (Use placeholders {year}, {month}, etc.)")
naming_format_label.grid(row=1, column=0)
naming_format_entry = tk.Entry(root, width=50)
naming_format_entry.grid(row=1, column=1)

# Organization Criteria
organization_criteria_label = tk.Label(root, text="Organization Criteria: (e.g., {month} to organize by month)")
organization_criteria_label.grid(row=2, column=0)
organization_criteria_entry = tk.Entry(root, width=50)
organization_criteria_entry.grid(row=2, column=1)

# Pattern
pattern_label = tk.Label(root, text="Pattern: (Use letters yyyymmdd_hhnnss for date components)")
pattern_label.grid(row=3, column=0)
pattern_entry = tk.Entry(root, width=50)
pattern_entry.grid(row=3, column=1)
pattern_example = "Example: ddmmyyyy_hhnnss"
pattern_tooltip = "Example: ddmmyyyy_hhnnss (For 28072023_120000)"
pattern_entry.bind("<Enter>", lambda event: show_tooltip(pattern_entry, pattern_tooltip))
pattern_entry.bind("<Leave>", lambda event: root.after(1000, pattern_entry.unbind, "<Leave>"))

# Theme Selection
theme_label = tk.Label(root, text="Select Theme:")
theme_label.grid(row=4, column=0)
theme_var = tk.StringVar(value="light")  # Default theme is light
theme_radio_dark = ttk.Radiobutton(root, text="Dark", variable=theme_var, value="dark", command=set_theme)
theme_radio_dark.grid(row=4, column=1)
theme_radio_light = ttk.Radiobutton(root, text="Light", variable=theme_var, value="light", command=set_theme)
theme_radio_light.grid(row=4, column=2)

# Organize Button
organize_button = ttk.Button(root, text="Organize Files", command=organize_files_gui)
organize_button.grid(row=5, column=0, columnspan=2)

# Status Label
status_label = tk.Label(root, text="")
status_label.grid(row=6, column=0, columnspan=2)


# Labels
label_widgets = []
folder_path_label = tk.Label(root, text="Folder Path:")
label_widgets.append(folder_path_label)
folder_path_label.grid(row=0, column=0)
naming_format_label = tk.Label(root, text="Naming Format: (Use placeholders {year}, {month}, etc.)")
label_widgets.append(naming_format_label)
naming_format_label.grid(row=1, column=0)
organization_criteria_label = tk.Label(root, text="Organization Criteria: (e.g., {month} to organize by month)")
label_widgets.append(organization_criteria_label)
organization_criteria_label.grid(row=2, column=0)
pattern_label = tk.Label(root, text="Pattern: (Use letters yyyymmdd_hhnnss for date components)")
label_widgets.append(pattern_label)
pattern_label.grid(row=3, column=0)

root.mainloop()
