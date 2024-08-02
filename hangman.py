"""
Hangman Program

Student ID: [REDECTED]
Name:       Foo Geng Hao
Class:      DISM/FT/1B/01
Assessment: CA1-1

Script name:
    hangman.py

Purpose:
    player to play hangman and view top games

Usage syntax:
    Run with play button in the submission folder (the folder which all the scripts and data files are stored)

Input file: (full path as on my laptop)
    D:/school_Y1S2/PSEC/CA1-1/word_list.json
    D:/school_Y1S2/PSEC/CA1-1/game_settings.json
    D:/school_Y1S2/PSEC/CA1-1/hang.json
    D:/school_Y1S2/PSEC/CA1-1/game_log.json

Output file:
    D:/school_Y1S2/PSEC/CA1-1/game_log.json

Python Version:
    Python 3.11.0

Reference:
    a) heapq documentation (links to nlargest section)
        https://docs.python.org/3/library/heapq.html#heapq.nlargest
    b) using lambda to sort items in list by key
        https://careerkarma.com/blog/python-sort-a-dictionary-by-value/

Library/module
    default modules:
        random
        datetime
        json
        heapq

Known issues:
    nil
"""
import random, datetime, json, heapq

# hangman functions
def hangman():
    """main body of hangman program - initanalise varibles used and generate random words, and then run function to play each set

    Returns:
        bool: True if player wishes to play next game, False if player does not want to continue
    """
    # setting varibles for the game
    with open('word_list.json','r') as fn:
        word_list = json.load(fn)
    words = []
    for key in word_list:
        words.append(key)
    randomWords = random.sample(words, noOfWords)
    complexCount = 0
    for word in randomWords:
        if (len(word) - word.count(' ')) >= 10:
            complexCount += 1
    playerScore = 0
    LifeLinesUsed = 0
    dtStart = datetime.datetime.now() # create datetime.datetime obj 
    
    for currentSet, word in enumerate(randomWords,1):
        a, LifeLinesUsed = hangmanSet(word, currentSet, word_list[word], LifeLinesUsed)
        playerScore += a
        option = ''
        if currentSet != len(randomWords):
            while True: # ask player to play next set
                option = input('Enter [Y]es to continue game or [N] to quit: ').strip().upper()
                if option == 'N' or option == 'Y':
                    break
                else:
                    print('Please enter a valid input')
        if option == 'N': 
            print('Terminating game...')
            return False # player exits mid game
    
    if playerScore > maxPoints: 
        playerScore = maxPoints
    elif playerScore <= 0:
        playerScore = 0
    print(f'You scored {playerScore} over {noOfWords} sets')
    if playerScore < winningPoints:
        print(f'Unforturnately, you scored below {winningPoints} and did not win')
    elif playerScore == maxPoints and LifeLinesUsed == 0: 
        print((f'Congulations! You scored the max points of {maxPoints} without any lifelines! This will be shown in the hall of fame!'))
    else: 
        print((f'Congulations! You scored at least {winningPoints} and won!'))
    # generate game log
    dtEnd = datetime.datetime.now()
    gameInfo = {
        'name':playerName,
        'score':playerScore,
        'sets played':noOfWords,
        'complex words':complexCount,
        'lifelines used':LifeLinesUsed,
        'date': dtStart.strftime('%d/%m/%Y'), # dd/mm/yyyy string
        'time': dtStart.strftime('%H:%M:%S'), # 24hour:min:seconds string
        'datetime ended':dtEnd.strftime('%d/%m/%Y %H:%M:%S')
    }
    with open('game_log.json','r') as fn:
        game_log = json.load(fn)
    game_log.append(gameInfo)

    with open('game_log.json','w') as fn:
        json.dump(game_log, fn, indent=4)
    
    while noOfAttempts - currAttempt: # ask user to play next attempt
        option = input(f'Enter [Y]es to play next game or [N] to quit: ').strip().upper()
        if option == 'N':
            return False # player exits between games
        elif option == 'Y':
            break
        else: 
            print('Please enter a valid input')    
    return True 

