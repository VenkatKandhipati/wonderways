import asyncio
import os
import re
import requests
import urllib.parse
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
INTERESTS = ['Outlets', 'Museums', 'Trails', 'Hotels', 'Restaurants']
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
    return [WONDERS[num] for num in answers]

async def setupSydney(wonder: list[str], cities: list[str]) -> list[str, str]:
    '''Create and initialize Sydney Client for Bing Chat'''
    async with SydneyClient(style="creative") as sydney:
        # response = await sydney.ask(f"format a list of 10 restaurants that are located in between {locationA} and {locationB} and sort by yelp rating")
        # response = await sydney.ask(f"generate a list of 10 restaurants between {locationA} and {locationB} in the format: 'restaurant - zipcode'. ")

        # response = await sydney.ask(f"Create a list the following cities ({', '.join(cities)}), for every interest ({', '.join(wonder)}), find me 1 highly recommended interest in the city with format: 'Name: Location'")
        # response1 = await sydney.ask(f"Create a list of the following cities ({', '.join(cities)}), and find me 1 highly recommended ({wonder[0]}) in the city with format: 'Name: Location'")
        # response2 = await sydney.ask(f"Create a list of the following cities ({', '.join(cities)}), and find me 1 highly recommended ({wonder[1]}) in the city with format: 'Name: Location'")
        
        response1 = await sydney.ask(f"create a list of the following cities ({', '.join(cities)}), and find me 1 highly recommended {wonder[0]} in each city. Don't include the citations. Use the following as an example output you should follow: - Dyer: John Dillinger Museum - Costa Mesa: Lyon Air Museum - Fountain Valley: Heritage Museum of Orange County - Westminster: Vietnam War Memorial - Los Alamitos: Los Alamitos Museum - Hawaiian Gardens: Hawaiian Gardens Historical Society - Cerritos: Cerritos Library - Norwalk: Hargitt House Museum - Downey: Columbia Memorial Space Center - East Los Angeles: Vincent Price Art Museum - Redondo Junction: California Science Center")
        response2 = await sydney.ask(f"create a list of the following cities ({', '.join(cities)}), and find me 1 highly recommended {wonder[1]} in each city. Don't include the citations. Use the following as an example output you should follow: - Dyer: John Dillinger Museum - Costa Mesa: Lyon Air Museum - Fountain Valley: Heritage Museum of Orange County - Westminster: Vietnam War Memorial - Los Alamitos: Los Alamitos Museum - Hawaiian Gardens: Hawaiian Gardens Historical Society - Cerritos: Cerritos Library - Norwalk: Hargitt House Museum - Downey: Columbia Memorial Space Center - East Los Angeles: Vincent Price Art Museum - Redondo Junction: California Science Center")
        # response1 = await sydney.ask(f"create a list of the following cities ({', '.join(cities)}), and find me 1 highly recommended {wonder[0]} or {wonder[1]} in each city. If there are no recommendations, do NOT include it in the list. Don't include the citations. Use the following as an example output you should follow: - Dyer: street address - Costa Mesa: street address - Fountain Valley: street address - Westminster: street address - Los Alamitos: street address - Hawaiian Gardens: street address - Cerritos: street address - Norwalk: street address - Downey: street address - East Los Angeles: street address - Redondo Junction: street address")

        # if city != 'restaurants':
        #     response = await sydney.ask(f"Find me 1 highly recommended {wonder} in the city {city} with format: 'Name: Location'")
        # else:
        #     response = await sydney.ask(f"Find me 3 highly recommended {wonder} in the city {city} with format: 'Name: Location'")
        print(response1)
        print(response2)
        return [response1, response2]
    
def parseBingOutput(response: str, userInterest) -> dict[str, str]:
    
    # # pattern = r"- (\w+):\n\s+- {}?: (.*?)\n\s+- {}?: (.*?)\n".format(user_interest[0], user_interest[1])
    # pattern = r"- (\w+): ([^\n]+)"
    # # matches = re.findall(pattern, response, re.DOTALL)
    # matches = re.findall(pattern, response)

    pattern = r"- (\w+): ([^\n]+)"
    matches = re.findall(pattern, response)


    # city_data = {}
    # for match in matches:
    #     city = match[0]
    #     interest0 = re.sub(r'[\[\]]|\*{2}', '', match[1])
    #     interest1 = re.sub(r'[\[\]]|\*{2}', '', match[2])
    #     city_data[city] = {user_interest[0]: interest0, user_interest[1]: interest1}
    # return city_data
    city_wonder_data = {}
    for match in matches:
        city = match[0]
        wonder = re.sub(r'\*\*|\[.*?\]', '', match[1])
        city_wonder_data[city] = {userInterest: wonder}
    return city_wonder_data

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

def createGoogleDirectionURL(startLocation: str, endLocation: str, waypoints: list[str] | None = None) -> str:
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

    if waypoints is not None:
        final_str += f'&waypoints={locationToURLEncodedLocation("|".join(waypoints))}'

    return final_str

def cleanDict(inputDict: dict[str, dict[str, str]]) -> list[list[str], dict[str, dict[str, str]]]:
    preWaypoints = []
    deleteList = []
    for city, innerDict in inputDict.items():
        for wonder, location in innerDict.items():
            cleanedLocation = location.split(',')[0]
            if cleanedLocation.startswith('No'):
                deleteList.append(city)
            else:
                inputDict[city][wonder] = cleanedLocation
                preWaypoints.append(f'{city} {cleanedLocation}')

    for d in deleteList:
        del inputDict[d]

    return [preWaypoints,inputDict]


if __name__ == '__main__':
    locationA = autocompleteUserInput(askUserInput(ASK_LOCATION_START))
    locationB = autocompleteUserInput(askUserInput(ASK_LOCATION_END))

    # locationA = 'UCI - North Campus, Irvine, CA, United States of America'
    # locationB = 'Ronald Reagan UCLA Medical Center, 757 Westwood Plaza, Los Angeles, CA 90095, United States of America'

    user_interest = askUserInterests()

    locALst = locationA.split(',')
    locBLst = locationB.split(',')
    cityA, stateA = locALst[-3].strip().replace(' ', '-'), locALst[-2].split()[0].strip()
    cityB, stateB = locBLst[-3].strip().replace(' ', '-'), locBLst[-2].split()[0].strip()

    all_cities = getCities(cityA, stateA, cityB, stateB)

    bingResponses = asyncio.run(setupSydney(user_interest, all_cities))

    waypoints0, output_dict0 = cleanDict(parseBingOutput(bingResponses[0], user_interest[0]))
    waypoints1, output_dict1 = cleanDict(parseBingOutput(bingResponses[1], user_interest[1]))

    print(waypoints0)
    print(waypoints1)
    print(output_dict0)
    print(output_dict1)
    # for city, interests in output_dict.items():
    #     print("City:", city)
    #     for interest, location in interests.items():
    #         print("- {}: {}".format(interest, location))
    #     print()

    
    