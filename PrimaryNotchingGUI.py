import tkinter
import tkinter.messagebox
import customtkinter
import PrimaryNotchingCalculator as PNC
import pandas as pd

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class WindowSettings(customtkinter.CTkFrame):
        def __init__(self, master):
            super().__init__(master) 
            # Color mode and Scaling sizing
            self.appearance_mode_label = customtkinter.CTkLabel(self, text="Theme:", anchor="w")
            self.appearance_mode_label.grid(row=0, column=0, padx=5, pady=(5, 5))
            self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self, values=["Light", "Dark", "System"],
                                                                        command=self.change_appearance_mode_event)
            self.appearance_mode_optionemenu.grid(row=0, column=1, padx=5, pady=(5, 5))
            self.scaling_label = customtkinter.CTkLabel(self, text="UI Scaling:", anchor="w")
            self.scaling_label.grid(row=0, column=2, padx=5, pady=(5, 5))
            self.scaling_optionemenu = customtkinter.CTkOptionMenu(self, values=["80%", "90%", "100%", "110%", "120%"],
                                                                command=self.change_scaling_event)
            self.scaling_optionemenu.grid(row=0, column=3, padx=5, pady=(5, 5))
            # set default values
            self.appearance_mode_optionemenu.set("Dark")
            self.scaling_optionemenu.set("100%")


        def change_appearance_mode_event(self, new_appearance_mode: str):
            customtkinter.set_appearance_mode(new_appearance_mode)

        def change_scaling_event(self, new_scaling: str):
            new_scaling_float = int(new_scaling.replace("%", "")) / 100
            customtkinter.set_widget_scaling(new_scaling_float)
       
        
