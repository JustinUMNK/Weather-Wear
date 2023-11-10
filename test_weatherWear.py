import unittest
from unittest.mock import patch, MagicMock
from weatherWear import getCoordinates, suggestClothing, getCurrentLocationWeather, getFutureLocationWeather, validateAirportCode, validateDate, getInput, formatCurrentWeatherQueryString, formatFutureWeatherQueryString, getCoordinatesBackupService
import requests

class testvalidateAirportCode(unittest.TestCase):
    def test_validAirportCode(self):
        airportCode = "LHR"

        result = validateAirportCode(airportCode)

        self.assertTrue(result)
    def test_invalidAirportCodeWithTooFewLetters(self):
        airportCode = "A"

        result = validateAirportCode(airportCode)

        self.assertFalse(result)
    def test_invalidAirportCodeWithTooManyLetters(self):
        airportCode = "ABCD"

        result = validateAirportCode(airportCode)

        self.assertFalse(result)
    def test_invalidAirportCodeWithNoLetters(self):
        airportCode = ""

        result = validateAirportCode(airportCode)

        self.assertFalse(result)
    def test_invalidAirportCodeWithNumbers(self):
        airportCode = "AB1"

        result = validateAirportCode(airportCode)

        self.assertFalse(result)

class testvalidateDate(unittest.TestCase):
    def test_validDate(self):
        date = "2023-11-25"

        result = validateDate(date)

        self.assertTrue(result)
    def test_invalidDateWithLetters(self):
        date = "2023-11-AA"

        result = validateDate(date)

        self.assertFalse(result)
    def test_invalidDateWithTooManyNumbersInYear(self):
        date = "20230-11-11"

        result = validateDate(date)

        self.assertFalse(result)
    def test_invalidDateWithTooManyNumbersInMonth(self):
        date = "2023-111-11"

        result = validateDate(date)

        self.assertFalse(result)
    def test_invalidDateWithTooManyNumbersInDay(self):
        date = "2023-11-111"

        result = validateDate(date)

        self.assertFalse(result)
    def test_invalidDateWithTooFewNumbersInYear(self):
        date = "202-11-11"

        result = validateDate(date)

        self.assertFalse(result)
    def test_invalidDateWithTooFewNumbersInMonth(self):
        date = "2023-0-11"

        result = validateDate(date)

        self.assertFalse(result)
    def test_invalidDateWithTooFewNumbersInDay(self):
        date = "2023-11-0"

        result = validateDate(date)

        self.assertFalse(result)
    def test_invalidDateWithNoDashes(self):
        date = "20231111"

        result = validateDate(date)

        self.assertFalse(result)
    def test_invalidDateWithSpaces(self):
        date = "2023 11 11"

        result = validateDate(date)

        self.assertFalse(result)

class testgetInput(unittest.TestCase):
    @patch('builtins.input', return_value='test')
    def test_getInput(self, mock_input):
        input = "test"

        result = getInput(input)

        self.assertEqual(result, input)

