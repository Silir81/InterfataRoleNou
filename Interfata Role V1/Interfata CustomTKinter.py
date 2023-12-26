import customtkinter as ctk

# Initialize the main window
root = ctk.CTk()
root.title("CustomTkinter GUI")
root.geometry("800x600")

# Create a CTkNotebook widget
notebook = ctk.CTkNotebook(root)
notebook.pack(expand=True, fill="both", padx=10, pady=10)

# Create the first tab
tab1 = ctk.CTkFrame(notebook)
notebook.add(tab1, text="First Tab")

# Create Buttons
button1 = ctk.CTkButton(root, text="Button 1")
button1.pack(pady=10)

button2 = ctk.CTkButton(root, text="Button 2")
button2.pack(pady=10)

button3 = ctk.CTkButton(root, text="Button 3")
button3.pack(pady=10)

button4 = ctk.CTkButton(root, text="Button 4")
button4.pack(pady=10)

# Create Dropdown Menus
dropdown1 = ctk.CTkOptionMenu(root, values=["Option 1", "Option 2", "Option 3"])
dropdown1.pack(pady=10)

dropdown2 = ctk.CTkOptionMenu(root, values=["Choice 1", "Choice 2", "Choice 3"])
dropdown2.pack(pady=10)

# Create a Treeview as a display area with four columns
columns = ("Column 1", "Column 2", "Column 3", "Column 4")
display_area = ttk.Treeview(root, columns=columns, show="headings")

# Define headings
for col in columns:
    display_area.heading(col, text=col)

# Add some sample data
for i in range(10):
    display_area.insert("", "end", values=(f"Data {i+1}", f"Info {i+1}", f"Detail {i+1}", f"More {i+1}"))

display_area.pack(expand=True, fill="both")

# Add content to the first tab (e.g., buttons, dropdowns)
# ...

# Create the second tab
tab2 = ctk.CTkFrame(notebook)
notebook.add(tab2, text="Second Tab")

# Add input fields to the second tab
label1 = ctk.CTkLabel(tab2, text="Input 1")
label1.pack(pady=(10, 0))
entry1 = ctk.CTkEntry(tab2)
entry1.pack(pady=(0, 10))

label2 = ctk.CTkLabel(tab2, text="Input 2")
label2.pack(pady=(10, 0))
entry2 = ctk.CTkEntry(tab2)
entry2.pack(pady=(0, 10))

label3 = ctk.CTkLabel(tab2, text="Input 3")
label3.pack(pady=(10, 0))
entry3 = ctk.CTkEntry(tab2)
entry3.pack(pady=(0, 10))

label4 = ctk.CTkLabel(tab2, text="Input 4")
label4.pack(pady=(10, 0))
entry4 = ctk.CTkEntry(tab2)
entry4.pack(pady=(0, 10))

root.mainloop()
