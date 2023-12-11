# POOR6
Repository of the group project of the "Database 2" course, Computer Engineering MD, Università degli Studi di Padova, a.a. 2023/24, by the POOR6 group: Merlo Simone, Gobbo Riccardo, Spinosa Diego.

### Introduction
This project aims at the organization and study of open data over a certain domain using rules and techniques as defined in the realm of the Semantic Web. In particular, this means modelling and processing our domain of interest and the available data into a machine-readable form, that is by construction easy to query and to make analyses from.

More specifically, we have chosen to work on three tightly linked **datasets**:
 - "*Electric Vehicle Population Data*" provided by the Dept. of Licensing of the State of Washington, US. This dataset shows the Battery Electric Vehicles (BEVs) and Plug-in Hybrid Electric Vehicles (PHEVs) that are currently registered through Washington State Department of Licensing (DOL).  [source](https://data.wa.gov/Transportation/Electric-Vehicle-Population-Data/f6w7-q2d2)
 - "*Alternative Fuel Stations*", as part of the Alternative Fuels Data Center of the U.S. Department of Energy. This dataset was used to obtain location and properties of all the registered EV charging stations in the state of Washington. [source](https://afdc.energy.gov/data_download/alt_fuel_stations_format)
 - "*SOI Tax Stats - Individual Income Tax Statistics*" provided by the IRS (Internal Revenue Service) of the US. Data are based on individual income tax returns filed with the IRS and are used to determine how the average income varies among Washington's zipcodes. [source](https://www.irs.gov/statistics/soi-tax-stats-individual-income-tax-statistics-2020-zip-code-data-soi)

The project aims at linking these 3 data sources to discover whether there are some interesting correlations between EV diffusion, EV charging station density and average income in the scope of the territory of state of Washington. We are focusing on this region since we have found a particularly good data quality and availability, and also because its scenario can resemble the one found in most other US states or even other first world countries worldwide.


### Repository Structure
The following tree represents the repository structure:
```
.
├── src_data/
│   ├── 20zpallnoagi-info.txt
│   ├── 20zpallnoagi.csv
│   ├── 20zpdoc.docx
│   ├── Electric_Vehicle_Population_Data.csv
│   ├── stations_pub+priv_open.csv
│   └── wa_zips_cities_counties.csv
├── clean_data/
├── output/
├── ElectricCarsOntology.drawio
├── ElectricCarsOntology.rdf
├── POOR6.ipynb
└── queries.txt

```
-src_data: contains all the source files from which we got the data.
-clean_data: will contain a cleaned version of the source data (if not present the folder will be created running the python notebook).
-output: will contain the output files of the python notebook (in turtle format), to be ingested in the graph database (if not present the folder will be created running the python notebook).
-ElectricCarsOntology.drawio: the schema of the ontology.
-ElectricCarsOntology.rdf: the ontology to be imported in the graph database.
-POOR6.ipynb: the python notebook that performs the cleaning and processing if the data.
-queries.txt: the file containing our proposed queries.

### Technical Information
Our workflow and elaboration pipeline is as follows:
- Data was acquired: downloaded as CSV files from the abovementioned sources.
 Those files are also contained in the *src_data* folder of this repository.
- The data model was created according to both the data's features and our work's scope.
	The resulting model is described by the *ElectricCarsOntology.drawio* (drawing) and *ElectricCarsOntology.rdf* (schema) files.
- Data cleaning through the python notebook (*POOR6.ipynb* file in this repository)
- Data ingestion in GraphDB
- Querying GraphDB for insights.

The queries that we have selected for analysis can be found in the *queries.txt* file of this repository.

