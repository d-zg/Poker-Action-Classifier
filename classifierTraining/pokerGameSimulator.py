import csv
from queue import Queue
from typing import List, Dict
from pokerface import *
from csv import *
from loadModel import *

class Game:
    # def __new__(cls):
    #     if not hasattr(cls, 'instance'):
    #         cls.instance = super(Game, cls).__new__(cls)
    #     return cls.instance
    def __init__(self, big_blind, small_blind, players):
        self.big_blind: int = big_blind
        self.small_blind: int = small_blind
        self.allPlayers : Dict[str, Player] = [player.id for player in players]
        for player in players:
            player.currentGame = self
        self.runningEventLoop : bool = True
        self.dealer = Dealer(players, big_blind, small_blind)
        self.history = Queue()
        self.bankruptPlayers = []
    def registerPlayer(self, newPlayer):
        if (not newPlayer.id in self.allPlayers):
            self.allPlayers.append(newPlayer)
            self.dealer.players.append(newPlayer)
            newPlayer.enterGame(self)
        else:
            print("\nError, player already registered.")
    def removePlayer(self, id):
        self.allPlayers[id].leaveGame
        del self.allPlayers[id]
    def __runEventLoop(self):
        while (self.runningEventLoop):
            for player in self.allPlayers.values():
                # get the state of the game and possible actions from dealer
                state = self.dealer.getState() 
                # pass in that state to player, prompt with appropriate possible actions
                # create the appropriate command, and attach it to this game
                command = player.getAction(self, state) 
                # then execute the command, updating the game state
                command.execute() 
    def foldPlayer(self, player):
        self.dealer.foldPlayer(player)
        self.history.put("Player " + player.id + " folded.")
        player.lastAction = "Fold"
    def raisePlayer(self, player, raiseAmount):
        self.dealer.raisePlayer(player, int(raiseAmount))
        self.history.put("Player " + player.id + " raised.")
        player.lastAction = "Raise"
    def raisePlayerThird(self, player):
        self.dealer.raisePlayer(player, self.dealer.pot/3)
        self.history.put("Player " + player.id + " raised 1/3rd of the pot.")
        player.lastAction = "Raise third pot"
    def raisePlayerPot(self, player):
        self.dealer.raisePlayer(player, self.dealer.pot)
        self.history.put("Player " + player.id + " raised by the pot size.")
        player.lastAction = "Raise pot"
    def raisePlayerAllIn(self, player):
        self.dealer.raisePlayer(player, player.stack)
        self.history.put("Player " + player.id + " raised all in.")
        player.lastAction = "All in"
    def checkPlayer(self, player):
        self.dealer.checkPlayer(player)
        self.history.put("Player " + player.id + " checked.")
        player.lastAction = "Check"
    def callPlayer(self, player):
        self.dealer.callPlayer(player)
        self.history.put("Player " + player.id + " called.")
        player.lastAction = "Call"
    def getEquity(self, player):
        self.dealer.getPlayerEquity(player)


