from hw import *
from hw.hv import *
from hwx.xmlui import gui
from hwx import gui as gui2
import os
import csv
dir(gui.OpenFileEntry)

def GUIprimarynotching():

    def openf06(filepath):
        global mass, xcog, ycog, zcog
        WClines=[]
        Superlines=[]
        masslines=[]
        setAlines=[]
        extendedfile=[]
        WCstring = "                                           O U T P U T   F R O M   W E I G H T   C H E C K"
        Super = "SUPERELEMENT 0"
        massstring ="MASS AXIS SYSTEM (S)"
        noSE = "DEGREES OF FREEDOM SET = A"
        file = open("%s" % filepath,"r")

        # Finds the lines which have the output from WC and line of Superelement 0
        for lineid, line in enumerate(file):
            extendedfile.append(line)
            if WCstring in line:
                WClines.append(lineid)
            if Super in line:
                Superlines.append(lineid)
            if massstring in line:
                masslines.append(lineid)
            if noSE in line:
                setAlines.append(lineid)
        
        for WCid in  WClines:
            # Checks if superelements are detected
            if Superlines != []:
                for superid in Superlines:
                    for massline in masslines:
                        if (WCid-superid == 2) and (massline-WCid == 15):
                            Xaxis = extendedfile[WCid+16].split()
                            Yaxis = extendedfile[WCid+17].split()
        # Else, in case no superelements are included
        else:
            for setA in setAlines:
                for massline in masslines:
                    if (setA-WCid == 1) and (massline-WCid == 23):
                        Xaxis = extendedfile[WCid+24].split()
                        Yaxis = extendedfile[WCid+25].split()
        mass = Xaxis[1]
        xcog = Yaxis[2]
        ycog = Xaxis[3]
        zcog = Xaxis[4]
        return mass, xcog, ycog, zcog


    def calculatenotch(mass,xcog,ycog,zcog,levelx,levely,levelz,axdir):
        global TX, TY, TZ, RX, RY, RZ
        TX = round(float(mass)*float(levelx)*9.81,2)
        TY = round(float(mass)*float(levely)*9.81,2)
        TZ = round(float(mass)*float(levelz)*9.81,2)
            #Axial direction as X
        if axdir == "lvl1":
            RX = 0
            RY = round((TZ*float(xcog)*9.81)+(TX*float(zcog)*9.81),2)
            RZ = round((TY*float(xcog)*9.81)+(TX*float(ycog)*9.81),2)

        #Axial direction as Y
        elif axdir == "lvl2":
            RX = round((TZ*float(ycog)*9.81)+(TY*float(zcog)*9.81),2)
            RY = 0
            RZ = round((TX*float(ycog)*9.81)+(TY*float(xcog)*9.81),2)

        #Axial direction as Z
        elif axdir == "lvl3":
            RX = round((TY*float(zcog)*9.81)+(TZ*float(ycog)*9.81),2)
            RY = round((TX*float(zcog)*9.81)+(TZ*float(xcog)*9.81),2)
            RZ = 0

    def onClose(event):
        dialog.Hide()

    def onRun(event):
        dialog.Hide()
        openf06(f06file.value)
        calculatenotch(mass,xcog,ycog,zcog,levelx.value,levely.value,levelz.value,combobox.value)

        # Save results to csv
        with open(str(csvfile.value), "w", newline="") as f:
        # creating the writer
            writer = csv.writer(f)
        # using writerow to write individual record one by one
            writer.writerow(["FX", "FY", "FZ", "MX", "MY", "MZ"])
            writer.writerow([TX, TY, TZ, RX, RY, RZ])


    def comboboxFunc(event):
        direction = event.value
        pass

    # Entry to specify the f06 file path
    f06label = gui.Label(text="Load *.f06 file")
    f06file = gui.OpenFileEntry(placeholdertext="Browse f06 file", filetypes="*.f06")
    
    # CSV path 
    csvlabel = gui.Label(text="*.csv file save")
    csvfile = gui.SaveFileEntry(placeholdertext="csv file save path", filetypes="*.csv")

    # Line entries for user data input of QS levels
    labelX = gui.Label(text="QS - X")
    levelx = gui.LineEdit(placeholdertext = "g")
    labelY = gui.Label(text="QS - Y")
    levely = gui.LineEdit(placeholdertext = "g")
    labelZ = gui.Label(text="QS - Z")
    levelz = gui.LineEdit(placeholdertext = "g")
    Directionlabel = gui.Label(text="Axial direction")
    levels = (("lvl1", "X"), ("lvl2", "Y"), ("lvl3", "Z"))
    combobox = gui2.ComboBox(levels, command=comboboxFunc)

    # Buttons for running or closing dialog
    close = gui.Button("Close", command=onClose)
    create = gui.Button("Run", command=onRun)

    mainFrame = gui.VFrame(
        (f06label, 10, f06file),
        (csvlabel, 10, csvfile),
        (labelX, 10, levelx, 30, labelY, 10, levely, 30, labelZ, 10, levelz),
        (Directionlabel, 10, combobox, "<->"),
        (create, close),
    )

    dialog = gui.Dialog(caption="Calculating primary notch levels")
    dialog.recess().add(mainFrame)
    dialog.setButtonVisibile("ok", False)
    dialog.setButtonVisibile("cancel", False)
    dialog.show(width=400, height=200)

GUIprimarynotching()