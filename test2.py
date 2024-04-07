import pygame
import string
import random
import time
import math

pygame.init()


# Classes
class PlayerHand:
    def __init__(self, last_change, hand_letter, current_letter, last_letter):
        self.last_change = last_change
        self.hand_letter = hand_letter
        self.current_letter = current_letter
        self.last_letter = last_letter

    def update(self):
        if self.current_letter != self.last_letter:
            self.last_change = time.time()
            self.hand_letter = ""
            self.last_letter = self.current_letter

        if time.time() - self.last_change >= 1:
            self.hand_letter = self.current_letter


class FallingSign:
    def __init__(self, speed, x, y, sprite):
        self.speed = speed
        self.x = x
        self.y = y
        self.sprite = sprite

    def update(self):
        self.y += self.speed


# Functions
def is_mouse_hover(mouse_position, button):
    confirm = False
    if button.x + button.width >= mouse_position[0] >= button.x and \
            button.y <= mouse_position[1] <= button.y + button.height:
        confirm = True
    return confirm


def create_button(text, coordinates, text_font, color):
    temp_font = text_font.render(text, True, color)
    temp_rect = temp_font.get_rect()
    temp_rect.center = coordinates
    return temp_font, temp_rect


# Color settings
colorDark = (0, 120, 255)
colorLight = (0, 200, 255)

# Screen settings
screenHeight = 620
screenWidth = 900

# Init
Player = PlayerHand(time.time(), "", "", "")
surface = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Sign Game Screen")
clock = pygame.time.Clock()
ongoing = True
letters = list(string.ascii_lowercase)
freezeDict = {"practiceDoing": False, "practiceRecognize": False, "test": False, "endless": False, "minigames": False}
playerInputFreeze = False
currentLetter = ""

# Font and Text for title screen
font = pygame.font.Font('Lato-Regular.ttf', 48)
font2 = pygame.font.Font('Lato-Regular.ttf', 36)
title = font.render("Learn your signs!", True, "black")
titleRect = title.get_rect()
titleRect.center = (screenWidth / 2, 50)
practiceButtonText, practiceButton = create_button("Calm Practice", (screenWidth / 2, 200), font2, "blue")
testButtonText, testButton = create_button("Test your knowledge", (screenWidth / 2, 300), font2, "blue")
endlessModeText, endlessModeButton = create_button("Endless Mode", (screenWidth / 2, 400), font2, "blue")
minigamesText, minigamesButton = create_button("Minigames!(VIP only)", (screenWidth / 2, 500), font2, "blue")
titleScreenButtonsList = [practiceButton, testButton, endlessModeButton, minigamesButton]

# Font and Text for practice screen
font3 = pygame.font.Font('Lato-Regular.ttf', 25)
practiceScoreText = font3.render("Correct: 0       Incorrect: 0       Accuracy: 0%", True, "black")
practiceScoreRect = practiceScoreText.get_rect()
practiceScoreRect.topleft = (10, 10)
practiceLetterIndex = random.randrange(0, 24)
practiceDoingIndex = random.randrange(0, 24)
practiceQuestion, practiceQuestionRect = create_button("What sign is this?", (700, 200), font2, "black")
thickUnderscore = pygame.image.load("thick_underline.png")
practiceCorrectAnswer = font3.render("The correct answer was: ", True, "black")
practiceNextText, practiceNextBox = create_button("Next", (900, 620), font2, "black")
practiceNextBox.topleft = (practiceNextBox.x - practiceNextBox.width / 2,
                           practiceNextBox.y - practiceNextBox.height / 2)
practiceBackText, practiceBackBox = create_button("Back", (900, 0), font2, "black")
practiceBackBox.topleft = (practiceBackBox.x - practiceBackBox.width / 2,
                           practiceBackBox.y + practiceBackBox.height / 2)