class testSuggestClothing(unittest.TestCase):
    @patch('builtins.print')
    def test_suggestClothingWithWarmTemp(self, mock_print):
        weather_data = {
            'current': {
                'temp_c': 17,
                'precip_mm': 0,
            },
            'location': {
                'name': 'Test Location'
            }
        }

        suggestClothing(weather_data)

        mock_print.assert_any_call("Temperature: 17")
        mock_print.assert_any_call("It is warm so you should wear light clothing")
    @patch('builtins.print')
    def test_suggestClothingWithColdTemp(self, mock_print):
        weather_data = {
            'current': {
                'temp_c': 13,
                'precip_mm': 0,
            },
            'location': {
                'name': 'London'
            }
        }

        suggestClothing(weather_data)

        mock_print.assert_any_call("Temperature: 13")
        mock_print.assert_any_call("It is cold so you should wear warm clothing")
    @patch('builtins.print')
    def test_suggestClothingWithWarmTempNoRain(self, mock_print):
        weather_data = {
            'current': {
                'temp_c': 17,
                'precip_mm': 0,
            },
            'location': {
                'name': 'Test Location'
            }
        }

        suggestClothing(weather_data)

        mock_print.assert_any_call("Temperature: 17")
        mock_print.assert_any_call("It is warm so you should wear light clothing")
        mock_print.assert_any_call("Precipitation: 0")
        mock_print.assert_any_call("It is not raining so you don't need an umbrella")
    @patch('builtins.print')
    def test_suggestClothingWithWarmTempAndRain(self, mock_print):
        weather_data = {
            'current': {
                'temp_c': 17,
                'precip_mm': 0.5,
            },
            'location': {
                'name': 'Test Location'
            }
        }

        suggestClothing(weather_data)

        mock_print.assert_any_call("Temperature: 17")
        mock_print.assert_any_call("It is warm so you should wear light clothing")
        mock_print.assert_any_call("Precipitation: 0.5")
        mock_print.assert_any_call("It is currently raining so you do need an umbrella")
    @patch('builtins.print')
    def test_suggestClothingWithColdTempNoRain(self, mock_print):
        weather_data = {
            'current': {
                'temp_c': 13,
                'precip_mm': 0,
            },
            'location': {
                'name': 'London'
            }
        }

        suggestClothing(weather_data)

        mock_print.assert_any_call("Temperature: 13")
        mock_print.assert_any_call("It is cold so you should wear warm clothing")
        mock_print.assert_any_call("Precipitation: 0")
        mock_print.assert_any_call("It is not raining so you don't need an umbrella")
    @patch('builtins.print')
    def test_suggestClothingWithColdTempAndRain(self, mock_print):
        weather_data = {
            'current': {
                'temp_c': 13,
                'precip_mm': 0.5,
            },
            'location': {
                'name': 'London'
            }
        }

        suggestClothing(weather_data)

        mock_print.assert_any_call("Temperature: 13")
        mock_print.assert_any_call("It is cold so you should wear warm clothing")
        mock_print.assert_any_call("Precipitation: 0.5")
        mock_print.assert_any_call("It is currently raining so you do need an umbrella")
    @patch('builtins.print')
    def test_suggestClothingWithNoRain(self, mock_print):
        weather_data = {
            'current': {
                'temp_c': 17,
                'precip_mm': 0,
            },
            'location': {
                'name': 'London'
            }
        }

        suggestClothing(weather_data)

        mock_print.assert_any_call("Precipitation: 0")
        mock_print.assert_any_call("It is not raining so you don't need an umbrella")
    @patch('builtins.print')
    def test_suggestClothingWithRain(self, mock_print):
        weather_data = {
            'current': {
                'temp_c': 17,
                'precip_mm': 0.5,
            },
            'location': {
                'name': 'London'
            }
        }

        suggestClothing(weather_data)

        mock_print.assert_any_call("Precipitation: 0.5")
        mock_print.assert_any_call("It is currently raining so you do need an umbrella")
    @patch('builtins.print')
    def test_suggestClothingWithNoneTemp(self, mock_print):
        weather_data = {
            'current': {
                'temp_c': None,
                'precip_mm': 0,
            },
            'location': {
                'name': 'Test Location'
            }
        }

        suggestClothing(weather_data)

        mock_print.assert_any_call("Temperature data unavailable")
    @patch('builtins.print')
    def test_suggestClothingWithNonePrecip(self, mock_print):
        weather_data = {
            'current': {
                'temp_c': 17,
                'precip_mm': None,
            },
            'location': {
                'name': 'Test Location'
            }
        }

        suggestClothing(weather_data)

        mock_print.assert_any_call("Precipitation data unavailable")
    @patch('builtins.print')
    def test_suggestClothingWithNoneLocation(self, mock_print):
        weather_data = {
            'current': {
                'temp_c': 17,
                'precip_mm': 0.5,
            },
            'location': {
                'name': None
            }
        }

        suggestClothing(weather_data)

        mock_print.assert_any_call("Location data unavailable")
    @patch('builtins.print')
    def test_suggestClothingWithExactly15TempNoRain(self, mock_print):
        weather_data = {
            'current': {
                'temp_c': 15,
                'precip_mm': 0,
            },
            'location': {
                'name': 'Test Location'
            }
        }

        suggestClothing(weather_data)

        mock_print.assert_any_call("Temperature: 15")
        mock_print.assert_any_call("It is cold so you should wear warm clothing")
        mock_print.assert_any_call("Precipitation: 0")
        mock_print.assert_any_call("It is not raining so you don't need an umbrella")
    @patch('builtins.print')
    def test_suggestClothingWithExactly15TempAndRain(self, mock_print):
        weather_data = {
            'current': {
                'temp_c': 15,
                'precip_mm': 0.5,
            },
            'location': {
                'name': 'Test Location'
            }
        }

        suggestClothing(weather_data)

        mock_print.assert_any_call("Temperature: 15")
        mock_print.assert_any_call("It is cold so you should wear warm clothing")
        mock_print.assert_any_call("Precipitation: 0.5")
        mock_print.assert_any_call("It is currently raining so you do need an umbrella")

class testformatCurrentWeatherQueryString(unittest.TestCase):
    def test_formatCurrentWeatherQueryString(self):
        latitude, longitude = 35.9375, 14.3754

        result = formatCurrentWeatherQueryString(latitude, longitude)

        self.assertEqual(result, {"q": "35.9375,14.3754"})
    def test_formatCurrentWeatherQueryStringNegativeValues(self):
        latitude, longitude = -35.9375, -14.3754

        result = formatCurrentWeatherQueryString(latitude, longitude)

        self.assertEqual(result, {"q": "-35.9375,-14.3754"})
    def test_formatCurrentWeatherQueryStringZeroValues(self):
        latitude, longitude = 0, 0

        result = formatCurrentWeatherQueryString(latitude, longitude)

        self.assertEqual(result, {"q": "0,0"})
    def test_formatCurrentWeatherQueryStringNoneValues(self):
        latitude, longitude = None, None

        result = formatCurrentWeatherQueryString(latitude, longitude)

        self.assertEqual(result, {"q": "None,None"})

