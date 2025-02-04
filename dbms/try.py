from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import cx_Oracle

global cursor, connection


def return_fields(selected_table):
    if selected_table == "Passenger":
        fields = ["passenger_id", "passenger_name", "address", "mobile_number", "date_of_birth", "age", "gender",
                  "aadhaar_card", "nationality", "special_case"]
    elif selected_table == "Train":
        fields = ["train_id", "train_name", "source_id", "destination_id", "route_id", "train_class",
                  "number_of_berths", "train_type", "time_duration"]
    elif selected_table == "Reservation":
        fields = ["reservation_id", "passenger_id", "train_id", "departure_time", "arrival_time", "train_seat_key",
                  "status", "reservation_date"]
    elif selected_table == "Payment":
        fields = ["transaction_id", "train_id", "reservation_id", "passenger_id", "mode_of_payment", "amount"]
    elif selected_table == "Seat":
        fields = ["seat_number", "train_id", "seat_class", "seat_type"]
    elif selected_table == "Ticket":
        fields = ["ticket_id", "reservation_id", "source_id", "destination_id", "train_seat_key", "issue_date",
                  "coach_number"]
    elif selected_table == "Cancellation":
        fields = ["cancellation_id", "reservation_id", "ticket_id", "cancellation_date", "refund_amount",
                  "refund_date", "cancellation_fee", "cancellation_reason"]
    elif selected_table == "Route":
        fields = ["route_id", "source_id", "destination_id", "intermediate_stations"]
    elif selected_table == "Station":
        fields = ["station_id", "platform_id", "station_name", "station_location"]
    elif selected_table == "Feedbacktable":
        fields = ["feedback_id", "passenger_id", "train_id", "feedback_text", "rating"]
    else:
        fields = []

    return fields


def attribute_type(attribute):
    int_attributes = ['station_id', 'platform_id', 'passenger_id', 'age', 'route_id', 'train_id',
                      'number_of_berths', 'reservation_id', 'ticket_id', 'cancellation_id', 'rating',
                      'transaction_id']
    float_attribute = ['amount']
    if attribute in int_attributes:
        type_a = int
    elif attribute in float_attribute:
        type_a = float
    else:
        type_a = str
    return type_a


def get_primary_key_column(table_name):
    # A mapping of table names to their primary key columns (you need to adjust this accordingly)
    primary_key_mapping = {
        "Passenger": "passenger_id",
        "Train": "train_id",
        "Reservation": "reservation_id",
        "Payment": "transaction_id",
        "Seat": "train_seat_key",
        "Ticket": "ticket_id",
        "Cancellation": "cancellation_id",
        "Route": "route_id",
        "Station": "station_platform_id",
        "Feedback": "feedback_id"
    }
    return primary_key_mapping.get(table_name, "")