practiceResetText, practiceResetBox = create_button("Reset record", (100, 600), font2, "black")
practiceRecogniseSelectionText, practiceRecogniseSelectionBox = create_button("Recognize Hand Signs!",
                                                                              (screenWidth / 2, 250), font2, "blue")
practiceDoingSelectionText, practiceDoingSelectionBox = create_button("Practice Doing Signs!",
                                                                      (screenWidth / 2, 400), font2, "blue")
practiceDoingCongratulationsText, practiceDoingCongratulationsBox = create_button("You got it correct!",
                                                                                  (200, 250), font2, "Dark Green")
practiceDoingNextText, practiceDoingNextBox = create_button("Continue!", (200, 400), font2, "black")

# Setting sign sprites
letterDict = {}
letterList = []
miniLettersList = []
for letter in letters:
    if letter == "j" or letter == "z":
        continue
    letterDict[letter] = pygame.image.load("signs/" + letter + ".png")
    letterList.append(pygame.image.load("signs/" + letter + ".png"))
for miniLetter in letterList:
    miniLettersList.append(pygame.transform.scale(miniLetter, (round(miniLetter.get_rect().width * 0.4),
                                                               round(miniLetter.get_rect().height * 0.4))))

# Screen variables
titleScreen = True
practiceScreen = False
testScreen = False
endlessScreen = False
minigameScreen = False
clicked = False

# Practice variables
practiceRecognise = False
practiceSigns = False
enter = False
practiceCorrectAnswerShow = False
practiceDoingCorrectShow = False
practiceC = 0
practiceI = 0
practiceC2 = 0
practiceI2 = 0
practiceHintCounter = 0
practiceDoingQuestionText, practiceDoingQuestionBox = create_button("Perform the sign for the following letter: " +
                                                                    list(letterDict.keys())[practiceDoingIndex],
                                                                    (screenWidth / 2, 50), font2, "black")
practiceDoingHintText, practiceDoingHintBox = create_button("Hint", (700, 150), font2, "black")

# Test variables
testReviewCounter = 0
testSubmit = False
testQuestionSigns = []
testPlayerAnswers = []
testQuestionCounter = 1
testQuestionIndex = random.randrange(0, 24)
testCheckList = []
while True:
    if letterList[testQuestionIndex] not in testQuestionSigns:
        testQuestionSigns.append(letterList[testQuestionIndex])
        testPlayerAnswers.append("")
        testCheckList.append(testQuestionIndex)
    if len(testQuestionSigns) >= 20:
        break
    testQuestionIndex = random.randrange(0, 24)

# Test Sprites and Fonts
testQuestionText, testQuestionBox = create_button("Question " + str(testQuestionCounter) + ":",
                                                  (100, 30), font2, "black")
testNextText, testNextBox = create_button("Next Question", (750, 550), font2, "blue")
testPreviousText, testPreviousBox = create_button("Previous Question", (150, 550), font2, "blue")
testPreviousBox.topleft = (0, screenHeight - testPreviousBox.height)
testNextBox.topleft = (screenWidth - testNextBox.width, screenHeight - testNextBox.height)
testReviewNextText, testReviewNextBox = create_button(">", (0, screenHeight / 2), font, "black")
testReviewNextBox.midright = (screenWidth, screenHeight / 2)
testReviewBackText, testReviewBackBox = create_button("<", (screenWidth, screenHeight / 2), font, "black")
testReviewBackBox.midleft = (0, screenHeight / 2)

# Endless Sprites and Fonts
endlessCountdownTimer = 3
endlessStart = time.time()
endlessCountdownSprite = font3.render(str(math.ceil(endlessCountdownTimer - endlessStart)), True, "black")

# Endless Variables

