"""
Admin Program

Student ID: [REDECTED]
Name:       Foo Geng Hao
Class:      DISM/FT/1B/01
Assessment: CA1-1

Script name:
    admin.py

Purpose:
    file for game admin to view game report, add or edit word list and change game settings

Usage syntax:
    Run with play button in the submission folder (the folder which all the scripts and data files are stored)

Input file: (full path as on my laptop)
    D:/school_Y1S2/PSEC/CA1-1/word_list.json
    D:/school_Y1S2/PSEC/CA1-1/game_settings.json
    D:/school_Y1S2/PSEC/CA1-1/passwd.json
    D:/school_Y1S2/PSEC/CA1-1/game_log.json

Output file:
    D:/school_Y1S2/PSEC/CA1-1/word_list.json
    D:/school_Y1S2/PSEC/CA1-1/game_settings.json
    D:/school_Y1S2/PSEC/CA1-1/passwd.json

Python Version:
    Python 3.11.0

Reference:
    a) validating password requirments
        https://www.geeksforgeeks.org/python-program-check-validity-password/
    b) json guide
        https://realpython.com/python-json/

Library/module
    default modules:
        datetime 
        json

Known issues:
    nil
"""
import json, datetime

# useful repeated functions
def returnFile(file:str):
    """load json file and return it as dict/str (depending on contents of file)

    Args:
        file (str): target file name

    Returns:
        dict/str/list: contents of file
    """
    with open(file,'r') as fn:
        data = json.load(fn)
    return data

def writeDicIntoFile(dic: dict, file: str):
    """write dictionary into target json file

    Args:
        dic (dict): dictionary to write with
        file (str): target file name
    """
    with open(file,'w') as fn:
        json.dump(dic,fn,indent=4)

# functions to validate admin and go to menu
def access(enteredUser:str,enteredPW:str): 
    """takes in user entered username and password and checks if it is valid credentials in passwd.txt file

    Args:
        enteredUser (str): username
        enteredPW (str): password

    Returns:
        bool: True if entered username and password matches valid credentials and False otherwise 
    """
    passwd = returnFile('passwd.json')
    return bool(enteredUser == 'admin' and passwd == enteredPW)

def menu():
    """main menu after user validation
    """
    while True:
        print('\nAdmin options:','1. Edit word list','2. Change game settings','3. Print game report','4. Change password', '5. Exit', sep='\n')
        try:
            option = int(input('>>> ')) #if isNaN entered, error occurs and caught
            match option:
                case 1: 
                    word()
                case 2:
                    changeSettings()
                case 3:
                    printReport()
                case 4:
                    editAccess()
                case 5: 
                    print('Exiting...')
                    break
                case _: # for ints < 1 and > 5
                    print('Not a valid integer (1-5)')
        except ValueError: 
            print('Please enter a integer ')

# functions for modifying word list
def word():
    """menu of options to edit word list
    """
    while True:
        word_list = returnFile('word_list.json')
        print('\nWord list editing options:','1. Print current list','2. Add new word','3. Edit existing word','4. Delete word', '5. Create new empty list','6. Exit', sep='\n\t')
        try:
            option = int(input('\t>>> '))
            match option:
                case 1: # print word list
                    simWord, comWord = {}, {}
                    for word, meaning in word_list.items():
                        if (len(word) - word.count(' ')) >= 10:
                            comWord[word] = (meaning)
                        else:
                            simWord[word] = (meaning)
                    print(f'There are {len(simWord)} simple words:')
                    for word in simWord:
                        print(f'{word:<16}: {word_list[word]}')
                    print(f'\nThere are {len(comWord)} complex words:')
                    for word in comWord:
                        print(f'{word:<16}: {word_list[word]}')
                
                case 2: # add new word
                    addWord(word_list)
                case 3: # edit existing entry
                    editWord(word_list)
                case 4: # delete word
                    selWord = input('Enter word to delete: ').lower().strip()
                    if selWord not in word_list:
                        print('Word not found')
                    else:
                        confirm = input(f'Press [Y]es to confirm removing word \'{selWord}\' : {word_list[selWord]} : ').upper().strip()
                        if confirm == 'Y':
                            del(word_list[selWord])
                            writeDicIntoFile(word_list, 'word_list.json')
                            print('Word deleted')
                        else:
                            print('Deleting cancelled')
                case 5: 
                    confirm = input('Creating a new list means deleting the previous list. Enter [Y]es to confirm: ').upper().strip()
                    if confirm == 'Y':
                        word_list = {}
                        writeDicIntoFile(word_list, 'word_list.json')
                        print('Old entries deleted and empty word list created')
                    else:
                        print('Creating new cancelled')
                case 6:
                    print('Exiting word list editing')
                    return
                case _: 
                    print('Not a valid integer (1-5)')
        except ValueError: 
            print('Please input a integer') 

