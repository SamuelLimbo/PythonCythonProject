#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     :: Data ::

class data_class(): #Construct the constructor and getter methods
    #Constructor::____________________________________________________________________________________________________
    def __init__(self):
        pass

    #Methods::________________________________________________________________________________________________________
    def all_filters(self, System, Filter, TypeOfReturn):
        #_____________________________________________________________________________________________________________
        #Description:: System Filter and TypeOfReturn are all integers. "TypeOfReturn" if equal to 1 allows us to ret-
        #              urn only one element from the catalogue mapping corresponding to the choosen filter.
        #_____________________________________________________________________________________________________________
        List = [ [["J", "Jmag", "2MASS"], ["H", "Hmag", "2MASS"], ["Ks", "Ksmag", "2MASS"],
                  ["M", "Mmag", "Washington"], ["T2", "T2mag", "Washington"],
                  ["3.6", "_3.6mag", "Spitzer/IRAC"], ["4.5", "_4.5mag", "Spitzer/IRAC"],
                  ["5.8", "_5.8mag", "Spitzer/IRAC"], ["8.0", "_8.0mag", "Spitzer/IRAC"],
                  ["W2", "_4.5magW", "WISE"]],

                 [["V", "UVM2mag", "XMM-OT"], ["V", "UVW1mag", "XMM-OT"],
                  ["V", "Umag", "XMM-OT"], ["B", "Bmag", "XMM-OT"],
                  ["V", "Vmag", "XMM-OT"]] ]

        if TypeOfReturn == 1:
            return List[System - 1][Filter - 1]

        else:
            return List[System - 1]
