Version of GDAL-NetCDF uses to create these results:

repo: git@github.com:etiennesky/gdal-netcdf.git
branch: netcdf-nc4
commit 5df4acd646881b8ef9ba3de81521935ecd0340a7
Author: PatSunter <patdevelop@gmail.com>
Date:   Thu Oct 20 10:10:23 2011 +1100

    Updated so scanline arrays in CreateCopy are allocated only to size of 1 scanline, as ET suggested (should save a lot of memory for large datasets).
    Also moved variable definition, scanline allocation etc to be in consistent order.

