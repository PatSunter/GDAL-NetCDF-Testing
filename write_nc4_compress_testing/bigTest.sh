/usr/bin/time -f "%E, %P, %M"  gdal_translate -of netCDF -co FILETYPE=NC L71092086_08620110129_B10.TIF L71092086_08620110129_B10-nc.nc
/usr/bin/time -f "%E, %P, %M"   gdal_translate -of netCDF -co FILETYPE=NC4C -co COMPRESS=deflate -co ZLEVEL=1 L71092086_08620110129_B10.TIF L71092086_08620110129_B10-nc4c-z1.nc
/usr/bin/time -f "%E, %P, %M"   gdal_translate -of netCDF -co FILETYPE=NC4C -co COMPRESS=deflate -co ZLEVEL=9 L71092086_08620110129_B10.TIF L71092086_08620110129_B10-nc4c-z9.nc