class FilesFrame(customtkinter.CTkFrame):
        f06path = ""
        sinexh5path = ""
        sineyh5path = ""
        sinezh5path = ""
        QScsvpath = ""
        SINEcsvpath = ""
        rndxh5path = ""
        rndyh5path = ""
        rndzh5path = ""
        RNDcsvpath = ""
        outputpath = ""

        def __init__(self, master):
            super().__init__(master)            

            # ALL FILE PATHS 
            self.f06file = customtkinter.CTkTextbox(self , width = 500, height = 10, text_color=("#87898a"))
            self.f06file.insert("0.0","Select f06 file")
            self.f06file.grid(row=0, column=0, padx=(0, 0), pady=(0, 5), sticky="nsew")
            self.f06file_button = customtkinter.CTkButton(master=self, text = "Browse ...", fg_color="transparent", border_width=2, text_color=("gray30", "#DCE4EE"), command=self.browse_f06file)
            self.f06file_button.grid(row=0, column=1, padx=(5, 0), pady=(0, 5), sticky="nsew")

            self.sinexh5 = customtkinter.CTkTextbox(self , width = 500, height = 10, text_color=("#87898a"))
            self.sinexh5.insert("0.0","Select Sine X h5 file")
            self.sinexh5.grid(row=1, column=0, padx=(0, 0), pady=(0, 5), sticky="nsew")
            self.sinexh5_button = customtkinter.CTkButton(master=self, text = "Browse ...", fg_color="transparent", border_width=2, text_color=("gray30", "#DCE4EE"), command=self.browse_sinexh5file)
            self.sinexh5_button.grid(row=1, column=1, padx=(5, 0), pady=(0, 5), sticky="nsew")

            self.sineyh5 = customtkinter.CTkTextbox(self , width = 500, height = 10, text_color=("#87898a"))
            self.sineyh5.insert("0.0","Select Sine Y h5 file")
            self.sineyh5.grid(row=2, column=0, padx=(0, 0), pady=(0, 5), sticky="nsew")
            self.sineyh5_button = customtkinter.CTkButton(master=self, text = "Browse ...", fg_color="transparent", border_width=2, text_color=("gray30", "#DCE4EE"), command=self.browse_sineyh5file)
            self.sineyh5_button.grid(row=2, column=1, padx=(5, 0), pady=(0, 5), sticky="nsew")

            self.sinezh5 = customtkinter.CTkTextbox(self , width = 500, height = 10, text_color=("#87898a"))
            self.sinezh5.insert("0.0","Select Sine Z h5 file")
            self.sinezh5.grid(row=3, column=0, padx=(0, 0), pady=(0, 5), sticky="nsew")
            self.sinezh5_button = customtkinter.CTkButton(master=self, text = "Browse ...", fg_color="transparent", border_width=2, text_color=("gray30", "#DCE4EE"), command=self.browse_sinezh5file)
            self.sinezh5_button.grid(row=3, column=1, padx=(5, 0), pady=(0, 5), sticky="nsew")

            self.QScsv = customtkinter.CTkTextbox(self , width = 500, height = 10, text_color=("#87898a"))
            self.QScsv.insert("0.0","Import QS levels file")
            self.QScsv.grid(row=4, column=0, padx=(0, 0), pady=(0, 5), sticky="nsew")
            self.QScsv_button = customtkinter.CTkButton(master=self, text = "Browse ...", fg_color="transparent", border_width=2, text_color=("gray30", "#DCE4EE"), command=self.browse_QScsvfile)
            self.QScsv_button.grid(row=4, column=1, padx=(5, 0), pady=(0, 5), sticky="nsew")

            self.SINEcsv = customtkinter.CTkTextbox(self , width = 500, height = 10, text_color=("#87898a"))
            self.SINEcsv.insert("0.0","Import Sine specification file")
            self.SINEcsv.grid(row=5, column=0, padx=(0, 0), pady=(0, 5), sticky="nsew")
            self.SINEcsv_button = customtkinter.CTkButton(master=self, text = "Browse ...", fg_color="transparent", border_width=2, text_color=("gray30", "#DCE4EE"), command=self.browse_SINEcsvfile)
            self.SINEcsv_button.grid(row=5, column=1, padx=(5, 0), pady=(0, 5), sticky="nsew")
            

            self.rndxh5 = customtkinter.CTkTextbox(self , width = 500, height = 10, text_color=("#87898a"))
            self.rndxh5.insert("0.0","Select Random X file")
            self.rndxh5.grid(row=6, column=0, padx=(0, 0), pady=(0, 5), sticky="nsew")
            self.rndxh5_button = customtkinter.CTkButton(master=self, text = "Browse ...", fg_color="transparent", border_width=2, text_color=("gray30", "#DCE4EE"), command=self.browse_rndxh5file)
            self.rndxh5_button.grid(row=6, column=1, padx=(5, 0), pady=(0, 5), sticky="nsew")

            self.rndyh5 = customtkinter.CTkTextbox(self , width = 500, height = 10, text_color=("#87898a"))
            self.rndyh5.insert("0.0","Select Random Y file")
            self.rndyh5.grid(row=7, column=0, padx=(0, 0), pady=(0, 5), sticky="nsew")
            self.rndyh5_button = customtkinter.CTkButton(master=self, text = "Browse ...", fg_color="transparent", border_width=2, text_color=("gray30", "#DCE4EE"), command=self.browse_rndyh5file)
            self.rndyh5_button.grid(row=7, column=1, padx=(5, 0), pady=(0, 5), sticky="nsew")        

            self.rndzh5 = customtkinter.CTkTextbox(self , width = 500, height = 10, text_color=("#87898a"))
            self.rndzh5.insert("0.0","Select Random Z file")
            self.rndzh5.grid(row=8, column=0, padx=(0, 0), pady=(0, 5), sticky="nsew")
            self.rndzh5_button = customtkinter.CTkButton(master=self, text = "Browse ...", fg_color="transparent", border_width=2, text_color=("gray30", "#DCE4EE"), command=self.browse_rndzh5file)
            self.rndzh5_button.grid(row=8, column=1, padx=(5, 0), pady=(0, 5), sticky="nsew")

            self.RNDcsv = customtkinter.CTkTextbox(self , width = 500, height = 10, text_color=("#87898a"))
            self.RNDcsv.insert("0.0","Import Random specification file")
            self.RNDcsv.grid(row=9, column=0, padx=(0, 0), pady=(0, 5), sticky="nsew")
            self.RNDcsv_button = customtkinter.CTkButton(master=self, text = "Browse ...", fg_color="transparent", border_width=2, text_color=("gray30", "#DCE4EE"), command=self.browse_RNDcsvfile)
            self.RNDcsv_button.grid(row=9, column=1, padx=(5, 0), pady=(0, 5), sticky="nsew")

            self.output = customtkinter.CTkTextbox(self , width = 500, height = 10, text_color=("#87898a"))
            self.output.insert("0.0","Output folder path")
            self.output.grid(row=10, column=0, padx=(0, 0), pady=(0, 5), sticky="nsew")
            self.output_button = customtkinter.CTkButton(master=self, text = "Browse ...", fg_color="transparent", border_width=2, text_color=("gray30", "#DCE4EE"), command=self.browse_output)
            self.output_button.grid(row=10, column=1, padx=(5, 0), pady=(0, 5), sticky="nsew")

            self.Load_button = customtkinter.CTkButton(master=self, text = "Load Database", fg_color="transparent", border_width=2, text_color=("gray30", "#DCE4EE"), command=self.LoadDB)
            self.Load_button.grid(row=11, column=0, columnspan = 2, padx=(5, 5), pady=(10, 5), sticky="nsew")


        def browse_f06file(self):
            path = customtkinter.filedialog.askopenfilename(filetypes=[("NASTRAN f06", ".f06")])
            if path != "":             
                self.f06file.delete("0.0","end") 
                self.f06file.insert("0.0",path)
                FilesFrame.f06path=path

        def browse_sinexh5file(self):
            path = customtkinter.filedialog.askopenfilename(filetypes=[("NASTRAN results", ".h5")])
            if path != "":                
                self.sinexh5.delete("0.0","end") 
                self.sinexh5.insert("0.0",path)
                FilesFrame.sinexh5path=path

        def browse_sineyh5file(self):
            path = customtkinter.filedialog.askopenfilename(filetypes=[("NASTRAN results", ".h5")])
            if path != "":                
                self.sineyh5.delete("0.0","end") 
                self.sineyh5.insert("0.0",path)
                FilesFrame.sineyh5path=path

        def browse_sinezh5file(self):
            path = customtkinter.filedialog.askopenfilename(filetypes=[("NASTRAN results", ".h5")])
            if path != "":                
                self.sinezh5.delete("0.0","end") 
                self.sinezh5.insert("0.0",path)
                FilesFrame.sinezh5path=path

        def browse_QScsvfile(self):
            path = customtkinter.filedialog.askopenfilename(filetypes=[("Excel file", ".csv")])
            if path != "":
                self.QScsv.delete("0.0","end") 
                self.QScsv.insert("0.0",path)
                FilesFrame.QScsvpath=path

        def browse_SINEcsvfile(self):
            path = customtkinter.filedialog.askopenfilename(filetypes=[("Excel file", ".csv")])
            if path != "":               
                self.SINEcsv.delete("0.0","end") 
                self.SINEcsv.insert("0.0",path)
                FilesFrame.SINEcsvpath=path

        def browse_rndxh5file(self):
            path = customtkinter.filedialog.askopenfilename(filetypes=[("NASTRAN results", ".h5")])
            if path != "":                
                self.rndxh5.delete("0.0","end") 
                self.rndxh5.insert("0.0",path)
                FilesFrame.rndxh5path=path

        def browse_rndyh5file(self):
            path = customtkinter.filedialog.askopenfilename(filetypes=[("NASTRAN results", ".h5")])
            if path != "":                
                self.rndyh5.delete("0.0","end") 
                self.rndyh5.insert("0.0",path)
                FilesFrame.rndyh5path=path

        def browse_rndzh5file(self):
            path = customtkinter.filedialog.askopenfilename(filetypes=[("NASTRAN results", ".h5")])
            if path != "":                
                self.rndzh5.delete("0.0","end") 
                self.rndzh5.insert("0.0",path)
                FilesFrame.rndzh5path=path

        def browse_RNDcsvfile(self):
            path = customtkinter.filedialog.askopenfilename(filetypes=[("Excel file", ".csv")])
            if path != "":                
                self.RNDcsv.delete("0.0","end") 
                self.RNDcsv.insert("0.0",path)
                FilesFrame.RNDcsvpath=path

        def browse_output(self):
            path = customtkinter.filedialog.asksaveasfilename(title="Select directory for saving the output csv files", filetypes=[("Excel file", ".csv")])
            if path != "":
                self.output.delete("0.0","end") 
                self.output.insert("0.0",path)
                FilesFrame.outputpath=path

        def LoadDB(self):
            DBpath = customtkinter.filedialog.askopenfilename(title="Select database to load...", filetypes=[("Excel file", ".xlsx")])

            excelbook = pd.read_excel(DBpath, usecols="B", keep_default_na= False)
            allfileslist = excelbook['File paths'].tolist()

            if DBpath != "":                
                self.f06file.delete("0.0","end") 
                self.f06file.insert("0.0",allfileslist[0])
                FilesFrame.f06path=allfileslist[0]

                self.sinexh5.delete("0.0","end") 
                self.sinexh5.insert("0.0",allfileslist[1])
                FilesFrame.sinexh5path=allfileslist[1]

                self.sineyh5.delete("0.0","end") 
                self.sineyh5.insert("0.0",allfileslist[2])
                FilesFrame.sineyh5path=allfileslist[2]

                self.sinezh5.delete("0.0","end") 
                self.sinezh5.insert("0.0",allfileslist[3])
                FilesFrame.sinezh5path=allfileslist[3]

                self.QScsv.delete("0.0","end") 
                self.QScsv.insert("0.0",allfileslist[4])
                FilesFrame.QScsvpath=allfileslist[4]

                self.SINEcsv.delete("0.0","end") 
                self.SINEcsv.insert("0.0",allfileslist[5])
                FilesFrame.SINEcsvpath=allfileslist[5]

                self.rndxh5.delete("0.0","end") 
                self.rndxh5.insert("0.0",allfileslist[6])
                FilesFrame.rndxh5path=allfileslist[6]

                self.rndyh5.delete("0.0","end") 
                self.rndyh5.insert("0.0",allfileslist[7])
                FilesFrame.rndyh5path=allfileslist[7]
                
                self.rndzh5.delete("0.0","end") 
                self.rndzh5.insert("0.0",allfileslist[8])
                FilesFrame.rndzh5path=allfileslist[8]

                self.RNDcsv.delete("0.0","end") 
                self.RNDcsv.insert("0.0",allfileslist[9])
                FilesFrame.RNDcsvpath=allfileslist[9]
                
                self.output.delete("0.0","end") 
                self.output.insert("0.0",allfileslist[10])
                FilesFrame.outputpath=allfileslist[10] 

    
