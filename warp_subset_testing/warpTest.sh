ULX=1050000
#ULX=1054929
ULX=1054929
ULY=-4218968
LRX=1060889
LRY=-4221948
#gdalwarp -overwrite -t_srs epsg:3112 -r bilinear -of VRT melb-small.tif melb-small-3112.vrt
#gdalwarp -overwrite -of GTIFF -te $ULX $LRY $LRX $ULY -tr 30 30 melb-small-3112.vrt melb-small-3112-moved.tif
gdalwarp -t_srs epsg:3112 -overwrite -of GTIFF -te $ULX $LRY $LRX $ULY -ts 500 300 melb-small.tif melb-small-3112-moved.tif
