
def h5_notchdata(h5file,randomspec):
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
        axs[0, 0].plot(randomspec[:,0], abs(randomspec[:,1]))
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

 
h5file = "C:/Users/a.silva/OneDrive - Swissto12/Desktop/Tool_TESTS/fem_is45_v90e_2000_sine_x.h5"
h5_notchdata(h5file)
