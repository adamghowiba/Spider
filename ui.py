import tkinter as tk
import arch
import fileutil

class SpiderUI:
    def __init__(self, title):
        self.title = title
        self.width, self.height = 600, 600
        self.master = tk.Tk(screenName=self.title)
        self.master.geometry("950x700")
        self.version = '1.0'

        self.navbar = None
        self.home = None
        self.scan_frame = None
        self.history = None

        # Initialization Spider
        self.spider = None

        # Get UI Entry Information
        self.location_entry = None
        self.type_options = None

        # Button Images
        self.home_button_image = tk.PhotoImage(file=fileutil.get_project_file('Spider', 'assets/Home.png'))
        self.scan_button_image = tk.PhotoImage(file=fileutil.get_project_file('Spider', 'assets/Scan.png'))
        self.history_button_image = tk.PhotoImage(file=fileutil.get_project_file('Spider', 'assets/History.png'))

        # Background image
        self.background_image = tk.PhotoImage(file=fileutil.get_project_file('Spider', 'assets/starbackground.png'))

        # Create frames
        self.create_navbar()
        self.create_home_frame()
        self.create_scan_frame()

        # Configure grid
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=4)

        # Other
        self.create_entries()
        self.create_labels()
        self.scan_buttons()
        self.create_options_menu()

        # Starts the TKinter GUI
        self.master.mainloop()

    def create_navbar(self):
        self.navbar = tk.Frame(self.master, bg='#202040')
        self.navbar.grid(row=0, column=0, sticky='nsew')

        home_button = tk.Button(self.navbar, command=lambda: self.show_frame('home'), image=self.home_button_image,
                                borderwidth=0, bg='#202040', fg='#202040', activebackground='black')

        scan_button = tk.Button(self.navbar, command=lambda: self.show_frame('scan'), image=self.scan_button_image,
                                borderwidth=0, bg='#202040', fg='#202040')
        self.history = tk.Button(self.navbar, image=self.history_button_image, borderwidth=0, bg='#202040')

        home_button.pack(fill=tk.X)
        scan_button.pack(fill=tk.X)
        self.history.pack(fill=tk.X)

    def create_home_frame(self):
        self.home = tk.Frame(self.master, bg='#ff5151')
        self.home.grid(row=0, column=1, sticky='nsew')

        for x in range(3):
            self.home.columnconfigure(x, weight=1)

        scanned_box = tk.Frame(self.home, bg='white', width=250, height=200)
        scanned_box.grid(row=0, column=0, pady=20)
        scanned_box.grid_propagate(False)
        scanned_box.columnconfigure(0, weight=1)

        scanned_list_label = tk.Label(scanned_box, bg='white', fg='black', font=(None, 18), text='Listings Scanned')
        scanned_list_label.grid(row=0, column=0)

        number_list_label = tk.Label(scanned_box, bg='white', fg='black', font=(None, 18), text='5')
        number_list_label.grid(row=1, column=0, pady=40)

        scanned_box1 = tk.Frame(self.home, bg='white', width=250, height=200)
        scanned_box1.grid(row=0, column=1)
        scanned_box1.grid_propagate(False)
        scanned_box1.columnconfigure(0, weight=1)

        scanned_list_label1 = tk.Label(scanned_box1, bg='white', fg='black', font=(None, 18), text='Records Added')
        scanned_list_label1.grid(row=0, column=0)

        number_list_label = tk.Label(scanned_box1, bg='white', fg='black', font=(None, 18), text='10')
        number_list_label.grid(row=1, column=0, pady=40)

        scanned_box2 = tk.Frame(self.home, bg='white', width=250, height=200)
        scanned_box2.grid(row=0, column=2)
        scanned_box2.grid_propagate(False)
        scanned_box2.columnconfigure(0, weight=1)

        scanned_list_label2 = tk.Label(scanned_box2, bg='white', fg='black', font=(None, 18), text='Cities Scanned')
        scanned_list_label2.grid(row=0, column=0)

        number_list_label = tk.Label(scanned_box2, bg='white', fg='black', font=(None, 18), text='15')
        number_list_label.grid(row=1, column=0, pady=40)

    def create_scan_frame(self):
        self.scan_frame = tk.Frame(self.master, bg='#ff5151', width=100, height=100)
        self.scan_frame.grid(row=0, column=1, sticky='nsew')

        self.scan_frame.lower()

    def create_entries(self, get_text=False):
        self.location_entry = tk.Entry(self.scan_frame, text="Location", width=20, bg="white")

        self.location_entry.grid(row=1, column=1, ipady=3, pady=3)

    def scan_buttons(self):
        submit_button = tk.Button(self.scan_frame, command=self.start_scan, width=9, height=2, text="Start Search")
        submit_button.grid(row=5, column=1, pady=8)

        stop_button = tk.Button(self.scan_frame, width=5, height=2, text='Stop')
        stop_button.grid(row=6, column=1, pady=0)

    def create_labels(self):
        title = tk.Label(self.scan_frame, text='Start Scanning', fg='white', bg='#ff5151', font=(None, 20))
        # self.scan.columnconfigure(1, weight=1)
        title.grid(row=0, column=1)

        self.location_entry = tk.Label(self.scan_frame, text='Location', fg='white', bg='#ff5151')
        self.location_entry.grid(row=1, column=0)

    def create_options_menu(self):
        options_var = tk.StringVar(self.scan_frame)
        options_var.set('For Lease')

        self.type_options = tk.OptionMenu(self.scan_frame, options_var, 'For Lease', 'For Sale')
        self.type_options.grid(row=1, column=0)

    def show_frame(self, name):
        if name == 'home':
            self.home.lift()
            self.scan_frame.lower()
        elif name == 'scan':
            self.scan_frame.lift()
            self.home.lower()
        else:
            raise Exception("Invalid frame given")

    def start_scan(self):
        self.spider = arch.Spider("https://www.loopnet.com", self.location_entry.get(), False)
        self.spider.run()

    def stop_scan(self):
        self.spider.save_listing()

    def get_property_type(self):
        return self.type_options.get(self.type_options.get())
