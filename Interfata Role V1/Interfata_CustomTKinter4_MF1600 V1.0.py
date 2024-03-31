import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, filedialog
import pandas as pd
import tkinter.messagebox as msgbox  # Import messagebox


# Function to move the window (used for custom title bar dragging)
def move_window(event):
    root.geometry(f'+{event.x_root}+{event.y_root}')


# Initialize main window without default title bar
root = ctk.CTk()
root.geometry('800x600')
root.overrideredirect(True)  # Turn off the default title bar

# Create a custom title bar with a specified height and color
title_bar = ctk.CTkFrame(root, height=5, fg_color='transparent')  # Corrected property name
title_bar.pack(fill='x')
title_bar.bind('<B1-Motion>', move_window)

# Custom title label with specified text, colors, and font
title_label = ctk.CTkLabel(title_bar, text="Smecherie by SRV", fg_color='red', text_color='black',
                           font=('Calibri', 10))
title_label.pack(side='left', padx=10)

# Close button on title bar to close the application
close_button = ctk.CTkButton(title_bar, text="X", command=root.destroy, fg_color='red', hover_color='dark red',
                             width=30, height=30, font=('Calibri', 15, 'bold'))
close_button.pack(side='right', padx=5, pady=5)
# close_button.pack(side='right')

# Global variables for Excel data and file path
df = None
file_path = None
grosime_dropdown_var = None

# Define colors for active and inactive tabs
active_tab_color = "Green"
inactive_tab_color = "Gray"


# Function to switch between tabs and update their appearance based on active state
def switch_tab(tab):
    global tab1_button, tab2_button
    tab1_frame.pack_forget()
    tab2_frame.pack_forget()
    if tab == 1:
        tab1_frame.pack(fill='both', expand=True)
        tab1_button.configure(fg_color=active_tab_color)
        tab2_button.configure(fg_color=inactive_tab_color)
    else:
        tab2_frame.pack(fill='both', expand=True)
        tab1_button.configure(fg_color=inactive_tab_color)
        tab2_button.configure(fg_color=active_tab_color)


# Function to update the Treeview based on selected 'Tambur' value from dropdown
def on_dropdown_select(*args):
    global df
    selected_tambur = dropdown_var.get()
    if df is not None and selected_tambur:
        filtered_df = df[(df['Tambur'] == selected_tambur) & (df['KG / Rola'] > 0)]
        update_treeview(filtered_df)


# Function to populate the Treeview with data from the DataFrame
def update_treeview(filtered_df):
    tree.delete(*tree.get_children())
    for index, row in filtered_df.iterrows():
        # tree.insert("", tk.END, values=(row['Tambur'], row['KG/Rola'], row['Nr.InternRola'], row['Nr. Rulou']))
        # Convert KG/Rola to integer
        kg_rola_int = int(row['KG / Rola']) if pd.notnull(row['KG / Rola']) else None
        # Insert data into the treeview
        tree.insert("", tk.END, values=(row['Tambur'], kg_rola_int, row['Nr. Intern Rola'],
                                        row.get('Nr. Rulou', '')))

def update_treeview_function(filtered_df):
    for item in tree.get_children():
        tree.delete(item)
    for index, row in filtered_df.iterrows():
        # tree.insert("", tk.END, values=(row['Tambur'], row['KG/Rola'], row['Nr.InternRola'], row['Nr. Rulou']))
        # Convert KG/Rola to integer
        kg_rola_int = int(row['KG / Rola']) if pd.notnull(row['KG / Rola']) else None
        # Insert data into the treeview
        tree.insert("", tk.END, values=(row['Tambur'], kg_rola_int, row['Nr. Intern Rola'],
                                        row.get('Nr. Rulou', '')))
        print("Treview was refreshed")


def open_excel_file():
    global df, file_path
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
    if file_path:
        try:
            df = pd.read_excel(file_path)
            tambur_values = df['Tambur'].unique().tolist()
            create_dropdown(tambur_values)
            # Process the file as needed
        except FileNotFoundError:
            msgbox.showerror("Fisierul nu a fost gasit", "The specified file was not found.")
        except PermissionError:
            msgbox.showerror("Permisiune refuzata", "Verifica daca fisierul nu este deschis pe o alta staie.")
        except pd.errors.EmptyDataError:
            msgbox.showerror("Fisier Gol", "The file is empty.")
        except pd.errors.ParserError:
            msgbox.showerror("Parse Error", "There was an error parsing the file.")
        except Exception as e:
            msgbox.showerror("Eroare", f"Eroare necunoscuta: {e}")


def refresh_excel_file():
    global df, file_path
    if file_path:
        try:
            df = pd.read_excel(file_path)
            # Re-populate the dropdown options
            grosime_values = df['Grosime'].unique().tolist()
            create_grosime_dropdown(grosime_values)
            tambur_values = df['Tambur'].unique().tolist()
            create_dropdown(tambur_values)
            # Update the Treeview
            filtered_df = df[(df['Tambur'] == dropdown_var.get()) & (df['KG / Rola'] > 0)]
            update_treeview(filtered_df)
            print("Excel file refreshed")
        except Exception as e:
            print(f"Failed to refresh Excel data: {e}")
    root.after(60000, refresh_excel_file)  # Schedule the next refresh



