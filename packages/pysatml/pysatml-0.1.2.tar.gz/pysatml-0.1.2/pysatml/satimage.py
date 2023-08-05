# for local I/O
import sys, os

# for handling geometry and AOIs
from shapely.geometry import Polygon, Point
from pyproj import Proj, transform
from shapely.wkt import dumps as wkt_dumps
import geojson
import math

# wrapper for GoogleMaps geocoding service
import geocoder

# for reading GeoTiffs
from osgeo import gdal, osr
from gdal import gdalconst
from gdalconst import * 
import osr

import rasterio
from rasterio.features import shapes
import geopandas as gp

# for processing image data
import skimage
from skimage import exposure, io

# the data will be exported as numpy arrays
import numpy as np
import struct

# constants
WHOLE_WORLD_BOUNDS = (-180, -85, 180, 85)

# Types used by struct.unpack
typeByGDT = {
    gdal.GDT_Byte: 'B',
    gdal.GDT_UInt16: 'H', 
    gdal.GDT_Float32: 'f'
}
modeByType = {
    gdal.GDT_Byte: 'L',
    gdal.GDT_UInt16: 'I;16', 
    gdal.GDT_Float32: 'I;16'
}

class SatImage(object):

	def __init__(self, rasterFile, force_wgs84=False):
		"""
		Initialize with either one or multiple raster files where the data of interest resides. Some times large raster files are broken down into several tiles to facilitate processing and distribution.
		force_wgs84: project raster to commonly-used WGS84 format.
					 Note: this takes a bit of time, for repeated use it's better to reproject rasters separately (done just once).
		"""
		self._rasterPaths = rasterFile
		self._raster = {}
		if type(rasterFile) == str:
			rasterFile = [rasterFile]
		for rf in rasterFile:
			data = gdal.Open(rf, GA_ReadOnly)	
			if data is None:
				continue
			if force_wgs84:
				data = project_to_wgs84(data) 
				# if gdal version >= 2.0, Warp is available
				# data = gdal.Warp("tmp.tif",data,dstSRS='EPSG:4326')
			print get_geotiff_bounds(data)
			self._raster[get_geotiff_bounds(data)] = data


	def polygonize_raster(self):
		pass

	def get_value_at_location(self, loc):
		return self.get_image_at_location(loc)


	def get_image_at_location(self, loc, w=None, dumpPath=None, pickle=False):
		"""
		Crop raster at location loc (lat,lon) with size w x w (in meters). Return a data matrix or save to file. 
		If w is not set, return just the pixel values at <loc>. 
		"""
		if type(loc) == str:
			# if location is given by a string, interpret that as an address
			# or city name and try to turn it to lat/lon via Google geocoding
			loc = tuple(geocoder.google(loc).latlng)
		if len(loc) == 0:
			return None

		img = [img for bounds, img in self._raster.iteritems() \
			if (loc[0]>=bounds[0] and loc[0]<bounds[2]) and \
				(loc[1]>=bounds[1] and loc[1]<bounds[3])]
		if len(img) == 0:
			return None

		w = 0 if w is None else w
		wLat, wLon = km_to_deg_at_location(loc, (w,w))
		# note that all the GDAL-based code assumes locations are given as (lon,lat), so we must reverse loc
		img = extract_centered_image_lonlat(img[0], loc[::-1], (wLon, wLat))

		if dumpPath is not None:
			dumpPath += "%2.6f_%2.6f_%dkm"%(loc[0], loc[1], w)
			save_image_data(img, dumpPath, pickle=False)
		return img


	def get_image_at_locations(self,locs,w=None,dumpPath=None,pickle=False):
		""" Obtain sample images at different locations.
		"""
		if type(locs) == tuple:
			return self.get_image_at_location(locs, w=w, \
				dumpPath=dumpPath, pickle=pickle)
		else:
			return {loc:self.get_image_at_location(loc, w=w, \
				dumpPath=dumpPath, pickle=pickle) for loc in locs}


	def sample_images_around_location(self, loc, w=None, W=None, nSamples=1,\
		dumpPath=None, pickle=False):
		""" 
		Sample nSamples images of size w x w within a bounding box of W x W around location loc. Returns the list of sampled locations.
		"""
		locs = generate_locations_around_latlon(loc, W=W, nSamples=nSamples)
		return self.get_image_at_locations(locs, w=w, \
			dumpPath=dumpPath, pickle=pickle)

	
	def sample_images_within_shape(self, shape, w=None, nSamples=1, \
		dumpPath=None, pickle=False):
		""" 
		Generate nSamples candidate (lat,lon) locations to sample images at. 
		"""
		locs = generate_locations_within_polygon(polygon, nSamples=1)
		return self.get_image_at_locations(locs, w=w, \
			dumpPath=dumpPath, pickle=pickle)


