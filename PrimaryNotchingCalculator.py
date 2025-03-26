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


    # Notches the responses and plots each notched profile - RANDOM
    if inputrandom != "":
        # Gets the random loads into an array
        getrandomlevels(inputrandom)
        h5_notchrandom(inputh5,randomspec)
    elif inputsine !="":   
        # Notches the responses and plots each notched profile - Sine
        getsinelevels(inputsine)
        h5_notchsine(inputh5, sinespec, storeTX, storeTY, storeTZ, storeRX, storeRY, storeRZ)
    else:
        import sys
        sys.exit("No file specified with inputs for Random or Sine.")
        

    # --- END OF SCRIPT --- #
    print("DONE")



####################################################################
###             FUNCTION SECTION - DO NOT MODIFY HERE            ###
#################################################################### 
# Function to retrieve all the input file paths
def loadallpaths(pathcsv):
    import pandas as pd

    # Set variables as global
    global inputf06, inputh5, outpath, inputlevels, inputrandom, inputsine, analysis      
        
    excelbook = pd.read_excel(pathcsv, usecols="B", keep_default_na= False)
    allfileslist = excelbook['File paths'].tolist()
    # Get input file paths
    inputf06 = allfileslist[0]
    inputh5 = allfileslist[1]
    inputlevels = allfileslist[2]
    inputsine = allfileslist[3]
    inputrandom = allfileslist[4]

    # Get output file paths
    outpath = allfileslist[5]

    if inputrandom == "":
        analysis = "sine"
    else:
        analysis = "random"
    return inputf06, inputh5, outpath, inputlevels, inputrandom, inputsine, analysis 

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
    global storeTX, storeTY, storeTZ, storeRX, storeRY, storeRZ

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
    return storeTX, storeTY, storeTZ, storeRX, storeRY, storeRZ

# Function to read the h5 file data and process the SPCD forces wrt. notch limits
def h5_notchrandom(h5file,randomspec):
    import h5py
    import numpy as np
    import matplotlib.pyplot as plt    

    with h5py.File(h5file, "r") as f:
        # Retrieving the SPCD node
        SPCDgroup = f["NASTRAN/RESULT/NODAL/SPC_FORCE_CPLX"][()]
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
        
        # Interpolation of the random spec to "match" the analysis freq range
        randomcurve = np.interp(SPCDaccel[0],randomspec[:,0],randomspec[:,1])

        
        fig, axs = plt.subplots(2, 3)
        axs[0, 0].plot(SPCDaccel[0], abs(SPCDaccel[2]))
        axs[0, 0].plot(SPCDaccel[0], randomcurve)
        axs[0, 0].plot(randomspec[:,0], randomspec[:,1])
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

