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
    if inputsine !="":
        # Notches the responses and plots each notched profile - Sine
        print("Performing Sine Notching")
        getsinelevels(inputsine)
        h5_notchsine(inputh5x, sinespec, storeTX, storeTY, storeTZ, storeRX, storeRY, storeRZ,xcog, ycog, zcog, "X")
        h5_notchsine(inputh5y, sinespec, storeTX, storeTY, storeTZ, storeRX, storeRY, storeRZ,xcog, ycog, zcog, "Y")
        h5_notchsine(inputh5z, sinespec, storeTX, storeTY, storeTZ, storeRX, storeRY, storeRZ,xcog, ycog, zcog, "Z")
    if inputrandom != "": 
        # Performs primarynotching on random level
        print("Performing Random Notching")
        getrandomlevels(inputrandom)
        h5_notchrandom(inputrh5x,randomspec, "X")
        h5_notchrandom(inputrh5y,randomspec, "Y")
        h5_notchrandom(inputrh5z,randomspec, "Z")
    elif inputrandom == "" and inputsine == "":
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
    global inputf06, inputh5x, inputh5y, inputh5z, outpath, inputlevels, inputrandom, inputsine, analysis, inputrh5x, inputrh5y , inputrh5z    
        
    excelbook = pd.read_excel(pathcsv, usecols="B", keep_default_na= False)
    allfileslist = excelbook['File paths'].tolist()
    # Get input file paths
    inputf06 = allfileslist[0]
    inputh5x = allfileslist[1]
    inputh5y = allfileslist[2]
    inputh5z = allfileslist[3]
    inputlevels = allfileslist[4]
    inputsine = allfileslist[5]
    inputrh5x = allfileslist[6]
    inputrh5y = allfileslist[7]
    inputrh5z = allfileslist[8]
    inputrandom = allfileslist[9]

    # Get output file paths
    outpath = allfileslist[10]

    if inputrandom == "":
        analysis = "sine"
    else:
        analysis = "random"
    return inputf06, inputh5x, inputh5y, inputh5z, outpath, inputlevels, inputrandom, inputsine, analysis, inputrh5x, inputrh5y , inputrh5z     

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

    if ".csv" in outputpath:
        outputpath = outputpath
    else:
        outputpath = outputpath + ".csv"

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
def h5_notchrandom(h5file,randomspec, subcase:str):
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

        # Retrieving the first frequency
        ModalFreq = f["NASTRAN/RESULT/SUMMARY/EIGENVALUE"][()]
        firstfreq = ModalFreq[0]["FREQ"]

        
        SPCDloads = np.stack((Eigendata[MaskEigen,1],SPCFcplx[MaskSPCD,0],SPCFcplx[MaskSPCD,1],SPCFcplx[MaskSPCD,2],SPCFcplx[MaskSPCD,3],
                    SPCFcplx[MaskSPCD,4],SPCFcplx[MaskSPCD,5],SPCFcplx[MaskSPCD,6]), axis=0)
        
        # Gets linear interpolated sine spec curve for each subcase
        loginterprandomspec(SPCDloads[0],randomspec,subcase)

        # Gets the semiempirical limit load curve for random notching
        SemiEmpiricalRandom(10,mass,firstfreq,randomcurve)
        LimForceCurve = np.stack([randomcurve[0],LimForce], axis=0)

        # Calculate the PSDout
        repeat = randomcurve.T[:,1]
        PSDin = np.stack([repeat, repeat, repeat, repeat, repeat, repeat], axis = 1)       
        PSDout = (np.absolute(SPCDloads.T[:,2:8])**2)*PSDin*(9.81**2)
        PSDout = PSDout.T

        ratioFX = LimForceCurve[1]/PSDout[0]
        ratioFY = LimForceCurve[1]/PSDout[1]
        ratioFZ = LimForceCurve[1]/PSDout[2]
        ratioFX[ratioFX > 1] = 1
        ratioFY[ratioFY > 1] = 1
        ratioFZ[ratioFZ > 1] = 1
        enveloperation = (np.stack((ratioFX,ratioFY,ratioFZ,), axis = 0).T).min(1) 

        # Save notched profile as csv
        csvwrite2darray(h5file,randomcurve[0],(enveloperation*randomcurve[1]), "Freq [Hz]", "Random " + subcase + " [g^2/Hz]")    
  
        # PLOTING CURVES
        fig, axs = plt.subplots(2, 3)
        axs[0, 0].set_title("Random "+ subcase + " Notch profile")
        axs[0, 0].set_ylabel("PSD [g^2/Hz]")
        axs[0, 0].set_xlabel("Frequency [Hz]")       
        axs[0, 0].plot(randomcurve[0], randomcurve[1], "r-", label = "Input Profile", linewidth=2)
        axs[0, 0].legend(fontsize="8")

        axs[0, 1].set_title("Notch Ratios")
        axs[0, 1].set_ylabel("-")
        axs[0, 1].set_xlabel("Frequency [Hz]")       
        axs[0, 1].plot(randomcurve[0], enveloperation, "k--", label = "Envelope of Ratios", linewidth=2)
        axs[0, 1].legend(fontsize="8")

        axs[0, 2].set_title("Notched Profile")
        axs[0, 2].set_ylabel("PSD [g^2/Hz]")
        axs[0, 2].set_xlabel("Frequency [Hz]")
        axs[0, 2].plot(randomcurve[0], randomcurve[1], "k--", label = "Unnotched Profile", linewidth=1.5)       
        axs[0, 2].plot(SPCDloads[0], enveloperation*randomcurve[1], "r-", label = "Notched Profile", linewidth=2)
        axs[0, 2].legend(fontsize="8")

        axs[1, 0].set_title("FX")
        axs[1, 0].set_ylabel("FSD [N^2/Hz]")
        axs[1, 0].set_xlabel("Frequency [Hz]")       
        axs[1, 0].plot(LimForceCurve[0], LimForceCurve[1], "k--", label = "Lim Force Profile", linewidth=1)
        axs[1, 0].plot(SPCDloads[0], PSDout[0], "r--", label = "Unnotched FX", linewidth=1)
        axs[1, 0].plot(SPCDloads[0], PSDout[0]*enveloperation, "r-", label = "NotchedFX", linewidth=2)
        axs[1, 0].legend(fontsize="8")

        axs[1, 1].set_title("FY")
        axs[1, 1].set_ylabel("FSD [N^2/Hz]")
        axs[1, 1].set_xlabel("Frequency [Hz]")       
        axs[1, 1].plot(LimForceCurve[0], LimForceCurve[1], "k--", label = "Lim Force Profile", linewidth=1)
        axs[1, 1].plot(SPCDloads[0], PSDout[1], "b--", label = "Unnotched FY", linewidth=1)
        axs[1, 1].plot(SPCDloads[0], PSDout[1]*enveloperation, "b-", label = "NotchedFY", linewidth=2)
        axs[1, 1].legend(fontsize="8")

        axs[1, 2].set_title("FZ")
        axs[1, 2].set_ylabel("FSD [N^2/Hz]")
        axs[1, 2].set_xlabel("Frequency [Hz]")       
        axs[1, 2].plot(LimForceCurve[0], LimForceCurve[1], "k--", label = "Lim Force Profile", linewidth=1)
        axs[1, 2].plot(SPCDloads[0], PSDout[2], "g--", label = "Unnotched FZ", linewidth=1)
        axs[1, 2].plot(SPCDloads[0], PSDout[2]*enveloperation, "g-", label = "NotchedFZ", linewidth=2)
        axs[1, 2].legend(fontsize="8")

        for ax in fig.get_axes():
            ax.set_xscale("log")
            ax.set_yscale("log")
            ax.set_xlim(left=min(SPCDloads[0]))
            ax.set_xlim(right=max(SPCDloads[0]))


        fig.suptitle("Random "+ subcase + " Primary Notching",fontsize = 14)
        fig.set_size_inches(20,11)
        fig.tight_layout()        
        plt.show()
        fig.savefig(h5file[:-3] + "_nochedprofile.png")       

