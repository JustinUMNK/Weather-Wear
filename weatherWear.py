import requests
import re
from requests import get

#Function which asks the user for an input and returns it
def getInput(message):
    return input(message)

#Ensures that airport codes follow the format of having 3 capital letters e.g 'LHR'
def validateAirportCode(airportCode):
    if re.match(r'^[A-Z]{3}$', airportCode):
        return True
    else:
        return False

#Ensures that date follows the format of YYYY-MM-DD
def validateDate(date):
    if re.match(r'^\d{4}-\d{2}-\d{2}$', date):
        return True
    else:
        return False

#Appropriately formats the querystring so that it can be accepted by the API to get current weather
def formatCurrentWeatherQueryString(latitude, longitude):
    querystring = {"q": f"{latitude},{longitude}"}
    return querystring

#Appropriately formats the querystring so that it can be accepted by the API to get future weather
def formatFutureWeatherQueryString(latitude, longitude, date):
    querystring = {"q": f"{latitude},{longitude}", "dt": f"{date}"}
    return querystring

#Makes a request to the API to retrieve the current weather data with latitude and longitude as paramters
def getCurrentLocationWeather(latitude, longitude):
    weatherURL = "https://weatherapi-com.p.rapidapi.com/current.json"

    querystringWeather = formatCurrentWeatherQueryString(latitude, longitude)

    weatherHeaders = {
        "X-RapidAPI-Key": "d938ed0f31msha48d8b8712726ccp18ed84jsn171d6b153ec0",
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }

    weatherResponse = requests.get(weatherURL, headers=weatherHeaders, params=querystringWeather)

    weatherData = weatherResponse.json()

    return weatherData

#Makes a request to the API to retrieve the future weather data with latitude, longitude, and date as parameters
def getFutureLocationWeather(latitude, longitude, date):
    forecastURL = "https://weatherapi-com.p.rapidapi.com/forecast.json"

    querystringForecast = formatFutureWeatherQueryString(latitude, longitude, date)

    forecastHeaders = {
        "X-RapidAPI-Key": "d938ed0f31msha48d8b8712726ccp18ed84jsn171d6b153ec0",
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }

    forecastResponse = requests.get(forecastURL, headers=forecastHeaders, params=querystringForecast)

    forecastData = forecastResponse.json()

    return forecastData

#Backup service to get the latitude and longitude based off the user's IP 
def getCoordinatesBackupService(querystring):
    locationURL = "http://ip-api.com/json/" + querystring

    locationResponse = requests.get(locationURL)

    #Return none if an error occurs
    if locationResponse.status_code >= 400:
        print("Error: Location not found.")
        return None, None

    locationData = locationResponse.json()

    latitude = locationData.get('lat')
    longitude = locationData.get('lon')

    return latitude, longitude

#Function to request the latitude and longitude from the API based off the user's IP 
def getCoordinates(querystring):
    try:
        querystringLocation = {"q":querystring}
        locationURL = "https://weatherapi-com.p.rapidapi.com/current.json"
        locationHeaders = {
            "X-RapidAPI-Key": "d938ed0f31msha48d8b8712726ccp18ed84jsn171d6b153ec0",
            "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
        }

        locationResponse = requests.get(locationURL, headers=locationHeaders, params=querystringLocation, timeout=3)

        #Return none if an error occurs
        if(locationResponse.status_code >= 400):
            print("Error: Location not found.")
            return None, None
        
        locationData = locationResponse.json()

        latitude = locationData.get('location', {}).get('lat')
        longitude = locationData.get('location', {}).get('lon')

        return latitude, longitude
    #If 3 seconds pass without a response from the API, switch to the backup service
    except requests.Timeout:
        print("Service did not respond. Switching to backup service.")
        latitude, longitude = getCoordinatesBackupService(querystring)
        return latitude, longitude


#Suggest clothing based on temperature and precipitation
def suggestClothing(weatherData):
        currentTemp = weatherData.get('current', {}).get('temp_c')
        currentPrecip = weatherData.get('current', {}).get('precip_mm')
        currentLocation = weatherData.get('location', {}).get('name')

        if currentTemp is not None:
            print("Temperature: " + str(currentTemp))
            if(currentTemp > 15):
                print("It is warm so you should wear light clothing")
            else:
                print("It is cold so you should wear warm clothing")
        else:
            print("Temperature data unavailable")

        if currentPrecip is not None:
            print("Precipitation: " + str(currentPrecip))
            if(currentPrecip > 0):
                print("It is currently raining so you do need an umbrella")
            else:
                print("It is not raining so you don't need an umbrella")
        else:
            print("Precipitation data unavailable")

        if currentLocation is not None:
            print("Location: " + str(currentLocation))
        else:
            print("Location data unavailable")

if __name__ == "__main__":

    print("WeatherWear.com")
    print("---------------")
    print("1. Recommend clothing for current location")
    print("2. Recommend clothing for future location")
    print("3. Exit")

    choice = input("Enter choice: ")

    match choice:
        case '1':
            ip = get('https://api.ipify.org').text
            latitude, longitude = getCoordinates(ip)
            weatherData = getCurrentLocationWeather(latitude, longitude)
            suggestClothing(weatherData)

        case '2':
            airportCode = getInput("Enter airport code: ")
            date = getInput("Enter date: ")
                
            if validateAirportCode(airportCode) == True:
                if validateDate(date) == True:
                    #If airport code and date formats are valid, then continue with calling the functions to get the weather of the location. 
                    #Otherwise, print an error.
                    latitude, longitude = getCoordinates(airportCode)
                    forecastData = getFutureLocationWeather(latitude, longitude, date)
                    suggestClothing(forecastData)
                else:
                    print("Error: Invalid date format.")
            else:
                print("Error: Invalid airport code.")
            
        case '3':
            print("Exiting...")

        case _:
            print("Invalid option.")









