#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     :: Imports ::

import functions
from astropy.table import Table
import numpy as np
import matplotlib.pyplot as plt

from data import data_class
from simbad import simbad_resolver_class


#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     :: SED and Coordinate plots ::

class sed_coord_class(data_class):
    #Constructor::____________________________________________________________________________________________________
    def __init__(self):
        data_class.__init__(self)

        List_Targets1 = ["TYC4619-98-1", "HD225002", "TYC2275-512-1", "2MASSJ00451128-1325229", "HD223559"]
        List_Targets2 = ["2dFGRSTGS432Z026", "2MASSJ00001719+6221324", "TYC4018-3553-1"]
        print("\n1. III/284/allstars\n2. II/340/xmmom2_1")
        Condition1 = 0

        while Condition1 == 0:
            NbSyst_ = input("Which catalogue would you like to use? ")
            self.NbSyst  = int(NbSyst_)

            if self.NbSyst == 1:
                Catalogue = "III/284/allstars"
                print("\n1. TYC 4619-98-1\n2. HD 225002\n3. 2MASS J00451128-1325229\n4. TYC 2275-512-1\n5. HD 223559\n6. Other")
                Condition2 = 0

                while Condition2 == 0:
                    NbTarget_ = input("Which star would you like to select? ")
                    NbTarget  = int(NbTarget_)

                    if NbTarget >= 1 and NbTarget <= 5:
                        self.Target = List_Targets1[NbTarget - 1]
                        Condition2 = 1
                        
                    if NbTarget == 6:
                        self.Target = input("Please enter the name of the star:: ")
                        Condition2 = 1
                        
                Condition1 = 1

            if self.NbSyst == 2:
                Catalogue = "II/340/xmmom2_1"
                print("\n1. 2dFGRS TGS432Z026\n2. 2MASS J00001719+6221324\n3. TYC 4018-3553-1\n4. Other")
                Condition2 = 0

                while Condition2 == 0:
                    NbTarget_ = input("Which star would you like to select? ")
                    NbTarget  = int(NbTarget_)

                    if NbTarget >= 1 and NbTarget <= 3:
                        self.Target = List_Targets2[NbTarget - 1]
                        Condition2 = 1
                        
                    if NbTarget == 4:
                        self.Target = input("Please enter the name of the star:: ")
                        Condition2 = 1
                        
                Condition1 = 1

        radius_ = input("Radius of the conesearch in degrees: ")

        self.url = "https://vizier.cds.unistra.fr/viz-bin/votable?-out.max=500000&-source=" + Catalogue + "&-c=" + self.Target + "&-c.rd=" + radius_ + "&-out.all=1"

    #Methods::________________________________________________________________________________________________________
    def sed(self):
        #_____________________________________________________________________________________________________________
        #Description:: Calculates the fluxes and their uncertainties in jsky and go look for the lambdas.
        #_____________________________________________________________________________________________________________
        Condition = 0
        while Condition == 0:
            string  = input("1. Yes\n2. No\nWould you like the error bars to be plotted? ")
            WithErr = int(string)
            if WithErr == 1 or WithErr == 2:
                Condition += 1

        table  = Table.read(self.url)
        Names = self.all_filters(self.NbSyst, 1, 0) #0 means we take all the lists of all filters for a given system

        Data_Names  = []
        Data_Fluxes = []

        if self.NbSyst == 1: #III/284/allstars
            for i in range(10):
                if isinstance(table[Names[i][1]].data[1], (np.float32)) == True: #Skip the NaN values
                    Data_Fluxes.append(table[Names[i][1]].data) #Adds the fluxes to the list
                    if i <= 4: #Dinstinction between name of the error columns and no NaN values
                        Data_Fluxes.append(table["e_" + Names[i][1]].data)
                    else:
                        Data_Fluxes.append(table["e" + Names[i][1]].data)

                    Data_Names.append([Names[i][0], Names[i][2]]) #List of a lists, e.g. [["Jmag", "e_Jmag"], ...]

        if self.NbSyst == 2: #II/340/xmmom2_1
            for i in range(5):
                if isinstance(table[Names[i][1]].data[1], (np.float32)) == True:
                    Data_Fluxes.append(table[Names[i][1]].data)
                    Data_Fluxes.append(table["e_" + Names[i][1]].data)
                    Data_Names.append([Names[i][0], Names[i][2]])

        count, Lambda, Lambdad, FMag, Fluxes, Fluxesd  = 0, [], [], [], [], []

        for i in range(0, len(Data_Fluxes), 2):
            returns = functions.wrap_c_search_vega_filter(Data_Names[count][1], Data_Names[count][0], 0, 0, 0)
            FMag.append(returns[2])
            for j in range(len(Data_Fluxes[i])):
                Lambda.append(returns[0])
                Lambdad.append(returns[1])
                Fluxes.append(functions.wrap_c_to_jsky(FMag[count], Data_Fluxes[i][j]))
                Fluxesd.append(Data_Fluxes[i][j]*0.4*functions.wrap_c_to_jsky(FMag[count], Data_Fluxes[i][j]))
            count += 1

        self.plot_sed(Lambda, Fluxes, Fluxesd, Lambdad, WithErr)


    def plot_sed(self, x, y, yerr, xerr, withorwithout):
        #_____________________________________________________________________________________________________________
        #Description:: Simple plot of the sed where withorwithout is a parameter to choose to plot the error bars if
        #              equal to 1 and plot the simple sed if equal to 2
        #_____________________________________________________________________________________________________________
        print(len(y))
        plt.title('Spectral Energy Distribution', fontname = 'Serif', size = 21)
        plt.scatter(x, y, c='black')
        if withorwithout == 1:
            plt.errorbar(x, y, yerr, xerr, fmt='none', ecolor='red', barsabove=True, capsize=3, label='Fit obtained with scipy')
        plt.xlabel('Wavelengths', fontname = 'Serif', size = 17)
        plt.ylabel('Flux (jsky)', fontname = 'Serif', size = 17)
        plt.yscale('log')
        plt.grid()
        plt.show()


    def plot_coord(self):
        #_____________________________________________________________________________________________________________
        #Description:: Plots the coordinates of the stars that have been found in the conesearch
        #_____________________________________________________________________________________________________________
        table  = Table.read(self.url)

        ObjSim = simbad_resolver_class(self.Target)
        A = ObjSim.gather_simbad_data()
        ObjSim.to_degrees()
        coord_star = ObjSim.Get_degree()

        if self.NbSyst == 1:
            ra  = table["RAJ2000"]
            dec = table["DEJ2000"]

        if self.NbSyst == 2:
            ra  = table["RAICRS"]
            dec = table["DEICRS"]

        #plt.title('Coordinate map of surrounding stars', fontname = 'Serif', size = 21)
        plt.plot(ra.data, dec.data, "*", color='gold')
        if A == 1: #This means that data have been found on simbad. If A = 0 no data were found. Prevent errors.
            plt.plot(coord_star[0], coord_star[1], c="darkred", marker="o")
        plt.xlabel('Right Ascension (deg)', fontname = 'Serif', size = 17)
        plt.ylabel('Declination (deg)', fontname = 'Serif', size = 17)
        plt.grid()
        plt.show()