class Player:
    def __init__(self, stack, id):
        self.stack: int = stack
        self.id: str = id
        self.currentBet : int = 0
        self.currentGame : Game = None
        self.hand = []
        self.lastAction = None
    def enterGame(self, instance):
        self.currentGame = instance
        # print some recognition that you were entered into this game
    def leaveGame(self):
        self.currentGame = None
    def getAction(self, pot, highestBet, lastRaisedID):
        data = self.currentGame.dealer.getPreActionState(self)
        self.promptAction(pot, highestBet, lastRaisedID)
        initialInput = input("Enter your action: ")
        processedInput = initialInput.split(' ')
        commandInput = processedInput[0]
        if len(processedInput) > 1:
            parameters = processedInput[1]
        if (commandInput == "fold"):
            data.append("Fold")
            self.currentGame.foldPlayer(self)
        elif (commandInput == "raise"):
            if (not len(processedInput) > 1):
                print("invalid raise, need amount.")
                self.getAction(pot, highestBet, lastRaisedID)
            elif (parameters == "1/3"):
                data.append("Raise one third pot")
                self.currentGame.raisePlayerThird(self)
            elif (parameters == "pot"):
                data.append("Raise pot")
                self.currentGame.raisePlayerPot(self)
            elif (parameters == "allin"):
                data.append("Raise all in")
                self.currentGame.raisePlayerAllIn(self)
            else :
                self.currentGame.raisePlayer(self, parameters)
        elif (commandInput == "check"):
            data.append("Check")
            self.currentGame.checkPlayer(self)
        elif (commandInput == "call"):
            data.append("Call")
            self.currentGame.callPlayer(self)
        elif (commandInput == "equity"):
            self.currentGame.getEquity(self)
        else :
            print("That's not a valid input. Folding " + self.id)
            self.currentGame.foldPlayer(self)
        self.writeInputOutputPairs(data)
    def writeInputOutputPairs(self, data):
        with open('actionsTest.csv', 'a', newline='') as f:
            writer_obj = writer(f)
            writer_obj.writerow(data)
            f.close()
    def promptAction(self, pot, highestBet, lastRaisedID):
        print("Current pot is " + str(pot))
        print("\nYou, " + self.id + " are in for " + str(self.currentBet))
        print("\n" + str(highestBet - self.currentBet) + "to play.")
        if (lastRaisedID != self.id and highestBet - self.currentBet < self.stack):
            print("\nYou may raise up to " + str(self.stack - (highestBet - self.currentBet)))
        if (highestBet - self.currentBet == 0):
            print("\nYou may check.")
        else: 
            print("\nYou may call with stack " + str(self.stack))
            if (self.stack <= highestBet - self.currentBet):
                print(". This will put you all in.")
    def changeStack(self, change):
        if (change + self.stack <= 0):
            print("Player " + self.id + " is all in for: " + str(self.stack))
            temp = self.stack
            self.stack = 0
            return temp
        else: 
            self.stack += change
            return -change
    def receiveCards(self, hand):
        self.hand = hand
        print(self.id + ", you have been dealt: " + str(self.hand))

class playerAI(Player):
    def getAction(self, pot, highestBet, lastRaisedID):
        data = self.currentGame.dealer.getPreActionState(self)
        action = getPrediction(data)
        if (action == "check"):
            data.append("Check")
            self.currentGame.checkPlayer(self)
        elif (action == "call"):
            data.append("Call")
            self.currentGame.callPlayer(self)
        elif (action == "fold"):
            data.append("Fold")
            self.currentGame.foldPlayer(self)
        elif (action == "raise 1/3"):
            data.append("raise one third pot")
            self.currentGame.raisePlayerThird(self)
        elif (action == "raise pot"):
            data.append("raise pot")
            self.currentGame.raisePlayerPot(self)
        elif (action == "raise all in"):
            data.append("raise all in")
            self.currentGame.raisePlayerAllIn(self)
        else :
            print("That's not a valid input. Folding " + self.id)
            self.currentGame.foldPlayer(self)
    def receiveCards(self, hand):
        self.hand = hand

