####################################################################
###                    AUTHOR - André Silva                      ###
####################################################################
#
# Gets the f06 file and extracts the mass and COG, then calculates
# the primary notch forces and moments and extracts the respective
# combinations. The results are written to a csv file.
# Reads the h5 file with the SPCforces and plots the results and
# plots the primary nothed profiles.
#___________________________________________________________________


def PrimaryNotchingCalculator(filemanager):
 

    ####################################################################
    ###                  PRIMARY NOTCHING CALCULATOR                 ###
    #################################################################### 
   
    # Loads all the paths to manage the files
    loadallpaths(filemanager)

    # Open the f06 file and extract the mass and COG
    openf06(inputf06)

    # Calculate the primary notch forces and moments and respective combinations
    loadcomb(inputlevels)

    # Writes the loads (detailed and max limits) to 2 csv files
    csvwriteloads(outpath)

    # Notches the responses and plots each notched profile
    h5_notchdata(inputh5)

    # --- END OF SCRIPT --- #
    print("DONE")



####################################################################
###             FUNCTION SECTION - DO NOT MODIFY HERE            ###
#################################################################### 
# Function to retrieve all the input file paths
def loadallpaths(pathcsv):
    import pandas as pd

    # Set variables as global
    global inputf06, inputh5, outpath, inputlevels      
        
    excelbook = pd.read_excel(pathcsv, usecols="B", keep_default_na= False)
    allfileslist = excelbook['File paths'].tolist()
    # Get input file paths
    inputf06 = allfileslist[0]
    inputh5 = allfileslist[1]
    inputlevels = allfileslist[2]

    # Get output file paths
    outpath = allfileslist[3]
    return inputf06, inputh5, outpath, inputlevels 

# Function to read the f06 file and extract the mass and COG
def openf06(filepath):
    global mass, xcog, ycog, zcog
    WClines = []
    Superlines = []
    masslines = []
    setAlines = []
    extendedfile = []
    WCstring = "                                           O U T P U T   F R O M   W E I G H T   C H E C K"
    Super = "SUPERELEMENT 0"
    massstring ="MASS AXIS SYSTEM (S)"
    noSE = "DEGREES OF FREEDOM SET = A"
    file = open(filepath,"r")       
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

# Function to calculate the primary notch forces and moments
def calculatenotchlimits(mass,xcog,ycog,zcog,levelx,levely,levelz):
    global TX, TY, TZ, RX, RY, RZ
    TX = round(float(mass)*float(levelx)*9.81,2)
    TY = round(float(mass)*float(levely)*9.81,2)
    TZ = round(float(mass)*float(levelz)*9.81,2) 
    RX = round((TZ*float(ycog))+(TY*float(zcog)),2)
    RY = round((TZ*float(xcog))+(TX*float(zcog)),2)
    RZ = round((TY*float(xcog))+(TX*float(ycog)),2)

# Function to compute the load combinations
def loadcomb(csvinput):
    import csv
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

# Function to write the loads to a csv file
def csvwriteloads(outputpath):
    import csv
    print(outputpath)
    with open(str(outputpath), "w", newline="") as f:
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
                calculatenotchlimits(mass,xcog,ycog,zcog,levelx,levely,levelz)
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
    with open(str(outputpath[:-4]+"_limits.csv"), "w", newline="") as f2:
    # creating the writer
        writer2 = csv.writer(f2)
        writer2.writerow(["FX", "FY", "FZ", "MX", "MY", "MZ"])
        writer2.writerow([abs(storeTX), abs(storeTY), abs(storeTZ), abs(storeRX), abs(storeRY), abs(storeRZ)])

# Function to read the h5 file data and process the SPCD forces wrt. notch limits
def h5_notchdata(h5file):
    import h5py
    import numpy as np
    import matplotlib.pyplot as plt    

    with h5py.File(h5file, "r") as f:
        # Retrieving the SPCD node
        SPCDgroup = f["NASTRAN/INPUT/CONSTRAINT/SPCD"][()]
        SPCDnode = SPCDgroup[0][1]

        #Get frequency per domainID
        DomainList = f["INDEX/NASTRAN/RESULT/NODAL/ACCELERATION_CPLX"]["DOMAIN_ID"]

        #Get frequency per domainID
        Eigendata = np.array((f["NASTRAN/RESULT/DOMAINS"]["ID","TIME_FREQ_EIGR"]).tolist())

        #Get SPCforce per frequency
        SPCFcplx = np.array((f["NASTRAN/RESULT/NODAL/SPC_FORCE_CPLX"]["ID","XR","YR","ZR","RXR","RYR","RZR","DOMAIN_ID"]).tolist())
        
        # Masking the domains which are wrt. sine and masking the SPCD accel data only
        MaskSPCD = np.isin(SPCFcplx[:,0],SPCDnode)
        MaskEigen = np.isin(Eigendata[:,0],DomainList)

        
        SPCDaccel = np.stack((Eigendata[MaskEigen,1],SPCFcplx[MaskSPCD,0],SPCFcplx[MaskSPCD,1],SPCFcplx[MaskSPCD,2],SPCFcplx[MaskSPCD,3],
                    SPCFcplx[MaskSPCD,4],SPCFcplx[MaskSPCD,5],SPCFcplx[MaskSPCD,6]), axis=0)
        
        
        fig, axs = plt.subplots(2, 3)
        axs[0, 0].plot(SPCDaccel[0], abs(SPCDaccel[2]))
        axs[0, 0].set_title("SPC Force TX")
        axs[0, 1].plot(SPCDaccel[0], abs(SPCDaccel[3]), 'tab:orange')
        axs[0, 1].set_title("SPC Force TY")
        axs[0, 2].plot(SPCDaccel[0], abs(SPCDaccel[4]), 'tab:green')
        axs[0, 2].set_title("SPC Force TZ")

        axs[1, 0].plot(SPCDaccel[0], abs(SPCDaccel[5]))
        axs[1, 0].set_title("SPC Force RX")
        axs[1, 1].plot(SPCDaccel[0], abs(SPCDaccel[6]), 'tab:orange')
        axs[1, 1].set_title("SPC Force RY")
        axs[1, 2].plot(SPCDaccel[0], abs(SPCDaccel[7]), 'tab:green')
        axs[1, 2].set_title("SPC Force RZ")

        for ax in fig.get_axes():
            ax.set_xscale("log")
            ax.set_yscale("log")
        
        plt.show()


mainfile = r"C:\Users\a.silva\OneDrive - Swissto12\Desktop\ToolDev\HM_ToolDev\FileManager.xlsx"
PrimaryNotchingCalculator(mainfile)