class testformatFutureWeatherQueryString(unittest.TestCase):
    def test_formatFutureWeatherQueryString(self):
        latitude, longitude = 35.9375, 14.3754
        date = 2023-11-25

        result = formatFutureWeatherQueryString(latitude, longitude, date)

        self.assertEqual(result, {"q": "35.9375,14.3754","dt": f"{date}"})
    def test_formatFutureWeatherQueryStringNegativeValues(self):
        latitude, longitude = -35.9375, -14.3754
        date = 2023-11-25

        result = formatFutureWeatherQueryString(latitude, longitude, date)

        self.assertEqual(result, {"q": "-35.9375,-14.3754","dt": f"{date}"})
    def test_formatFutureWeatherQueryStringZeroValues(self):
        latitude, longitude = 0, 0
        date = 2023-11-25

        result = formatFutureWeatherQueryString(latitude, longitude, date)

        self.assertEqual(result, {"q": "0,0","dt": f"{date}"})
    def test_formatFutureWeatherQueryStringNoneValues(self):
        latitude, longitude = None, None
        date = 2023-11-25

        result = formatFutureWeatherQueryString(latitude, longitude, date)

        self.assertEqual(result, {"q": "None,None","dt": f"{date}"})
    

class testgetCurrentLocationWeather(unittest.TestCase):
    @patch('weatherWear.requests.get')
    #Mocks the API call and tests that the function correctly returns the data
    def test_getCurrentLocationWeatherCorrectlyReturnsWeatherData(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {'current': {'temp_c': 20}, 'location': {'name': 'Birkirkara'}}
        mock_get.return_value = mock_response

        result = getCurrentLocationWeather(35.9375, 14.3754)
        
        self.assertEqual(result, {'current': {'temp_c': 20}, 'location': {'name': 'Birkirkara'}})

class testgetFutureLocationWeather(unittest.TestCase):
    @patch('weatherWear.requests.get')
    def test_getFutureLocationWeatherCorrectlyReturnsWeatherData(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {'current': {'temp_c': 20}, 'location': {'name': 'Birkirkara'}}
        mock_get.return_value = mock_response

        result = getFutureLocationWeather(35.9375, 14.3754, 2023-11-25)
        
        self.assertEqual(result, {'current': {'temp_c': 20}, 'location': {'name': 'Birkirkara'}})

class testgetCoordinates(unittest.TestCase):
    @patch('weatherWear.requests.get')
    def test_getCoordinatesWithSuccessfulAPICall(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'location': {
                'lat': 35.9375,
                'lon': 14.3754
            }
        }
        mock_get.return_value = mock_response

        latitude, longitude = getCoordinates('querystring')

        self.assertEqual(latitude, 35.9375)
        self.assertEqual(longitude, 14.3754)
    @patch('weatherWear.requests.get')
    @patch('builtins.print')
    #Mocks a status code of 400 to test whether the function correctly handles an error
    def test_getCoordinatesWithError(self, mock_print, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_get.return_value = mock_response

        latitude, longitude = getCoordinates('querystring')

        self.assertIsNone(latitude)
        self.assertIsNone(longitude)
        mock_print.assert_called_with("Error: Location not found.")
    @patch('weatherWear.requests.get')
    @patch('builtins.print')
    #Mocks a timeout to test whether the function correctly detects a timeout
    def test_getCoordinatesWithTimeout(self, mock_print, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.side_effect = [requests.Timeout(), mock_response]

        latitude, longitude = getCoordinates('querystring')

        mock_print.assert_called_with("Service did not respond. Switching to backup service.")

class testgetCoordinatesBackupService(unittest.TestCase):
    @patch('weatherWear.requests.get')
    def test_getCoordinatesBackupServiceWithSuccessfulAPICall(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'lat': 35.9375,
            'lon': 14.3754
        }
        mock_get.return_value = mock_response

        latitude, longitude = getCoordinatesBackupService('querystring')

        self.assertEqual(latitude, 35.9375)
        self.assertEqual(longitude, 14.3754)
    @patch('weatherWear.requests.get')
    @patch('builtins.print')
    def test_getCoordinatesBackupServiceWithError(self, mock_print, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_get.return_value = mock_response

        latitude, longitude = getCoordinatesBackupService('querystring')

        self.assertIsNone(latitude)
        self.assertIsNone(longitude)
        mock_print.assert_called_with("Error: Location not found.")

if __name__ == '__main__':
    unittest.main()