def addWord(wordlist: dict):
    """prompt user for word and meaning and enter it in word list

    Args:
        wordlist (dict): current dictionary of words
    """
    newWord = input('Enter new word: ').lower().strip()
    if newWord in wordlist:
        print(f'\'{newWord}\' already in list')
        return
    elif len(newWord) == 0:
        print('0-length word not allowed')
        return
    for letter in newWord: # check if all characters are letters, " ' " or space
        if (not letter.isalpha()) and not (letter == ' ' or letter == "\'"): 
            print('Word must only contain letters, spaces and apostrophes')
            break
    else:
        if (len(newWord) - newWord.count(' ')) >= 10:
            print(f'\'{newWord}\' is a Complex word (10 or more characters)')
        else:
            print(f'{newWord} is a Simple word (less than 10 characters)')
        while True:
            newMean = input('Enter meaning for word: ').strip()
            if newMean != '':
                wordlist[newWord] = newMean
                writeDicIntoFile(wordlist,'word_list.json')
                print('New word added!')
                break
            print('Meaning should not be blank')

def editWord(wordlist: dict):
    """ prompt admin to edit the word spelling or word meaning

    Args:
        wordlist (dict): dictionary of word list
    """
    selWord = input('Enter word to edit: ').lower().strip()
    if selWord not in wordlist:
        print('Word not found')
        return
    print(f'Word selected: \'{selWord}\': {wordlist[selWord]}')
    a = input('Enter [W]ord or [M]eaning to edit corresponding data: ').upper().strip()
    if a == 'W': # edit word spelling
        newWord = input('Enter new word: ').lower()
        if len(newWord) == 0: 
            print('0-length word not allowed')
            return
        if newWord in wordlist:
            print(f'\'{newWord}\' already in list')
            return
        for letter in newWord: 
            if (not letter.isalpha()) and not (letter == ' ' or letter == "\'"): 
                print('Word must only contain letters, spaces and apostrophes')
                return
        else:
            wordlist[newWord] = wordlist.pop(selWord) # tranferring word meaning to new word
            print(f'Word successfully changed to \'{newWord}\'!')
            writeDicIntoFile(wordlist, 'word_list.json')
    
    elif a == 'M': # edit word meaning
        print(f'Current meaning: {wordlist[selWord]}')
        newMean = input('Enter new meaning: ').strip()
        wordlist[selWord] = newMean
        if len(newMean) == 0: 
            print('0-length word not allowed')
            return
        print('Word meaning changed successfully')
        writeDicIntoFile(wordlist, 'word_list.json')
    else:
        print('Invalid option')
    
# function to change game settings
def changeSettings():
    """function to change any one setting specified by user

    Raises:
        Exception: user entered '0' to exit settings editing selection
        Exception: user entered an integer for a value not in range
        Exception: user entered a value that is less or equal to 0 or not a integer
    """
    game_settings = returnFile('game_settings.json')
    try:
        print('No.\tSetting\t\t\tValue')
        settingList = []
        for i, set in list(enumerate(game_settings,1)):
            print(f'{i}\t{set:<24}{game_settings[set]}')
            settingList.append(set)
        
        select = int(input('Choose setting number to edit (enter nothing to quit): ')) - 1 # enumuate list starts from 1 while indexing is form 0
        if select == -1:
            print('Changing settings cancelled')
            raise Exception
        elif not (select in range(0,len(settingList)) ):
            print('Number entered out of range')
            raise Exception
    
        while True: 
            try:
                newValue = int(input(f'Input new value for \'{settingList[select]}\' (current value: {game_settings[settingList[select]]}): '))
                if newValue < 1:
                    raise Exception
                else:    
                    break
            except:
                print('Value must be a positive integer')
        game_settings[settingList[select]] = newValue
        writeDicIntoFile(game_settings, 'game_settings.json')
        print(f'\'{settingList[select]}\' has been changed to {newValue}')
    except ValueError:
        print('Input must be an integer')
    except:
        return

