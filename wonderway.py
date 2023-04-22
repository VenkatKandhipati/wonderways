import asyncio
import os
import urllib.parse
import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
from sydney import SydneyClient

ASK_LOCATION_START = 'What is your starting location: '
ASK_LOCATION_END = 'What is your destination: '
SELECT_YOUR_LOCATION = 'Select an option: '

# autocomplete_api_key = 'AIzaSyCtc3PJQHYVAZc0qvA1X_8AVisLOHBY4NU'
AUTOCOMPLETE_API_KEY = '&apiKey=04ac17cb87a948e090b32ab737424ede'
AUTOCOMPLETE_URL = "https://api.geoapify.com/v1/geocode/autocomplete?text="
os.environ["BING_U_COOKIE"] = "1ItVFIzKeJ4ET1TMuQo7Tkbj9NEwiA6HF8TbvJgKvbA1M8hh5C1sKlJ5HN1q9XP0amEvc6xYdn4VRL16NqJFDXVtLta6flRLc_n3gCRwfEtb-xn_pUSMDcSILsYdNH-U__e1H6TJns2Ew-W_57OIa1I_XjXoCCY0Qq2pnU2v0G1c8KwN23fWmm-QBewz5SBGzmc3z_DT4JY3fBn_nWsJ2rPpVdz-1D0jSUB2WOYN9R0U"

#locations
locationA = ''
locationB = ''
ASK_INTERESTS = 'What interests do you want to see? (Hit "Enter" to quit)'
INTERESTS = ['outlets', 'museums', 'nature', 'hotels', 'restaurants']
WONDERS = OrderedDict(enumerate(INTERESTS, 1))

BASE_GOOGLEDIR_URL = "https://www.google.com/maps/dir/?api=1"

def askUserInput(prompt: str) -> str:
    return input(prompt)

def autocompleteUserInput(userLocation: str) -> str:
    '''
    @brief Asks user to select a location from autocompleted list.
    
    @param userLocation: The inputted location the user typed.

    @return The chosen location in a string format.
    '''
    autocompleteOptions = autocompleteApiPing(userLocation)
    # TODO what if the autocomplete options are empty??
    for index, location in enumerate(autocompleteOptions):
        print(index, location)
    return autocompleteOptions[int(askUserInput(SELECT_YOUR_LOCATION))]

def autocompleteApiPing(query: str) -> list[str]:
    '''
    @brief Ping the autocomplete api with what the user has entered. Returns a list of possible options.
    @param query: What the user inputed prior to autocompletion.

    @return A list containing all the auto completed options.
    '''
    rawResult = requests.get(AUTOCOMPLETE_URL + query + AUTOCOMPLETE_API_KEY)
    jsonResult = rawResult.json()
    try:
        simplifiedResults = jsonResult['features']
    except KeyError:
        pass
    return list(simplifiedResults[i]['properties']['formatted'] for i in range(len(simplifiedResults)))

def askUserInterests() -> list[int]:
    '''
    @brief Prompts the user from a curated list to select wonders that interest them. 

    @return A list containing what interests the user.
    '''
    print(ASK_INTERESTS)
    response = 'temp'
    answers = []
    while response != '':
        for key, val in WONDERS.items():
            print(f'{key}. {val}')
        response = askUserInput('') 
        if response != '':
            answers.append(int(response))
    return answers

async def setupSydney() -> None:
    '''Create and initialize Sydney Client for Bing Chat'''
    # sydney = SydneyClient()

    # sydney = SydneyClient(style="creative")
    async with SydneyClient(style="creative") as sydney:
        # response = await sydney.ask(f"format a list of 10 restaurants that are located in between {locationA} and {locationB} and sort by yelp rating")
        # response = await sydney.ask(f"generate a list of 10 restaurants between {locationA} and {locationB} in the format: 'restaurant - zipcode'. ")
        response = await sydney.ask(f"Generate a list of restaurants between {locationA} and {locationB} in the format: Name, Location")

        print(response)

    return

def getCities(cityA: str, stateA: str, cityB: str, stateB: str) -> list[str]:
    r = requests.post(f'https://citiesbetween.com/{cityA}-{stateA}-and-{cityB}-{stateB}')
    b = BeautifulSoup(r.text, 'lxml')

    cities = []
    for div in b.find_all('div', class_='cityinfo'):
        a_tag = div.find('a')
        cities.append(a_tag.text.strip())
    
    return cities


def locationToURLEncodedLocation(location: str) -> str:
    '''
    @brief Encodes a given string into a url-safe string.

    @param location: A real world address in plain string format.

    @return URL-encoded version of the string passed in.
    '''
    return urllib.parse.quote(location)

def createGoogleDirectionURL(startLocation: str, endLocation: str) -> str:
    '''
    @brief Given the starting location as a string and the ending location as a string,
           the function will return google map link that routes between point A and
           point B.

    @param startLocation: The starting location as a string.
    @param endLocation:   The ending location as a string.

    @return A google map URL.
    '''
    startEncoded = locationToURLEncodedLocation(startLocation)
    endEncoded = locationToURLEncodedLocation(endLocation)

    final_str = f'{BASE_GOOGLEDIR_URL}&origin={startEncoded}&destination={endEncoded}&travelmode=driving'

    return final_str

if __name__ == '__main__':
    locationA = autocompleteUserInput(askUserInput(ASK_LOCATION_START))
    locationB = autocompleteUserInput(askUserInput(ASK_LOCATION_END))

    locALst = locationA.split(',')
    locBLst = locationB.split(',')
    cityA, stateA = locALst[-3].strip().replace(' ', '-'), locALst[-2].split()[0].strip()
    cityB, stateB = locBLst[-3].strip().replace(' ', '-'), locBLst[-2].split()[0].strip()

    print(getCities(cityA, stateA, cityB, stateB))
    
    # asyncio.run(setupSydney())

    
    