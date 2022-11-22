import functions
import re
import urllib.request as http
import urllib.parse
from astropy.table import QTable
from astropy import units as u
from astropy.coordinates import Angle

#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     :: Simbad Resolver ::

class simbad_resolver_class():
    #Constructor::____________________________________________________________________________________________________
    def __init__(self, TargetChoice): #This TargetChoice will be used while calling the function from sed_coord_class
        if TargetChoice == 0:
            List_Targets = ["HD1", "sirius", "3C273"]
            print("\n1. HD1\n2. sirius\n3. 3C273\n4. Other")
            Condition = 0
            while Condition == 0:
                NbTarget_ = input("Please enter the number of your desired target:: ")
                NbTarget  = int(NbTarget_)
                if NbTarget >= 1 and NbTarget <= 3:
                    self.TargeT = List_Targets[NbTarget - 1]
                    Condition = 1
                if NbTarget == 4:
                    self.TargeT = input("Name of the star:: ")
        else:
            self.TargeT = TargetChoice

        self.url = "https://simbad.u-strasbg.fr/simbad/sim-id?output.format=ascii&Ident=" + self.TargeT

        self.data            = {} #Initialisation of an empty dicitonnary
        self.correct_filters = [] #Empty list, will store the names (as strings) of the filters found on simbad

        self.table      = 0
        self.degree_ra  = 0
        self.degree_dec = 0


    #Getters::________________________________________________________________________________________________________

    def Get_target(self):
        return self.TargeT
        
    def Get_degree(self):
        return self.degree_ra, self.degree_dec
        
    #Methods::________________________________________________________________________________________________________
    def gather_simbad_data(self):
        #_____________________________________________________________________________________________________________
        #Description:: This method allows us to look for the coordinates and the different magnitudes and their errors
        #              in the different filters. The values are stored in the self.data dictionary
        #_____________________________________________________________________________________________________________
        Filters = ["U", "B", "V", "R", "I", "J", "H", "K", "L", "M"] #List of strings (different filters)
        with http.urlopen(self.url) as fd:
            for line in fd:
                Line_String = line.decode('utf-8').strip()
                if Line_String.find("Coordinates(ICRS,ep=J2000,eq=2000)") != -1: #Find the text corresponding
                    if re.search(r"\s\d\d\s\d\d\s\d\d\.\d\d", Line_String): #Search this pattern
                        RA = re.findall(r"\s\d\d\s\d\d\s\d\d\.\d\d", Line_String) #Extract the pattern
                        self.data.update({'ra': RA[0]}) #Add text and its corresponding value to the dictionnary

                    if re.search(r"[\+-]\d\d\s\d\d\s\d\d\.\d\d", Line_String):
                        DEC = re.findall(r"[\+-]\d\d\s\d\d\s\d\d\.\d\d", Line_String)
                        self.data.update({'dec': DEC[0]})

                for filter_name in Filters: #Goes through all the possible filters
                    if Line_String.find("Flux " + filter_name) != -1: #Find the text "Flux U" for instance
                        if re.search(r"(?<=:\s)(.*)(?=\s)", Line_String):
                            flux = re.findall(r"(?<=:\s)(.*)(?=\s\[)", Line_String)
                            self.data.update({filter_name: flux[0]})
                            self.correct_filters.append(filter_name)

                        if re.search(r"(?<=\[)(.*)(?=\])", Line_String):
                            err_flux = re.findall(r"(?<=\[)(.*)(?=\])", Line_String)
                            self.data.update({filter_name + "err": err_flux[0]})
                            
        if len(self.data) == 0: #This means that no data have been found on simbad.
            return 0
        else:
            return 1


    def jsky_and_wavelengths(self):
        #_____________________________________________________________________________________________________________
        #Description:: Updates to jsky the values of the different fluxes in the "self.data" dictionary, and returns 1
        #              dictionary, each elements being a list [wave_center, wave_width]
        #_____________________________________________________________________________________________________________
        wave = {}
        for key in self.correct_filters: #Loop over all the possible filters found in the simbad text
            returns = functions.wrap_c_search_vega_filter("Johnson", key, 0, 0, 0) #Returns three floats
            wave.update({key: [returns[0], returns[1]]})
            fmag         = returns[2]
            fmag_in_jsky = functions.wrap_c_to_jsky(fmag, float(self.data[key]))
            self.data[key] = fmag_in_jsky #Update of the self.data to jsky fluxes
        return wave


    def readable_table(self):
        #_____________________________________________________________________________________________________________
        #Description:: Gets the information previously aquired in the "gather_simbad_data" method and builds a table
        #_____________________________________________________________________________________________________________
        A = self.gather_simbad_data()

        print("The position of the object is::")
        print("    ra:  ", self.data["ra"])
        print("    dec: ", self.data["dec"], "\n")

        A = self.to_degrees()

        wave_data = self.jsky_and_wavelengths() #Gets the values from the wave center/width from the above method

        values_names = ("Filter", "Wavelength center", "Wavelength width", "Flux (jsky)", "Flux error")
        filter_names, wavelength_center, wavelength_width, flux, flux_err = [], [], [], [], []
        filter_names = self.correct_filters #Names of the different correct filters

        for key in filter_names:
            wavelength_center.append(wave_data[key][0]) #Corresponding wavelength centers
            wavelength_width.append(wave_data[key][1]) #Corresponding wavelength widths
            flux.append(self.data[key]) #Corresponding fluxes in jsky
            flux_err.append(self.data[key + "err"]) #Corresponding errors on fluxes

        t = QTable([filter_names, wavelength_center, wavelength_width, flux, flux_err],
                   names = values_names,
                   meta  ={'Samuel': 'First table'})
        print(t, "\n \n") #Print a astopy tab


    def to_degrees(self):
        #_____________________________________________________________________________________________________________
        #Description:: Converts the hour angles of the ra and dec into degrees. Returns the ra and dec in degrees
        #_____________________________________________________________________________________________________________
        self.degree_ra = Angle(self.data["ra"] + " hours").degree #Use the degree from astropy

        d = [float(i) for i in self.data["dec"].split()] #Separates all the numbers of the string storing the dec

        min_    = str(d[1]) + "\'" #Add special caracters allowing to do the conversion here from arcmin to deg
        sec_    = str(d[2]) + "\""
        min_deg = Angle(min_).degree #Conversion is done here
        sec_deg = Angle(sec_).degree

        if self.data["dec"][0] == "+": #Determines the sign of the declination
            self.degree_dec = d[0] + min_deg + sec_deg #Adds up all the contibutions deg + ' + "
        else:
            self.degree_dec = d[0] - min_deg - sec_deg

        print("The position of the object in degrees is::")
        print("    ra:  ", self.degree_ra)
        print("    dec: ", self.degree_dec, "\n")
