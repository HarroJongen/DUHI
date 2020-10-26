# DUHI
Internship KNMI

All code written by Harro Jongen during the internship at KNMI.

Required python packages:
-calendar
-datetime
-geopandas
-geopy.geocoders
-glob
-inspect
-math
-matplotlib.pyplot
-mpl_toolkits.basemap
-netCDF4
-numpy
-os
-pandas
-pickle
-rasterio
-rasterio.plot
-re
-seaborn
-sklearn.linear_model
-urllib.request
-winsound
-xlrd

main_metadata builds metadata based on a list of coordinates, needs to be ran before main_main.
main_main excecutes the main script.
main_validation_soilmoisture validates the ESA-CCI Soil Moisture for the Netherlands.
main_soilmoisturemap creates a global map of the soil moisture range between twi dates.

Before running the code create the folder stucture with the appropriate data:
DUHI
	-Data
		-Cities
			-Per city one folder with city name containing all urban files
			-Rural
				-File for rural station of the city
		-Maps
			-KEA
				-Request klimaateffectatlas data at https://www.klimaateffectatlas.nl/nl/helpdesk, extract map layers: seepage as tif and neighbourhoods as shp and place in this folder
			-Population
				-Download populations statistics at https://www.cbs.nl/nl-nl/dossier/nederland-regionaal/geografische-data/gegevens-per-postcode and place shapefile in this folder
			-Soil
				-Download soil map at  https://geodata.nationaalgeoregister.nl/bodemkaart50000/wfs?request=getCapabilities, link the soil codes to the shaped in a geosoftware package and place in this folder
			-SVF
				-Download appropriate files for this map, when instructed by the main_metdata script
			-Seperate tiff file of LCZ map by Demuzere et al. 2019 (preferably clipped to the Netherlands)
		-Metadata
			-CSV with all heatwave periods
			-CSV with all locations in the research, already create and fill columns: City, Locations, Lat_urban, Lon_urban, Rural, Lat_rural, Lon_rural, prof
		-Preprocessed
			-This folder will be filled and emptied automatically
		-SoilMoisture
			-Cabauw
				-Download Cabauw soilmoisture at https://ruisdael-observatory.nl/cesar-database/pages/datasetsKDC.html and place in this folder
			-ESACCI-COMBINED
				-Follow download instructions at https://www.esa-soilmoisture-cci.org/node/145 for the combined product and place here
	-Figures
	-Functions (already exists in repository)
	


