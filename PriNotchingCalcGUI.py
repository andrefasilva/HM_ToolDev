from hw import *
from hw.hv import *
from hwx.xmlui import gui
from hwx import gui as gui2
import os
import csv


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

    def calculatenotch(mass,xcog,ycog,zcog,levelx,levely,levelz):
        global TX, TY, TZ, RX, RY, RZ
        TX = round(float(mass)*float(levelx)*9.81,2)
        TY = round(float(mass)*float(levely)*9.81,2)
        TZ = round(float(mass)*float(levelz)*9.81,2) 
        RX = round((TZ*float(ycog))+(TY*float(zcog)),2)
        RY = round((TZ*float(xcog))+(TX*float(zcog)),2)
        RZ = round((TY*float(xcog))+(TX*float(ycog)),2)

    def loadcomb(csvinput):
        global permutations
        inputlvl = []
        with open(csvinput, newline='') as csvinfile:
            inputlevels = csv.reader(csvinfile, delimiter=' ', quotechar='|')
            for row in inputlevels:
                inputlvl.append(row)

        combinations = []
        permutations = []
        for eachrow in inputlvl[1:]:
            combinations.append(tuple(eachrow))

        for comb in combinations:
            comb = comb[0].split(",")
            Xlvl=round(float(comb[0]),2)
            Ylvl=round(float(comb[1]),2)
            Zlvl=round(float(comb[2]),2)
            variations = (
            [Xlvl,Ylvl,Zlvl],[Xlvl,Ylvl*(-1),Zlvl],[Xlvl,Ylvl*(-1),Zlvl*(-1)],
            [Xlvl*(-1),Ylvl,Zlvl],[Xlvl*(-1),Ylvl*(-1),Zlvl],[Xlvl*(-1),Ylvl*(-1),Zlvl*(-1)],
            [Xlvl,Ylvl,Zlvl*(-1)],[Xlvl*(-1),Ylvl,Zlvl*(-1)]            
            )   
            permutations.append(variations)
   
    def onClose(event):
        dialog.Hide()

    def onRun(event):
        dialog.Hide()
        openf06(f06file.value)
        loadcomb(inputfile.value)

        # Save results to csv
        with open(str(csvfile.value), "w", newline="") as f:
        # creating the writer
            writer = csv.writer(f)
            writer.writerow(["X-level","Y-level","Z-level","FX", "FY", "FZ", "MX", "MY", "MZ"])
            combin = []
            storeTX = 0
            storeTY = storeTX
            storeTZ = storeTX
            storeRX = storeTX
            storeRY = storeTX
            storeRZ = storeTX
            for permid in permutations:
                for combin in permid:
                    levelx = combin[0]
                    levely = combin[1]
                    levelz = combin[2]                    
                    calculatenotch(mass,xcog,ycog,zcog,levelx,levely,levelz)
                    # using writerow to write individual record one by one
                    writer.writerow([levelx,levely,levelz, TX, TY, TZ, RX, RY, RZ])
                    if abs(TX) > abs(storeTX):
                        storeTX = TX
                    if abs(TY) > abs(storeTY):
                        storeTY = TY
                    if abs(TZ) > abs(storeTZ):
                        storeTZ = TZ
                    if abs(RX) > abs(storeRX):
                        storeRX = RX
                    if abs(RY) > abs(storeRY):
                        storeRY = RY
                    if abs(RZ) > abs(storeRZ):
                        storeRZ = RZ

        
        # Save results to csv
        with open(str(csvfile.value[:-4]+"_limits.csv"), "w", newline="") as f2:
        # creating the writer
            writer2 = csv.writer(f2)
            writer2.writerow(["FX", "FY", "FZ", "MX", "MY", "MZ"])
            writer2.writerow([abs(storeTX), abs(storeTY), abs(storeTZ), abs(storeRX), abs(storeRY), abs(storeRZ)])
        gui2.tellUser("Done!")


    def comboboxFunc(event):
        direction = event.value
        pass

    # CSV with input loads 
    inputlabel = gui.Label(text="*.csv file with input loads")
    inputfile = gui.OpenFileEntry(placeholdertext="csv file load path", filetypes="*.csv", title = "Select the input levels csv file")

    # Entry to specify the f06 file path
    f06label = gui.Label(text="Load *.f06 file")
    f06file = gui.OpenFileEntry(placeholdertext="Browse f06 file", filetypes="*.f06", title = "Select the f06 file with weightcheck data")
    
    # CSV path 
    csvlabel = gui.Label(text="*.csv file save")
    csvfile = gui.SaveFileEntry(placeholdertext="csv file save path", filetypes="*.csv", title = "Select the desired output csv file path")

    # Buttons for running or closing dialog
    close = gui.Button("Close", command=onClose)
    create = gui.Button("Run", command=onRun)

    mainFrame = gui.VFrame(
        (inputlabel, 10, inputfile),
        (f06label, 10, f06file),
        (csvlabel, 10, csvfile),
        ("<->"),
        (create, close),
    )

    dialog = gui.Dialog(caption="Calculating primary notch levels")
    dialog.recess().add(mainFrame)
    dialog.setButtonVisibile("ok", False)
    dialog.setButtonVisibile("cancel", False)
    dialog.show(width=450, height=170)

GUIprimarynotching()