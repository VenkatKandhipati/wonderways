import requests

#prompts
from collections import OrderedDict

ASK_LOCATION_START = 'What is your starting location: '
ASK_LOCATION_END = 'What is your destination: '
SELECT_YOUR_LOCATION = 'Select an option: '

# autocomplete_api_key = 'AIzaSyCtc3PJQHYVAZc0qvA1X_8AVisLOHBY4NU'
autocomplete_api_key = '&apiKey=04ac17cb87a948e090b32ab737424ede'
autocomplete_url = "https://api.geoapify.com/v1/geocode/autocomplete?text="

#locations
locationA = ''
locationB = ''
ASK_INTERESTS = 'What interests do you want to see? (Hit "Enter" to quit)'
INTERESTS = ['concert', 'restaurant']
WONDERS = OrderedDict(enumerate(INTERESTS, 1))

def askUserInput(prompt: str) -> str:
    return input(prompt)

def autocompleteUserInput(userLocation: str) -> str:
    '''Asks user to select a location from autocompleted list'''
    autocompleteOptions = autocompleteApiPing(userLocation)
    for index, location in enumerate(autocompleteOptions):
        print(index, location)
    return autocompleteOptions[int(askUserInput(SELECT_YOUR_LOCATION))]

def autocompleteApiPing(query:str ) -> list[str]:
    '''Ping the autocomplete api with what the user has entered. Returns a list of possible options'''
    rawResult = requests.get(autocomplete_url + query + autocomplete_api_key)
    jsonResult = rawResult.json()
    try:
        simplifiedResults = jsonResult['features']
    except KeyError:
        pass
    return list(simplifiedResults[i]['properties']['formatted'] for i in range(len(simplifiedResults)))

def askUserInterests() -> list[int]:
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

if __name__ == '__main__':
    locationA = autocompleteUserInput(askUserInput(ASK_LOCATION_START))
    locationB = autocompleteUserInput(askUserInput(ASK_LOCATION_END))
    print("Selected location A: " + locationA)
    print("Selected location B: " + locationB)