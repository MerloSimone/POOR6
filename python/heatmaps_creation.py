import pandas as pd
import plotly.express as px
from os import listdir
from os.path import isfile

PATH = "./data/"

files = listdir("./data")
print(files)

for file in files:
    f = open(PATH + file)
    line = f.readline().strip().split(',')
    
    df = pd.read_csv(PATH + file)
    fig = px.density_mapbox(df, lat = line[0], lon = line[1], z = line[2],
                            radius = 8,
                            center = dict(lat = 47.5, lon = -120.5),
                            zoom = 7,
                            mapbox_style = 'carto-positron',
                            title=file)

    fig.show() 