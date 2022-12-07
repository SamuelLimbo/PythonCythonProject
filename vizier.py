#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     :: Imports ::

import functions
from astropy.table import QTable
from astropy.table import Table

from data import data_class

#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     :: Vizier API ::

class vizier_api_class(data_class):
    #Constructor::____________________________________________________________________________________________________
    def __init__(self, Target):
        self.Target = Target
        data_class.__init__(self)

    #Methods::________________________________________________________________________________________________________
    def vizier_api(self):
        #_____________________________________________________________________________________________________________
        #Description:: Gathers the information given by the "self.select_a_filter" method and then returns a table of
        #              the targets IDs and their respective fluxe in a given chosen filter.
        #_____________________________________________________________________________________________________________
        A      = self.filter_choice()
        url    = "https://vizier.cds.unistra.fr/viz-bin/votable?-source=" + A[0] + "&-c=" + self.Target + "&-c.rd=" + A[4] + "&-out.all=1"
        table  = Table.read(url)
        Fluxes = table[A[2]]
        Target = table["ID"]

        returns        = functions.wrap_c_search_vega_filter(A[3], A[1], 0, 0, 0)
        fmag           = returns[2] #returns[2] returns the zero magnitude for a given filter and system
        fluxes_in_jsky = []
        target_list    = [] #empty list that will contain the names of the targets

        for mag in Fluxes.data:
            fluxes_in_jsky.append(functions.wrap_c_to_jsky(fmag, mag))
        for targets in Target.data:
            target_list.append(targets)

        t = QTable([target_list, fluxes_in_jsky],
                    names = ("Target ID", "Flux (jsky)"),
                    meta  = {'Samuel': 'Second table'})
        print("\n", t, "\n") #Print a astopy tab


    def filter_choice(self):
        #_____________________________________________________________________________________________________________
        #Description:: Asks and returns the name of the table (TableName), the name of the filter (FilterName), the n-
        #              ame of the column (ColumnName) and the name of the system (System)
        #_____________________________________________________________________________________________________________
        Condition1 = 0
        Condition2 = 0
        Radius = input("Let's now extract some photometry from VizieR. To do so, please first enter the radius of your conesearch in degrees: ")
        TableName, FilterName, ColumnName, SystemName = "Ar", "a", "n", "za"
        while Condition1 == 0:
            print("\n1. III/284/allstars\n2. II/340/xmmom2_1\n3. Other table")
            TableTest = input("Please enter your choice: ")
            TT = int(TableTest)

            if TT == 1:
                Condition1 = 1
                TableName  = "III/284/allstars"
                TargetName = "Target"
                Print      = self.all_filters(1, 0, 0)
                while Condition2 == 0:
                    for i in range(len(Print)):
                        if i == 0:
                            print("\n")
                        print(f"{i+1}. {Print[i][0]} from the {Print[i][2]} system")

                    FilterTest = input("Please enter the number of the filter you would like to use: ")
                    FT = int(FilterTest)

                    if FT >= 1 and FT <= 10:
                        Condition2 = 1
                        List_Names = self.all_filters(TT, FT, 1) #e.g. (1, 1, 1) -> ['J', 'Jmag', '2MASS']
                        FilterName = List_Names[0]
                        ColumnName = List_Names[1]
                        SystemName = List_Names[2]

            if TT == 2:
                Condition1 = 1
                TableName  = "II/340/xmmom2_1"
                TargetName = "ObsID"
                Print      = self.all_filters(2, 0, 0)
                while Condition2 == 0:
                    for i in range(len(Print)):
                        if i == 0:
                            print("\n")
                        print(f"{i+1}. {Print[i][0]} from the {Print[i][2]} system")

                    FilterTest = input("Please enter the number of the filter you would like to use: ")
                    FT = int(FilterTest)

                    if FT >= 1 and FT <= 5:
                        Condition2 = 1
                        List_Names = self.all_filters(TT, FT, 1)
                        FilterName = List_Names[0]
                        ColumnName = List_Names[1]
                        SystemName = List_Names[2]

            if TT == 3:
                Condition1 = 1
                print("\nPlease follow the following instructions.\n")
                TableName  = input("Name of the table: ")
                FilterName = input("Name of the filter: ")
                ColumnName = input("Name of the column corresponding to the choosen filter (VizieR table): ")
                SystemName = input("Name of the system: ")

            else:
                continue

        return TableName, FilterName, ColumnName, SystemName, Radius
