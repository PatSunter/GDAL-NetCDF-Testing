The aim in this directory is:

1. Start with a known WELD dataset, which we've grabbed a 500x500 slice out of.
The original dataset is in AEA coordinates.

2. Do a gdal_warp to create a copy of this data projected into every allowed CF-1 conventions dataset - and save these to an intermediate directory

3. Translate each of these to NetCDF.

4. Check that all the required attribs from http://cf-pcmdi.llnl.gov/documents/cf-conventions/1.5/apf.html made it across.