class RunsFrame(customtkinter.CTkFrame,):
        def __init__(self, master):
            super().__init__(master)                     
                       
            self.RunAll_button = customtkinter.CTkButton(master=self, text = "RUN", fg_color="transparent", border_width=2, text_color=("gray30", "#DCE4EE"), command=self.RunALL_)
            self.RunAll_button.grid(row=0, column=0, columnspan = 1, padx=(5, 5), pady=(10, 5), sticky="nsew")

            self.Save_button = customtkinter.CTkButton(master=self, text = "Save Database", fg_color="transparent", border_width=2, text_color=("gray30", "#DCE4EE"), command=self.SaveDB)
            self.Save_button.grid(row=0, column=1, columnspan = 1, padx=(5, 5), pady=(10, 5), sticky="nsew")
            

        def RunALL_(self):

            f06path = (FilesFrame.f06path).replace("/", '\\')
            sinexh5path= (FilesFrame.sinexh5path).replace("/", '\\')
            sineyh5path = (FilesFrame.sineyh5path).replace("/", '\\')
            sinezh5path = (FilesFrame.sinezh5path).replace("/", '\\')
            QScsvpath = (FilesFrame.QScsvpath).replace("/", '\\')
            SINEcsvpath = (FilesFrame.SINEcsvpath).replace("/", '\\')
            rndxh5path = (FilesFrame.rndxh5path).replace("/", '\\')
            rndyh5path = (FilesFrame.rndyh5path).replace("/", '\\')
            rndzh5path = (FilesFrame.rndzh5path).replace("/", '\\')
            RNDcsvpath = (FilesFrame.RNDcsvpath).replace("/", '\\')
            outputpath = (FilesFrame.outputpath).replace("/", '\\')

            import pathlib
            DBpath = pathlib.Path(outputpath)
            DBpath = (str(DBpath.parent)+"/GUIdatabase.xlsx").replace("/", '\\')

                 
            writeDB(DBpath ,f06path,sinexh5path,sineyh5path,sinezh5path,QScsvpath,SINEcsvpath,rndxh5path,rndyh5path,rndzh5path,RNDcsvpath,outputpath)

            PNC.PrimaryNotchingCalculator(DBpath)        


        def SaveDB(self):
            global DBpath
            DBpath = customtkinter.filedialog.asksaveasfilename(title="Select directory for saving Database", filetypes=[("Excel file", ".xlsx")])

            f06path = (FilesFrame.f06path).replace("/", '\\')
            sinexh5path= (FilesFrame.sinexh5path).replace("/", '\\')
            sineyh5path = (FilesFrame.sineyh5path).replace("/", '\\')
            sinezh5path = (FilesFrame.sinezh5path).replace("/", '\\')
            QScsvpath = (FilesFrame.QScsvpath).replace("/", '\\')
            SINEcsvpath = (FilesFrame.SINEcsvpath).replace("/", '\\')
            rndxh5path = (FilesFrame.rndxh5path).replace("/", '\\')
            rndyh5path = (FilesFrame.rndyh5path).replace("/", '\\')
            rndzh5path = (FilesFrame.rndzh5path).replace("/", '\\')
            RNDcsvpath = (FilesFrame.RNDcsvpath).replace("/", '\\')
            outputpath = (FilesFrame.outputpath).replace("/", '\\')

            writeDB(DBpath,f06path,sinexh5path,sineyh5path,sinezh5path,QScsvpath,SINEcsvpath,rndxh5path,rndyh5path,rndzh5path,RNDcsvpath,outputpath)
      

