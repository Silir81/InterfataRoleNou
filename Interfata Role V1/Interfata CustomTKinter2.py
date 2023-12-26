import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, filedialog
import pandas as pd

# Initialize main window
root = ctk.CTk()
root.geometry('800x600')
root.title("CustomTkinter Tabs")

# Global DataFrame for Excel data
df = None

# Function to switch between tabs
def switch_tab(tab):
    tab1_frame.pack_forget()
    tab2_frame.pack_forget()
    if tab == 1:
        tab1_frame.pack(fill='both', expand=True)
    else:
        tab2_frame.pack(fill='both', expand=True)

# Function to update the Treeview with data based on selected Tambur
def on_dropdown_select(*args):
    global df
    selected_tambur = dropdown_var.get()
    if df is not None and selected_tambur:
        filtered_df = df[(df['Tambur'] == selected_tambur) & (df['KG/Rola'] > 0)]
        update_treeview(filtered_df)

# Function to update the Treeview with data
def update_treeview(filtered_df):
    tree.delete(*tree.get_children())
    for index, row in filtered_df.iterrows():
        tree.insert("", tk.END, values=(row['Tambur'], row['KG/Rola'], row['Nr.InternRola']))

# Function to open an Excel file and update dropdown
def open_excel_file():
    global df
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
    if file_path:
        try:
            df = pd.read_excel(file_path)
            tambur_values = df['Tambur'].unique().tolist()
            create_dropdown(tambur_values)
        except Exception as e:
            print("Error opening file:", e)

# Function to create dropdown with new values in the placeholder frame
def create_dropdown(values):
    global dropdown_var, dropdown

    # Clear placeholder frame for dropdown
    for widget in dropdown_placeholder.winfo_children():
        widget.destroy()

    # Create new dropdown in the placeholder frame
    dropdown_var = tk.StringVar()
    dropdown = ctk.CTkOptionMenu(dropdown_placeholder, variable=dropdown_var, values=values)
    dropdown.pack(fill='x', expand=True)
    dropdown_var.trace('w', lambda *args: on_dropdown_select())

# Create tab frames
tab1_frame = ctk.CTkFrame(root)
tab2_frame = ctk.CTkFrame(root)

# Container frame for tab buttons
tabs_container = ctk.CTkFrame(root)
tabs_container.pack(side='top', fill='x')

# Create buttons for switching tabs
tab1_button = ctk.CTkButton(tabs_container, text="Registru Role", command=lambda: switch_tab(1))
tab2_button = ctk.CTkButton(tabs_container, text="Registru Rebut", command=lambda: switch_tab(2))
tab1_button.pack(side='left', fill='x', expand=True)
tab2_button.pack(side='left', fill='x', expand=True)


# Add Open Excel button to Tab 1
open_excel_button = ctk.CTkButton(tab1_frame, text="Open Excel File", command=open_excel_file)
open_excel_button.pack(pady=10)


# Placeholder frame for dropdown in Tab 1
dropdown_placeholder = ctk.CTkFrame(tab1_frame)
dropdown_placeholder.pack(pady=10)


# Create initial empty dropdown in Tab 1 with a placeholder value
create_dropdown(["Select Tambur"])

# Create Treeview in Tab 1
tree_columns = ("Tambur", "KG/Rola", "Nr.InternRola")
tree = ttk.Treeview(tab1_frame, columns=tree_columns, show='headings')
for col in tree_columns:
    tree.heading(col, text=col)
tree.pack(expand=True, fill='both', pady=20, padx=20)

# Create input fields in Tab 2
for i in range(1, 3):
    entry_var = tk.StringVar()
    entry = ctk.CTkEntry(tab2_frame, textvariable=entry_var, placeholder_text=f"Input {i}")
    entry.pack(pady=10)

# Initially display Tab 1
switch_tab(1)

# Start the GUI
root.mainloop()
