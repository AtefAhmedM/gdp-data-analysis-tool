from django.shortcuts import render
import json
import matplotlib
matplotlib.use("Agg") # Use Agg backend for Matplotlib to generate plots
import matplotlib.pyplot as plt
from .models import YourModel  # Import the model for database interaction
from django.http import HttpResponse
from datetime import datetime
from .models import YourModel

# Function to read JSON data from a file
def Json_Read_Function():
    try:
        with open('JsonData.json', 'r') as file:
            jsonData = json.load(file)
        return jsonData
    except FileNotFoundError:
        print("Error: The JSON file 'JsonData.json' was not found.")
        return []
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON data from the file.")
        return []

# Function to filter data based on criteria (e.g., country and year)
def filter_data(json_data, criteria_value, year_value):
    filtered_data_name = [item for item in json_data if item['country_name'] == criteria_value or item["country_code"] == criteria_value]
    filtered_data_year = [item for item in json_data if item['year'] == year_value]
    filtered_2021 = [item for item in json_data if item['year'] == 2021]
    filtered_2022 = [item for item in json_data if item['year'] == 2022]
    return filtered_data_name, filtered_data_year, filtered_2022, filtered_2021

# Replace this with your actual data sorting logic
def sort_data(json_data, key):
    sorted_data = sorted(json_data, key=lambda x: x[key], reverse=True)
    return sorted_data

# Function to perform GDP calculations
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

# View function for rendering the web page
def index(request):
    # Get distinct country names and years from the database
    known_countries = YourModel.objects.values_list('country_name', flat=True).distinct()
    known_years = YourModel.objects.values_list('year', flat=True).distinct().order_by('year')

    if request.method == 'POST':
        selected_country = request.POST.get('country')
        selected_year = request.POST.get('year')

        if selected_country and selected_year:
            # Query the database to retrieve the GDP value for the selected country and year
            try:
                gdp_value = YourModel.objects.get(country_name=selected_country, year=selected_year).gdp_value
            except YourModel.DoesNotExist:
                # Handle the case where no data is found for the selected country and year
                gdp_value = None
        else:
            gdp_value = None
    else:
        selected_country = None
        selected_year = None
        gdp_value = None

    context = {
        'known_countries': known_countries,
        'known_years': known_years,
        'selected_country': selected_country,
        'selected_year': selected_year,
        'gdp_value': gdp_value,  # Pass the GDP value to the template
    }

    return render(request, 'gdp_templates.html', context)