# Function to read the h5 file data and process the SPCD forces wrt. notch limits
def h5_notchsine(h5file,inputsine, storeTX, storeTY, storeTZ, storeRX, storeRY, storeRZ):
    import h5py
    import numpy as np
    import matplotlib.pyplot as plt    

    with h5py.File(h5file, "r") as f:
        # Retrieving the SPCD node
        SPCDgroup = f["NASTRAN/RESULT/NODAL/SPC_FORCE_CPLX"][()]
        SPCDnode = SPCDgroup[0]["ID"]

        #Get frequency per domainID
        DomainList = f["INDEX/NASTRAN/RESULT/NODAL/SPC_FORCE_CPLX"]["DOMAIN_ID"]

        #Get frequency per domainID
        Eigendata = np.array((f["NASTRAN/RESULT/DOMAINS"]["ID","TIME_FREQ_EIGR"]).tolist())

        #Get SPCforce per frequency
        SPCFcplx = np.array((f["NASTRAN/RESULT/NODAL/SPC_FORCE_CPLX"]["ID","XR","YR","ZR","RXR","RYR","RZR","DOMAIN_ID"]).tolist())
        
        # Masking the domains which are wrt. sine and masking the SPCD accel data only
        MaskSPCD = np.isin(SPCFcplx[:,0],SPCDnode)
        MaskEigen = np.isin(Eigendata[:,0],DomainList)

        
        SPCDloads = np.stack((Eigendata[MaskEigen,1],SPCFcplx[MaskSPCD,0],SPCFcplx[MaskSPCD,1],SPCFcplx[MaskSPCD,2],SPCFcplx[MaskSPCD,3],
                    SPCFcplx[MaskSPCD,4],SPCFcplx[MaskSPCD,5],SPCFcplx[MaskSPCD,6]), axis=0)
        
        # Sine profiles and notch limits arranged per frequency value
        sineXcurve = np.stack((SPCDloads[0],np.interp(SPCDloads[0],inputsine[:,0],inputsine[:,1])), axis=0)
        sineYcurve = np.stack((SPCDloads[0],np.interp(SPCDloads[0],inputsine[:,2],inputsine[:,3])), axis=0)
        sineZcurve = np.stack((SPCDloads[0],np.interp(SPCDloads[0],inputsine[:,4],inputsine[:,5])), axis=0)

        limitFX = np.stack((SPCDloads[0],np.full((len(SPCDloads[0])),abs(storeTX))), axis=0)
        limitFY = np.stack((SPCDloads[0],np.full((len(SPCDloads[0])),abs(storeTY))), axis=0)
        limitFZ = np.stack((SPCDloads[0],np.full((len(SPCDloads[0])),abs(storeTZ))), axis=0)
        limitRX = np.stack((SPCDloads[0],np.full((len(SPCDloads[0])),abs(storeRX))), axis=0)
        limitRY = np.stack((SPCDloads[0],np.full((len(SPCDloads[0])),abs(storeRY))), axis=0)
        limitRZ = np.stack((SPCDloads[0],np.full((len(SPCDloads[0])),abs(storeRZ))), axis=0)


        ratioFX = np.absolute(limitFX[1]/(SPCDloads[2]*sineXcurve[1]*9.81))
        ratioFY = np.absolute(limitFY[1]/(SPCDloads[3]*sineXcurve[1]*9.81))
        ratioFZ = np.absolute(limitFZ[1]/(SPCDloads[4]*sineXcurve[1]*9.81))
        ratioRX = np.absolute(limitRX[1]/(SPCDloads[5]*sineXcurve[1]*9.81))
        ratioRY = np.absolute(limitRY[1]/(SPCDloads[6]*sineXcurve[1]*9.81))
        ratioRZ = np.absolute(limitRZ[1]/(SPCDloads[7]*sineXcurve[1]*9.81))
        
        
        ratioFX[ratioFX > 1] = 1
        ratioFY[ratioFY > 1] = 1
        ratioFZ[ratioFZ > 1] = 1
        ratioRX[ratioRX > 1] = 1
        ratioRY[ratioRY > 1] = 1
        ratioRZ[ratioRZ > 1] = 1
        enveloperatio = (np.stack((ratioFX,ratioFY,ratioFZ,ratioRX,ratioRY,ratioRZ), axis = 0).T).min(1)

        notchedX = enveloperatio*sineXcurve[1]  


        
        fig, axs = plt.subplots(3, 3)        
        axs[0, 0].set_title("Sine X Notch profiles")        
        axs[0, 0].plot(SPCDloads[0], sineXcurve[1], label = "Input Profile")
        axs[0, 0].plot(SPCDloads[0], notchedX, label = "Notched Profile")
        axs[0, 0].legend(fontsize="7")
        
        axs[0, 1].set_title("Sine X Notch ratios")        
        axs[0, 1].plot(SPCDloads[0], enveloperatio, 'tab:orange', label = "Envelope ratios")
        axs[0, 1].plot(SPCDloads[0], ratioFX, label = "Ratio FX")
        axs[0, 1].plot(SPCDloads[0], ratioFY, label = "Ratio FY")
        axs[0, 1].plot(SPCDloads[0], ratioFZ, label = "Ratio FZ")
        axs[0, 1].plot(SPCDloads[0], ratioRX, label = "Ratio MX")
        axs[0, 1].plot(SPCDloads[0], ratioRY, label = "Ratio MY")
        axs[0, 1].plot(SPCDloads[0], ratioRZ, label = "Ratio MZ")
        axs[0, 1].legend(fontsize="7")

        axs[0, 2].set_title("Notched FX")        
        axs[0, 2].plot(limitFX[0], limitFX[1], 'tab:orange', label = "Limit FX")
        axs[0, 2].plot(SPCDloads[0], np.absolute(notchedX*SPCDloads[2]*9.81), label = "SPC - Fx")     
        axs[0, 2].legend(fontsize="7")

        axs[1, 0].set_title("Notched FY")        
        axs[1, 0].plot(limitFY[0], limitFY[1], 'tab:orange', label = "Limit FY")
        axs[1, 0].plot(SPCDloads[0], np.absolute(notchedX*SPCDloads[3]*9.81), label = "SPC - FY")     
        axs[1, 0].legend(fontsize="7")

        axs[1, 1].set_title("Notched FZ")        
        axs[1, 1].plot(limitFZ[0], limitFZ[1], 'tab:orange', label = "Limit FZ")
        axs[1, 1].plot(SPCDloads[0], np.absolute(notchedX*SPCDloads[4]*9.81), label = "SPC - FZ")     
        axs[1, 1].legend(fontsize="7")

        axs[1, 2].set_title("Notched MX")        
        axs[1, 2].plot(limitRX[0], limitRX[1], 'tab:orange', label = "Limit MX")
        axs[1, 2].plot(SPCDloads[0], np.absolute(notchedX*SPCDloads[5]*9.81), label = "SPC - MX")     
        axs[1, 2].legend(fontsize="7")

        axs[2, 0].set_title("Notched MY")        
        axs[2, 0].plot(limitRY[0], limitRY[1], 'tab:orange', label = "Limit MY")
        axs[2, 0].plot(SPCDloads[0], np.absolute(notchedX*SPCDloads[6]*9.81), label = "SPC - MY")     
        axs[2, 0].legend(fontsize="7")

        axs[2, 1].set_title("Notched MZ")        
        axs[2, 1].plot(limitRZ[0], limitRZ[1], 'tab:orange', label = "Limit MZ")
        axs[2, 1].plot(SPCDloads[0], np.absolute(notchedX*SPCDloads[7]*9.81), label = "SPC - MZ")     
        axs[2, 1].legend(fontsize="7")





        for ax in fig.get_axes():
            ax.set_xscale("linear")
            ax.set_yscale("linear")   
        plt.show()

