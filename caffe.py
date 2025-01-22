import tkinter as tk
from tkinter import messagebox, font
import qrcode
from PIL import Image, ImageTk

# Menu dictionary
menu = {
    'Pizza': {
        'Margherita': 99,
        'Pepperoni': 120,
        'Veggie': 110,
    },
    'Coffee': {
        'Hot Coffee': 70,
        'Cold Coffee': 80,
        'Espresso': 90,
    },
    'Burger': {
        'Beef Burger': 150,
        'Chicken Burger': 140,
        'Veggie Burger': 120,
    },
    'Desserts': {
        'Brownie': 60,
        'Cheesecake': 80,
        'Tiramisu': 90,
    }
}

order_total = 0
order_list = []

# Function to update item options when a category is selected
def update_items(event):
    selected_category = category_var.get()
    item_menu['menu'].delete(0, 'end')
    if selected_category in menu:
        for item in menu[selected_category]:
            item_menu['menu'].add_command(label=item, command=lambda value=item: item_var.set(value))

# Function to add item to the order
def add_to_order():
    global order_total, order_list
    selected_category = category_var.get()
    selected_item = item_var.get()

    if selected_category and selected_item:
        price = menu[selected_category].get(selected_item, 0)
        order_total += price
        order_list.append(f"{selected_item} - Rs{price}")
        messagebox.showinfo("Item Added", f"'{selected_item}' has been added to your order.")
        update_order_display()
    else:
        messagebox.showwarning("Selection Error", "Please select a category and an item!")

# Function to update the order display
def update_order_display():
    order_display.config(state='normal')
    order_display.delete(1.0, tk.END)
    if order_list:
        order_display.insert(tk.END, "\n".join(order_list))
        order_display.insert(tk.END, f"\n\nTotal: Rs{order_total}")
    else:
        order_display.insert(tk.END, "Your order is empty.")
    order_display.config(state='disabled')

# Function to confirm the order and generate QR code
def confirm_order():
    if order_list:
        qr_data = f"Order Details:\n{', '.join(order_list)}\nTotal: Rs{order_total}"
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(qr_data)
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')
        img.save("payment_qr.png")

        # Display the QR code
        qr_window = tk.Toplevel(root)
        qr_window.title("Payment QR Code")
        qr_window.geometry("300x400")
        qr_window.configure(bg="#f9f9f9")

        qr_label = tk.Label(qr_window, text="Scan to Pay", font=('Helvetica', 16), bg="#f9f9f9")
        qr_label.pack(pady=10)

        qr_img = ImageTk.PhotoImage(Image.open("payment_qr.png"))
        qr_display = tk.Label(qr_window, image=qr_img, bg="#f9f9f9")
        qr_display.image = qr_img
        qr_display.pack(pady=10)

        qr_window.mainloop()
    else:
        messagebox.showwarning("Order Error", "Your order is empty!")

# Function to reset the order
def reset_order():
    global order_total, order_list
    order_total = 0
    order_list = []
    update_order_display()

# GUI Setup
root = tk.Tk()
root.title(" Golden Saffron Cafe Menu")
root.geometry("450x600")
root.configure(bg="#f4f4f4")

# Fonts
title_font = font.Font(family="Helvetica", size=20, weight="bold")
label_font = font.Font(family="Helvetica", size=12)
button_font = font.Font(family="Helvetica", size=10, weight="bold")

# Title
title_label = tk.Label(root, text="Saffron Cafe Menu", font=title_font, bg="#ffcc00", fg="white", pady=10)
title_label.pack(fill=tk.X)

# Category dropdown
category_var = tk.StringVar()
category_var.set("Select a category")
category_label = tk.Label(root, text="Category:", font=label_font, bg="#f4f4f4")
category_label.pack(pady=5)
category_menu = tk.OptionMenu(root, category_var, *menu.keys(), command=update_items)
category_menu.pack(pady=5)

# Item dropdown
item_var = tk.StringVar()
item_var.set("Select an item")
item_label = tk.Label(root, text="Item:", font=label_font, bg="#f4f4f4")
item_label.pack(pady=5)
item_menu = tk.OptionMenu(root, item_var, [])
item_menu.pack(pady=5)

# Add to Order Button
add_button = tk.Button(root, text="Add to Order", command=add_to_order, font=button_font, bg="#007acc", fg="white")
add_button.pack(pady=10)

# Order Display
order_label = tk.Label(root, text="Your Order:", font=label_font, bg="#f4f4f4")
order_label.pack(pady=5)
order_display = tk.Text(root, height=10, width=40, state='disabled', bg="#ffffff", fg="black")
order_display.pack(pady=10)

# Confirm and Reset Buttons
button_frame = tk.Frame(root, bg="#f4f4f4")
button_frame.pack(pady=10)

confirm_button = tk.Button(button_frame, text="Confirm Order", command=confirm_order, font=button_font, bg="#28a745", fg="white")
confirm_button.pack(side=tk.LEFT, padx=10)

reset_button = tk.Button(button_frame, text="Reset Order", command=reset_order, font=button_font, bg="#dc3545", fg="white")
reset_button.pack(side=tk.RIGHT, padx=10)

# Start the GUI loop
root.mainloop()
