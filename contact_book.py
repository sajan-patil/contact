import tkinter as tk
from tkinter import messagebox, simpledialog
import tkinter.ttk as ttk

# ========== Data and Functions ==========

contacts = []

def refresh_contacts():
    contact_list.delete(*contact_list.get_children())
    for i, contact in enumerate(contacts):
        contact_list.insert("", "end", iid=i, values=(contact['name'], contact['phone']))

def add_contact():
    name = entry_name.get()
    phone = entry_phone.get()
    email = entry_email.get()
    address = entry_address.get()

    if not name or not phone:
        messagebox.showwarning("Missing Info", "Name and Phone are required.")
        return

    contacts.append({"name": name, "phone": phone, "email": email, "address": address})
    refresh_contacts()
    clear_fields()
    messagebox.showinfo("Success", "Contact added successfully.")

def search_contact():
    query = simpledialog.askstring("Search", "Enter Name or Phone Number:")
    if not query:
        return

    found = False
    for i, contact in enumerate(contacts):
        if query.lower() in contact["name"].lower() or query in contact["phone"]:
            contact_list.selection_set(i)
            contact_list.focus(i)
            found = True
            break

    if not found:
        messagebox.showinfo("Not Found", "No matching contact found.")

def update_contact():
    selected = contact_list.focus()
    if not selected:
        messagebox.showwarning("No Selection", "Please select a contact to update.")
        return

    index = int(selected)
    contacts[index] = {
        "name": entry_name.get(),
        "phone": entry_phone.get(),
        "email": entry_email.get(),
        "address": entry_address.get()
    }
    refresh_contacts()
    clear_fields()
    messagebox.showinfo("Updated", "Contact updated successfully.")

def delete_contact():
    selected = contact_list.focus()
    if not selected:
        messagebox.showwarning("No Selection", "Please select a contact to delete.")
        return

    index = int(selected)
    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this contact?")
    if confirm:
        contacts.pop(index)
        refresh_contacts()
        clear_fields()

def show_details(event):
    selected = contact_list.focus()
    if not selected:
        return

    index = int(selected)
    contact = contacts[index]

    entry_name.delete(0, tk.END)
    entry_name.insert(0, contact['name'])

    entry_phone.delete(0, tk.END)
    entry_phone.insert(0, contact['phone'])

    entry_email.delete(0, tk.END)
    entry_email.insert(0, contact['email'])

    entry_address.delete(0, tk.END)
    entry_address.insert(0, contact['address'])

def clear_fields():
    entry_name.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_address.delete(0, tk.END)

# ========== UI Setup ==========

root = tk.Tk()
root.title("📒 Contact Book")
root.geometry("650x540")
root.config(bg="#e3f2fd")

style = ttk.Style()
style.configure("Treeview", font=("Segoe UI", 11), rowheight=28)
style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))
style.map("Treeview", background=[("selected", "#90caf9")])

# Top Frame
frame_top = tk.Frame(root, bg="#e3f2fd")
frame_top.pack(pady=15)

label_font = ("Segoe UI", 11)

tk.Label(frame_top, text="Name", font=label_font, bg="#e3f2fd").grid(row=0, column=0, padx=8, pady=4, sticky="e")
entry_name = tk.Entry(frame_top, width=28, font=("Segoe UI", 11))
entry_name.grid(row=0, column=1, pady=4)

tk.Label(frame_top, text="Phone", font=label_font, bg="#e3f2fd").grid(row=1, column=0, padx=8, pady=4, sticky="e")
entry_phone = tk.Entry(frame_top, width=28, font=("Segoe UI", 11))
entry_phone.grid(row=1, column=1, pady=4)

tk.Label(frame_top, text="Email", font=label_font, bg="#e3f2fd").grid(row=2, column=0, padx=8, pady=4, sticky="e")
entry_email = tk.Entry(frame_top, width=28, font=("Segoe UI", 11))
entry_email.grid(row=2, column=1, pady=4)

tk.Label(frame_top, text="Address", font=label_font, bg="#e3f2fd").grid(row=3, column=0, padx=8, pady=4, sticky="e")
entry_address = tk.Entry(frame_top, width=28, font=("Segoe UI", 11))
entry_address.grid(row=3, column=1, pady=4)

# Button Frame
frame_buttons = tk.Frame(root, bg="#e3f2fd")
frame_buttons.pack(pady=12)

def create_btn(text, cmd, color):
    return tk.Button(frame_buttons, text=text, command=cmd, font=("Segoe UI", 10), bg=color, fg="white", width=14)

create_btn("➕ Add Contact", add_contact, "#43a047").grid(row=0, column=0, padx=6)
create_btn("✏️ Update", update_contact, "#0288d1").grid(row=0, column=1, padx=6)
create_btn("❌ Delete", delete_contact, "#e53935").grid(row=0, column=2, padx=6)
create_btn("🔍 Search", search_contact, "#6a1b9a").grid(row=0, column=3, padx=6)
create_btn("🧹 Clear Fields", clear_fields, "#546e7a").grid(row=0, column=4, padx=6)

# Treeview
columns = ("Name", "Phone")
contact_list = ttk.Treeview(root, columns=columns, show="headings", height=8)
contact_list.heading("Name", text="Name")
contact_list.heading("Phone", text="Phone")
contact_list.bind("<<TreeviewSelect>>", show_details)
contact_list.pack(padx=20, fill="x", pady=10)

# Footer
tk.Label(root, text="© Contact Book App", font=("Segoe UI", 9), bg="#e3f2fd", fg="#555").pack(pady=5)

# Launch App
root.mainloop()
