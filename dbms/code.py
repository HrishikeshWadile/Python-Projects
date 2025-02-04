import cx_Oracle
from tkinter import *
from tkinter import ttk

class OnlineShoppingSystem:
    def _init_(self, master):
        self.master = master
        self.master.title("Online Shopping System")
        self.master.geometry("800x600")

        # Frame for Table Selection
        self.frame_table_selection = Frame(self.master)
        self.frame_table_selection.pack(pady=10)

        self.table_label = Label(self.frame_table_selection, text="Select Table:")
        self.table_label.pack(side=LEFT)

        self.table_dropdown = ttk.Combobox(self.frame_table_selection,
                                            values=["Customer", "Product", "Order", "OrderItem", "Payment"])
        self.table_dropdown.pack(side=LEFT)
        self.table_dropdown.bind("<<ComboboxSelected>>", self.update_table_fields)

        # Frame for Input Fields
        self.frame_input = Frame(self.master)
        self.frame_input.pack(pady=10)

        self.frame_input_content = Frame(self.frame_input)
        self.frame_input_content.pack(side=LEFT)

        # Frame for Buttons
        self.frame_buttons = Frame(self.master)
        self.frame_buttons.pack(pady=10)

        self.add_button = Button(self.frame_buttons, text="Add", command=self.add_data)
        self.add_button.pack(side=LEFT, padx=10)

        self.update_button = Button(self.frame_buttons, text="Update", command=self.update_data)
        self.update_button.pack(side=LEFT, padx=10)

        self.delete_button = Button(self.frame_buttons, text="Delete", command=self.delete_data)
        self.delete_button.pack(side=LEFT, padx=10)

        # Frame for Results
        self.frame_results = Frame(self.master)
        self.frame_results.pack(pady=10)

        self.details = ttk.Treeview(self.frame_results, columns=(), show='headings')
        self.details.pack(side=LEFT)

        self.scrollbar = Scrollbar(self.frame_results, orient="vertical", command=self.details.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.details.configure(yscrollcommand=self.scrollbar.set)

        self.query_display = Label(self.master, text="", font=("Arial", 12))
        self.query_display.pack(pady=10)

        self.selected_table = None

    def update_table_fields(self, event):
        # Clear existing input fields
        for widget in self.frame_input_content.winfo_children():
            widget.destroy()

        selected_table = self.table_dropdown.get()
        self.selected_table = selected_table

        # Define fields based on selected table
        if selected_table == "Customer":
            fields = ["Customer ID", "Name", "Email", "Address"]
        elif selected_table == "Product":
            fields = ["Product ID", "Product Name", "Price", "Stock"]
        elif selected_table == "Order":
            fields = ["Order ID", "Customer ID", "Order Date", "Status"]
        elif selected_table == "OrderItem":
            fields = ["Order Item ID", "Order ID", "Product ID", "Quantity"]
        elif selected_table == "Payment":
            fields = ["Payment ID", "Order ID", "Amount", "Payment Date", "Payment Method"]
        else:
            fields = []

        # Add labels and entries for the fields in the input frame
        for i, field in enumerate(fields):
            label = Label(self.frame_input_content, text=field, font=("Arial", 12))
            label.grid(row=i, column=0, padx=10, pady=5, sticky=W)
            entry = Entry(self.frame_input_content, font=("Arial", 12))
            entry.grid(row=i, column=1, padx=10, pady=5, sticky=W)

        # Update records listbox
        self.update_records_listbox()

    def update_records_listbox(self):
        # Clear existing columns
        self.details["columns"] = []
        self.details.delete(*self.details.get_children())

        if self.selected_table == "Customer":
            self.details["columns"] = ("customer_id", "name", "email", "address")
            self.details.heading("customer_id", text="Customer ID")
            self.details.heading("name", text="Name")
            self.details.heading("email", text="Email")
            self.details.heading("address", text="Address")

        elif self.selected_table == "Product":
            self.details["columns"] = ("product_id", "product_name", "price", "stock")
            self.details.heading("product_id", text="Product ID")
            self.details.heading("product_name", text="Product Name")
            self.details.heading("price", text="Price")
            self.details.heading("stock", text="Stock")

        elif self.selected_table == "Order":
            self.details["columns"] = ("order_id", "customer_id", "order_date", "status")
            self.details.heading("order_id", text="Order ID")
            self.details.heading("customer_id", text="Customer ID")
            self.details.heading("order_date", text="Order Date")
            self.details.heading("status", text="Status")

        elif self.selected_table == "OrderItem":
            self.details["columns"] = ("order_item_id", "order_id", "product_id", "quantity")
            self.details.heading("order_item_id", text="Order Item ID")
            self.details.heading("order_id", text="Order ID")
            self.details.heading("product_id", text="Product ID")
            self.details.heading("quantity", text="Quantity")

        elif self.selected_table == "Payment":
            self.details["columns"] = ("payment_id", "order_id", "amount", "payment_date", "payment_method")
            self.details.heading("payment_id", text="Payment ID")
            self.details.heading("order_id", text="Order ID")
            self.details.heading("amount", text="Amount")
            self.details.heading("payment_date", text="Payment Date")
            self.details.heading("payment_method", text="Payment Method")

        # Update