class Dealer:
    def __init__(self, players, big_blind, small_blind):
        self.players = players
        self.foldedPlayers = []
        self.calledPlayers = []
        self.allInnedPlayers = []
        self.inactivePlayers = [] # TODO: handle case where player is out of money
        self.lastRaisedID: str = ""
        self.big_blind: int = big_blind
        self.small_blind: int = small_blind
        self.pot = 0
        self.sidePot = 0 # TODO: sidepot logic, all in logic. Handle cases where received != what we need 
        self.currentBlind = 0 # represents the position of the big blind. UTG is currentBlind + 1, small blind is currentBlind -1, dealer is currentBlind - 2
        self.currentBet = 0
        self.deck = None
        self.communityCards = []
    def collectBlinds(self):
        self.currentBet = self.big_blind
        received_big = self.players[self.currentBlind].changeStack(-(self.big_blind))
        self.players[self.currentBlind].currentBet = received_big
        print("Collected " + str(received_big) + " as big blind from " + self.players[self.currentBlind].id)
        self.players[self.currentBlind].lastAction = "Posted big"
        self.pot += received_big
        received_small = self.players[self.currentBlind - 1].changeStack(-(self.small_blind))
        self.players[self.currentBlind - 1].currentBet = received_small
        print("Collected " + str(received_small) + " as small blind from " + self.players[self.currentBlind - 1].id)
        self.players[self.currentBlind - 1].lastAction = "Posted small"
        self.pot += received_small

    def getPreActionState(self, player):
        amountToPlay = self.currentBet - player.currentBet
        potSize = self.pot
        stack = player.stack
        previousBet = player.currentBet
        lastAction = player.lastAction
        equityVsUnknown = self.getPlayerEquity(player) 
        position = self.players.index(player) - self.big_blind # right now, headsup, so just returns if small or big. Change this for more players
        return [amountToPlay, previousBet, lastAction, position, potSize, stack, equityVsUnknown]

    def foldPlayer(self, player):
        if (player in self.players and not player in self.foldedPlayers):
            self.foldedPlayers.append(player)
            player.currentBet = 0
            print("Player " + player.id + " has folded.")
        else:
            print("Error: this player isn't eligible to fold.")

    def raisePlayer(self, player, raiseAmount):
        if (player in self.players and player.id == self.lastRaisedID or player.stack + player.currentBet <= self.currentBet):
            print(player.id + " cannot raise. Current bet is " + str(self.currentBet) + ". You are in for " + str(player.currentBet))
        if (player in self.players and player.id != self.lastRaisedID):
            coverAmount = self.currentBet - player.currentBet
            totalAdded = coverAmount + raiseAmount
            received = player.changeStack(-(totalAdded))
            player.currentBet = player.currentBet + received
            self.pot += received
            self.lastRaisedID = player.id
            self.currentBet += received - coverAmount if received - coverAmount > 0 else 0
            self.calledPlayers.clear()
            self.calledPlayers.append(player)
            print("Player " + player.id + " has raised to : " + str(self.currentBet))
        else:
            print("Error: this player isn't eligible to raise.")
    
    def callPlayer(self, player):
        if (player in self.players):
            receivedCall = player.changeStack(-(self.currentBet - player.currentBet))
            player.currentBet += receivedCall
            self.pot += receivedCall
            self.calledPlayers.append(player)
            print("Player " + player.id + " has called " + str(self.currentBet))
        else:
            print("Error: this player isn't eligible to call.")

    def checkPlayer(self, player):
        if (player in self.players and player.currentBet != self.currentBet):
            print("Player can't check. Currently, " + str(self.currentBet) + " to play. " + player.id + " in for " + str(player.currentBet))
            player.getAction(self.pot, self.currentBet, self.lastRaisedID)
        elif (player in self.players):
            print("Player " + player.id + " checked.")
            self.calledPlayers.append(player)
        else :
            print("Error: this player isn't eligible to check.")

    def winPot(self, player):
        if (player in self.players):
            player.changeStack(self.pot)
            print("Player " + player.id + " won the pot of " + str(self.pot) + " with the hand " + str(player.hand))
            self.pot = 0
            self.currentBet = 0
            self.currentBlind = (self.currentBlind + 1) % (len(self.players))
            self.resetPlayerBets()
            self.foldedPlayers.clear()
        for player in self.players:
            print("Player " + player.id + " held " + str(player.hand))
    
    def resetPlayerBets(self):
        for player in self.players:
            player.currentBet = 0

    def runBettingLoop(self, currentPosition): 
        self.lastRaisedID = ""
        self.calledPlayers.clear()
        # we have 4 (for now, need to include inactive players) categories of players
        # players who are all in
        # players who have folded out of a hand
        # players who are IN a hand, i.e, they have paid the current highest bet
        # and players who have not made a decision yet
        # we want to go through every player until every player is one of the first three categories
        # folding places you in the folded category. Calling, raising, and checking all put in the IN category.
        # if you raise, you put everyone who was IN in the undecided category.
        # if you've spent all your money and haven't folded, you don't need to make decisions and are in for the rest of the hand.
        # also, if everyone is all inned but one person, then we don't care about that person's action bc no one needs to respond.
        while (len(self.foldedPlayers) + len(self.calledPlayers) + len(self.allInnedPlayers) != len(self.players) and len(self.allInnedPlayers) + 1 != len(self.players)): 
            if (not self.players[currentPosition] in self.foldedPlayers):
                if (self.players[currentPosition].stack == 0):
                    self.allInnedPlayers.append(self.players[currentPosition]) if not self.players[currentPosition] in self.allInnedPlayers else None
                    print("\nPlayer " + self.players[currentPosition].id + " is all in. No actions." )
                else: 
                    self.players[currentPosition].getAction(self.pot, self.currentBet, self.lastRaisedID)
            currentPosition = (currentPosition + 1) % len(self.players)
            if (len(self.foldedPlayers) + 1 == len(self.players)):
                remainingPlayer = list(set(self.players) - set(self.foldedPlayers))
                self.winPot(remainingPlayer[0])
                return True
        return False
    
    def playPreFlop(self):
        for player in self.players:
            player.lastAction = None
        self.collectBlinds()
        self.dealHoleCards()
        return self.runBettingLoop((self.currentBlind + 1) % (len(self.players)))

    def playFlop(self):
        print("\nThe flop comes out as: ") 
        self.communityCards += (self.deck.draw(3))
        print(self.communityCards)
        self.currentBet = 0
        self.resetPlayerBets()
        return self.runBettingLoop(self.currentBlind - 1)
    
    def playTurn(self):
        print("\nThe turn comes out as: ") 
        self.communityCards += (self.deck.draw(1))
        print(self.communityCards)
        self.currentBet = 0
        self.resetPlayerBets()
        return self.runBettingLoop(self.currentBlind - 1)
    
    def playRiver(self):
        print("\nThe river is: ")
        self.communityCards += (self.deck.draw(1))
        print(self.communityCards)
        self.currentBet = 0
        self.resetPlayerBets()
        return self.runBettingLoop(self.currentBlind - 1)


    def playRound(self):
        self.deck = StandardDeck()
        self.foldedPlayers.clear()
        gameOver : bool = self.playPreFlop()
        if (not gameOver):
            gameOver = self.playFlop()
        if (not gameOver): 
            gameOver = self.playTurn()
        if (not gameOver):
            gameOver = self.playRiver()
        if (not gameOver):
            for player in self.determineWinner():
                print("\n" + player.id + " wins the hand with " + str(player.hand))
                self.winPot(player) # todo: sidepot logic
        self.communityCards.clear()

    def dealToPlayer(self, player):
        if player in self.players:
            player.receiveCards(self.deck.draw(2))

    def dealHoleCards(self):
        for player in self.players:
            self.dealToPlayer(player)
    
    def determineWinner(self):
        evaluator = StandardEvaluator()
        remainingPlayers = list(set(self.players) - set(self.foldedPlayers))
        bestHands = []
        currentBest = None
        for player in remainingPlayers:
            currentHandStrength = evaluator.evaluate_hand(player.hand, self.communityCards) 
            if currentBest == None or currentBest < currentHandStrength:
                currentBest = currentHandStrength
                bestHands.clear()
                bestHands.append(player)
            elif currentBest == currentHandStrength:
                bestHands.append(player)
        return bestHands

    def getPlayerEquity(self, player): # monte carlo method for getting player equity w/ 2500 sims
        evaluator = StandardEvaluator()
        riversWon = 0
        for i in range(3000):
            potentialDeck = StandardDeck()
            potentialDeck.draw(player.hand)
            potentialDeck.draw(self.communityCards)
            opponentHand = potentialDeck.draw(2)
            potentialRiver = self.communityCards + potentialDeck.draw(5 - len(self.communityCards))
            if (evaluator.evaluate_hand(player.hand, potentialRiver) >= evaluator.evaluate_hand(opponentHand, potentialRiver)):
                riversWon = riversWon + 1
        return riversWon/3000

    def playGame(self):
        self.inactivePlayers.clear()
        while (len(self.inactivePlayers) + 1 < len(self.players)):
            self.playRound()
            for player in self.players:
                if player.stack == 0: 
                    self.inactivePlayers.append(player)
        remainingPlayers = list(set(self.players) - set(self.inactivePlayers))
        print(remainingPlayers[0].id + " wins.")


class situationPredictor():
    def situationToPrediction():
        stack = input('StackSize?')
        hand = input('Hand?')
        communityCards = input('Community cards?')
        pot = input('pot?')
        amountToPlay = input('How much to play?')
        position = input('position?')
        


        
player1 = Player(1000, "Warringloser")
player2 = playerAI(1000, "The goat")

test = Game(10, 5, [player1, player2])

test.dealer.playGame()

# for historymessage in iter(test.history.get, None):
#     print(historymessage)