def raster2polygon(raster_file, band=1):
	mask = None
	with rasterio.drivers():
	    with rasterio.open(raster_file) as src:
	        image = src.read(band) # first band
	        results = (
	        	{'properties': {'raster_val': v}, 'geometry': s}
	        		for i, (s, v) in enumerate(shapes(image, mask=mask, transform=src.affine)))
	geoms = list(results)
	gpd_polygonized_raster = gp.GeoDataFrame.from_features(geoms)
	return gpd_polygonized_raster


def generate_locations_around_latlon(latlon, W=None, nSamples=1):
	boundingBox = bounding_box_at_location(latlon, (W,W))
	locs = generate_locations_within_bounding_box(boundingBox, nSamples)
	return locs


def generate_locations_within_bounding_box(bbox, nSamples=1, seed=None):
	np.random.seed(seed)
	minX, minY, maxX, maxY = bbox
	x = np.random.uniform(minX, maxX, nSamples)
	y = np.random.uniform(minY, maxY, nSamples)
	return zip(x,y)


def generate_locations_within_polygon(polygon, nSamples=1, seed=None, \
	strict=True):
	"""
	There doesn't seem to be an efficient way to do this sampling for an arbitrary polygon. We use a rejection sampling method instead.
	"""
	bbox = polygon.bounds
	shape = polygon if strict else polygon.convex_hull
	points = []
	while len(points) < nSamples:
		ps = generate_locations_within_bounding_box(bbox, \
			nSamples=nSamples, seed=seed)
		ps = [p for p in ps if Point(p).within(shape)]
		points += ps
	return points[:nSamples]


def project_to_wgs84(src_ds):
	# Define target SRS
	dst_srs = osr.SpatialReference()
	dst_srs.ImportFromEPSG(4326)
	dst_wkt = """
	GEOGCS["WGS 84",
	    DATUM["WGS_1984",
	        SPHEROID["WGS 84",6378137,298.257223563,
	            AUTHORITY["EPSG","7030"]],
	        AUTHORITY["EPSG","6326"]],
	    PRIMEM["Greenwich",0,
	        AUTHORITY["EPSG","8901"]],
	    UNIT["degree",0.01745329251994328,
	        AUTHORITY["EPSG","9122"]],
	    AUTHORITY["EPSG","4326"]]"""

	error_threshold = 0.125  # error threshold --> use same value as in gdalwarp
	resampling = gdal.GRA_NearestNeighbour

	# Call AutoCreateWarpedVRT() to fetch default values for target raster dimensions and geotransform
	new_ds = gdal.AutoCreateWarpedVRT( src_ds,
	                                   None, # src_wkt : left to default value --> will use the one from source
	                                   dst_wkt,
	                                   resampling,
	                                   error_threshold )
	gdal.ReprojectImage(src_ds, new_ds, None, dst_wkt)

	return new_ds


def get_geotiff_bounds(raster):

	# get the existing coordinate system
	old_cs= osr.SpatialReference()
	old_cs.ImportFromWkt(raster.GetProjectionRef())

	# create the new coordinate system
	wgs84_wkt = """
	GEOGCS["WGS 84",
	    DATUM["WGS_1984",
	        SPHEROID["WGS 84",6378137,298.257223563,
	            AUTHORITY["EPSG","7030"]],
	        AUTHORITY["EPSG","6326"]],
	    PRIMEM["Greenwich",0,
	        AUTHORITY["EPSG","8901"]],
	    UNIT["degree",0.01745329251994328,
	        AUTHORITY["EPSG","9122"]],
	    AUTHORITY["EPSG","4326"]]"""
	new_cs = osr.SpatialReference()
	new_cs.ImportFromWkt(wgs84_wkt)

	# create a transform object to convert between coordinate systems
	transform = osr.CoordinateTransformation(old_cs,new_cs) 

	#get the point to transform, pixel (0,0) in this case
	width = raster.RasterXSize
	height = raster.RasterYSize
	gt = raster.GetGeoTransform()
	minx = gt[0]
	miny = gt[3] + width*gt[4] + height*gt[5] 
	maxx = gt[0] + width*gt[1] + height*gt[2]
	maxy = gt[3] 

	#get the coordinates in lat long
	latlongMin = transform.TransformPoint(minx,miny) 
	latlongMax = transform.TransformPoint(maxx,maxy) 

	return latlongMin[1], latlongMin[0], latlongMax[1], latlongMax[0]


