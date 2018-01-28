# Load library 
# Braille Library
import louis



CONST_DOTCODE = ['','2-3-4-6','5','3-4-5-6','1-2-4-6','1-4-6','1-2-3-4-6','3','1-2-3-5-6','2-3-4-5-6','1-6','3-4-6','6','3-6','4-6',
            '3-4','3-5-6','2','2-3','2-5','2-5-6','2-6','2-3-5','2-3-5-6','2-3-6','3-5','1-5-6','5-6','1-2-6','1-2-3-4-5-6',
            '3-4-5','1-4-5-6','4','1','1-2','1-4','1-4-5','1-5','1-2-4','1-2-4-5','1-2-5','2-4','2-4-5','1-3','1-2-3','1-3-4',
            '1-3-4-5','1-3-5','1-2-3-4','1-2-3-4-5','1-2-3-5','2-3-4','2-3-4-5','1-3-6','1-2-3-6','2-4-5-6','1-3-4-6','1-3-4-5-6',
            '1-3-5-6','2-4-6','1-2-5-6','1-2-4-5-6','4-5','4-5-6']

CONST_BRAILLES = ['⠀','⠮','⠐','⠼','⠫','⠩','⠯','⠄','⠷','⠾','⠡','⠬','⠠','⠤','⠨','⠌','⠴','⠂','⠆','⠒','⠲','⠢',
            '⠖','⠶','⠦','⠔','⠱','⠰','⠣','⠿','⠜','⠹','⠈','⠁','⠃','⠉','⠙','⠑','⠋','⠛','⠓','⠊','⠚','⠅',
'⠇','⠍','⠝','⠕','⠏','⠟','⠗','⠎','⠞','⠥','⠧','⠺','⠭','⠽','⠵','⠪','⠳','⠻','⠘','⠸']

# Given a string it return the braille mapping
def convertStringToCor(words):

	# Convert the sentence via grade 2 into dot representation
	# Set mode to ucBrl + dot
    
    print("Converting the image to words... \n" + words + "\n")

    asciiSymbols = louis.translate(['en-us-g2.ctb'],  words, mode=132)[0]
    returnArray = []

    print("Resulting Braille of the image : \n" + asciiSymbols + "\n")

    for character in asciiSymbols:
        
        returnArray.append(CONST_DOTCODE[CONST_BRAILLES.index(character)])

    return returnArray