def hangmanSet(secretWord: str, setNo: int, wordMeaning: str,LifeLinesUsed:int):
    """ function to play a set of the hangman game

    Args:
        secretWord (str): word to be guessed
        setNo (int): set number
        wordMeaning (str): description of word to be guessed
        LifeLinesUsed (int): lifelines used so far in current game

    Raises:
        Exception: if player does not guess a single letter (length is not 1)
        Exception: player guess invalid character (numbers or special characters)

    Returns:
        int: scores earned by player in the set
        int: lifelines used in current game
    """
    # defining varibles for set
    revealedLetters, correctLetters,incorrectGuess = ' ', '',''
    # revealedLetters - letters guessed by player (contains space since player need not guess that)
    # correctLetters - all characters in secretWord
    # incorrectGuess - all wrong guesses by player
    score = 0
    showMean, showVowels = False, False # if these hints have been given this round

    for letter in secretWord:
        if not (letter in correctLetters or letter == ' '):
            correctLetters += letter
    if (len(secretWord) - secretWord.count(' ')) >= 10:
        diff = 'Complex' 
    else: 
        diff = 'Simple'

    # printing game info
    with open('hang.json','r') as fn:
        hang = json.load(fn) # contains different states of hangman
    while True:
        print('\nH A N G M A N\n', f'Attempt {currAttempt} of {noOfAttempts}',f'Player: {playerName}', f'Set {setNo} of {noOfWords}', sep='\n')
        print(hang[len(incorrectGuess)]) # print hangman in ascii
        print('Incorrect letters: ',end=' ')
        for letter in incorrectGuess: #print out correct guesses and blanks
            print(letter, end=' ')
        print( f'({len(incorrectGuess)})' )
        for letter in secretWord:
            if letter in revealedLetters:
                print(letter, end='')
            else: 
                print('_', end='')
        print('\n')
        
        if len(incorrectGuess) == 5 or (len(revealedLetters) - 1 == len(correctLetters) ): # end of set
            if len(incorrectGuess) == 5: # max guesses reached
                print('Maximum number of guesses!')
                print(f'After {len(incorrectGuess)} incorrect guesses and {len(revealedLetters)} correct guess(es), the word was \"{secretWord}\" ({diff}):', wordMeaning)
            else: # win
                print(f'Congratulations. The secret Word is \"{secretWord}\"({diff})', wordMeaning, sep=': ')
            break

        try: # set continues
            if showMean:
                print('Hint:', wordMeaning)
            if showVowels:
                print('Vowels revealed (a e i o u) ')
            print(f'You have {noOfLifeLines - LifeLinesUsed} remaining lifelines (lose {LifeLinesCost} points per use)')

            playerGuess = input('Select a valid character [a-z,\'] or \'0\' to use lifeline: ').strip().lower()
            # lifeline
            if playerGuess == '0' and noOfLifeLines - LifeLinesUsed: 
                print('\tChoose lifeline (enter nothing to not use lifeline)')
                if not showVowels:
                    print('\t1. Reveal hidden vowels in word')                    
                if not showMean:
                    print('\t2. Show word meaning')
                playerGuess = input('\t>>> ').strip()
                if not showVowels and playerGuess == '1':
                    vowels = 'aeiou'
                    for letter in vowels:
                        if letter in correctLetters:
                            if letter not in revealedLetters:
                                revealedLetters += letter
                    LifeLinesUsed = LifeLinesUsed + 1
                    showVowels = True
                    score -= 4
                elif not showMean and playerGuess == '2':
                    showMean = True
                    LifeLinesUsed = LifeLinesUsed + 1
                    score -= 4
            elif playerGuess == '0':
                print('Out of lifelines')
           
            # guessing processing
            elif len(playerGuess) != 1:
                raise Exception
            elif not (playerGuess.isalpha() or playerGuess == '\''):
                raise Exception
            else:
                if playerGuess in revealedLetters or playerGuess in incorrectGuess:
                    print('\nYou already tried this letter')
                elif showVowels and playerGuess in 'aeiou': # prevent player from guesing revealed vowels
                    print('\nYou already tried this letter')
                elif playerGuess in correctLetters:
                    revealedLetters += playerGuess
                    score += 2
                else: 
                    incorrectGuess += playerGuess
        except:
            print('\nPlease enter a valid character')
    print('*****')
    return score, LifeLinesUsed