# Read the random input levels
def getrandomlevels(filerandom):
    import pandas as pd
    import numpy as np

    global randomspec
    randomspec = []        
    listfreqs = (pd.read_csv(filerandom, delimiter=',', usecols=[0], keep_default_na= False).to_numpy().T)[0]
    listlevels = (pd.read_csv(filerandom, usecols=[1], keep_default_na= False).to_numpy().T)[0]
    randomspec = np.vstack([listfreqs,listlevels]).T

# Read the random input levels
def getsinelevels(filesine):
    import pandas as pd
    import numpy as np

    global sinespec
    sinespec = []        
    FreqX = (pd.read_csv(filesine, delimiter=',', usecols=[0], keep_default_na= False).to_numpy().T)[0]
    FreqY = (pd.read_csv(filesine, delimiter=',', usecols=[2], keep_default_na= False).to_numpy().T)[0]
    FreqZ = (pd.read_csv(filesine, delimiter=',', usecols=[4], keep_default_na= False).to_numpy().T)[0]
    LevelsX = (pd.read_csv(filesine, usecols=[1], keep_default_na= False).to_numpy().T)[0]
    LevelsY = (pd.read_csv(filesine, usecols=[3], keep_default_na= False).to_numpy().T)[0]
    LevelsZ = (pd.read_csv(filesine, usecols=[5], keep_default_na= False).to_numpy().T)[0]
    sinespec = np.vstack([FreqX,LevelsX,FreqY,LevelsY,FreqZ,LevelsZ]).T

# Temporary - Just for debug
mainfile = r"N:\YODA_I8\20_ANALYSIS\10_SINE\FileManager.xlsx"
PrimaryNotchingCalculator(mainfile)