def read_prj(prj_file):
	'''
	Read projection file into string.
	'''
	prj_text = open(prj_file, 'r').read()
	srs = osr.SpatialReference()
	if srs.ImportFromWkt(prj_text):
	    raise ValueError("Error importing PRJ information from: %s" % prj_file)
	prj = srs.ExportToProj4()
	if prj == "":
	    return '+proj=merc +lon_0=0 +lat_ts=0 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs '
	else:
	    return prj


def xy2lonlat(xy, prj=""):
	'''
	Convert northing/easting coordinates to commonly-used lat/lon.
	'''
	x, y = xy
	inProj = Proj(prj) 
	outProj = Proj(init='epsg:4326')
	lon, lat = transform(inProj,outProj,x,y) 
	return lon, lat
    

def lonlat2xy(lonlat, prj=""):
	'''
	Convert commonly-used lat/lon to northing/easting coordinates.
	'''
	lon, lat = lonlat
	inProj = Proj(init='epsg:4326')
	outProj = Proj(prj) 
	x, y = transform(inProj,outProj,lon,lat) 
	return x, y
    

def polygon_xy2lonlat(p, prj=""):
	'''
	Convert polygon coordinates from meter to lon/lat.
	'''
	inProj = Proj(prj) 
	outProj = Proj(init='epsg:4326')
	x, y = p.exterior.coords.xy
	locs_meter = zip(x, y)
	locs_lonlat= [transform(inProj,outProj,x1,y1) for x1,y1 in locs_meter]
	return Polygon(locs_lonlat)


def polygon_lonlat2xy(p, prj=""):
	'''
	Convert polygon coordinates from lon/lat to meter.
	'''
	inProj = Proj(init='epsg:4326')
	outProj = Proj(prj) 
	lon, lat = p.exterior.coords.xy
	locs_lonlat = zip(lon, lat)
	locs_meter = [transform(inProj,outProj,x,y) for x,y in locs_lonlat]
	return Polygon(locs_meter)


def save_image_data(img, dumpPath, pickle=False):
    basedir = os.path.dirname(dumpPath)
    # img = exposure.rescale_intensity(img, out_range='float')
    # img = skimage.img_as_uint(img)
    img = img.astype(np.uint8)
    if not os.path.exists(basedir):
        os.makedirs(basedir)
    if pickle:
        with gzip.open(dumpPath+".pickle.gz", 'w'):
            pickle.dump(img, dumpPath)
    elif img.shape[0] in [3,4]:
        io.imsave(dumpPath+".jpg", img.reshape(img.shape[::-1]))
    elif img.shape[0] == 1:
        io.imsave(dumpPath+".png", np.squeeze(img))
    else:
        io.imsave(dumpPath+".tif", img, compress=6)


def km_to_deg_at_location(loc, sizeKm):
	latMin, lonMin, latMax, lonMax = bounding_box_at_location(loc, sizeKm)
	return latMax - latMin, lonMax - lonMin


# Bounding box surrounding the point at given coordinates,
# assuming local approximation of Earth surface as a sphere
# of radius given by WGS84
def bounding_box_at_location(latlon, sizeKm):
	widthKm, heightKm = sizeKm
	latitudeInDegrees, longitudeInDegrees = latlon
	# degrees to radians
	def deg2rad(degrees):
	    return math.pi*degrees/180.0

	# radians to degrees
	def rad2deg(radians):
	    return 180.0*radians/math.pi

	# Semi-axes of WGS-84 geoidal reference
	WGS84_a = 6378137.0  # Major semiaxis [m]
	WGS84_b = 6356752.3  # Minor semiaxis [m]

	# Earth radius at a given latitude, according to the WGS-84 ellipsoid [m]
	def WGS84EarthRadius(lat):
	    # http://en.wikipedia.org/wiki/Earth_radius
	    An = WGS84_a*WGS84_a * math.cos(lat)
	    Bn = WGS84_b*WGS84_b * math.sin(lat)
	    Ad = WGS84_a * math.cos(lat)
	    Bd = WGS84_b * math.sin(lat)
	    return math.sqrt( (An*An + Bn*Bn)/(Ad*Ad + Bd*Bd) )

	lat = deg2rad(latitudeInDegrees)
	lon = deg2rad(longitudeInDegrees)
	widthMeters = 1000*widthKm/2.0
	heightMeters = 1000*heightKm/2.0

	# Radius of Earth at given latitude
	radius = WGS84EarthRadius(lat)
	# Radius of the parallel at given latitude
	pradius = radius*math.cos(lat)

	latMin = lat - heightMeters/radius
	latMax = lat + heightMeters/radius
	lonMin = lon - widthMeters/pradius
	lonMax = lon + widthMeters/pradius

	return (rad2deg(latMin), rad2deg(lonMin), rad2deg(latMax), rad2deg(lonMax))


