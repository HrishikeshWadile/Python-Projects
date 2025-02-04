from tkinter import *
from tkinter import ttk
import cx_Oracle  # Assuming you will handle Oracle connection


class Reservation:
    def __init__(self, roots):
        self.scrollbar_right_details = None
        self.canvas_right_details = None
        self.frame_right_details_content = None
        self.root = roots
        self.root.state("zoomed")

        # Get the screen width and height
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.title("Railway Reservation Database Management System")

        # Set the window size to full screen
        self.root.geometry(f"{self.screen_width}x{self.screen_height}")

        title = Label(self.root, bd=20, relief=RIDGE, text="Railway Reservation Database Management System",
                      font=('Times New Roman', 36, "bold"), fg='red', bg='white')
        title.pack(side=TOP, fill=X)

        # ======================================Dataframe======================================
        self.dataframe = Frame(self.root, bd=20, relief=RIDGE)
        self.dataframe.place(x=0, y=100, width=self.screen_width, height=400)

        # Left Frame with Scrollbar
        self.dataframeleft = LabelFrame(self.dataframe, bd=10, padx=20, relief=RIDGE, font=("Arial", 12, "bold"),
                                        text="Reservation Input Information")
        self.dataframeleft.place(x=0, y=5, width=650, height=275)

        self.canvas_left = Canvas(self.dataframeleft)
        self.scrollbar_left = Scrollbar(self.dataframeleft, orient=VERTICAL, command=self.canvas_left.yview)
        self.canvas_left.configure(yscrollcommand=self.scrollbar_left.set)

        self.scrollbar_left.pack(side=RIGHT, fill=Y)
        self.canvas_left.pack(side=LEFT, fill=BOTH, expand=TRUE)

        self.frame_left_content = Frame(self.canvas_left)
        self.canvas_left.create_window((0, 0), window=self.frame_left_content, anchor="nw")

        self.dataframeleftcorner = LabelFrame(self.dataframe, bd=10, padx=20, relief=RIDGE, font=("Arial", 12, "bold"),
                                              text="New Query")
        self.dataframeleftcorner.place(x=0, y=280, width=650, height=75)

        # Input box for custom SQL query in dataframeleftcorner
        self.query_input = Entry(self.dataframeleftcorner, font=("Arial", 12), width=50)
        self.query_input.grid(row=0, column=0, padx=10, pady=10)

        # Execute button in dataframeleftcorner to execute the query entered in query_input
        execute_btn = Button(self.dataframeleftcorner, text="Execute", font=("Arial", 12, "bold"),
                             command=self.execute_query)
        execute_btn.grid(row=0, column=1, padx=10, pady=0)

        self.dataframerightcorner = LabelFrame(self.dataframe, bd=10, padx=20, relief=RIDGE, font=("Arial", 12, "bold"),
                                               text="Previous fired Query")
        self.dataframerightcorner.place(x=660, y=280, width=830, height=75)

        # Display box for showing executed queries
        self.query_display = Label(self.dataframerightcorner, text="", font=("Arial", 12), anchor="w")
        self.query_display.pack(fill=BOTH, padx=10, pady=10)

        # Bind scrolling
        self.frame_left_content.bind("<Configure>",
                                     lambda e: self.canvas_left.configure(scrollregion=self.canvas_left.bbox("all")))

        # Right Frame with Scrollbar
        self.dataframeright = LabelFrame(self.dataframe, bd=10, padx=20, relief=RIDGE, font=("Arial", 12, "bold"),
                                         text="Reservation Information Display")
        self.dataframeright.place(x=660, y=5, width=830, height=275)

        self.canvas_right = Canvas(self.dataframeright)
        self.scrollbar_right = Scrollbar(self.dataframeright, orient=VERTICAL, command=self.canvas_right.yview)
        self.canvas_right.configure(yscrollcommand=self.scrollbar_right.set)

        self.scrollbar_right.pack(side=RIGHT, fill=Y)
        self.canvas_right.pack(side=LEFT, fill=BOTH, expand=TRUE)

        self.frame_right_content = Frame(self.canvas_right)
        self.canvas_right.create_window((0, 0), window=self.frame_right_content, anchor="nw")

        # Bind scrolling
        self.frame_right_content.bind("<Configure>",
                                      lambda e: self.canvas_right.configure(scrollregion=self.canvas_right.bbox("all")))

        # Details Frame with Scrollbar
        self.detailsframe = Frame(self.root, bd=20, relief=RIDGE)
        self.detailsframe.place(x=0, y=585, width=self.screen_width, height=210)

        self.canvas_details = Canvas(self.detailsframe)
        self.scrollbar_details = Scrollbar(self.detailsframe, orient=VERTICAL, command=self.canvas_details.yview)
        self.canvas_details.configure(yscrollcommand=self.scrollbar_details.set)

        self.scrollbar_details.pack(side=RIGHT, fill=Y)
        self.canvas_details.pack(side=LEFT, fill=BOTH, expand=TRUE)

        self.frame_details_content = Frame(self.canvas_details)
        self.canvas_details.create_window((0, 0), window=self.frame_details_content, anchor="nw")

        # Bind scrolling
        self.frame_details_content.bind("<Configure>", lambda e: self.canvas_details.configure(
            scrollregion=self.canvas_details.bbox("all")))

        # ======================================Buttonframe======================================
        buttonframe = Frame(self.root, bd=20, relief=RIDGE)
        buttonframe.place(x=0, y=500, width=self.screen_width, height=85)

        # Dropdown (Combobox) to select tables (Train, Seat, Payment, etc.)
        self.table_names = ["Passenger", "Train", "Reservation", "Payment", "Seat", "Ticket", "Cancellation", "Route", "Station", "Feedback"]
        self.table_dropdown = ttk.Combobox(buttonframe, values=self.table_names, font=("Arial", 12, "bold"),
                                           state="readonly")
        self.table_dropdown.grid(row=0, column=0, padx=10, pady=10)
        self.table_dropdown.current(0)  # Default selection

        # "Select Table" label for the dropdown
        table_label = Label(buttonframe, text="Select Table", font=("Arial", 12, "bold"))
        table_label.grid(row=0, column=1, padx=10, pady=10)

        # Bind the event to change fields when the table is selected
        self.table_dropdown.bind("<<ComboboxSelected>>", self.update_table_fields)

        # ADD Button
        add_btn = Button(buttonframe, text="Add", font=("Arial", 12, "bold"), command=self.add_data)
        add_btn.grid(row=0, column=2, padx=10, pady=0)

        # UPDATE Button
        update_btn = Button(buttonframe, text="Update", font=("Arial", 12, "bold"), command=self.update_data)
        update_btn.grid(row=0, column=3, padx=10, pady=0)

        # DELETE Button
        delete_btn = Button(buttonframe, text="Delete", font=("Arial", 12, "bold"), command=self.delete_data)
        delete_btn.grid(row=0, column=4, padx=10, pady=0)

        # CLEAR Button (To clear input fields)
        clear_btn = Button(buttonframe, text="Clear", font=("Arial", 12, "bold"), command=self.clear_input_fields)
        clear_btn.grid(row=0, column=5, padx=10, pady=0)

        # ======================================Detailsframe======================================
        self.records_listbox = Listbox(self.frame_details_content, font=("Arial", 12), selectmode=SINGLE)
        self.records_listbox.pack(fill=BOTH, expand=TRUE)
        self.records_listbox.bind("<<ListboxSelect>>", self.show_selected_record)

        # Initialize the UI with the default table (Train)
        self.update_table_fields(None)

    # Function to update UI fields when a different table is selected from the dropdown
    def update_table_fields(self, event):
        # Clear existing fields in left frame and right frame
        for widget in self.frame_left_content.winfo_children():
            widget.destroy()
        for widget in self.frame_right_content.winfo_children():
            widget.destroy()
        for widget in self.frame_details_content.winfo_children():
            widget.destroy()

        selected_table = self.table_dropdown.get()

        # Define fields based on the selected table
        if selected_table == "Passenger":
            fields = ["Passenger ID", "Name", "Address", "Mobile Number", "Date of Birth", "Age", "Gender", "Aadhaar Card", "Nationality", "Special Case"]
        elif selected_table == "Train":
            fields = ["Train ID", "Train Name", "Source", "Destination", "Route", "Class", "Number of Berths", "Type", "Time Duration"]
        elif selected_table == "Reservation":
            fields = ["Reservation ID", "Passenger ID", "Train ID", "Departure Time", "Arrival Time", "Seat Number", "Status", "Reservation Date"]
        elif selected_table == "Payment":
            fields = ["Transaction ID", "Train ID", "Reservation ID", "Passenger ID", "Mode of Pay", "Payment", "Amount"]
        elif selected_table == "Seat":
            fields = ["Seat Number", "Train ID", "Reservation ID", "Seat Class", "Seat Type"]
        elif selected_table == "Ticket":
            fields = ["Ticket ID", "Reservation ID", "Source", "Destination", "Seat Number", "Issue Date", "Coach Number"]
        elif selected_table == "Cancellation":
            fields = ["Cancellation ID", "Reservation ID", "Ticket ID", "Cancellation Date", "Refund Amount", "Refund Date", "Cancellation Fee"]
        elif selected_table == "Route":
            fields = ["Route ID", "Source Station", "Intermidiate Stations", "Destination Station"]
        elif selected_table == "Station":
            fields = ["Stat_Plat(Station ID, Platform ID)", "Station Name", "Station Locaton(state, city)"]
        elif selected_table == "Feedback":
            fields = ["Feedback ID", "Passenger ID", "Train ID", "Feedback Text", "Rating"]
        else:
            fields = []

        # Add labels and entries for the fields in the left frame
        for i, field in enumerate(fields):
            label = Label(self.frame_left_content, text=field, font=("Arial", 12, "bold"))
            label.grid(row=i, column=0, padx=10, pady=5, sticky=W)
            entry = Entry(self.frame_left_content, font=("Arial", 12))
            entry.grid(row=i, column=1, padx=10, pady=5, sticky=W)

        # Add Listbox for displaying records in detailsframe
        self.update_records_listbox(selected_table)

    def update_records_listbox(self, table_name):
        # Check if records_listbox is created before trying to delete items
        if self.records_listbox.winfo_exists():
            # Clear existing records in the listbox
            self.records_listbox.delete(0, END)

            # Dummy data - Replace with actual database retrieval based on the selected table
            records = [
                f"{table_name} Record 1",
                f"{table_name} Record 2",
                f"{table_name} Record 3"
            ]

            for record in records:
                self.records_listbox.insert(END, record)


        else:
            print("Listbox does not exist.")

        # Update the detailsframe based on the selected table
        self.update_details_frame(table_name)

    # Function to execute the custom query entered in query_input
    def execute_query(self):
        query = self.query_input.get()
        if query:
            try:
                # Execute custom SQL query here
                # For example: cursor.execute(query) for Oracle
                # conn.commit()
                self.query_display.config(text=f"Executed Query: {query}")
            except Exception as e:
                self.query_display.config(text=f"Error: {e}")

    def update_details_frame(self, table_name):
        # Clear existing widgets in the details frame
        for widget in self.frame_details_content.winfo_children():
            widget.destroy()

        # Define the columns to display in details frame based on the selected table
        if table_name == "Train":
            columns = ["Train ID", "Train Name", "Source", "Destination", "Route", "Class", "No. of Seats"]
        elif table_name == "Seat":
            columns = ["Seat ID", "Train ID", "Seat Number", "Seat Class"]
        elif table_name == "Payment":
            columns = ["Transaction ID", "Train ID", "Reservation ID", "Passenger ID", "Mode of Pay", "Payment",
                       "Amount"]
        elif table_name == "Reservation":
            columns = ["Reservation ID", "Passenger ID", "Train ID", "Departure Time", "Destination Time", "Seat"]
        elif table_name == "Passenger":
            columns = ["Passenger ID", "Name", "Address", "Mob No", "DOB", "Age", "Gender", "Aadhaar Card"]
        else:
            columns = []

        # Add labels for columns in the details frame
        for i, column in enumerate(columns):
            label = Label(self.frame_details_content, text=column, font=("Arial", 12, "bold"), relief=RIDGE, width=15)
            label.grid(row=0, column=i, padx=2, pady=2)

        # Display dummy data for now (replace with actual data retrieval logic)
        for j in range(1, 4):  # Example with 3 rows
            for i, column in enumerate(columns):
                value = f"{column} {j}"  # Dummy value, replace with actual data
                label = Label(self.frame_details_content, text=value, font=("Arial", 12), relief=RIDGE, width=15)
                label.grid(row=j, column=i, padx=2, pady=2)

    def show_selected_record(self, event):
        selected_index = self.records_listbox.curselection()
        if selected_index:
            selected_record = self.records_listbox.get(selected_index)
            # Placeholder for record details
            details = f"Details for {selected_record}"
            self.display_reservation_info(details)

    def display_reservation_info(self, details):
        # Clear existing details in the right frame
        for widget in self.dataframeright.winfo_children():
            widget.destroy()

        # Add Canvas and Scrollbar to the right frame (dataframeright)
        self.canvas_right_details = Canvas(self.dataframeright)
        self.scrollbar_right_details = Scrollbar(self.dataframeright, orient=VERTICAL,
                                                 command=self.canvas_right_details.yview)
        self.canvas_right_details.configure(yscrollcommand=self.scrollbar_right_details.set)

        self.scrollbar_right_details.pack(side=RIGHT, fill=Y)
        self.canvas_right_details.pack(side=LEFT, fill=BOTH, expand=TRUE)

        # Create a new frame inside the canvas to hold the record details
        self.frame_right_details_content = Frame(self.canvas_right_details)
        self.canvas_right_details.create_window((0, 0), window=self.frame_right_details_content, anchor="nw")

        # Bind scrolling to the frame's size
        self.frame_right_details_content.bind("<Configure>", lambda e: self.canvas_right_details.configure(
            scrollregion=self.canvas_right_details.bbox("all")))

        # Adding a placeholder label for the selected record details
        details_label = Label(self.frame_right_details_content, text=details, font=("Arial", 12), anchor="w",
                              justify=LEFT)
        details_label.pack(pady=10)

        # Add more labels or widgets to display additional detailed information
        # For example:
        for i in range(20):  # Example for long details, can be replaced with actual data
            additional_detail = Label(self.frame_right_details_content, text=f"Additional Info {i + 1}",
                                      font=("Arial", 12), anchor="w", justify=LEFT)
            additional_detail.pack(pady=5)

    def add_data(self):
        print("Add button clicked")
        # Implement logic to add data to the selected table

    def update_data(self):
        print("Update button clicked")
        # Implement logic to update data in the selected table

    def delete_data(self):
        print("Delete button clicked")
        # Implement logic to delete data from the selected table

    def clear_input_fields(self):
        for field, entry in self.dynamic_fields.items():
            entry.delete(0, END)


if __name__ == "__main__":
    root = Tk()
    application = Reservation(root)
    root.mainloop()
