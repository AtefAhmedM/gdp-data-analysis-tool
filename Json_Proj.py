import json
import matplotlib.pyplot as plt

def Json_Read_Function():
    try:
        with open("JsonData.json", "r") as file:
            jsonData = json.load(file)
        return jsonData
    except FileNotFoundError:
        print("Error: The JSON file 'JsonData.json' was not found.")
        return []
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON data from the file.")
        return []

json_data_results = Json_Read_Function()

# User input and function variables
criteria = ""
year = 0
filter = input("Do you want to filter the GDP data by name and years? Enter 'y' or 'n': ").strip().lower()
while filter not in ['y', 'n']:
    print("Invalid input. Please enter 'y' or 'n'.")
    filter = input("Do you want to filter the GDP data by name and years? Enter 'y' or 'n': ").strip().lower()

if filter == "y":
    criteria = input("Enter filtering criteria by country name or code: ").strip()
    year_input = input("Enter year for GDP by country: ").strip()
    try:
        year = int(year_input)
    except ValueError:
        print("Error: Year should be a valid integer.")
        year = 0

noncountry_codes = ["WLD","HIC","ECA|","OED","PST","IBT","LMY","MIC","IBD","EAS","UMC","LTE","NAC","ECS","EAP","TEA","EUU","EAR","EMU","LMC","LCN","TLA","LAC","TEC","MEA","SAS","TSA","ECA","ARB","IDA","SSF","SSA","TSS","CEB","FCS","MNA","TMN","IDX","PRE","LDC","AFE","AFW"]
noncountry_items = []

def json_write_funtion():
    for item in json_data_results:
        for i in noncountry_codes:
            if item["country_code"] == i:
                noncountry_items.append(item)
                json_data_results.remove(item)
    noncountry_data = json.dumps(noncountry_items, indent=4)
    with open("NonCountryData.json", "w") as file:
        file.write(noncountry_data)
    json_data_results_altered = json.dumps(json_data_results, indent=4)
    with open("JsonData.json","w") as outfile:
        outfile.write(json_data_results_altered)
        

def filter_data(json_data, criteria_value, year_value):
    filtered_data_name = [item for item in json_data if item['country_name'] == criteria_value or item["country_code"] == criteria_value]
    filtered_data_year = [item for item in json_data if item['year'] == year_value]
    filtered_2021 = [item for item in json_data if item['year'] == 2021]
    filtered_2022 = [item for item in json_data if item['year'] == 2022]
    return filtered_data_name, filtered_data_year, filtered_2022, filtered_2021

def sort_data(json_data, key):
    sorted_data = sorted(json_data, key=lambda x: x[key], reverse=True)
    return sorted_data

def GDP_calculations(GDP2, GDP1):
    K = "growth"
    for item in GDP1:
        for item2 in GDP2:
            if item["country_name"] == item2["country_name"]:
                try:
                    growth = (int(item2["value"]) - int(item["value"])) / int(item["value"])
                    growth = "%.3f" % growth
                    item2[K] = float(growth)
                except ZeroDivisionError:
                    print("Warning: Division by zero encountered for", item["country_name"])
    

# Filter data based on user criteria
# json_write_funtion()
filtered_data = filter_data(json_data_results, criteria, year)

# Sort data by a specific field
sorted_2022 = filtered_data[2]
Sort_Key = "value"
sorted_data = sort_data(sorted_2022, Sort_Key)


# Calculate the growth field
gdp_2022 = filtered_data[2]
gdp_2021 = filtered_data[3]
GDP_calculations(gdp_2022, gdp_2021)

# Display the results/visualizations
if filter == "y":
    print("Filtered Data:", filtered_data)
    print("Sorted Data:", sorted_data)

Sorted_gdp_2022 = sort_data(gdp_2022, Sort_Key)


##FIRST BAR PLOT##
xAxis = [key["country_name"] for key  in Sorted_gdp_2022[:15]]
yAxis = [value["value"] for value in Sorted_gdp_2022[:15]]

fig, ax = plt.subplots(figsize =(16, 9))
ax.barh(xAxis, yAxis)
 
# Remove axes splines
for s in ['top', 'bottom', 'left', 'right']:
    ax.spines[s].set_visible(False)
 
# Remove x, y Ticks
ax.xaxis.set_ticks_position('none')
ax.yaxis.set_ticks_position('none')
 
# Add padding between axes and labels
ax.xaxis.set_tick_params(pad = 5)
ax.yaxis.set_tick_params(pad = 10)
 
# Add x, y gridlines
ax.grid(axis='x', linestyle='-.', linewidth=0.5, alpha=0.2)
ax.grid(axis='y', linestyle='-.', linewidth=0.5, alpha=0.2)
# Show top values
ax.invert_yaxis()
# Add Plot Title
ax.set_title('Top 15 GDP for 2022',loc ='left', )
 
# Show Plot
plt.show()

##SECOND BAR PLOT##
xAxis = [key["country_name"] for key  in Sorted_gdp_2022[:15]]
yAxis = [value["growth"] for value in Sorted_gdp_2022[:15]]

fig, ax = plt.subplots(figsize =(16, 9))
ax.barh(xAxis, yAxis)
 
# Remove axes splines
for s in ['top', 'bottom', 'left', 'right']:
    ax.spines[s].set_visible(False)
 
# Remove x, y Ticks
ax.xaxis.set_ticks_position('none')
ax.yaxis.set_ticks_position('none')
 
# Add padding between axes and labels
ax.xaxis.set_tick_params(pad = 5)
ax.yaxis.set_tick_params(pad = 10)
 
# Add x, y gridlines
ax.grid(axis='x', linestyle='-.', linewidth=0.5, alpha=0.2)
ax.grid(axis='y', linestyle='-.', linewidth=0.5, alpha=0.2)
# Show top values
ax.invert_yaxis()
# Add Plot Title
ax.set_title('GDP Growth 2021-2022',loc ='left', )
 
# Show Plot
plt.show()