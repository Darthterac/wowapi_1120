import tkinter as tk
from tkinter import messagebox, scrolledtext
import csv
import re
import webbrowser

CSV_FILE = "wowAPI_FuncParam_11_2_0.csv"
GITHUB_BASE_URL = "https://github.com/Gethe/wow-ui-source/tree/live/Interface/AddOns/"

# Fetch matching functions from CSV
def fetch_functions(func_name):
    matches = []
    try:
        with open(CSV_FILE, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if re.search(func_name, row['Function Name'], re.IGNORECASE):
                    matches.append(row)
        return matches
    except FileNotFoundError:
        messagebox.showerror("Error", f"CSV file '{CSV_FILE}' not found.")
        return []

# Handle search button click
def on_search():
    search_query = entry.get().strip()
    results_area.config(state=tk.NORMAL)
    results_area.delete("1.0", tk.END)

    if not search_query:
        messagebox.showwarning("Input Error", "Please enter a function name.")
        return

    matches = fetch_functions(search_query)
    if not matches:
        results_area.insert(tk.END, "No matching functions found.\n")
        results_area.config(state=tk.DISABLED)
        return

    for idx, match in enumerate(matches):
        func_name = match['Function Name']
        params = match['Parameters']
        source_file = match['Source File']
        line_number = match['Line Number']
        github_link = f"{GITHUB_BASE_URL}{source_file}#L{line_number}"

        results_area.insert(tk.END, f"Function: {func_name}\n")
        results_area.insert(tk.END, f"Parameters: {params}\n")
        results_area.insert(tk.END, f"Source File: {source_file}\n")
        results_area.insert(tk.END, f"Line Number: {line_number}\n")

        # Insert clickable link
        start_idx = results_area.index(tk.INSERT)
        results_area.insert(tk.END, f"GitHub Link: {github_link}\n")
        end_idx = results_area.index(tk.INSERT)
        results_area.tag_add(f"link{idx}", start_idx, end_idx)
        results_area.tag_config(f"link{idx}", foreground="blue", underline=True)
        results_area.tag_bind(f"link{idx}", "<Button-1>", lambda e, url=github_link: webbrowser.open(url))

        results_area.insert(tk.END, "-"*60 + "\n")

    results_area.config(state=tk.DISABLED)

# Setup GUI
root = tk.Tk()
root.title("WoW API Function Lookup")
root.geometry("700x500")

tk.Label(root, text="Enter Function Name:").pack(pady=10)
entry = tk.Entry(root, width=50)
entry.pack(pady=5)

search_button = tk.Button(root, text="Search", command=on_search)
search_button.pack(pady=10)

results_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=25)
results_area.pack(pady=10)
results_area.config(state=tk.DISABLED)

root.mainloop()