# Function to read the h5 file data and process the SPCD forces wrt. notch limits
def h5_notchsine(h5file,inputsine, storeTX, storeTY, storeTZ, storeRX, storeRY, storeRZ, CoGX, CoGY, CoGZ, subcase: str):
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

        
        # Calculates the sine limits along the frequency range
        calcsinelimits(SPCDloads[0], storeTX, storeTY, storeTZ, storeRX, storeRY, storeRZ)

        # Gets linear interpolated sine spec curve for each subcase
        lininterpsinespec(SPCDloads[0],inputsine,subcase)

        # Calculate sine notch ratios and retrieves the ratios and envelope
        sinenotchratios(limitFX,limitFY,limitFZ,limitRX,limitRY,limitRZ,SPCDloads,sinecurve, CoGX, CoGY, CoGZ)

        # Gets notched profile by multiplying the notch ratios by the sine curve
        notchedprofile = enveloperation*sinecurve[1]

        # Save notched profile as csv
        csvwrite2darray(h5file,SPCDloads[0],notchedprofile,"Freq [Hz]", "Sine " + subcase + " [g]") 

        # PLOTING CURVES
        fig, axs = plt.subplots(3, 3)
        axs[0, 0].set_title("Notch profile")
        axs[0, 0].set_ylabel("Acceleration [g]")
        axs[0, 0].set_xlabel("Frequency [Hz]")       
        axs[0, 0].plot(SPCDloads[0], sinecurve[1], "k--", label = "Input Profile", linewidth=2)
        axs[0, 0].plot(SPCDloads[0], notchedprofile, label = "Notched Profile")
        axs[0, 0].legend(fontsize="7")
        
        axs[0, 1].set_title("Notch triggers")
        axs[0, 1].set_ylabel("-")
        axs[0, 1].set_xlabel("Frequency [Hz]")         
        axs[0, 1].plot(SPCDloads[0], enveloperation, 'k:', label = "Envelope ratios", linewidth=2)
        axs[0, 1].plot(SPCDloads[0], ratioFX, label = "Ratio FX")
        axs[0, 1].plot(SPCDloads[0], ratioFY, label = "Ratio FY")
        axs[0, 1].plot(SPCDloads[0], ratioFZ, label = "Ratio FZ")
        if axialdirection != "X": 
            axs[0, 1].plot(SPCDloads[0], ratioRX, label = "Ratio MX")
        if axialdirection != "Y":
            axs[0, 1].plot(SPCDloads[0], ratioRY, label = "Ratio MY")
        if axialdirection != "Z":
            axs[0, 1].plot(SPCDloads[0], ratioRZ, label = "Ratio MZ")
        axs[0, 1].legend(fontsize="7")

        axs[0, 2].set_title("FX")
        axs[0, 2].set_ylabel("Force [N]")
        axs[0, 2].set_xlabel("Frequency [Hz]")          
        axs[0, 2].plot(limitFX[0], limitFX[1], 'r', label = "Limit FX")
        axs[0, 2].plot(SPCDloads[0], np.absolute(notchedprofile*SPCDloads[2]*9.81), label = "Notched FX", linewidth=2)
        axs[0, 2].plot(SPCDloads[0], np.absolute(sinecurve[1]*SPCDloads[2]*9.81),  'g--', label = "Unnotched FX")     
        axs[0, 2].legend(fontsize="7")

        axs[1, 0].set_title("FY")
        axs[1, 0].set_ylabel("Force [N]")
        axs[1, 0].set_xlabel("Frequency [Hz]")         
        axs[1, 0].plot(limitFY[0], limitFY[1], 'r', label = "Limit FY")
        axs[1, 0].plot(SPCDloads[0], np.absolute(notchedprofile*SPCDloads[3]*9.81), label = "Notched FY", linewidth=2)
        axs[1, 0].plot(SPCDloads[0], np.absolute(sinecurve[1]*SPCDloads[3]*9.81),  'g--', label = "Unnotched FY")       
        axs[1, 0].legend(fontsize="7")

        axs[1, 1].set_title("FZ")
        axs[1, 1].set_ylabel("Force [N]")
        axs[1, 1].set_xlabel("Frequency [Hz]")         
        axs[1, 1].plot(limitFZ[0], limitFZ[1], 'r', label = "Limit FZ")
        axs[1, 1].plot(SPCDloads[0], np.absolute(notchedprofile*SPCDloads[4]*9.81), label = "Notched FZ", linewidth=2)
        axs[1, 1].plot(SPCDloads[0], np.absolute(sinecurve[1]*SPCDloads[4]*9.81),  'g--', label = "Unnotched FZ")        
        axs[1, 1].legend(fontsize="7")

        axs[1, 2].set_title("MX")
        axs[1, 2].set_ylabel("Moment [N.m]")
        axs[1, 2].set_xlabel("Frequency [Hz]")         
        axs[1, 2].plot(limitRX[0], limitRX[1], 'r', label = "Limit MX")
        axs[1, 2].plot(SPCDloads[0], np.absolute(notchedprofile*SPCDloads[5]*9.81), label = "Notched MX", linewidth=2)
        axs[1, 2].plot(SPCDloads[0], np.absolute(sinecurve[1]*SPCDloads[5]*9.81),  'g--', label = "Unnotched MX")        
        axs[1, 2].legend(fontsize="7")

        axs[2, 0].set_title("MY")
        axs[2, 0].set_ylabel("Moment [N.m]")
        axs[2, 0].set_xlabel("Frequency [Hz]")         
        axs[2, 0].plot(limitRY[0], limitRY[1], 'r', label = "Limit MY")
        axs[2, 0].plot(SPCDloads[0], np.absolute(notchedprofile*SPCDloads[6]*9.81), label = "Notched MY", linewidth=2)
        axs[2, 0].plot(SPCDloads[0], np.absolute(sinecurve[1]*SPCDloads[6]*9.81),  'g--', label = "Unnotched MY")      
        axs[2, 0].legend(fontsize="7")

        axs[2, 1].set_title("MZ")
        axs[2, 1].set_ylabel("Moment [N.m]")
        axs[2, 1].set_xlabel("Frequency [Hz]")          
        axs[2, 1].plot(limitRZ[0], limitRZ[1], 'r', label = "Limit MZ")
        axs[2, 1].plot(SPCDloads[0], np.absolute(notchedprofile*SPCDloads[7]*9.81), label = "Notched MZ", linewidth=2)
        axs[2, 1].plot(SPCDloads[0], np.absolute(sinecurve[1]*SPCDloads[7]*9.81),  'g--', label = "Unnotched MZ")      
        axs[2, 1].legend(fontsize="7")



        for ax in fig.get_axes():
            ax.set_xscale("linear")
            ax.set_yscale("linear")
            ax.set_ylim(bottom=0)
            ax.set_xlim(left=min(SPCDloads[0]))
            ax.set_xlim(right=max(SPCDloads[0]))
            ax.set_xticks(np.arange(min(SPCDloads[0]), max(SPCDloads[0]), 10.0))


        fig.suptitle("Sine "+ subcase + " Primary Notching",fontsize = 14)
        fig.delaxes(axs[2,2])
        fig.set_size_inches(20,11)
        fig.tight_layout()        
        plt.show()        
        fig.savefig(h5file[:-3] + "_nochedprofile.png")

