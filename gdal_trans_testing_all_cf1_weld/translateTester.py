#!/usr/bin/env python

import os, sys, subprocess

origTiff = "CONUS.week01.2010.h10v10.v1.5.Band1_TOA_REF_small.tif"
outPath = os.path.join(".", "out")
ncCoOpts = "-co WRITEGDALTAGS=yes"

projTuples = [
    ("AEA", "Albers Equal Area", "EPSG:3577", "albers_conical_equal_area",
        ['standard_parallel', 'longitude_of_central_meridian',
         'latitude_of_projection_origin', 'false_easting', 'false_northing']),
    ("AZE", "Azimuthal Equidistant", "EPSG:54032", "azimuthal_equidistant",
        ['longitude_of_projection_origin',
         'latitude_of_projection_origin', 'false_easting', 'false_northing'])
    ]

if not os.path.exists(outPath):
    os.makedirs(outPath)

for proj in projTuples:
    projTiff = os.path.join(outPath, "%s_%s.tif" % (origTiff.rstrip('.tif'), proj[0] ))
    projOpts = "-a_srs %s" % (proj[2])
    cmd = " ".join(['gdal_translate', projOpts, origTiff, projTiff])
    print cmd
    subprocess.call(cmd, shell=True)
    print "Translated %s to %s" % (proj[0], projTiff)
    projNc = os.path.join(outPath, "%s_%s.nc" % (origTiff.rstrip('.tif'), proj[0] ))
    cmd = " ".join(['gdal_translate', "-of netCDF", ncCoOpts, projTiff, projNc])
    print cmd
    subprocess.call(cmd, shell=True)
    print "Translated to %s" % (projNc)
    cmd = " ".join(['ncdump -h', projNc, "> %s.ncdump" % (projNc)])
    subprocess.call(cmd, shell=True)
    dumpFile = open("%s.ncdump" % (projNc), "r")
    dumpStr = dumpFile.read()
    for attrib in proj[4]:
        if attrib not in dumpStr:
            print "**Error for proj '%s': CF-1 attrib '%s' not found.**" % \
                (proj[0], attrib)

