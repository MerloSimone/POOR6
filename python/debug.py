import os
import shutil as sh
from pathlib import Path
from unidecode import unidecode
import pandas as pd
from urllib.parse import quote
from rdflib import Graph, Literal, RDF, RDFS, URIRef, Namespace
from rdflib.namespace import XSD
import re

DATA_FOLDER = "clean_data"
SOURCE_FOLDER = "src_data/"
OUTPUT_FOLDER = "output"
STATIONS_FILE = "stations_pub+priv_open.csv"
LOCATIONS = SOURCE_FOLDER + "wa_zips_cities_counties.csv"
CARS_FILE = SOURCE_FOLDER + "Electric_Vehicle_Population_Data.csv"
WAGE_FILE = SOURCE_FOLDER + "20zpallnoagi.csv"

def urify_string(s: str):
    s=unidecode(s)
    pattern = "[^0-9a-zA-Z\s]+"
    s = re.sub(pattern, " ", s).title().replace(" ", "")
    return s

# Get the absolute path
path = str(Path(os.path.abspath(os.getcwd())).parent.absolute())
try:
    # Remove the existing folder
    sh.rmtree(DATA_FOLDER)
    sh.rmtree(OUTPUT_FOLDER)
except FileNotFoundError:
    print("--- No folder to remove ---")

# Create new folder for clean data
os.mkdir(DATA_FOLDER)
print(f"Folder '{DATA_FOLDER}' created.")
os.mkdir(OUTPUT_FOLDER)
print(f"Folder '{OUTPUT_FOLDER}' created.")

DATA_FOLDER += "/"
OUTPUT_FOLDER += "/"

file = open(SOURCE_FOLDER + STATIONS_FILE, "r", encoding="utf-8")                  # Input file
wa_fuel_stations = wa_e_stations = open(DATA_FOLDER + STATIONS_FILE, "w", encoding="utf-8")     # Output file

# Write CSV headers
wa_fuel_stations.write(file.readline())

row = file.readline()               # Read first line
while (row2 := file.readline()):
    row2_error = False              

    # If the row is interrupted, recover it (there can be multiple interruption)
    while("ELEC" not in row2):
        row2_error = True
        index = row2.find('",')                                     # Find the end of last interrupted string, if exists
        row = row.strip() + row2[index if index != -1 else 0 : ]    # Concatenate the row begin with the second part
        row2 = file.readline()

    if ",WA," in row: wa_e_stations.write(row)
    row = row2                                                      # Check on next cycle

file.close()
wa_e_stations.close()

places = pd.read_csv(LOCATIONS, sep=",")

ECO = Namespace("http://www.dei.unipd.it/~poor6/db2/ontologies/2023/electricCars#")

graph = Graph()
graph.bind("elec", ECO)


for index, row in places.iterrows():
    #Creating the URIs using the urify_string function
    ZipCode = URIRef(ECO[str(row['Zipcode'])])
    City = URIRef(ECO[urify_string(str(row['City']))])
    County = URIRef(ECO[urify_string(str(row['County']))])

    graph.add((ZipCode, RDF.type, ECO.ZipCode)) #Adding ZipCodes
    graph.add((City, RDF.type, ECO.City)) #Adding City
    graph.add((County, RDF.type, ECO.County)) #Adding County
    
    #Adding labels to keep the original strings
    graph.add((City, RDFS.label, Literal(str(row['City']), datatype=XSD.string)))
    graph.add((County, RDFS.label, Literal(str(row['County']), datatype=XSD.string)))

    #Adding relations
    graph.add((ZipCode, ECO["ofCity"], City))
    graph.add((City, ECO["belongsTo"], County))

# print all the data in the Turtle format
print("--- saving serialization ---")
with open(OUTPUT_FOLDER + 'locations.ttl', 'w') as file:
    file.write(graph.serialize(format='turtle'))

stations = pd.read_csv(DATA_FOLDER + STATIONS_FILE, sep=",")

stations.info()

graph = Graph()
graph.bind("elec", ECO)

dati = '"longitude","latitude","tot_pob"\n'

for index, row in stations.iterrows():
    Station = URIRef(ECO[str(index)])     # Create node (prefix + incremental id)

    #Adding the statio type (private or public)
    if(re.search(".*[Pp]rivate.*",row['Access Code'])):
        graph.add((Station, RDF.type, ECO.PrivateStation))
    elif (re.search(".*[Pp]ublic.*",row['Access Code'])):
        graph.add((Station, RDF.type, ECO.PublicStation))
    
    graph.add((Station, RDF.type, ECO.Station))             

    # Adding station name and address if present
    graph.add((Station, ECO['hasName'], Literal(row['Station Name'], datatype=XSD.string)))
    if row['Street Address']:
        graph.add((Station, ECO['hasAddress'], Literal(row['Street Address'], datatype=XSD.string)))
    
    latitude = None
    longitude = None
    latitude = row['Latitude']
    longitude = row['Longitude']

    # "longitude","latitude","tot_pob"

    if latitude is not None and longitude is not None:
        dati += f"{longitude},{latitude},1\n"

    #     graph.add((Station, ECO['hasLat'], Literal(row['Latitude'], datatype=XSD.string)))
    #     graph.add((Station, ECO['hasLong'], Literal(row['Longitude'], datatype=XSD.string)))

    # #Avoiding strange cases
    # if " " in row['ZIP']: 
    #     print(f"Error in ZIP '{row['ZIP']}', skipped")
    #     continue

    # #Linking a station to its ZipCode
    # ZipCode = URIRef(ECO[row['ZIP']])
    # graph.add((Station, ECO['locatedIn'], ZipCode))


file = open("coordinate.csv", "w")
file.writelines(dati)
file.close()

import pandas as pd
import plotly.express as px

# Data with latitude/longitude and values
df = pd.read_csv("coordinate.csv")

fig = px.density_mapbox(df, lat = 'latitude', lon = 'longitude', z = 'tot_pob',
                        radius = 8,
                        center = dict(lat = 42.83, lon = -8.35),
                        zoom = 6,
                        mapbox_style = 'carto-positron')
fig.show() 