# Read the random input levels
def getrandomlevels(filerandom):
    import pandas as pd
    import numpy as np

    global randomspec
    randomspec = []        
    FreqX = (pd.read_csv(filerandom, delimiter=',', usecols=[0], keep_default_na= False).to_numpy().T)[0]
    FreqY = (pd.read_csv(filerandom, delimiter=',', usecols=[2], keep_default_na= False).to_numpy().T)[0]
    FreqZ = (pd.read_csv(filerandom, delimiter=',', usecols=[4], keep_default_na= False).to_numpy().T)[0]
    LevelsX = (pd.read_csv(filerandom, usecols=[1], keep_default_na= False).to_numpy().T)[0]
    LevelsY = (pd.read_csv(filerandom, usecols=[3], keep_default_na= False).to_numpy().T)[0]
    LevelsZ = (pd.read_csv(filerandom, usecols=[5], keep_default_na= False).to_numpy().T)[0]
    randomspec = np.vstack([FreqX,LevelsX,FreqY,LevelsY,FreqZ,LevelsZ]).T

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

# Converts the notch limits to limits over the freq range
def calcsinelimits(freq,FX,FY,FZ,MX,MY,MZ):
    import numpy as np
    global limitFX,limitFY,limitFZ,limitRX,limitRY,limitRZ
    limitFX = np.stack((freq,np.full((len(freq)),abs(FX))), axis=0)
    limitFY = np.stack((freq,np.full((len(freq)),abs(FY))), axis=0)
    limitFZ = np.stack((freq,np.full((len(freq)),abs(FZ))), axis=0)
    limitRX = np.stack((freq,np.full((len(freq)),abs(MX))), axis=0)
    limitRY = np.stack((freq,np.full((len(freq)),abs(MY))), axis=0)
    limitRZ = np.stack((freq,np.full((len(freq)),abs(MZ))), axis=0)

