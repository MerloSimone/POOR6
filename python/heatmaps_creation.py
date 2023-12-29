import pandas as pd
import plotly.express as px
from os import listdir
from os.path import isfile

PATH = "python/data/"

files = listdir("python/data")
print(files)

for file in files:
    f = open(PATH + file)
    line = f.readline().strip().split(',')
    
    df = pd.read_csv(PATH + file)
    fig = px.density_mapbox(df, lat = line[1], lon = line[0], z = line[2],
                            radius = 8,
                            center = dict(lat = 47.5, lon = -120.5),
                            zoom = 7,
                            mapbox_style = 'carto-positron')
    fig.show() 