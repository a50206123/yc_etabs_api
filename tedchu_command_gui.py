import customtkinter as ctk
from yc_etabs_api.etabs import ETABS

class TedChuCommand :
    def __init__(self) -> None:
        self.etabs = None

        ctk.set_appearance_mode('dark') 
        # ctk.set_default_color_theme()

        app = ctk.CTk()
        app.geometry('640x480')
        app.title('ETABS Helper ft. TedChu')
        
        app.grid_rowconfigure(0,)
        app.grid_rowconfigure(1,)
        app.grid_rowconfigure(2)
        app.grid_rowconfigure(3)
        app.grid_rowconfigure(4)
        app.grid_columnconfigure(0, weight=3)
        app.grid_columnconfigure(1, weight=0)
        app.grid_columnconfigure(2, weight=3)

        btn_connect = ctk.CTkButton(app, text="Connect to ETABS", width=600, command=self.connect_etabs)
        btn_connect.grid(row=0, column=0, columnspan = 3, padx=20, pady=(20, 0))
        
        label_show_path = ctk.CTkLabel(app, text="")
        label_show_path.grid(row=1, column=0, columnspan = 3, padx=20, pady=0)

        btn_release_i = ctk.CTkButton(app, text="Release I", command=self.release_i, height = 20)
        btn_release_i.grid(row=2, column=0, padx=0, pady=5)
        btn_release_j = ctk.CTkButton(app, text="Release J", command=self.release_j, height = 20)
        btn_release_j.grid(row=2, column=1, padx=0, pady=5)
        btn_release_ij = ctk.CTkButton(app, text="Release IJ", command=self.release_ij, height = 20)
        btn_release_ij.grid(row=2, column=2, padx=0, pady=5)

        btn_loading = ctk.CTkButton(app, text="Click Me to Loading", command=self.open_loading)
        btn_loading.grid(row=3, column=0, padx=0, pady=5)

        self.app = app
        self.btn_connect = btn_connect
        self.btn_release_i = btn_release_i
        self.btn_release_j = btn_release_j
        self.btn_release_ij = btn_release_ij
        self.label_show_path = label_show_path

        app.mainloop()
    
    def connect_etabs(self) :
        if self.etabs == None :
            etabs = ETABS()
            self.etabs = etabs
            self.btn_connect.configure(text = f'Connected to {self.etabs.EDB_name}!!')
            self.label_show_path.configure(text = f'Path is {self.etabs.EDB_path}')

        else :
            self.btn_connect.configure(text = f"Disconnect to {self.etabs.EDB_name}!! Click to connect again !! ")
            self.etabs = None

            self.label_show_path.configure(text = '')
            
        print(f"{' Click btn_connect ':*^60s}")
    
    def release_i(self) :
        self.etabs.model_unlock()

        selected_frames = self.etabs.Select.get(type_='Frame')

        for frame in selected_frames :
            self.etabs.Frames.set_release(frame, quick='Mi')

        print(f"{' Click btn_release_i ':*^60s}")
    
    
    def release_j(self) :
        self.etabs.model_unlock()

        selected_frames = self.etabs.Select.get(type_='Frame')

        for frame in selected_frames :
            self.etabs.Frames.set_release(frame, quick='Mj')

        print(f"{' Click btn_release_j ':*^60s}")

    
    def release_ij(self) :
        self.etabs.model_unlock()

        selected_frames = self.etabs.Select.get(type_='Frame')

        for frame in selected_frames :
            self.etabs.Frames.set_release(frame, quick='Mij')

        print(f"{' Click btn_release_ij ':*^60s}")

    def open_loading(self) :
        self.Loading = Loading()

class Loading :
    def __init__(self) -> None:
        ctk.set_appearance_mode('dark') 
        # ctk.set_default_color_theme()

        app = ctk.CTk()
        app.geometry('1200x600')
        app.title('Loading Helper ft. TedChu')

        label_story_height = ctk.CTkLabel(app, text='Story Height : (m)')
        entry_story_height = ctk.CTkEntry(app)
        label_story_height.grid(row = 0, column = 0, padx = 5, pady = 5)
        entry_story_height.grid(row = 0, column = 1, pady = 5)

        label_beam_depth = ctk.CTkLabel(app, text='The depth of beam : (m)')
        entry_beam_depth = ctk.CTkEntry(app)
        label_beam_depth.grid(row = 0, column = 2, padx = 5, pady = 5)
        entry_beam_depth.grid(row = 0, column = 3, pady = 5)

        btn_calc = ctk.CTkButton(app, text='Calculating', width = 300, command=self.calc_load)
        btn_calc.grid(row = 0, column = 4, columnspan = 2, pady = 5)

        label_t_rc = ctk.CTkLabel(app, text='Thickness of RC Wall : (cm)')
        entry_t_rc = ctk.CTkEntry(app)
        label_t_rc.grid(row = 1, column = 0, padx = 5, pady = 5)
        entry_t_rc.grid(row = 1, column = 1, pady = 5)

        label_t_ot = ctk.CTkLabel(app, text='Thickness of OTHER Wall : (cm)')
        entry_t_ot = ctk.CTkEntry(app)
        label_t_ot.grid(row = 1, column = 2, padx = 5, pady = 5)
        entry_t_ot.grid(row = 1, column = 3, pady = 5)
        label_w_ot = ctk.CTkLabel(app, text='Unit Weight of OTHER Wall : (tf/m3)')
        entry_w_ot = ctk.CTkEntry(app)
        label_w_ot.grid(row = 1, column = 4, padx = 5, pady = 5)
        entry_w_ot.grid(row = 1, column = 5, pady = 5)
        

        self.app = app
        self.label_story_height = label_story_height
        self.entry_story_height = entry_story_height
        self.label_beam_depth = label_beam_depth
        self.entry_beam_depth = entry_beam_depth
        self.label_t_rc = label_t_rc
        self.entry_t_rc = entry_t_rc
        self.label_t_ot = label_t_ot
        self.entry_t_ot = entry_t_ot
        self.label_w_ot = label_w_ot
        self.entry_w_ot = entry_w_ot
        self.btn_loading = []

        app.mainloop()

    def calc_load(self) :
        story_height = float(self.entry_story_height.get())
        beam_depth = float(self.entry_beam_depth.get())
        try :
            t_rc = float(self.entry_t_rc.get())/100
            w_rc = 2.4
            haveRC = True
        except :
            haveRC = False

        try :
            t_ot = float(self.entry_t_ot.get())/100
            w_ot = float(self.entry_w_ot.get())
            haveOT = True
        except : 
            haveOT = False

        clear_height = story_height - beam_depth

        line_loading = lambda w, h, t : w * h * t

        btn_loading_rc = []
        btn_loading_ot = []
        commands = [add_loading()]

        for i in range(4) :
            if haveRC :
                tmp1 = ctk.CTkButton(self.app, text = f'RC {(i+1)*25}%-{line_loading(w_rc, clear_height, t_rc)*(i+1)*0.25:.3f}')
                tmp1.grid(row = 5- i, column = 0, pady = 10)
                btn_loading_rc.append(tmp1)
            
            if haveOT :
                tmp2 = ctk.CTkButton(self.app, text = f'Other {(i+1)*25}%-{line_loading(w_ot, clear_height, t_ot)*(i+1)*0.25:.3f}')
                tmp2.grid(row =  5- i, column = 1, pady = 10)
                btn_loading_ot.append(tmp2)


        self.btn_loading_rc = btn_loading_rc
        self.btn_loading_ot = btn_loading_ot
            
        

if __name__ == '__main__' :
    app = TedChuCommand()