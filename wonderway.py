ASK_LOCATION_START = 'What is your current location: '
ASK_LOCATION_END = 'What is your destination: '

def askUserInput(prompt: str) -> str:
    return input(prompt)



if __name__ == '__main__':
    print(askUserInput(ASK_LOCATION_START))
    print(askUserInput(ASK_LOCATION_END))