# show top players
def showTopX():
    """import game logs file and show top X games with current number of sets per game (both specified in game settings)
    """
    with open('game_log.json','r') as fn:
        game_log = json.load(fn)
    game_logCurrSet = []
    for item in game_log:
        if item['sets played'] == noOfWords: # print out only top scorers of gaames with current sets no. 
            game_logCurrSet.append(item)
    topX = heapq.nlargest(noOfTop, game_logCurrSet, key=lambda x: x['score'], ) # sort by dictionary value 'score'
    if len(topX) == noOfTop:
        print(f'Showing top {noOfTop} players of {noOfWords}-set games')
    elif len(topX) == 0:
        print(f'There are no recorded games with {noOfWords}-set games')
        return
    else:
        print(f'Not enough players to show top {noOfTop} players for {noOfWords}-set games', f'Showing {len(topX)} players', sep='\n')
    print('Rank\tPlayer name\tScore\tComplex words\tLifelines used\tDate Played\t')
    for rank, item in enumerate(topX,1):
        print(rank, f'{item["name"]:<12}',item["score"],item['complex words'], '',item['lifelines used'],'',item['date'],sep='\t')
    
# additional feature 
def hallOfFrame():
    """function that generates players who have got max points without the use of a lifeline
    """
    with open('game_log.json','r') as fn:
        game_log = json.load(fn)
    hallofFrameName, hallOfFrameCount = [],[]
    for item in game_log:
        if item['score'] == item['sets played'] * 10 and item['lifelines used'] == 0:
            if item['name'] in hallofFrameName:
                hallOfFrameCount[hallofFrameName.index(item['name'])] += 1
            else:
                hallofFrameName.append(item['name'])
                hallOfFrameCount.append(1)
    if len(hallofFrameName):
        hallofFrameList = list(zip(hallofFrameName, hallOfFrameCount))
        hallofFrameList.sort(key= lambda x: x[1], reverse=True)
        print('These are a list of players who managed to score the max points for hangman while not using any lifelines')
        print('Rank\tPlayer name\tMax score games without lifelines')
        for i,info in list(enumerate(hallofFrameList,1)):
            print(i,f'{info[0]:<12}',info[1],sep='\t')
        
# ask for player name and lead to main menu
print('Welcome to hangman')
while True: 
    playerName = input('Please enter your name: ').strip()
    validChars = True
    for char in playerName:
        if not (char.isalpha() or char == '-' or char == '/'):
            validChars = False
    if not validChars:
        print('Use only valid characters for name (letters, - and /) ')
    elif len(playerName) != 0: # ensure player does not enter nothing
        break
    else:
        print('Please enter a name with characters')

# import and define game settings varibles
with open('game_settings.json','r') as fn:
    game_settings = json.load(fn)
noOfAttempts = game_settings["number of attempts"]
noOfWords = game_settings["number of words"]
noOfTop = game_settings["number of top players"]
noOfLifeLines = game_settings['number of lifelines']
LifeLinesCost = game_settings['lifeline cost']

maxPoints = noOfWords * 10
winningPoints = int(maxPoints / 2)
currAttempt = 0

# menu
while True:
    try:
        print(f'\nWhat would you like to do, {playerName}?')
        if noOfAttempts - currAttempt:
            print('1. Play Hangman')
        else:
            print('Out of attempts for hangman')
        print(f'2. View Top {noOfTop} Scores','3. View Hall of Fame','4. Quit',sep='\n')
        option = int(input('>>> '))
        if option == 1 and noOfAttempts - currAttempt:
            placeholderVar = " Hangman rules "
            print(f'{placeholderVar:*^30}')
            print(f'\t1. You can play up to {noOfAttempts - currAttempt} games of hangman',f'2. There will be {noOfWords} sets in a game', f'3. You may use up to {noOfLifeLines} lifelines per game to help you guess the word, but lose {LifeLinesCost} points for each use',f'4. Maxinum number of incorrect guesses per set is 5','5. 2 points will be awarded for each correct letter guessed',f'6. Maxminum points for {noOfWords} sets is {maxPoints}', f'7. You win if your points exceed {winningPoints}', '8. Have Fun!', sep='\n\t' )
            if (input('\nEnter [Y] to play or nothing to quit: ').upper().strip()) == 'Y':
                playGame = True
                while noOfAttempts - currAttempt and playGame: # playGame is the indicator if player is still playing
                    currAttempt += 1
                    playGame = hangman()
            else: print('Cancelled')
        elif option == 2:
            showTopX()
        elif option == 3:
            hallOfFrame()
        elif option == 4:
            print('Have a good day!')
            break
        else:
            print('Number not a valid option')
    except ValueError:
        print('Please enter a integer')