# Function to create and position a new dropdown in the placeholder frame
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

def create_grosime_dropdown(values):
    global grosime_dropdown_var, grosime_dropdown  # Ensure grosime_dropdown_var is declared as global

    # Clear previous dropdown content
    # for widget in grosime_dropdown_placeholder.winfo_children():
    #     widget.destroy()

    # Initialize the variable and create the dropdown
    grosime_dropdown_var = tk.StringVar()
    string_values = [str(value) for value in values]  # Convert float values to strings if necessary
    grosime_dropdown = ctk.CTkOptionMenu(grosime_dropdown_placeholder, variable=grosime_dropdown_var, values=string_values)
    grosime_dropdown.pack(fill='x', expand=True)






# Function to update a specific 'KG/Rola' value in the DataFrame and save to the Excel file
def update_kg_rola():
    global df, file_path
    new_kg_rola_value = new_kg_rola_entry.get()
    selected_item = tree.selection()
    if selected_item and file_path:
        selected_row_id = tree.item(selected_item[0], 'values')[2]
        df.loc[df['Nr. Intern Rola'] == selected_row_id, 'KG / Rola'] = float(new_kg_rola_value)
        update_treeview(df[(df['Tambur'] == dropdown_var.get()) & (df['KG / Rola'] > 0)])
        df.to_excel(file_path, index=False)
        print("Data saved to Excel.")
        new_kg_rola_entry.delete(0, tk.END)  # Clear the entry field


# Create and configure tab frames
tab1_frame = ctk.CTkFrame(root)
tab2_frame = ctk.CTkFrame(root)

# Container frame for tab buttons
tabs_container = ctk.CTkFrame(root)
tabs_container.pack(side='top', fill='x')

# Create buttons for switching tabs with initial inactive appearance
tab1_button = ctk.CTkButton(tabs_container, text="Registru Role", command=lambda: switch_tab(1),
                            fg_color=inactive_tab_color)
tab2_button = ctk.CTkButton(tabs_container, text="Registru Rebut", command=lambda: switch_tab(2),
                            fg_color=inactive_tab_color)
tab1_button.pack(side='left', fill='none', expand=True)
tab2_button.pack(side='left', fill='none', expand=True)

# Add Open Excel button to Tab 1
open_excel_button = ctk.CTkButton(tab1_frame, text="Open Excel File", command=open_excel_file)
open_excel_button.pack(pady=10)

# Placeholder frame for dropdown in Tab 1
dropdown_placeholder = ctk.CTkFrame(tab1_frame)
dropdown_placeholder.pack(pady=10)
grosime_dropdown_placeholder = ctk.CTkFrame(tab1_frame)
#grosime_dropdown_placeholder.pack(pady=10)

# Create initial empty dropdown in Tab 1 with a placeholder value
create_dropdown(["Select Tambur"])

# Create entry field for new KG/Rola value
new_kg_rola_var = tk.StringVar()
new_kg_rola_entry = ctk.CTkEntry(tab1_frame, textvariable=new_kg_rola_var, placeholder_text="New KG / Rola")
new_kg_rola_entry.pack(pady=10)

# Create Update button to update KG/Rola value
update_button = ctk.CTkButton(tab1_frame, text="Update KG / Rola", command=update_kg_rola)
update_button.pack(pady=10)

# Initialize the style object
style = ttk.Style()
# Change the background color of the Treeview and its fields
style.configure("Treeview", backgroud="orange", filebackgroud="red", font=('Calibri', 14, 'bold', 'italic'))  # Change font and size for content
style.configure("Treeview.Heading", font=('Calibri', 14, 'bold'))  # Change font and size for headings

# Create Treeview in Tab 1 for displaying data
tree_columns = ("Tambur", "KG / Rola", "Nr. Intern Rola", "Nr. Rulou")
tree = ttk.Treeview(tab1_frame, columns=tree_columns, show='headings')


# Configure the tag for items
tree.tag_configure('oddrow', background='orange')
tree.tag_configure('evenrow', background='red')

for col in tree_columns:
    tree.heading(col, text=col, anchor='center')  # Align text to 'center'
    tree.column(col, anchor='center')  # Ensure the column cells are also aligned to the 'center'
tree.pack(expand=True, fill='both', pady=20, padx=20)

# Create input fields in Tab 2 for additional functionalities
for i in range(1, 3):
    entry_var = tk.StringVar()
    entry = ctk.CTkEntry(tab2_frame, textvariable=entry_var, placeholder_text=f"Input {i}")
    entry.pack(pady=30)

# Initially display Tab 1 by default
switch_tab(1)

# Start the Excel data refresh loop
#refresh_excel_file()

root.after(60000, refresh_excel_file)  # Start the refresh cycle

# Start the GUI loop
root.mainloop()

