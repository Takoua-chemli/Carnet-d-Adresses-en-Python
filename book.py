import sqlite3
from tkinter import *
from tkinter import messagebox, ttk

# Function to refresh the table
def refresh_table():
    cursor.execute("SELECT * FROM contacts")
    rows = cursor.fetchall()
    tree.delete(*tree.get_children())
    for row in rows:
        # Assurez-vous que les données sont insérées dans les colonnes correctes
        tree.insert('', 'end', values=(row[0], row[1], row[2], row[3]))

# Function to add a contact
def add_contact():
    if name_entry.get() == "" or address_entry.get() == "" or phone_entry.get() == "":
        messagebox.showerror("Error", "Please fill all the fields")
    else:
        cursor.execute("INSERT INTO contacts (name, address, phone) VALUES (?, ?, ?)",
                       (name_entry.get(), address_entry.get(), phone_entry.get()))
        conn.commit()
        messagebox.showinfo("Success", "Contact added successfully")
        refresh_table()

# Function to delete a contact
def delete_contact():
    selected_item = tree.selection()
    if len(selected_item) > 0:
        cursor.execute("DELETE FROM contacts WHERE id = ?", (tree.item(selected_item)['values'][0],))
        conn.commit()
        messagebox.showinfo("Success", "Contact deleted successfully")
        refresh_table()

# Function to modify contact details
def modify_contact():
    selected_item = tree.selection()
    if len(selected_item) > 0:
        id_to_modify = tree.item(selected_item)['values'][0]
        new_name = input("Enter new name: ")  # You can replace this with an Entry widget for user input
        new_address = input("Enter new address: ")
        new_phone = input("Enter new phone: ")

        cursor.execute("UPDATE contacts SET name=?, address=?, phone=? WHERE id=?",
                       (new_name, new_address, new_phone, id_to_modify))
        conn.commit()
        messagebox.showinfo("Success", "Contact modified successfully")
        refresh_table()

# Create the database and table
conn = sqlite3.connect('addressbook.db')
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS contacts (id INTEGER PRIMARY KEY, name TEXT, address TEXT, phone TEXT)")

# Create the Tkinter GUI
window = Tk()
window.title("Address Book")

# Create the entry fields
name_label = Label(window, text="Nom:")
name_entry = Entry(window)

address_label = Label(window, text="Adresse Email:")
address_entry = Entry(window)

phone_label = Label(window, text="Téléphone:")
phone_entry = Entry(window)

# Create the table
tree = ttk.Treeview(window, columns=('id', 'name', 'address', 'phone'), show='headings')
tree.heading('id', text='ID')
tree.heading('name', text='Nom')
tree.heading('address', text='Adresse Email')
tree.heading('phone', text='Téléphone')

# Create the buttons
add_button = Button(window, text="Add", command=add_contact)
delete_button = Button(window, text="Delete", command=delete_contact)
modify_button = Button(window, text="Modify", command=modify_contact)

# Pack the GUI elements
name_label.grid(row=0, column=0)
name_entry.grid(row=0, column=1)

address_label.grid(row=1, column=0)
address_entry.grid(row=1, column=1)

phone_label.grid(row=3, column=0)
phone_entry.grid(row=3, column=1)

tree.grid(row=0, column=2, rowspan=4)

add_button.grid(row=4, column=0)
delete_button.grid(row=4, column=1)
modify_button.grid(row=4, column=2)

# Refresh the table
refresh_table()

# Run the Tkinter event loop
window.mainloop()

# Close the database connection
conn.close()