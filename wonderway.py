from collections import OrderedDict

ASK_LOCATION_START = 'What is your current location: '
ASK_LOCATION_END = 'What is your destination: '
ASK_INTERESTS = 'What interests do you want to see? (Hit "Enter" to quit)'
INTERESTS = ['concert', 'restaurant']
WONDERS = OrderedDict(enumerate(INTERESTS, 1))

def askUserInput(prompt: str) -> str:
    return input(prompt)

def findLocationSuggestions():
    pass

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
    # print(askUserInput(ASK_LOCATION_START))
    # print(askUserInput(ASK_LOCATION_END))
    print(askUserInterests())