# Calculates the notch ratios for sine (limit/SPCFload)
def sinenotchratios(limFX,limFY,limFZ,limRX,limRY,limRZ,h5results,sinecurve,X,Y,Z):
    import numpy as np
    global ratioFX,ratioFY,ratioFZ,ratioRX,ratioRY,ratioRZ, enveloperation
    ratioFX = np.absolute(limFX[1]/(h5results[2]*sinecurve[1]*9.81))
    ratioFY = np.absolute(limFY[1]/(h5results[3]*sinecurve[1]*9.81))
    ratioFZ = np.absolute(limFZ[1]/(h5results[4]*sinecurve[1]*9.81))
    ratioRX = np.absolute(limRX[1]/(h5results[5]*sinecurve[1]*9.81))
    ratioRY = np.absolute(limRY[1]/(h5results[6]*sinecurve[1]*9.81))
    ratioRZ = np.absolute(limRZ[1]/(h5results[7]*sinecurve[1]*9.81))

    detectaxial(X,Y,Z)
    ratioFX[ratioFX > 1] = 1
    ratioFY[ratioFY > 1] = 1
    ratioFZ[ratioFZ > 1] = 1
    ratioRX[ratioRX > 1] = 1
    ratioRY[ratioRY > 1] = 1
    ratioRZ[ratioRZ > 1] = 1
    if axialdirection == "X":
        enveloperation = (np.stack((ratioFX,ratioFY,ratioFZ,ratioRY,ratioRZ), axis = 0).T).min(1)
    elif axialdirection =="Y":
        enveloperation = (np.stack((ratioFX,ratioFY,ratioFZ,ratioRX,ratioRZ), axis = 0).T).min(1)
    elif axialdirection =="Z":
        enveloperation = (np.stack((ratioFX,ratioFY,ratioFZ,ratioRX,ratioRY), axis = 0).T).min(1)

