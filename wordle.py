import pygame, random, sys, json


# Vi åbner en ord dump og laver en ordliste,
# hvorefter vi så i et for loop tjekker alle ord i filen.
# og appender ordet med nogle special chars fjernet

data = open('newdump.json', encoding = 'utf-8')
ord_list = []
for ord in data:
    ord_list.append(ord.replace('"', '').replace(',', '').replace('\n', '').upper())
secret_word = random.choice(ord_list)


#Initializere pygame og font
pygame.init()
pygame.font.init()


#Opretter et board, hvor der er 5 lister inde i en liste, med 5 tomme felter
board = [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "]]
# Mængden af gæt man har ud fra hvor mange lister/rows der er i boardet.
guess_amount = len(board)

# Opretter start variabler vi ændrer senere
turn = 0
letters = 0
game_over = False
guess = ''
correct = ''
won = False
lost = False
tidStart = 0
tid = tidStart
top_score = 0

# Opretter forskellige konstanter vi ikke ændrer i spillets forløb.
WINDOW = WIDTH, HEIGHT = 450,650
BOX_HEIGHT = 500
BOX_X_SIZE = WIDTH / 5 - 20
BOX_Y_SIZE = BOX_HEIGHT / guess_amount - 20
MARGIN_X = (WIDTH/5 - BOX_X_SIZE) / 2
MARGIN_Y = (BOX_HEIGHT / guess_amount)
FPS = 30
CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode(WINDOW)
ALPHABET = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z","Æ", "Ø", "Å"]

# Opretter farver og font til spillet
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
GRAY = (128,128,128)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

font = pygame.font.SysFont("letterhead", 52)
end_font = pygame.font.SysFont("letterhead", 42)


"""
def checks():
vi starter med at sætte globale variabler turn, letters, game_over, correct, så vi kan ændre dem i spillets forløb
vi laver for loop med et nested for loop som kører fra 0 til mængde af gæt og i nested fra 0,5
Vi tjekker om bogstavet secret_word[col] == brugerens 5 tegns gæt, ved at tjekke secret_word[col] på alle 5 tegn
Hvis et tegn er lig med secret_word[col] gør vi boksen grøn og så går til det næste tal i for loopet

ellers går vi videre og tjekker om board[row][col] altså de enkelte ord i gættet, om de er i secret_word
hvis ja så tegner vi dem gul og gå videre til næste tal, hvis nej tegner vi dem grå og går videre til næste tal
"""
def checks():
    global turn, letters, game_over, correct
    for col in range(0, guess_amount):
        for row in range(0, 5):
            if secret_word[col] == board[row][col] and turn > row:
                pygame.draw.rect(SCREEN, GREEN, [col*(WIDTH/5)+MARGIN_X, row*MARGIN_Y, BOX_X_SIZE, BOX_Y_SIZE],0,5)
                correct = ''.join(i for i in board[row])
                if secret_word == correct and turn > row:
                    game_over = True
            elif board[row][col] in secret_word and turn > row:
                pygame.draw.rect(SCREEN, YELLOW, [col*(WIDTH/5)+MARGIN_X, row*MARGIN_Y, BOX_X_SIZE, BOX_Y_SIZE],0,5)
            elif board[row][col] not in secret_word and turn>row:
                pygame.draw.rect(SCREEN, GRAY, [col*(WIDTH/5)+MARGIN_X, row*MARGIN_Y, BOX_X_SIZE, BOX_Y_SIZE],0,5)


"""
def draw_board():
Her tegner vi boardet, ved at først sætte turn og board some globals så vi kan ændre dem
Så tager vi for col in range af 0 til guess_amount og laver et nested for loop for row i range af 0 til 5

Her tegner vi kasser ud fra col*(skærmens brædde/5), og row*MARGIN_Y så kasserne bliver lavet på et row af 5 og col af 5 så vi får et 5*5 grid
Vi tegner også en outline med farven blå, på samme måde som de andre bokse, dog i stedet for at vi gange med row,
så ganger vi med turn så når vi trykker enter går den en række ned til hvor man skriver

Vi gemmer også en render_text variable hvor vi tjekker board[row][col] for at tjekke om der er andet end tomme strings
og så displayer vi texten inde i kasserne
"""
def draw_board():
    global turn, board
    for col in range(0, guess_amount):
        for row in range(0, 5):
            #Tegner kasserne
            pygame.draw.rect(SCREEN, BLACK, [col*(WIDTH/5)+MARGIN_X, row*MARGIN_Y, BOX_X_SIZE, BOX_Y_SIZE],3,5)
            #Highligter kasserne i farven blå så man kan se hvilken tur man er på
            pygame.draw.rect(SCREEN, BLUE, [col*(WIDTH/5)+MARGIN_X, turn*MARGIN_Y, BOX_X_SIZE, BOX_Y_SIZE],3,5)
            render_text = font.render(board[row][col], True, BLACK)
            SCREEN.blit(render_text, (col*(WIDTH/5)+BOX_X_SIZE*.45, row*MARGIN_Y+ BOX_Y_SIZE*.3))


"""
def write_letters():
Vi starer med at gøre letters, guess og board global så vi kan ændre dem i funktionen
så giver text værdien af event.unicode.upper() hvilket er ligger under pygames events,
og tager alle key pressed og giver char værdien i upper_case.

så tjekker vi om letters er mindre end 5 og and texten er i ALPHABET som er en liste af alfabetet
hvis ja så gemmer vi tegnet i variablen board[turn][letters] som er placeringen af hvor man er
så gemmer vi letters til at være += 1
og gemmer også texten i guess så vi senere kan tjekke om ordet findes i ordlisten
"""
def write_letters():
    global letters, guess, board
    text = event.unicode.upper()
    if letters < 5 and text in ALPHABET:
        board[turn][letters] = text
        letters += 1
        guess +=text

"""
def delete_letters():
Vi starter med at sætte letters, board og guess til globals
Så gemmer vi letters til at være -= 1 så vi er tilbage på placeringen hvor ordet vi fjerner er.
Så slicer guess til at være minus 1 fra det bagerste tegn.
Derfeter gemmer boardets[turn][letters] som er placeringen hvor vi er til at være en tom str så.
og til sidst tegner vi en kasse med samme farve blå over hvor vi er i forhold til placeringen så vi fjerner tegnet
"""
def delete_letters():
    global letters, board, guess
    letters-=1
    guess = guess[:-1]
    board[turn][letters] = ''
    pygame.draw.rect(SCREEN, BLUE, [letters*(WIDTH/5)+MARGIN_X, turn*MARGIN_Y, BOX_X_SIZE, BOX_Y_SIZE],3,5)

"""
def stats():
vi starter med at sætte top_score til global
Så tjekker vi om top_score er mindre end score() som er resultatet fra runden
hvis ja så giver vi top_score scoren man har fået i runden

så laver vi top_score text som vi derefter displayer
og hvis man vandt runden ved at gætte ordet, så laver vi en score_text og displayer også scoren man fik
"""
def stats():
    global top_score
    if top_score < score():
        top_score = score()
    text_topscore = end_font.render(f'Din highscore er: {top_score}', True, BLACK)
    SCREEN.blit(text_topscore, ((WIDTH-text_topscore.get_width())/2, HEIGHT/5))
    if won:
        text_score = end_font.render(f'Din score er: {score()}', True, BLACK)
        SCREEN.blit(text_score, ((WIDTH-text_score.get_width())/2, HEIGHT/4))

"""
def score():
vi starter med at tjekke om man har tabt
hvis ja så returnerer vi bare værdien 0
hvis nej så retunere vi int af 500-tiden man har brugt/ mængde af ture man har brugt
"""
def score():
    if lost:
        return 0
    return int((500-tid)/turn)

"""
def play_again
Vi starter med at fylde skærmen med farven hvid
Så laver vi en text variable som giver mulighed for at spille igen og displayer den
så kalder vi stats() funktionen

og hvis man har tabt så gemmer vi også secret_word i en variable og displayer det til brugeren
"""
def play_again():
    SCREEN.fill(WHITE)
    text = end_font.render('Tryk enter for at spille igen', True, BLACK)
    SCREEN.blit(text,((WIDTH-text.get_width())/2, HEIGHT/2))
    stats()
    if lost:
        word_text = end_font.render(f'Ordet var: {secret_word}', True, BLACK)
        SCREEN.blit(word_text,((WIDTH-word_text.get_width())/2, HEIGHT/3))


while True:
    # Vi sætter fps til en fast værdi på 30
    CLOCK.tick(FPS)
    # Updater pygame displayet
    pygame.display.flip()

    #Tjekker om game_over er false hvis ja kør nedenstående kode
    if not game_over:
        # Holder styr på sekundter gået, ved at sig += 1/FPS da fps er capped og programmet kører det antal gange i sekundet
        tid += tidStart + 1/FPS
        # Variable for tid text som vi kan display
        tid_text = end_font.render(f'Tid: {int(tid)}', True, BLACK)
        # Variable for tur text som vi kan display
        turn_text = end_font.render(f'Tur: {turn+1}', True, BLACK)
        # Fylder skærmen hvis
        SCREEN.fill(WHITE)
        # Kalder checks() funktion
        checks()
        # Kalder draw_board() funktion
        draw_board()
        # Displayer tid text
        SCREEN.blit(tid_text,(WIDTH-tid_text.get_width(), HEIGHT-50))
        # Displayer tur text
        SCREEN.blit(turn_text,(0, HEIGHT-50))
        # Tjekker for alle pygame events der sker
        for event in pygame.event.get():
            # Hvis event er quit så lukker vi programmet ordenligt for sikkerheds skyld
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Hvis eventet er Keydown holder styr på alle taster der bliver trykket af brugeren
            if event.type == pygame.KEYDOWN:
                # Hvis key er enter og letters == 5 og tur er mindre end el lig med 5 og guess er i ordlisten
                if event.key == pygame.K_RETURN and letters == 5 and turn <= 5 and guess in ord_list:
                    # Gem variable guess som en tom str
                    guess = ''
                    # Gå til næste tur
                    turn += 1
                    # Sæt letters til nul da der ikke skal være nogle
                    letters = 0
                    # Hvis turen er 5 or det correct gæt ikke er secret_word
                    if turn == 5 and correct != secret_word:
                        # Sæt spillet til tabt og kør play_again() funktionen
                        lost = True
                        game_over = True
                        play_again()
                # Hvis key er backspace og letters er størrer end 0 kør delete_letters() funktionen
                if event.key == pygame.K_BACKSPACE and letters > 0:
                    delete_letters()
                else:
                    #Ellers hvis det er hvilken som helst anden key kør write_letters() funktionen
                    write_letters()
    # Hvis game_over er true
    else:
        #Tjek om man ikke har tabt
        if not lost:
            #hvis ja sæt won til true
            won = True
        # Ellers kør play_again() funktionen
        play_again()
        #Tjek for alle events i pygame events
        for event in pygame.event.get():
            # Hvis event er quit så lukker vi programmet ordenligt for sikkerheds skyld
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                #Hvis man trykker enter resetter vi alle variabler og resetter spillet ved at sige game_over = False
                if event.key == pygame.K_RETURN:
                    lost, won = False, False
                    secret_word = random.choice(ord_list).replace('"', '').replace(',', '').replace('\n', '').upper()
                    board = [[" ", " ", " ", " ", " "],
                             [" ", " ", " ", " ", " "],
                             [" ", " ", " ", " ", " "],
                             [" ", " ", " ", " ", " "],
                             [" ", " ", " ", " ", " "],
                             [" ", " ", " ", " ", " "]]

                    turn = 0
                    letters = 0
                    guess = ''
                    tid = 0
                    called = 0
                    game_over = False
