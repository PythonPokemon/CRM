import sqlite3
import tkinter as tk
from tkinter import messagebox

# Verbindung zur Datenbank herstellen (oder eine neue erstellen, falls sie nicht existiert)
conn = sqlite3.connect("crm_system.db")

# Erstellen einer Tabelle, um die Aufgaben zu speichern, falls sie noch nicht existiert
conn.execute('''CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_name TEXT NOT NULL,
                priority TEXT,
                comment TEXT
            )''')

# Erstellen einer Tabelle, um Kundeninformationen zu speichern, falls sie noch nicht existiert
conn.execute('''CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT,
                phone TEXT,
                email TEXT
            )''')

# Funktion zum Hinzufügen einer Aufgabe zur Datenbank
def add_task():
    task = entry_task.get()
    priority = var_priority.get()
    comment = entry_comment.get("1.0", tk.END).strip()  # Kommentar aus dem Textfeld erhalten
    conn.execute("INSERT INTO tasks (task_name, priority, comment) VALUES (?, ?, ?)", (task, priority, comment))
    conn.commit()
    messagebox.showinfo("Aufgabe hinzugefügt", f"Aufgabe hinzugefügt: {task}, Priorität: {priority}")
    show_tasks()

# Funktion zum Anzeigen der Aufgaben aus der Datenbank
def show_tasks():
    cursor = conn.execute("SELECT id, task_name, priority, comment FROM tasks")
    task_list.delete(0, tk.END)
    for row in cursor:
        task_list.insert(tk.END, f"{row[0]}. {row[1]} - Priorität: {row[2]} - Kommentar: {row[3]}")

# Funktion zum Entfernen einer Aufgabe aus der Datenbank
def remove_task():
    index = task_list.curselection()
    if index:
        index = int(index[0]) + 1
        cursor = conn.execute("SELECT id, task_name, priority, comment FROM tasks")
        tasks = cursor.fetchall()

        if 1 <= index <= len(tasks):
            removed_task = tasks[index - 1]
            conn.execute("DELETE FROM tasks WHERE id=?", (removed_task[0],))
            conn.commit()
            messagebox.showinfo("Aufgabe entfernt", f"Aufgabe entfernt: {removed_task[1]}")
            show_tasks()

# Funktion zum Bearbeiten einer Aufgabe in der Datenbank
def edit_task():
    index = task_list.curselection()
    if index:
        index = int(index[0]) + 1
        cursor = conn.execute("SELECT id, task_name, priority, comment FROM tasks")
        tasks = cursor.fetchall()

        if 1 <= index <= len(tasks):
            edited_task = tasks[index - 1]
            new_task_name = entry_task.get()
            new_priority = var_priority.get()
            new_comment = entry_comment.get("1.0", tk.END).strip()  # Aktualisierten Kommentar erhalten
            conn.execute("UPDATE tasks SET task_name=?, priority=?, comment=? WHERE id=?", 
                         (new_task_name, new_priority, new_comment, edited_task[0]))
            conn.commit()
            messagebox.showinfo("Aufgabe bearbeitet", f"Aufgabe bearbeitet: {new_task_name}, Priorität: {new_priority}")
            show_tasks()

# Funktion zum Hinzufügen eines Kunden zur Datenbank
def add_customer():
    name = entry_name.get()
    address = entry_address.get()
    phone = entry_phone.get()
    email = entry_email.get()
    conn.execute("INSERT INTO customers (name, address, phone, email) VALUES (?, ?, ?, ?)", (name, address, phone, email))
    conn.commit()
    messagebox.showinfo("Kunde hinzugefügt", f"Kunde hinzugefügt: {name}")
    show_customers()

# Funktion zum Anzeigen der Kunden aus der Datenbank
def show_customers():
    cursor = conn.execute("SELECT id, name, address, phone, email FROM customers")
    customer_list.delete(0, tk.END)
    for row in cursor:
        customer_list.insert(tk.END, f"{row[0]}. {row[1]} - {row[2]}, {row[3]}, {row[4]}")

# Funktion zum Entfernen eines Kunden aus der Datenbank
def remove_customer():
    index = customer_list.curselection()
    if index:
        index = int(index[0]) + 1
        cursor = conn.execute("SELECT id, name, address, phone, email FROM customers")
        customers = cursor.fetchall()

        if 1 <= index <= len(customers):
            removed_customer = customers[index - 1]
            conn.execute("DELETE FROM customers WHERE id=?", (removed_customer[0],))
            conn.commit()
            messagebox.showinfo("Kunde entfernt", f"Kunde entfernt: {removed_customer[1]}")
            show_customers()