# Converts the sine spec dataset to data over the frequency range - LINEAR INTERPOLATION
def lininterpsinespec(freq,inputspec,direction):
    import numpy as np
    global sinecurve
    if direction == "X":
        sinecurve = np.stack((freq,np.interp(freq,inputspec[:,0],inputspec[:,1])), axis=0)
    elif direction  == "Y":
        sinecurve = np.stack((freq,np.interp(freq,inputspec[:,2],inputspec[:,3])), axis=0)
    elif direction  == "Z":
        sinecurve = np.stack((freq,np.interp(freq,inputspec[:,4],inputspec[:,5])), axis=0)

# Function to write any array of 2 columns in csv format
def csvwrite2darray(path,arrayX,arrayY,titleX:str,titleY:str):
    import csv
    import numpy as np
    path = path[:-3] + "_nochedprofile.csv"
    array = np.stack((arrayX,arrayY), axis = 1)
    with open(str(path), "w", newline="") as f:
    # creating the writer
        writer = csv.writer(f)
        writer.writerow([titleX,titleY])
        for row in array:
            writer.writerow([row[0],row[1]])

# Detect what is the axial direction of the S/C. Returns X, Y or Z
def detectaxial(Xcog,Ycog,Zcog):
    global axialdirection
    if Xcog > Ycog and Xcog > Zcog:
        axialdirection = "X"
    elif Ycog > Xcog and Ycog > Zcog:
        axialdirection = "Y"
    elif Zcog > Xcog and Zcog > Ycog:
        axialdirection = "Z"

# Converts the sine spec dataset to data over the frequency range - LINEAR INTERPOLATION
def loginterprandomspec(freq,inputspec,direction):
    import numpy as np
    import math as m
    global randomcurve

    def loginterp(newx, oldx, oldy):
        newyvalues = []
        for x in newx:
            for i in range(len(oldx)-1):                               
                if x >= oldx[i] and x <= oldx[i+1]:                  
                    x0 = oldx[i]
                    x1 = oldx[i+1]
                    y0 = oldy[i]
                    y1 = oldy[i+1]

            newy =m.exp(m.log(y0) + ((m.log(x/x0))*((m.log(y1/y0)/m.log(x1/x0)))))
            if x == 20:
                print(x)
                print(x0)
                print(m.log(x/x0))
            newyvalues.append(newy)

        newyvalues = np.array(newyvalues)
        return newyvalues                             


    if direction == "X":
        randomcurve = np.stack((freq,loginterp(freq,inputspec[:,0],inputspec[:,1])), axis=0)
    elif direction  == "Y":
        randomcurve = np.stack((freq,loginterp(freq,inputspec[:,2],inputspec[:,3])), axis=0)
    elif direction  == "Z":
        randomcurve = np.stack((freq,loginterp(freq,inputspec[:,4],inputspec[:,5])), axis=0)

# Calculates the semiempirical random limit force
def SemiEmpiricalRandom(C,itemmass,f0,randomdata):
    import numpy as np
    global LimForce
    itemmass = float(itemmass)
    LimForce = []
    Trandomdata = np.transpose(randomdata)
    id = 0
    for rowrandom in Trandomdata[:,0]:
        if rowrandom < f0:
            Force = C*(itemmass**2)*Trandomdata[id,1]*(9.81**2)  
        elif rowrandom >= f0:
            Force = C*(itemmass**2)*Trandomdata[id,1]*((f0/rowrandom)**2)*(9.81**2)
        id=id+1                    
        LimForce.append(Force)




# Temporary - Just for debugging
#mainfile = r"N:\YODA_I8\20_ANALYSIS\10_SINE\GUIdatabase.xlsx"
#mainfile = r"N:\IS45_Tank\20_ANALYSIS\GUIdatabase.xlsx"
#PrimaryNotchingCalculator(mainfile)