def writeDB(path,f06,SXh5,SYh5,SZh5,QScsv,Sinecsv,RXh5,RYh5,RZh5,RNDcsv,output):
    import csv 
    import xlsxwriter
    
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet()

    worksheet.write("A2", "*.f06 path")
    worksheet.write("A3", "*.h5 X file")
    worksheet.write("A4", "*.h5 Y file")
    worksheet.write("A5", "*.h5 Z file")
    worksheet.write("A6", "QS csv file")
    worksheet.write("A7", "Sine csv file")
    worksheet.write("A8", "*.h5 X file")
    worksheet.write("A9", "*.h5 Y file")
    worksheet.write("A10", "*.h5 Z file")
    worksheet.write("A11", "Random csv file")
    worksheet.write("A12", "Output path")

    worksheet.write("B1", "File paths")
    worksheet.write("B2", f06)
    worksheet.write("B3", SXh5)
    worksheet.write("B4", SYh5)
    worksheet.write("B5", SZh5)
    worksheet.write("B6", QScsv)
    worksheet.write("B7", Sinecsv)
    worksheet.write("B8", RXh5)
    worksheet.write("B9", RYh5)
    worksheet.write("B10", RZh5)
    worksheet.write("B11", RNDcsv)
    worksheet.write("B12", output)

    workbook.close()


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Sine and Random Primary Notching")
        self.geometry(f"{680}x{600}")
        self.after(10, self.eval, f'tk::PlaceWindow {self} center')

        self.FilesFrame = FilesFrame(self)
        self.FilesFrame.grid(row=0, column=0, padx=10, pady=(20, 0), sticky="n")

        self.RunsFrame = RunsFrame(self)
        self.RunsFrame.grid(row=1, column=0,columnspan = 2, padx=20, pady=(20, 15), sticky="s")


        self.WindowSettingsFrame = WindowSettings(self)
        self.WindowSettingsFrame.grid(row=2, column=0, padx=20, pady=(15, 15), sticky="s")       


if __name__ == "__main__":
    App().mainloop()

