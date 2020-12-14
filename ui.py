import tkinter as tk
import arch
import fileutil


# TODO Work on base version of UI, perferably deisgn first.
class SpiderUI:
    def __init__(self, title):
        self.title = title
        self.width, self.height = 600, 600
        self.master = tk.Tk(screenName=self.title)
        self.master.geometry("950x700")
        self.version = '1.0'

        # self.frame = None
        self.navbar = None
        self.home = None
        self.scan = None
        self.history = None

        # Buttons

        self.home_button_image = tk.PhotoImage(file=fileutil.get_project_file('Spider', 'assets/Home.png'))
        self.scan_button_image = tk.PhotoImage(file=fileutil.get_project_file('Spider', 'assets/Scan.png'))
        self.history_button_image = tk.PhotoImage(file=fileutil.get_project_file('Spider', 'assets/History.png'))

        self.create_navbar()
        self.create_home_frame()
        self.create_scan_frame()

        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=4)

        self.create_entries()
        self.create_labels()
        self.submit_button()

        # Starts the TKinter GUI
        self.master.mainloop()

    def show_frame(self, name):
        if name == 'home':
            self.home.lift()
            self.scan.lower()
        elif name == 'scan':
            self.scan.lift()
            self.home.lower()
        else:
            raise Exception("Invalid frame given")

    def create_navbar(self):
        self.navbar = tk.Frame(self.master, bg='#202040')
        self.navbar.grid(row=0, column=0, sticky='nsew')

        home_button = tk.Button(self.navbar, command=lambda: self.show_frame('home'), image=self.home_button_image,
                                borderwidth=0, bg='#202040', fg='#202040', activebackground='black')

        scan = tk.Button(self.navbar, command=lambda: self.show_frame('scan'), image=self.scan_button_image,
                         borderwidth=0, bg='#202040', fg='#202040')
        self.history = tk.Button(self.navbar, image=self.history_button_image, borderwidth=0, bg='#202040')

        home_button.pack(fill=tk.X)
        scan.pack(fill=tk.X)
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

        scanned_list_label = tk.Label(scanned_box, bg='white', fg='black', font=(None, 18),  text='Listings Scanned')
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
        self.scan = tk.Frame(self.master, bg='white', width=100, height=100)
        self.scan.grid(row=0, column=1, sticky='nsew')

        self.scan.lower()

    def create_entries(self, get_text=False):
        website = tk.Entry(self.scan, text="Website", width=20, bg="white")
        location = tk.Entry(self.scan, text="Location", width=20, bg="white")
        max = tk.Entry(self.scan, text="Max Search Results", width=20, bg="white")

        website.grid(row=1, column=1, ipady=3, padx=7, pady=3)
        location.grid(row=2, column=1, ipady=3, pady=3)
        max.grid(row=3, column=1, ipady=3, pady=3)

        if get_text:
            return str(website.get())

    def submit_button(self):
        submit_button = tk.Button(self.scan, width=5, height=1, text="Search")
        submit_button.grid_columnconfigure(0, weight=0)
        submit_button.grid(row=5, column=1, pady=8)

    def create_labels(self):
        title = tk.Label(self.scan, text='Spider v1.0', fg='black', bg='#ff5151', font=(None, 20))
        self.scan.columnconfigure(1, weight=1)
        title.grid(row=0, column=1)

        website_label = tk.Label(self.scan, text='Website', fg='black', bg='#ff5151')
        location_label = tk.Label(self.scan, text='Location', fg='black', bg='#ff5151')
        max_label = tk.Label(self.scan, text='Max Values', fg='black', bg='#ff5151')

        website_label.grid(row=1, column=0)
        location_label.grid(row=2, column=0)
        max_label.grid(row=3, column=0)

    # def start_scan(self):
    #     spider = arch.Spider("https://www.loopnet.com", self.search_city_entry(True))
    #     spider.lookup_location_action()
    #     spider.store_current_listings()
    #     spider.scan_listings()
