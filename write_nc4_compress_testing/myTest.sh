#!/bin/bash
export CUSTOM_GDAL_PATH="/home/pds/+Codes/gdal_trunk_netcdfWork-git-nc4/gdal"
. $CUSTOM_GDAL_PATH/update_path.sh
gdal_translate -of netCDF -co FILETYPE=NC melb-small.tif melb-small-nc.nc
gdal_translate -of netCDF -co FILETYPE=NC2 melb-small.tif melb-small-nc2.nc
gdal_translate -of netCDF -co FILETYPE=NC4 melb-small.tif melb-small-nc4.nc
gdal_translate -of netCDF -co FILETYPE=NC4C melb-small.tif melb-small-nc4c.nc
gdal_translate -of netCDF -co FILETYPE=NC4C -co COMPRESS=deflate -co ZLEVEL=1\
    melb-small.tif melb-small-nc4c-z1.nc
gdal_translate -of netCDF -co FILETYPE=NC4C -co COMPRESS=deflate -co ZLEVEL=5\
    melb-small.tif melb-small-nc4c-z5.nc
gdal_translate -of netCDF -co FILETYPE=NC4C -co COMPRESS=deflate -co ZLEVEL=9\
    melb-small.tif melb-small-nc4c-z9.nc