def extract_centered_image_lonlat(raster, lonlat, geoSize):
	gt = raster.GetGeoTransform()
	pixCenter = geoLoc_to_pixLoc(lonlat, gt)
	geoWidth, geoHeight = geoSize
	if geoWidth==0 or geoHeight==0 or geoWidth is None or geoHeight is None:
		return extract_centered_image_pix(raster, pixCenter, (1,1))[:,0,0]
	else:
		pixWidth, pixHeight = geoSize_to_pixSize(geoSize, gt)
		return extract_centered_image_pix(raster, pixCenter, (pixWidth, pixHeight))


def extract_centered_image_pix(raster, pixLoc, pixSize):
	pixWidth, pixHeight = pixSize
	pixUpperLeft = get_image_center_pix(pixLoc, (pixWidth, pixHeight))[:2]
	return extract_image_pix(raster, pixUpperLeft, (pixWidth, pixHeight))


def get_image_center_pix(pixLoc, pixSize):
    # Compute frame
    pixelWidth, pixelHeight = pixSize
    pixelLeft = max([0,pixLoc[0] - pixelWidth / 2])
    pixelTop = max([0,pixLoc[1] - pixelHeight / 2])
    pixelRight = pixelLeft + pixelWidth
    pixelBottom = pixelTop + pixelHeight
    # Return
    return pixelLeft, pixelTop, pixelRight, pixelBottom


def extract_image_pix(raster, pixLoc, pixSize):
	# Set bounds
	pixWidth, pixHeight = pixSize
	iLeft   = int(pixLoc[0])
	iTop    = int(pixLoc[1])
	iWidth  = int(pixWidth)
	iHeight = int(pixHeight)
	rWidth  = raster.RasterXSize
	rHeight = raster.RasterYSize
	iWidth  = iWidth if iLeft + iWidth <= rWidth \
				else rWidth - iLeft
	iHeight = iHeight if iTop + iHeight <= rHeight \
				else rHeight - iTop
	# Extract data
	bands = map(raster.GetRasterBand, xrange(1, raster.RasterCount + 1))
	img = [b.ReadAsArray(iLeft, iTop, iWidth, iHeight).astype(np.float) \
		for b in bands]
	img = np.asarray(img)
	return img


def convert_geoWindow_to_pixelWindow(geoWindow, gt):
	geoLeft, geoTop, geoRight, geoBottom = geoWindow
	pixelLeft, pixelTop = geoLoc_to_pixLoc((geoLeft, geoTop), gt)
	pixelRight, pixelBottom = geoLoc_to_pixLoc((geoRight, geoBottom), gt)
	pixelLeft, pixelRight = sorted((pixelLeft, pixelRight))
	pixelTop, pixelBottom = sorted((pixelTop, pixelBottom))
	return pixelLeft, pixelTop, pixelRight, pixelBottom


def convert_pixelWindow_to_geoWindow(pixWindow, gt):
	pixelLeft, pixelTop, pixelRight, pixelBottom = pixWindow
	geoLeft, geoTop = geoLoc_to_pixLoc((pixelLeft, pixelTop), gt)
	geoRight, geoBottom = geoLoc_to_pixLoc((pixelRight, pixelBottom), gt)
	geoLeft, geoRight = sorted((geoLeft, geoRight))
	geoTop, geoBottom = sorted((geoTop, geoBottom))
	return geoLeft, geoTop, geoRight, geoBottom


def geoLoc_to_pixLoc(geoLoc, gt):
	"""
	Transforms a geographical location geoLoc (lat,lon) to pixel coordinates in a geographic reference given by the geotransform gt.
	"""
	g0, g1, g2, g3, g4, g5 = gt
	xGeo, yGeo = geoLoc
	if g2 == 0:
	    xPixel = (xGeo - g0) / float(g1)
	    yPixel = (yGeo - g3 - xPixel*g4) / float(g5)
	else:
	    xPixel = (yGeo*g2 - xGeo*g5 + g0*g5 - g2*g3) / float(g2*g4 - g1*g5)
	    yPixel = (xGeo - g0 - xPixel*g1) / float(g2)
	return int(round(xPixel)), int(round(yPixel))


def geoSize_to_pixSize(geoSize, gt):
	g0, g1, g2, g3, g4, g5 = gt
	geoWidth, geoHeight = geoSize
	return int(round(abs(float(geoWidth) / g1))), int(round(abs(float(geoHeight) / g5)))