# function to print game report
def printReport():
    """allow admin to view games played between two dates

    Raises:
        Exception: start date inputed is not in DD/MM/YYYY format
        Exception: end date inputed is not in DD/MM/YYYY format
        Exception: start date is greater than end date
    """
    game_log = returnFile('game_log.json') # list
    print('Enter dates to find games played in date range (by start time)')
    try:
        startDateStr = input('Enter start date in DD/MM/YYYY format (enter nothing to not specify start): ').strip()
        if startDateStr == '':
            startDate = convertToDate('1/1/0001')  # set deault start in year 1, as it is reasonable to assume no games are played before then
        else: 
            startDate = convertToDate(startDateStr) 
            if not startDate: # function returns nothing if date format is wrong
                raise Exception
        endDateStr = input('Enter end date in DD/MM/YYYY format (enter nothing to not specify end): ').strip()
        if endDateStr == '':
            endDate = datetime.datetime.now() # set default end as current system time, as no game logs should have been from the future
        else: 
            endDate = convertToDate(endDateStr)
            if not endDate:
                raise Exception
        if startDate > endDate:
            print('Start date must not be later than end date')
            raise Exception
    except:
        return
        
    gamesInRange = []
    for item in game_log:
        if startDate <= convertToDate(item['date']) <= endDate:
            gamesInRange.append(item)
    if len(gamesInRange):
        print('Player name\tScore\tSets\tLifelines Used\tComplex\tStart Date & Time\tEnd Date & Time')
        for item in gamesInRange:
            print(f'{item["name"]:<12}', item['score'], item['sets played'], str(item['lifelines used']) + '\t',item['complex words'],f'{item["date"]} {item["time"]}',item['datetime ended'],sep='\t')
    else: 
        print('No games found in date range')

def convertToDate(dateString: str):
    """string with DD/MM/YYYY format get changed to date object

    Args:
        dateString (str): date in DD/MM/YYYY format

    Returns:
        datetime.datetime: inputed date as datetime object
    """
    try:
        DMY = dateString.split('/') # split to DD, MM, YYYY 
        newDMY = list()
        for i in DMY:
            newDMY.append(int(i))
        date = datetime.datetime(newDMY[2], newDMY[1],newDMY[0])
        return date
    except:
        print('Date not in correct format (DD/MM/YYYY)')
        return  

# function to change password
def editAccess():
    """allow admin to change their password
    """
    print('Password requirments:','Between 4-20 characters long','At least 1 uppercase and 1 lowercase letter','At least 1 number','At least one special symbol (! @ # $ %)',sep='\n\t')
    while True:
        newPW = input('Enter new password (enter nothing to cancel): ')
        if len(newPW) == 0:
            print('Password change cancelled')
            return
        upperCase = 'QWERTYUIOPASDFGHJKLZXCVBNM'
        lowerCase = 'qwertyuiopasdfghjklzxcvbnm'
        nums = '1234567890'
        spChar = '!@#$%'
        if len(newPW) in range(4,21): # check len
            pwRequire = { # basically the checkbox for other requirments
                'Uppercase': False,
                'Lowercase': False,
                'Number': False,
                'Special character':False,
                'No invalid special character': True }
            for char in newPW:
                if char in upperCase: 
                    pwRequire['Uppercase'] = True
                elif char in lowerCase: 
                    pwRequire['Lowercase'] = True
                elif char in nums: 
                    pwRequire['Number'] = True
                elif char in spChar: 
                    pwRequire['Special character'] = True
                else: # if it ends up here, character is invalid for password
                    pwRequire['No invalid special character'] = False
            if False in pwRequire.values(): # check all values in checklist
                print('Password is missing:')
                for item in pwRequire:
                    if not pwRequire[item]:
                        print('\t'+ item)
            else:
                if (input('Re-enter password: ')) == newPW:
                    with open('passwd.json','w') as passwd:
                        json.dump(newPW,passwd)
                    print('Password successfully changed')
                    return
                else: 
                    print('Passwords does not match')
        else:
            print('Password is not within length range')

# start of script
print('Welcome to admin script')
for i in range(2,-1,-1): # to allow admin to attempt login 3 times
    user = input('Please enter username: ')
    pw = input('Plase enter your password: ')
    if access(user, pw):
        print('Access granted')
        menu()
        break # ends loop once the admin exits menu
    elif i > 0:
        print(f'Username or password incorrect. {i} tries left')
    else:
        print(f'Username or password incorrect. Terminating...')