class Reservation:
    def __init__(self, roots):
        self.scrollbar = None
        self.listbox = None
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

        # Frame for Previous Fired Queries
        self.dataframerightcorner = LabelFrame(self.dataframe, bd=10, padx=20, relief=RIDGE, font=("Arial", 12, "bold"),
                                               text="Previous Fired Query")
        self.dataframerightcorner.place(x=660, y=255, width=830, height=100)

        # Create a canvas to hold the Label
        self.canvas_query = Canvas(self.dataframerightcorner)
        self.scrollbar_vertical_query = Scrollbar(self.dataframerightcorner, orient=VERTICAL,
                                                  command=self.canvas_query.yview)
        self.scrollbar_horizontal_query = Scrollbar(self.dataframerightcorner, orient=HORIZONTAL,
                                                    command=self.canvas_query.xview)

        self.scrollbar_vertical_query.pack(side=RIGHT, fill=Y)
        self.scrollbar_horizontal_query.pack(side=BOTTOM, fill=X)
        self.canvas_query.configure(yscrollcommand=self.scrollbar_vertical_query.set)
        self.canvas_query.configure(xscrollcommand=self.scrollbar_horizontal_query.set)

        # Pack the canvas
        self.canvas_query.pack(side=LEFT, fill=BOTH, expand=True)

        # Frame inside the canvas to hold the Label
        self.frame_query_content = Frame(self.canvas_query)
        self.canvas_query.create_window((0, 0), window=self.frame_query_content, anchor="nw")

        # Display box for showing executed queries
        self.query_display = Label(self.frame_query_content, text="", font=("Arial", 12), anchor="w")
        self.query_display.pack(fill=BOTH, padx=10, pady=10)

        # Bind scrolling
        self.frame_query_content.bind("<Configure>",
                                      lambda e: self.canvas_query.configure(scrollregion=self.canvas_query.bbox("all")))

        # Bind scrolling
        self.frame_left_content.bind("<Configure>",
                                     lambda e: self.canvas_left.configure(scrollregion=self.canvas_left.bbox("all")))

        # Right Frame with Scrollbar
        self.dataframeright = LabelFrame(self.dataframe, bd=10, padx=20, relief=RIDGE, font=("Arial", 12, "bold"),
                                         text="Reservation Information Display")
        self.dataframeright.place(x=660, y=5, width=830, height=250)

        self.canvas_right = Canvas(self.dataframeright)
        self.scrollbar_right = Scrollbar(self.dataframeright, orient=VERTICAL, command=self.canvas_right.yview)
        self.scrollbar_right.pack(side=RIGHT, fill=Y)
        self.canvas_right.configure(yscrollcommand=self.scrollbar_right.set)

        self.scrollbar_horizontal_right = Scrollbar(self.dataframeright, orient=HORIZONTAL,
                                                    command=self.canvas_right.xview)
        self.scrollbar_horizontal_right.pack(side=BOTTOM, fill=X)
        self.canvas_right.configure(xscrollcommand=self.scrollbar_horizontal_right.set)

        self.canvas_right.pack(side=LEFT, fill=BOTH, expand=TRUE)

        self.frame_right_content = Frame(self.canvas_right)
        self.canvas_right.create_window((0, 0), window=self.frame_right_content, anchor="nw")

        # Bind scrolling
        self.frame_right_content.bind("<Configure>",
                                      lambda e: self.canvas_right.configure(scrollregion=self.canvas_right.bbox("all")))

        # Details Frame with Scrollbar
        self.detailsframe = Frame(self.root, bd=20, relief=RIDGE)
        self.detailsframe.place(x=0, y=585, width=self.screen_width, height=210)

        # self.canvas_details = Canvas(self.detailsframe)
        # self.scrollbar_details = Scrollbar(self.detailsframe, orient=VERTICAL, command=self.canvas_details.yview)
        # self.canvas_details.configure(yscrollcommand=self.scrollbar_details.set)
        #
        # self.scrollbar_horizontal_details = Scrollbar(self.detailsframe, orient=HORIZONTAL,
        #                                               command=self.canvas_details.xview)
        # self.scrollbar_horizontal_details.pack(side=BOTTOM, fill=X)
        # self.canvas_details.configure(xscrollcommand=self.scrollbar_horizontal_details.set)
        #
        # self.scrollbar_details.pack(side=RIGHT, fill=Y)
        # self.canvas_details.pack(side=LEFT, fill=BOTH, expand=TRUE)
        #
        # self.frame_details_content = Frame(self.canvas_details)
        # self.canvas_details.create_window((0, 0), window=self.frame_details_content, anchor="nw")
        #
        # # Bind scrolling
        # self.frame_details_content.bind("<Configure>", lambda e: self.canvas_details.configure(
        #     scrollregion=self.canvas_details.bbox("all")))

        # ======================================Buttonframe======================================
        buttonframe = Frame(self.root, bd=20, relief=RIDGE)
        buttonframe.place(x=0, y=500, width=self.screen_width, height=85)

        # Dropdown (Combobox) to select tables (Train, Seat, Payment, etc.)
        self.table_names = ["Passenger", "Train", "Reservation", "Payment", "Seat", "Ticket", "Cancellation", "Route",
                            "Station", "Feedbacktable"]
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

        scroll_x = ttk.Scrollbar(self.detailsframe, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(self.detailsframe, orient=VERTICAL)
        self.details = ttk.Treeview(self.detailsframe,
                                    columns=("seat_number", "train_id", "train_seat_key", "seat_class", "seat_type"),
                                    xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x = ttk.Scrollbar(command=self.details.xview)
        scroll_y = ttk.Scrollbar(command=self.details.yview)

        self.details["show"] = "headings"
        self.details.pack(fill=BOTH, expand=1)

        # Bind the Treeview selection event to the get_cursor function
        self.details.bind("<<TreeviewSelect>>", self.get_cursor)

    def execute_query(self, query=None):
        global cursor, connection, query_input

        # If no query is provided, get it from the query_input
        if not query:
            query_input = self.query_input.get().strip()  # Get the input from the query_input and strip whitespace
            if query_input.isdigit():  # Check if the input is a digit
                query = int(query_input)  # Convert to an integer
            else:
                query = query_input  # Use the input directly as a SQL query
        if isinstance(query, int) and 1 <= query <= 25:
            try:
                # Query mapping based on the input number
                if query == 1:
                    query = "SELECT * FROM train WHERE number_of_berths > 500"
                    messagebox.showinfo("Query Question",
                                        "Display the details of train where number of berths is greater than 500")
                elif query == 2:
                    query = "SELECT p.passenger_id, p.passenger_name, p.mobile_number, p.age FROM passenger p, train t WHERE train_type = 'Express'"
                    messagebox.showinfo("Query Question",
                                        "Display the passenger ID, name, mobile number and age who travel in express train")
                elif query == 3:
                    query = "SELECT station_id, station_name, station_location, COUNT(platform_id) AS platform_count FROM station GROUP BY station_id, station_name, station_location HAVING COUNT(platform_id) > 1"
                    messagebox.showinfo("Query Question", "Display the stations having more than one platform")
                elif query == 4:
                    query = "SELECT COUNT(s.seat_number) FROM seat s JOIN train t ON s.train_id = t.train_id WHERE t.train_id = 2004"
                    messagebox.showinfo("Query Question",
                                        "Display the total number of seats in the train with train id as 2004")
                elif query == 5:
                    query = "SELECT t.* FROM train t JOIN reservation r ON t.train_id = r.train_id WHERE (r.reservation_date BETWEEN '01-JAN-2024' AND '01-OCT-2024') AND t.train_class = 'AC'"
                    messagebox.showinfo("Query Question",
                                        "Display the train details of whose reservation is done from 1 Jan 2024 to 1 Oct 2024 for AC compartment")
                elif query == 6:
                    query = "SELECT * FROM cancellation WHERE EXTRACT(YEAR FROM cancellation_date) = EXTRACT(YEAR FROM SYSDATE)"
                    messagebox.showinfo("Query Question", "Display all cancellation from current year")
                elif query == 7:
                    query = "SELECT * FROM passenger WHERE special_case != 'None'"
                    messagebox.showinfo("Query Question", "Display all passengers having special case")
                elif query == 8:
                    query = "SELECT p.* FROM passenger p JOIN reservation r ON p.passenger_id = r.passenger_id WHERE r.reservation_date BETWEEN '01-APR-2023' AND '30-SEP-2024'"
                    messagebox.showinfo("Query Question",
                                        "Display all passenger details whose reservation date is between 1 APR 2023 to 30 SEP 2024")
                elif query == 9:
                    query = "SELECT r.intermediate_stations FROM train t JOIN route r ON t.route_id = r.route_id WHERE t.train_id = 2021"
                    messagebox.showinfo("Query Question", "Display the intermediate stations where train id is 2021")
                elif query == 10:
                    query = "SELECT t.train_name FROM train t JOIN feedbacktable f ON t.train_id = f.train_id GROUP BY t.train_id, t.train_name HAVING AVG(f.rating) < (SELECT AVG(rating) FROM feedbacktable)"
                    messagebox.showinfo("Query Question",
                                        "Display the details of train whose rating is lower than average rating")
                elif query == 11:
                    query = "SELECT * FROM train WHERE train_id IN (SELECT train_id FROM reservation WHERE status = 'Confirmed')"
                    messagebox.showinfo("Query Question", "Display details of trains with confirmed reservations")
                elif query == 12:
                    query = "SELECT COUNT(*) FROM ticket WHERE train_seat_key IN (SELECT train_seat_key FROM seat WHERE seat_class = 'Sleeper')"  # Display total number of sleeper class tickets
                    messagebox.showinfo("Query Question", "Display total number of sleeper class tickets")
                elif query == 13:
                    query = "SELECT DISTINCT train_id FROM reservation WHERE reservation_date > '01-JAN-2024'"  # Display trains that have reservations after 1st Jan 2024
                    messagebox.showinfo("Query Question", "Display trains that have reservations after 1st Jan 2024")
                elif query == 14:
                    query = "SELECT train_id FROM reservation GROUP BY train_id HAVING COUNT(reservation_id) > 2"  # Display train IDs with more than 2 reservations
                    messagebox.showinfo("Query Question", "Display train IDs with more than 2 reservations")
                elif query == 15:
                    query = "SELECT * FROM passenger WHERE age > ALL (SELECT age FROM passenger WHERE gender = 'Female')"
                    messagebox.showinfo("Query Question", "Display passengers older than all female passengers")
                elif query == 16:
                    query = "SELECT train_name FROM train WHERE number_of_berths = (SELECT MAX(number_of_berths) FROM train)"  # Display train with the highest number of berths
                    messagebox.showinfo("Query Question", "Display train with the highest number of berths")
                elif query == 17:
                    query = "SELECT t.train_name FROM train t JOIN feedbacktable f ON t.train_id = f.train_id GROUP BY t.train_id, t.train_name HAVING AVG(f.rating) > 3"
                    messagebox.showinfo("Query Question", "Display trains with an average rating greater than 3")
                elif query == 18:
                    query = "SELECT * FROM cancellation WHERE cancellation_reason LIKE '%emergency%' OR cancellation_reason LIKE '%personal%'"
                    messagebox.showinfo("Query Question", "Display cancellations due to emergency or personal reasons")
                elif query == 19:
                    query = "SELECT r.intermediate_stations FROM route r WHERE r.route_id IN (SELECT DISTINCT route_id FROM train WHERE train_type = 'Express')"
                    messagebox.showinfo("Query Question", "Display intermediate stations for express trains")
                elif query == 20:
                    query = "SELECT DISTINCT train_id FROM reservation WHERE passenger_id IN (SELECT passenger_id FROM passenger WHERE age < 30) AND train_id IN (SELECT train_id FROM ticket)"  # Corrected INTERSECT to AND
                    messagebox.showinfo("Query Question",
                                        "Display train IDs with reservations made by passengers under 30 who also have tickets")
                elif query == 21:
                    query = "SELECT train_id FROM train WHERE train_class = 'AC' AND train_id IN (SELECT train_id FROM reservation WHERE status = 'Confirmed')"  # Corrected INTERSECT to AND
                    messagebox.showinfo("Query Question",
                                        "Display train IDs that are both AC class and have confirmed reservations")
                elif query == 22:
                    query = "SELECT p.passenger_name FROM passenger p WHERE p.passenger_id IN (SELECT passenger_id FROM reservation WHERE status = 'Confirmed') AND special_case = 'None'"  # Corrected EXCEPT to AND
                    messagebox.showinfo("Query Question",
                                        "Display names of passengers with confirmed reservations but no special cases")
                elif query == 23:
                    query = "SELECT t.* FROM train t JOIN station s ON t.source_id = s.station_platform_id WHERE s.station_location LIKE '%Maharashtra%'"  # Retrieve all trains whose source station is in a specific state.
                    messagebox.showinfo("Query Question",
                                        "Display all trains whose source station is in a specific state.")
                elif query == 24:
                    query = "SELECT train_id, COUNT(*) AS reservation_count FROM reservation GROUP BY train_id"  # Count the number of reservations for each train
                    messagebox.showinfo("Query Question", "Display train IDs with fewer than 2 confirmed reservations")
                elif query == 25:
                    query = "   SELECT train_id, SUM(amount) AS total_amount FROM payment GROUP BY train_id"  # Calculate the total payment amount collected for each train
                    messagebox.showinfo("Query Question", "Calculate the total payment amount collected for each train")

                # Log the generated SQL query for debugging
                print(f"Executing SQL Query: {query}")

            except NameError:
                self.query_display.config(text="Error: Query not found.")
                return
        else:
            query = query_input  # This allows for custom SQL queries outside the predefined ones

            # Establishing a connection to the Oracle database with SYSDBA privileges
        try:
            connection = cx_Oracle.connect(
                user="sys",
                password="sys123",
                dsn="FREE",
                mode=cx_Oracle.SYSDBA
            )
            cursor = connection.cursor()
            cursor.execute(query)

            # If it's a SELECT query, fetch and display the results
            if query.strip().lower().startswith("select"):
                rows = cursor.fetchall()
                self.display_query_results(rows)
                self.query_display.config(text=f"Executed Query: {query}")  # Update query display for SELECT
            else:
                connection.commit()
                self.query_display.config(text=f"Executed Query: {query}")  # Update query display for non-SELECT

            # Optionally clear input fields after adding the data
            self.clear_input_fields()
        except cx_Oracle.DatabaseError as e:
            self.query_display.config(text=f"Database Error: {e}")
        except Exception as e:
            self.query_display.config(text=f"Error: {e}")  # General error handling
        finally:
            # Close the cursor and connection
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def display_query_results(self, rows):
        # Displaying the results of a SELECT query
        for widget in self.frame_right_content.winfo_children():
            widget.destroy()

        for i, row in enumerate(rows):
            label = Label(self.frame_right_content, text=str(row), font=("Arial", 12), anchor="w")
            label.pack(fill=BOTH)

    # Placeholder methods for additional functionalities
    # noinspection PyUnusedLocal
    def update_table_fields(self, event):
        # Clear existing fields in left frame and right frame
        for widget in self.frame_left_content.winfo_children():
            widget.destroy()
        for widget in self.frame_right_content.winfo_children():
            widget.destroy()
        # for widget in self.frame_details_content.winfo_children():
        #     widget.destroy()

        selected_table = self.table_dropdown.get()

        # Define fields based on the selected table
        if selected_table == "Passenger":
            fields = ["Passenger ID", "Passenger Name", "Address", "Mobile Number", "Date of Birth", "Age", "Gender",
                      "Aadhaar Card", "Nationality", "Special_case"]
        elif selected_table == "Train":
            fields = ["Train ID", "Train Name", "Source", "Destination"]
        elif selected_table == "Reservation":
            fields = ["Reservation ID", "Passenger ID", "Train ID", "Departure Time", "Arrival Time", "Train Seat Key",
                      "Status", "Reservation Date"]
        elif selected_table == "Payment":
            fields = ["Transaction ID", "Train ID", "Reservation ID", "Passenger ID", "Mode of Pay", "Amount"]
        elif selected_table == "Seat":
            fields = ["Seat Number", "Train ID", "Seat Class", "Seat Type"]
        elif selected_table == "Ticket":
            fields = ["Ticket ID", "Passenger ID", "Reservation ID", "Source ID", "Destination ID", "Train Seat Key",
                      "Issue Date",
                      "Coach Number"]
        elif selected_table == "Cancellation":
            fields = ["Cancellation ID", "Reservation ID", "Ticket ID", "Cancellation Date", "Refund Amount",
                      "Refund Date", "Cancellation Fee", "Cancellation Reason"]
        elif selected_table == "Route":
            fields = ["Route ID", "Source ID", "Destination Station", "Intermidiate Stations"]
        elif selected_table == "Station":
            fields = ["Station ID", "Platform ID", "Station Name", "Station Locaton(city, state)"]
        elif selected_table == "Feedbacktable":
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
        self.update_records_listbox()

        self.fetch_data()

    def update_records_listbox(self):
        selected_table = self.table_dropdown.get()

        # Clear existing columns
        self.details["columns"] = []
        self.details.delete(*self.details.get_children())

        if selected_table == "Passenger":
            self.details["columns"] = (
                "passenger_id", "passenger_name", "address", "mobile_number", "date_of_birth", "age", "gender",
                "aadhaar_card", "nationality", "special_case")
            self.details.heading("passenger_id", text="Passenger ID")
            self.details.heading("passenger_name", text="Name")
            self.details.heading("address", text="Age")
            self.details.heading("mobile_number", text="Mobile Number")
            self.details.heading("date_of_birth", text="Date of Birth")
            self.details.heading("age", text="Age")
            self.details.heading("gender", text="Gender")
            self.details.heading("aadhaar_card", text="Aadhaar")
            self.details.heading("nationality", text="Nationality")
            self.details.heading("special_case", text="Special Case")

        elif selected_table == "Train":
            self.details["columns"] = (
                "train_id", "train_name", "source_id", "destination_id", "route_id", "train_class", "number_of_berths",
                "train_type", "time_duration")
            self.details.heading("train_id", text="Train ID")
            self.details.heading("train_name", text="Train Name")
            self.details.heading("source_id", text="Source")
            self.details.heading("destination_id", text="Destination")
            self.details.heading("route_id", text="Route")
            self.details.heading("train_class", text="Train Class")
            self.details.heading("number_of_berths", text="Number of Berths")
            self.details.heading("train_type", text="Train Type")
            self.details.heading("time_duration", text="Time Duration")

        elif selected_table == "Reservation":
            self.details["columns"] = (
                "reservation_id", "passenger_id", "train_id", "departure_time", "arrival_time", "train_seat_key",
                "status",
                "reservation_date")
            self.details.heading("reservation_id", text="Reservation ID")
            self.details.heading("passenger_id", text="Passenger ID")
            self.details.heading("train_id", text="Train ID")
            self.details.heading("departure_time", text="Departure Time")
            self.details.heading("arrival_time", text="Arrival Time")
            self.details.heading("train_seat_key", text="Train Seat Number")
            self.details.heading("status", text="Status")
            self.details.heading("reservation_date", text="Reservation Date")

        elif selected_table == "Payment":
            self.details["columns"] = (
                "transaction_id", "train_id", "reservation_id", "passenger_id", "mode_of_payment", "amount")
            self.details.heading("transaction_id", text="Transaction ID")
            self.details.heading("train_id", text="Train ID")
            self.details.heading("reservation_id", text="Resrvation ID")
            self.details.heading("passenger_id", text="Passenger ID")
            self.details.heading("mode_of_payment", text="Mode of Payment")
            self.details.heading("amount", text="Amount")

        elif selected_table == "Seat":
            self.details["columns"] = ("seat_number", "train_id", "train_seat_key", "seat_class", "seat_type")
            self.details.heading("seat_number", text="Seat Number")
            self.details.heading("train_id", text="Train ID")
            self.details.heading("train_seat_key", text="Train Set Key")
            self.details.heading("seat_class", text="Seat Class")
            self.details.heading("seat_type", text="Seat Type")

        elif selected_table == "Ticket":
            self.details["columns"] = (
                "ticket_id", "passenger_id", "reservation_id", "source_id", "destination_id", "train_seat_key",
                "issue_date", "seat_number")
            self.details.heading("ticket_id", text="Ticket ID")
            self.details.heading("passenger_id", text="Passenger ID")
            self.details.heading("reservation_id", text="Reservation ID")
            self.details.heading("source_id", text="Source ID")
            self.details.heading("destination_id", text="Destination ID")
            self.details.heading("train_seat_key", text="Train Seat Key")
            self.details.heading("issue_date", text="Issue Date")
            self.details.heading("seat_number", text="Seat Number")

        elif selected_table == "Cancellation":
            self.details["columns"] = (
                "cancellation_id", "reservation_id", "ticket_id", "cancellation_date", "refund_amount", "refund_date",
                "cancellation_fee", "cancellation_reason")
            self.details.heading("cancellation_id", text="Cancellation ID")
            self.details.heading("reservation_id", text="Reservation ID")
            self.details.heading("ticket_id", text="Ticket ID")
            self.details.heading("cancellation_date", text="Cancellation Date")
            self.details.heading("refund_amount", text="Refund Amount")
            self.details.heading("refund_date", text="Refund Date")
            self.details.heading("cancellation_fee", text="Cancellation Fee")
            self.details.heading("cancellation_reason", text="Cancellation Reason")

        elif selected_table == "Route":
            self.details["columns"] = ("route_id", "source_id", "destination_id", "intermediate_stations")
            self.details.heading("route_id", text="Route ID")
            self.details.heading("source_id", text="Source ID")
            self.details.heading("destination_id", text="Destination ID")
            self.details.heading("intermediate_stations", text="Intermediate Stations")

        elif selected_table == "Station":
            self.details["columns"] = (
                "station_id", "platform_id", "station_platform_id", "station_name", "station_location")
            self.details.heading("station_id", text="Station ID")
            self.details.heading("platform_id", text="Platform ID")
            self.details.heading("station_platform_id", text="Station Platform ID")
            self.details.heading("station_name", text="Station Name")
            self.details.heading("station_location", text="Station Location")

        elif selected_table == "Feedbacktable":
            self.details["columns"] = ("feedback_id", "passenger_id", "train_id", "feedback_text", "rating")
            self.details.heading("feedback_id", text="Feedback ID")
            self.details.heading("passenger_id", text="Passenger ID")
            self.details.heading("train_id", text="Train ID")
            self.details.heading("feedback_text", text="Feedback Text")
            self.details.heading("rating", text="Rating")

        # Update the Treeview with the new columns
        self.details["show"] = "headings"
        for col in self.details["columns"]:
            self.details.column(col, anchor="center")

    def add_data(self):
        table_name = self.table_dropdown.get()
        attr = return_fields(table_name)

        # Gather the values from input fields
        values = []
        for entry in self.frame_left_content.winfo_children():
            if isinstance(entry, Entry):
                values.append(entry.get())  # Get the value from each Entry widget

        placeholder = []
        for attribute, value in zip(attr, values):
            if attribute_type(attribute) == int:
                placeholder.append(value)
            elif attribute_type(attribute) == float:
                placeholder.append(f"{float(value):.2f}")
            else:
                placeholder.append(f"'{value}'")

        # Prepare the SQL command for inserting data
        placeholders_str = ', '.join(placeholder)
        command = f"INSERT INTO {table_name.lower()} ({', '.join(attr)}) VALUES ({placeholders_str})"
        print(command)
        self.execute_query(command)

    def update_data(self):
        global cursor, connection
        table_name = self.table_dropdown.get()  # Get the selected table from the dropdown
        selected_row = self.details.focus()  # Get the selected row
        row_data = self.details.item(selected_row, 'values')  # Get the row's values

        if not row_data:
            self.query_display.config(text="No row selected for update.")
            return

        # Gather updated values from the input fields
        updated_values = []
        for entry in self.frame_left_content.winfo_children():
            if isinstance(entry, Entry):
                updated_values.append(entry.get())

        # Get primary key column to identify the row in the table
        primary_key = get_primary_key_column(table_name)
        primary_value = row_data[0]  # Assuming first column is the primary key

        # Prepare the update query
        set_clause = ", ".join(f"{attr} = '{value}'" if attribute_type(attr) == str else f"{attr} = {value}"
                               for attr, value in zip(return_fields(table_name), updated_values))

        query = f"UPDATE {table_name} SET {set_clause} WHERE {primary_key} = {primary_value}"

        try:
            connection = cx_Oracle.connect(
                user="sys",
                password="sys123",
                dsn="FREE",
                mode=cx_Oracle.SYSDBA
            )
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            self.query_display.config(text=f"Updated {table_name} with {primary_key} = {primary_value}.")
            self.fetch_data()  # Refresh the data in the Treeview
        except cx_Oracle.DatabaseError as e:
            self.query_display.config(text=f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

    def delete_data(self):
        global cursor, connection
        table_name = self.table_dropdown.get()  # Get the selected table from the dropdown
        selected_row = self.details.focus()  # Get the selected row
        row_data = self.details.item(selected_row, 'values')  # Get the row's values

        if not row_data:
            self.query_display.config(text="No row selected for deletion.")
            return

        # Get primary key column and value to identify the row in the table
        primary_key = get_primary_key_column(table_name)
        primary_value = row_data[0]  # Assuming first column is the primary key

        # Prepare the delete query
        query = f"DELETE FROM {table_name} WHERE {primary_key} = {primary_value}"

        try:
            connection = cx_Oracle.connect(
                user="sys",
                password="sys123",
                dsn="FREE",
                mode=cx_Oracle.SYSDBA
            )
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            self.query_display.config(text=f"Deleted record from {table_name} where {primary_key} = {primary_value}.")
            self.fetch_data()  # Refresh the data in the Treeview
        except cx_Oracle.DatabaseError as e:
            self.query_display.config(text=f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

    def clear_input_fields(self):
        # Iterate over all widgets in frame_left_content
        for widget in self.frame_left_content.winfo_children():
            if isinstance(widget, Entry):
                widget.delete(0, END)  # Clear the text in the Entry widget

    def fetch_data(self):
        global cursor, connection
        try:
            selected_table = self.table_dropdown.get()  # Get the selected table from dropdown
            query = f"SELECT * FROM {selected_table}"  # Dynamic query based on selected table
            # Establishing a connection to the Oracle database
            connection = cx_Oracle.connect(
                user="sys",
                password="sys123",
                dsn="FREE",
                mode=cx_Oracle.SYSDBA
            )
            cursor = connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()  # Fetch all rows from the table

            # Clear previous data from the Treeview (self.details)
            self.details.delete(*self.details.get_children())

            # Insert new data into the Treeview
            for row in rows:
                self.details.insert('', END, values=row)

        except cx_Oracle.DatabaseError as e:
            self.query_display.config(text=f"Error: {e}")

        finally:
            # Close the cursor and connection
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def get_cursor(self, event):
        # Get the currently selected row from the Treeview (self.details)
        selected_row = self.details.focus()  # Get the selected row ID
        row_data = self.details.item(selected_row, 'values')  # Get the row's values

        # Clear any existing input in the fields
        input_entries = [widget for widget in self.frame_left_content.winfo_children() if isinstance(widget, Entry)]

        # Fill the input boxes with the selected row's data
        for i, entry in enumerate(input_entries):
            entry.delete(0, END)  # Clear the existing data in each Entry widget
            if i < len(row_data):
                entry.insert(END, row_data[i])  # Insert the corresponding row data into each input box


# Initialize the Reservation class with Tkinter root window
if __name__ == "__main__":
    root = Tk()
    obj = Reservation(root)
    root.mainloop()
