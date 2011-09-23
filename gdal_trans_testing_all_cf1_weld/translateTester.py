#!/usr/bin/env python

import os, sys, subprocess
import datetime

origTiff = "CONUS.week01.2010.h10v10.v1.5.Band1_TOA_REF_small.tif"
outPath = os.path.join(".", "out")
ncCoOpts = "-co WRITEGDALTAGS=yes"

# TODO: for each projection, need to check the coordinate variables 
# (X and Y) have been created with correct standard_name

# Tuple structure:
#  0: Short code (eg AEA)
#  1: official name from CF-1 conventions
#  2: EPSG code, or WKT, to tell GDAL to do reprojection
#  3: Actual attribute official name of grid mapping
#  4: List of required attributes to define projection
#  5: List of required coordinate variable standard name attributes

projTuples = [
    ("AEA", "Albers Equal Area", "EPSG:3577", "albers_conical_equal_area",
        ['standard_parallel', 'longitude_of_central_meridian',
         'latitude_of_projection_origin', 'false_easting', 'false_northing'],
         ['projection_x_coordinate','projection_y_coordinate']),
    ("AZE", "Azimuthal Equidistant", "EPSG:54032", "azimuthal_equidistant",
        ['longitude_of_projection_origin',
         'latitude_of_projection_origin', 'false_easting', 'false_northing'],
         ['projection_x_coordinate','projection_y_coordinate']),
    ("LAEA", "Lambert azimuthal equal area", "EPSG:2163", "lambert_azimuthal_equal_area",
        ['longitude_of_projection_origin',
         'latitude_of_projection_origin', 'false_easting', 'false_northing'],
         ['projection_x_coordinate','projection_y_coordinate']),
    ("LC", "Lambert conformal", "EPSG:3112", "lambert_conformal_conic",
        ['standard_parallel', # TODO: with 1 or 2 values allowed, checking?
         'longitude_of_central_meridian',
         'latitude_of_projection_origin', 'false_easting', 'false_northing'],
         ['projection_x_coordinate','projection_y_coordinate']),
    ("LCEA", "Lambert Cylindrical Equal Area", "EPSG:3410",
        #Is "Cylindrical_Equal_Area" in WKT
        "lambert_cylindrical_equal_area",
        ['longitude_of_central_meridian',
         'standard_parallel', # TODO: OR 'scale_factor_at_projection_origin' 
         'false_easting', 'false_northing'],
         ['projection_x_coordinate','projection_y_coordinate']),
    # 2 entries for Mercator, since attribs different for 1SP or 2SP
    ("M-1SP", "Mercator", "EPSG:3832",
        "mercator",
        ['longitude_of_projection_origin',
         'standard_parallel', # require 1 value in this case
         'scale_factor_at_projection_origin',
         'false_easting', 'false_northing'],
         ['projection_x_coordinate','projection_y_coordinate']),
    # EPSG 3994 is _supposed_ to be a 2SP according to spatialreference.org,
    # but GDAL disagrees - and epsg-registry.org seems to support this
    #("M-2SP", "Mercator", "EPSG:3994",
    #    "mercator",
    #    ['longitude_of_projection_origin',
    #     'standard_parallel', # require 2 values
    #     'false_easting', 'false_northing'],
    #     ['projection_x_coordinate','projection_y_coordinate'])
    #("Ortho", "Orthographic", "EPSG:?",
    #    "orthographic",
    #    ['longitude_of_projection_origin',
    #     'latitude_of_projection_origin',
    #     'false_easting', 'false_northing'],
    #     ['projection_x_coordinate', 'projection_y_coordinate']),
    # Seems GDAL may have problems with Polar stereographic, as it 
    #  considers these "local coordinate systems"
    #("PS", "Polar stereographic", "EPSG:3031",
    #    "polar_stereographic",
    #    ['straight_vertical_longitude_from_pole',
    #    'latitude_of_projection_origin',
    #     'scale_factor_at_projection_origin', # OR 'standard_parallel', 
    #     'false_easting', 'false_northing'],
    #     ['projection_x_coordinate', 'projection_y_coordinate']),
    ("TM", "Transverse Mercator", "EPSG:2000",
        "transverse_mercator",
        [
         'scale_factor_at_central_meridian',
        'longitude_of_central_meridian',
        'latitude_of_projection_origin',
         'false_easting', 'false_northing'],
         ['projection_x_coordinate','projection_y_coordinate'])
    ]

# Note: rotated_pole projection seems not currently supported by GDAL, thus
#  not in the list above.
#  See http://www.osgeo.org/pipermail/gdal-dev/2007-June/013282.html
#  An effort to _import_ from RP in a NetCDF CF-1 compliant file also seems
#  to have failed: http://osgeo-org.1803224.n2.nabble.com/Re-rotated-pole-ob-tran-help-needed-td5149504.html

resFName = "translate_results.txt"
resFile = open(resFName, "w")

if not os.path.exists(outPath):
    os.makedirs(outPath)

heading = "Testing GDAL translation results to NetCDF\n"
resFile.write(heading)
resFile.write(len(heading)*"="+"\n")

now = datetime.datetime.now()
resFile.write("*Date/time:* %s\n\n" % (now.strftime("%Y-%m-%d %H:%M")))

missingAttr = {}
missingCoordVarStdName = {}

for proj in projTuples:
    """Note: current testing strategy is a pretty straightforward search."""

    # Our little results data structures
    transWorked = True
    missingAttr[proj[0]] = []
    missingCoordVarStdName[proj[0]] = []

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
    #TODO: check grid mapping name
    for attrib in proj[4]:
        # The ':' prefix and ' ' suffix is to help check for exact name,
        # eg to catch the standard_parallel_1 and 2 issue.
        if (":"+attrib+" ") not in dumpStr:
            transWorked = False
            missingAttr[proj[0]].append(attrib)
            print "**Error for proj '%s': CF-1 attrib '%s' not found.**" % \
                (proj[0], attrib)
    for coordVarStdName in proj[5]:
        if coordVarStdName not in dumpStr:
            transWorked = False
            missingCoordVarStdName[proj[0]].append(coordVarStdName)
    resFile.write("%s (%s): " % (proj[0], proj[1]))
    if transWorked:
        resFile.write("OK\n")
    else:
        resFile.write("BAD\n")
        for attrib in missingAttr[proj[0]]:
            resFile.write("\tMissing attrib '%s'\n" % (attrib))
        for cVarStdName in missingCoordVarStdName[proj[0]]:
            resFile.write("\tMissing coord var with std name '%s'\n" \
                % (cVarStdName))

resFile.close()
print "\n" + "*" * 80
print "Saved results to file %s" % resFName