# Game Loop
while ongoing:

    # Background
    surface.fill((188, 233, 237))

    # Input detection(should be replaced by camera)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ongoing = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        if playerInputFreeze:
            continue
        if event.type == pygame.KEYDOWN and (pygame.key.name(event.key) in letters):
            currentSign = pygame.key.name(event.key)
            Player.current_letter = currentSign
            Player.update()
            currentLetter = pygame.key.name(event.key)
        if event.type == pygame.KEYDOWN and (pygame.key.name(event.key) == "return"):
            enter = True
        if event.type == pygame.KEYUP:
            Player.current_letter = ""
            Player.update()
    Player.update()
    mousePos = pygame.mouse.get_pos()

    # Title screen code
    if titleScreen:
        # Title screen background
        surface.blit(pygame.transform.rotate(miniLettersList[3], 45), (20, 100))
        surface.blit(pygame.transform.rotate(miniLettersList[16], 340), (140, 350))
        surface.blit(pygame.transform.rotate(miniLettersList[9], 190), (650, 75))
        surface.blit(pygame.transform.rotate(miniLettersList[0], 0), (730, 450))
        surface.blit(pygame.transform.rotate(miniLettersList[14], 0), (750, 280))
        # Title screen sprites
        for selectButton in titleScreenButtonsList:
            if is_mouse_hover(mousePos, selectButton):
                if clicked:
                    titleScreenButtonsList = [practiceButton, testButton, endlessModeButton, minigamesButton]
                    if selectButton == practiceButton:
                        titleScreen = False
                        practiceScreen = True
                        testScreen = False
                        endlessScreen = False
                        minigameScreen = False
                    elif selectButton == testButton:
                        titleScreen = False
                        practiceScreen = False
                        testScreen = True
                        endlessScreen = False
                        minigameScreen = False
                        currentLetter = ""
                    elif selectButton == endlessModeButton:
                        titleScreen = False
                        practiceScreen = False
                        testScreen = False
                        endlessScreen = True
                        minigameScreen = False
                        endlessStart = time.time()
                    else:
                        titleScreen = False
                        practiceScreen = False
                        testScreen = False
                        endlessScreen = False
                        minigameScreen = True
                pygame.draw.rect(surface, colorLight, selectButton)
            else:
                pygame.draw.rect(surface, colorDark, selectButton)
        surface.blit(practiceButtonText, practiceButton)
        surface.blit(testButtonText, testButton)
        surface.blit(endlessModeText, endlessModeButton)
        surface.blit(minigamesText, minigamesButton)
        surface.blit(title, titleRect)

    # Practice Screen
    if practiceScreen:
        # Options picking
        if not practiceRecognise and not practiceSigns:
            if is_mouse_hover(mousePos, practiceRecogniseSelectionBox):
                pygame.draw.rect(surface, colorLight, practiceRecogniseSelectionBox)
                if clicked:
                    practiceSigns = False
                    practiceRecognise = True
            else:
                pygame.draw.rect(surface, colorDark, practiceRecogniseSelectionBox)

            if is_mouse_hover(mousePos, practiceDoingSelectionBox):
                pygame.draw.rect(surface, colorLight, practiceDoingSelectionBox)
                if clicked:
                    practiceSigns = True
                    practiceRecognise = False
            else:
                pygame.draw.rect(surface, colorDark, practiceDoingSelectionBox)
            surface.blit(practiceRecogniseSelectionText, practiceRecogniseSelectionBox)
            surface.blit(practiceDoingSelectionText, practiceDoingSelectionBox)

        # Practice doing the hand signs
        if practiceSigns:

            # Back Button and Hint Button
            if is_mouse_hover(mousePos, practiceBackBox):
                pygame.draw.rect(surface, colorLight, practiceBackBox)
                if clicked:
                    titleScreen = True
                    practiceScreen = False
                    testScreen = False
                    endlessScreen = False
                    minigameScreen = False
                    practiceRecognise = False
                    practiceSigns = False
            else:
                pygame.draw.rect(surface, colorDark, practiceBackBox)

            if is_mouse_hover(mousePos, practiceDoingHintBox):
                pygame.draw.rect(surface, colorLight, practiceDoingHintBox)
                if clicked:
                    if practiceHintCounter <= 3:
                        practiceHintCounter += 1
            else:
                pygame.draw.rect(surface, colorDark, practiceDoingHintBox)

            # Questions and Text Blit
            surface.blit(practiceBackText, practiceBackBox)
            surface.blit(practiceDoingQuestionText, practiceDoingQuestionBox)
            surface.blit(practiceDoingHintText, practiceDoingHintBox)

            # Hint Blit
            tempHintImage = letterDict[list(letterDict.keys())[practiceDoingIndex]]
            if practiceHintCounter >= 3:
                surface.blit(tempHintImage, (590, 200))
            elif 0 < practiceHintCounter < 3:
                blurPower = 5 * (3 - practiceHintCounter)
                tempHintImage = pygame.transform.scale(tempHintImage, (tempHintImage.get_height() / blurPower,
                                                                       tempHintImage.get_width() / blurPower))
                tempHintImage = pygame.transform.scale(tempHintImage, (tempHintImage.get_height() * blurPower,
                                                                       tempHintImage.get_width() * blurPower))
                surface.blit(tempHintImage, (590, 200))
            if Player.hand_letter == list(letterDict.keys())[practiceDoingIndex]:
                practiceDoingCorrectShow = True
                freezeDict["practiceDoing"] = True

            # Checking Answers
            if practiceDoingCorrectShow:
                if is_mouse_hover(mousePos, practiceDoingNextBox):
                    pygame.draw.rect(surface, colorLight, practiceDoingNextBox)
                    if clicked:
                        practiceDoingIndex = random.randrange(0, 24)
                        freezeDict["practiceDoing"] = False
                        practiceHintCounter = 0
                        practiceDoingCorrectShow = False
                        practiceDoingQuestionText, practiceDoingQuestionBox = create_button(
                            "Perform the sign for the following letter: " +
                            list(letterDict.keys())[practiceDoingIndex],
                            (screenWidth / 2, 50), font2, "black")

                else:
                    pygame.draw.rect(surface, colorDark, practiceDoingNextBox)
                surface.blit(practiceDoingCongratulationsText, practiceDoingCongratulationsBox)
                surface.blit(practiceDoingNextText, practiceDoingNextBox)
        # Practice recognising hand signs
        if practiceRecognise:
            # Back Button and Reset Button
            if is_mouse_hover(mousePos, practiceBackBox):
                pygame.draw.rect(surface, colorLight, practiceBackBox)
                if clicked:
                    titleScreen = True
                    practiceScreen = False
                    testScreen = False
                    endlessScreen = False
                    minigameScreen = False
                    practiceRecognise = False
                    practiceSigns = False
            else:
                pygame.draw.rect(surface, colorDark, practiceBackBox)

            if is_mouse_hover(mousePos, practiceResetBox):
                pygame.draw.rect(surface, colorLight, practiceResetBox)
                if clicked:
                    practiceI = 0
                    practiceC = 0
                    practiceScoreText = font3.render("Correct: 0       Incorrect: 0       Accuracy: 0%", True, "black")
            else:
                pygame.draw.rect(surface, colorDark, practiceResetBox)

            surface.blit(practiceBackText, practiceBackBox)
            surface.blit(practiceResetText, practiceResetBox)
            # Showing sign image
            tempLetter = letterList[practiceLetterIndex].get_rect()
            tempLetter.center = (10, 50)
            surface.blit(practiceScoreText, practiceScoreRect)
            surface.blit(pygame.transform.scale(letterList[practiceLetterIndex],
                                                (tempLetter.width * 1.6, tempLetter.height * 1.6)), tempLetter.center)
            surface.blit(practiceQuestion, practiceQuestionRect)
            surface.blit(thickUnderscore, (700 - (practiceQuestionRect.width / 4), 350))

            # Checking answer
            if currentLetter in letters:
                tempPlayerInput = font.render(currentLetter, True, "black")
                tempPlayerInputBox = tempPlayerInput.get_rect()
                tempPlayerInputBox.center = (700 - (practiceQuestionRect.width / 4) +
                                             thickUnderscore.get_rect().width / 2, 320)
                surface.blit(tempPlayerInput, tempPlayerInputBox)
            if enter and currentLetter in letters:
                practiceCorrectAnswerShow = False
                if currentLetter == "j" or currentLetter == "z":
                    practiceI += 1
                    practiceScoreText = font3.render(f"Correct: {practiceC}       Incorrect: {practiceI}       "
                                                     f"Accuracy: {round((practiceC / (practiceI + practiceC)) * 100)}%",
                                                     True, "black")
                    enter = False
                    practiceCorrectAnswerShow = True
                elif str(letterDict[currentLetter]) == str(letterList[practiceLetterIndex]):
                    practiceC += 1
                    practiceScoreText = font3.render(f"Correct: {practiceC}       Incorrect: {practiceI}       "
                                                     f"Accuracy: {round((practiceC / (practiceI + practiceC)) * 100)}%",
                                                     True, "black")
                    enter = False
                    practiceCorrectAnswerShow = True
                else:
                    practiceI += 1
                    practiceScoreText = font3.render(f"Correct: {practiceC}       Incorrect: {practiceI}       "
                                                     f"Accuracy: {round((practiceC / (practiceI + practiceC)) * 100)}%",
                                                     True, "black")
                    enter = False
                    practiceCorrectAnswerShow = True

            # Practice output
            if practiceCorrectAnswerShow:
                freezeDict["practiceRecognize"] = True
                if currentLetter != "z" and currentLetter != "j" and currentLetter != "":
                    if str(letterDict[currentLetter]) == str(letterList[practiceLetterIndex]):
                        practiceCorrectAnswer = font3.render("Correct!", True, "black")
                    else:
                        practiceCorrectAnswer = font3.render(f"The correct answer was: "
                                                             f"{list(letterDict.keys())[practiceLetterIndex]}",
                                                             True, "black")
                else:
                    practiceCorrectAnswer = font3.render(f"The correct answer was: "
                                                         f"{list(letterDict.keys())[practiceLetterIndex]}",
                                                         True, "black")
                if is_mouse_hover(mousePos, practiceNextBox):
                    pygame.draw.rect(surface, colorLight, practiceNextBox)
                    if clicked:
                        practiceCorrectAnswerShow = False
                        practiceLetterIndex = random.randrange(0, 24)
                        currentLetter = ""
                        enter = False
                        freezeDict["practiceRecognize"] = False
                else:
                    pygame.draw.rect(surface, colorDark, practiceNextBox)
                surface.blit(practiceCorrectAnswer, (practiceQuestionRect.x - 10, 430))
                surface.blit(practiceNextText, practiceNextBox)

    # Test Screen
    if testScreen:

        # Testing
        if not testSubmit:
            if is_mouse_hover(mousePos, testNextBox):
                if clicked:
                    if testQuestionCounter >= 20:
                        testPlayerAnswers[testQuestionCounter - 1] = currentLetter
                        testSubmit = True
                        freezeDict["test"] = True
                        continue
                    if testQuestionCounter < 20:
                        testPlayerAnswers[testQuestionCounter - 1] = currentLetter
                        testQuestionCounter += 1
                        currentLetter = testPlayerAnswers[testQuestionCounter - 1]
                if testQuestionCounter < 20:
                    testQuestionText, testQuestionBox = create_button("Question " + str(testQuestionCounter) + ":",
                                                                      (100, 30), font2, "black")
                elif testQuestionCounter >= 20:
                    testQuestionText, testQuestionBox = create_button("Question " + str(testQuestionCounter) + ":",
                                                                      (100, 30), font2, "black")
                    testNextText, testNextBox = create_button("Submit", (750, 550), font2, "blue")
                    testNextBox.topleft = (screenWidth - testNextBox.width, screenHeight - testNextBox.height)
                pygame.draw.rect(surface, colorLight, testNextBox)
            else:
                pygame.draw.rect(surface, colorDark, testNextBox)
            if is_mouse_hover(mousePos, testPreviousBox):
                if clicked:
                    if testQuestionCounter > 1:
                        testPlayerAnswers[testQuestionCounter - 1] = currentLetter
                        if testQuestionCounter >= 20:
                            testNextText, testNextBox = create_button("Next Question", (750, 550), font2, "blue")
                            testNextBox.topleft = (screenWidth - testNextBox.width, screenHeight - testNextBox.height)
                        testQuestionCounter -= 1
                        currentLetter = testPlayerAnswers[testQuestionCounter - 1]

                    testQuestionText, testQuestionBox = create_button("Question " + str(testQuestionCounter) + ":",
                                                                      (100, 30), font2, "black")
                if testQuestionCounter > 1:
                    pygame.draw.rect(surface, colorLight, testPreviousBox)
            else:
                if testQuestionCounter > 1:
                    pygame.draw.rect(surface, colorDark, testPreviousBox)
            surface.blit(practiceQuestion, practiceQuestionRect)
            surface.blit(thickUnderscore, (700 - (practiceQuestionRect.width / 4), 350))
            if currentLetter in letters:
                tempTestPlayerInput = font.render(currentLetter, True, "black")
                tempTestPlayerInputBox = tempTestPlayerInput.get_rect()
                tempTestPlayerInputBox.center = (700 - (practiceQuestionRect.width / 4) +
                                                 thickUnderscore.get_rect().width / 2, 320)
                surface.blit(tempTestPlayerInput, tempTestPlayerInputBox)
            tempTestQuestionCurrent = testQuestionSigns[testQuestionCounter - 1]
            tempTestQuestionCurrentBox = tempTestQuestionCurrent.get_rect()
            tempTestQuestionCurrentBox.center = (10, 50)
            surface.blit(pygame.transform.scale(tempTestQuestionCurrent,
                                                (tempTestQuestionCurrent.get_rect().width * 1.6,
                                                 tempTestQuestionCurrent.get_rect().height * 1.6)), (10, 50))
            surface.blit(testQuestionText, testQuestionBox)
            surface.blit(testNextText, testNextBox)
            if testQuestionCounter > 1:
                surface.blit(testPreviousText, testPreviousBox)

        # Results Screen
        if testSubmit:
            if is_mouse_hover(mousePos, practiceBackBox):
                pygame.draw.rect(surface, colorLight, practiceBackBox)
                if clicked:
                    titleScreen = True
                    practiceScreen = False
                    testScreen = False
                    endlessScreen = False
                    minigameScreen = False
                    practiceRecognise = False
                    practiceSigns = False
                    testSubmit = False
                    freezeDict["test"] = False
                    testQuestionSigns = []
                    testPlayerAnswers = []
                    testCheckList = []
                    testQuestionCounter = 1
                    testQuestionIndex = random.randrange(0, 24)
                    currentLetter = ""
                    while True:
                        if letterList[testQuestionIndex] not in testQuestionSigns:
                            testQuestionSigns.append(letterList[testQuestionIndex])
                            testPlayerAnswers.append("")
                            testCheckList.append(testQuestionIndex)
                        if len(testQuestionSigns) >= 20:
                            break
                        testQuestionIndex = random.randrange(0, 24)
                    testQuestionText, testQuestionBox = create_button("Question " + str(testQuestionCounter) + ":",
                                                                      (100, 30), font2, "black")
                    testNextText, testNextBox = create_button("Next Question", (750, 550), font2, "blue")
                    testPreviousText, testPreviousBox = create_button("Previous Question", (150, 550), font2, "blue")
                    testPreviousBox.topleft = (0, screenHeight - testPreviousBox.height)
                    testNextBox.topleft = (screenWidth - testNextBox.width, screenHeight - testNextBox.height)
            else:
                pygame.draw.rect(surface, colorDark, practiceBackBox)
            if is_mouse_hover(mousePos, testReviewNextBox):
                pygame.draw.rect(surface, colorLight, testReviewNextBox)
                if clicked:
                    testReviewCounter += 1
                    if testReviewCounter >= 20:
                        testReviewCounter = 0
            else:
                pygame.draw.rect(surface, colorDark, testReviewNextBox)
            if is_mouse_hover(mousePos, testReviewBackBox):
                pygame.draw.rect(surface, colorLight, testReviewBackBox)
                if clicked:
                    testReviewCounter -= 1
                    if testReviewCounter < 0:
                        testReviewCounter = 19
            else:
                pygame.draw.rect(surface, colorDark, testReviewBackBox)
            testIncorrect = 0
            testCorrect = 0
            reviewGuide = []
            for answer in testPlayerAnswers:
                if answer == "":
                    testIncorrect += 1
                    reviewGuide.append(False)
                elif str(letterDict[answer]) != str(testQuestionSigns[testCorrect + testIncorrect]):
                    testIncorrect += 1
                    reviewGuide.append(False)
                else:
                    testCorrect += 1
                    reviewGuide.append(True)
            testScoreReveal = "You got a " + str(testCorrect) + " out of " + str(testCorrect + testIncorrect)
            testScoreText, testScoreBox = create_button(testScoreReveal, (50, 50), font2, "black")
            testScoreBox.topleft = (20, 20)
            surface.blit(testScoreText, testScoreBox)
            surface.blit(practiceBackText, practiceBackBox)
            surface.blit(testReviewNextText, testReviewNextBox)
            surface.blit(testReviewBackText, testReviewBackBox)
            testReviewQuestion = font2.render("Question " + str(testReviewCounter + 1), True, "black")
            if reviewGuide[testReviewCounter]:
                testAnswerText = font2.render("You got it correct!", True, "black")
            elif testPlayerAnswers[testReviewCounter] == "":
                testAnswerText = font2.render("You did not answer this question.", True, "black")
            else:
                testAnswerText = font3.render("You got this incorrect. You chose " +
                                              str(testPlayerAnswers[testReviewCounter]) +
                                              " but the correct answer was " +
                                              list(letterDict.keys())[testCheckList[testReviewCounter]] + ".",
                                              True, "black")
            testAnswerTextBox = testAnswerText.get_rect()
            testAnswerTextBox.center = (screenWidth / 2, screenHeight - 50)
            testReviewQuestionBox = testReviewQuestion.get_rect()
            testReviewQuestionBox.center = (screenWidth / 2, 90)
            surface.blit(testReviewQuestion, testReviewQuestionBox)
            surface.blit(testAnswerText, testAnswerTextBox)
            surface.blit(testQuestionSigns[testReviewCounter], ((screenWidth / 2) - 60, 150))

    # Endless Screen
    if endlessScreen:
        if time.time() - endlessStart < endlessCountdownTimer:
            print(endlessCountdownTimer - endlessStart)
            endlessCountdownSprite = font.render(str(math.ceil(3 - (time.time() - endlessStart))),
                                                 True, "black")
            surface.blit(endlessCountdownSprite, (screenWidth / 2, screenHeight / 2))
    if minigameScreen:
        print("minigames")
    if practiceRecognise and freezeDict["practiceRecognize"]:
        playerInputFreeze = True
    elif practiceSigns and freezeDict["practiceDoing"]:
        playerInputFreeze = True
    elif testScreen and freezeDict["test"]:
        playerInputFreeze = True
    elif endlessScreen and freezeDict["endless"]:
        playerInputFreeze = True
    elif minigameScreen and freezeDict["minigames"]:
        playerInputFreeze = True
    else:
        playerInputFreeze = False
    clicked = False
    pygame.display.update()
    clock.tick(60)
