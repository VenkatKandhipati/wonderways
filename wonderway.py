ASK_LOCATION_START = 'What is your current location: '
ASK_LOCATION_END = 'What is your destination: '
ASK_INTERESTS = 'What interests do you want to see?'
WONDERS = ['concert', 'restaurant']

def askUserInput(prompt: str) -> str:
    return input(prompt)

def findLocationSuggestions():
    pass

def askUserInterests() -> str:
    print(ASK_INTERESTS)
    for idx, itm in enumerate(WONDERS, 1):
        print(f'{idx}. {itm}')
    return askUserInput('')

if __name__ == '__main__':
    print(askUserInput(ASK_LOCATION_START))
    print(askUserInput(ASK_LOCATION_END))