# Funktion zum Bearbeiten eines Kunden in der Datenbank
def edit_customer():
    index = customer_list.curselection()
    if index:
        index = int(index[0]) + 1
        cursor = conn.execute("SELECT id, name, address, phone, email FROM customers")
        customers = cursor.fetchall()

        if 1 <= index <= len(customers):
            edited_customer = customers[index - 1]
            new_name = entry_name.get()
            new_address = entry_address.get()
            new_phone = entry_phone.get()
            new_email = entry_email.get()
            conn.execute("UPDATE customers SET name=?, address=?, phone=?, email=? WHERE id=?", 
                         (new_name, new_address, new_phone, new_email, edited_customer[0]))
            conn.commit()
            messagebox.showinfo("Kunde bearbeitet", f"Kunde bearbeitet: {new_name}")
            show_customers()

# Funktion für die Suchfunktion nach Aufgaben
def search_tasks():
    keyword = entry_search.get()
    cursor = conn.execute("SELECT id, task_name, priority, comment FROM tasks WHERE task_name LIKE ?", ('%' + keyword + '%',))
    task_list.delete(0, tk.END)
    for row in cursor:
        task_list.insert(tk.END, f"{row[0]}. {row[1]} - Priorität: {row[2]} - Kommentar: {row[3]}")

# Funktion für die Suchfunktion nach Kunden
def search_customers():
    keyword = entry_search.get()
    cursor = conn.execute("SELECT id, name, address, phone, email FROM customers WHERE name LIKE ?", ('%' + keyword + '%',))
    customer_list.delete(0, tk.END)
    for row in cursor:
        customer_list.insert(tk.END, f"{row[0]}. {row[1]} - {row[2]}, {row[3]}, {row[4]}")

# Tkinter GUI erstellen
root = tk.Tk()
root.title("CRM-System")

frame_task = tk.Frame(root)
frame_task.pack(padx=20, pady=10)

label_task = tk.Label(frame_task, text="Aufgabe:")
label_task.pack(side=tk.LEFT)

entry_task = tk.Entry(frame_task, width=30)
entry_task.pack(side=tk.LEFT)

label_priority = tk.Label(frame_task, text="Priorität:")
label_priority.pack(side=tk.LEFT)

var_priority = tk.StringVar()
var_priority.set("Niedrig")
option_menu_priority = tk.OptionMenu(frame_task, var_priority, "Niedrig", "Mittel", "Hoch")
option_menu_priority.pack(side=tk.LEFT)

label_comment = tk.Label(frame_task, text="Kommentar:")
label_comment.pack(side=tk.LEFT)

entry_comment = tk.Text(frame_task, width=30, height=3)
entry_comment.pack(side=tk.LEFT)

btn_add_task = tk.Button(frame_task, text="Hinzufügen", command=add_task)
btn_add_task.pack(side=tk.LEFT, padx=10)

btn_remove_task = tk.Button(frame_task, text="Entfernen", command=remove_task)
btn_remove_task.pack(side=tk.LEFT)

btn_edit_task = tk.Button(frame_task, text="Bearbeiten", command=edit_task)
btn_edit_task.pack(side=tk.LEFT)

task_list = tk.Listbox(root, width=200, height=10)
task_list.pack(padx=20, pady=10)

show_tasks()

frame_customer = tk.Frame(root)
frame_customer.pack(padx=20, pady=10)

label_name = tk.Label(frame_customer, text="Name:")
label_name.pack(side=tk.LEFT)

entry_name = tk.Entry(frame_customer, width=30)
entry_name.pack(side=tk.LEFT)

label_address = tk.Label(frame_customer, text="Adresse:")
label_address.pack(side=tk.LEFT)

entry_address = tk.Entry(frame_customer, width=30)
entry_address.pack(side=tk.LEFT)

label_phone = tk.Label(frame_customer, text="Telefon:")
label_phone.pack(side=tk.LEFT)

entry_phone = tk.Entry(frame_customer, width=30)
entry_phone.pack(side=tk.LEFT)

label_email = tk.Label(frame_customer, text="E-Mail:")
label_email.pack(side=tk.LEFT)

entry_email = tk.Entry(frame_customer, width=30)
entry_email.pack(side=tk.LEFT)

btn_add_customer = tk.Button(frame_customer, text="Kunde hinzufügen", command=add_customer)
btn_add_customer.pack(side=tk.LEFT, padx=10)

btn_remove_customer = tk.Button(frame_customer, text="Kunde entfernen", command=remove_customer)
btn_remove_customer.pack(side=tk.LEFT)

btn_edit_customer = tk.Button(frame_customer, text="Kunde bearbeiten", command=edit_customer)
btn_edit_customer.pack(side=tk.LEFT)

customer_list = tk.Listbox(root, width=200, height=10)
customer_list.pack(padx=20, pady=10)

show_customers()

frame_search = tk.Frame(root)
frame_search.pack(padx=20, pady=10)

entry_search = tk.Entry(frame_search, width=30)
entry_search.pack(side=tk.LEFT)

btn_search_tasks = tk.Button(frame_search, text="Suchen (Aufgaben)", command=search_tasks)
btn_search_tasks.pack(side=tk.LEFT, padx=10)

btn_search_customers = tk.Button(frame_search, text="Suchen (Kunden)", command=search_customers)
btn_search_customers.pack(side=tk.LEFT)

root.mainloop()
