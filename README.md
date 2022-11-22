#PythonCythonProject: Compute the SED using the Simbad and VizieR databases. 

In order to run the program the first thing to be done is to untar the astro.tar. In the terminal write:

   >>> tar -xzvf astro.tar.gz

   >>> cd astro

   >>> make

Once this is done we need to to compile the cython extension:

   >>> python setup.py build_ext --inplace

Then, simply running the main.py in the terminal will lauch the program.
The user will simply need to follow the instructions displayed on the terminal.
