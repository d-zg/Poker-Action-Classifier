from queue import Queue
from typing import List, Dict

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
    def __registerPlayer(self, newPlayer):
        if (not newPlayer.id in self.allPlayers):
            self.allPlayers.append(newPlayer)
            newPlayer.enterGame(self)
        else:
            print("\nError, player already registered.")
    def __removePlayer(self, id):
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
    def raisePlayer(self, player):
        self.dealer.raisePlayer(player, 500)
        self.history.put("Player " + player.id + " raised.")
    def checkPlayer(self, player):
        self.dealer.checkPlayer(player)
        self.history.put("Player " + player.id + " checked.")
    def callPlayer(self, player):
        self.dealer.callPlayer(player)
        self.history.put("Player " + player.id + " called.")
    


class Player:
    def __init__(self, stack, id):
        self.stack: int = stack
        self.id: str = id
        self.currentBet : int = 0
        self.currentGame : Game = None
    def enterGame(self, instance):
        self.currentGame = instance
        # print some recognition that you were entered into this game
    def leaveGame(self):
        self.currentGame = None
    def getAction(self, pot, highestBet, lastRaisedID):
        self.promptAction(pot, highestBet, lastRaisedID)
        commandInput = input("Enter your action: ")
        if (commandInput == "fold"):
            self.currentGame.foldPlayer(self)
        if (commandInput == "raise"):
            self.currentGame.raisePlayer(self)
        if (commandInput == "check"):
            self.currentGame.checkPlayer(self)
        if (commandInput == "call"):
            self.currentGame.callPlayer(self)
    def promptAction(self, pot, highestBet, lastRaisedID):
        print("Current pot is " + str(pot))
        print("\nYou, " + self.id + " are in for " + str(self.currentBet))
        print("\n" + str(highestBet - self.currentBet) + "to play.")
        if (lastRaisedID != self.id and highestBet - self.currentBet < self.stack):
            print("\nYou may raise up to " + str(self.stack))
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
    def currentBet(self, betSize):
        self.currentBet = betSize
    


class Dealer:
    def __init__(self, players, big_blind, small_blind):
        self.players = players
        self.foldedPlayers = []
        self.calledPlayers = []
        self.allInnedPlayers = []
        self.lastRaisedID: str = ""
        self.big_blind: int = big_blind
        self.small_blind: int = small_blind
        self.pot = 0
        self.currentBlind = 0 # represents the position of the big blind. UTG is currentBlind + 1, small blind is currentBlind -1, dealer is currentBlind - 2
        self.currentBet = 0
    def collectBlinds(self):
        self.currentBet = self.big_blind
        received_big = self.players[self.currentBlind].changeStack(-(self.big_blind))
        self.players[self.currentBlind].currentBet = received_big
        print("Collected " + str(received_big) + " as big blind from " + self.players[self.currentBlind].id)
        self.pot += received_big
        received_small = self.players[self.currentBlind - 1].changeStack(-(self.small_blind))
        self.players[self.currentBlind - 1].currentBet = received_small
        print("Collected " + str(received_small) + " as small blind from " + self.players[self.currentBlind - 1].id)
        self.pot += received_small

    def foldPlayer(self, player):
        if (player in self.players and not player in self.foldedPlayers):
            self.foldedPlayers.append(player)
            player.currentBet = 0
            print("Player " + player.id + " has folded.")
        else:
            print("Error: this player isn't eligible to fold.")

    def raisePlayer(self, player, raiseAmount):
        if (player in self.players and player.id != self.lastRaisedID):
            coverAmount = self.currentBet - player.currentBet
            totalAdded = coverAmount + raiseAmount
            received = player.changeStack(-(totalAdded))
            player.currentBet = player.currentBet + received
            self.pot += received
            self.lastRaisedID = player.id
            self.currentBet += received
            self.calledPlayers.clear()
            self.calledPlayers.append(player)
            print("Player " + player.id + " has raised to : " + str(self.currentBet))
        else:
            print("Error: this player isn't eligible to raise.")
    
    def callPlayer(self, player):
        if (player in self.players):
            receivedCall = player.changeStack(-(self.currentBet - player.currentBet))
            self.pot += receivedCall
            self.calledPlayers.append(player)
            print("Player " + player.id + " has called " + str(self.currentBet))
        else:
            print("Error: this player isn't eligible to call.")

    def checkPlayer(self, player):
        if (player in self.players):
            print("Player " + player.id + " checked.")
            self.calledPlayers.append(player)
        else :
            print("Error: this player isn't eligible to check.")

    def winPot(self, player):
        if (player in self.players):
            player.changeStack(self.pot)
            print("Player " + player.id + " won the pot of " + str(self.pot))
            self.pot = 0
            self.currentBet = 0
            self.currentBlind = (self.currentBlind + 1) % (len(self.players))
            self.foldedPlayers.clear()
    
    def playRound(self):
        self.lastRaisedID = ""
        self.foldedPlayers.clear()
        self.calledPlayers.clear()
        self.collectBlinds()
        # currentPosition = self.currentBlind + 1 % (len(self.players))
        currentPosition = 0
        while (len(self.foldedPlayers) + len(self.calledPlayers) + len(self.allInnedPlayers) != len(self.players)):
            if (not self.players[currentPosition] in self.foldedPlayers):
                if (self.players[currentPosition].stack == 0):
                    self.allInnedPlayers.append(self.players[currentPosition]) if not self.players[currentPosition] in self.calledPlayers else None
                else: 
                    self.players[currentPosition].getAction(self.pot, self.currentBet, self.lastRaisedID)
            currentPosition = (currentPosition + 1) % len(self.players)
            if (len(self.foldedPlayers) + 1 == len(self.players)):
                remainingPlayer = list(set(self.players) - set(self.foldedPlayers))
                self.winPot(remainingPlayer[0])
                return True
        # flop happens here
        self.currentBet = 0
        currentPosition = self.currentBlind - 1
        self.calledPlayers.clear()
        while (len(self.foldedPlayers) + len(self.allInnedPlayers) + len(self.calledPlayers) != len(self.players)):
            if (not self.players[currentPosition] in self.foldedPlayers):
                if (self.players[currentPosition].stack == 0):
                    self.allInnedPlayers.append(self.players[currentPosition]) if not self.players[currentPosition] in self.allInnedPlayers else None
                    print("\nPlayer " + self.players[currentPosition].id + " is all in. No actions.")
                else: 
                    self.players[currentPosition].getAction(self.pot, self.currentBet, self.lastRaisedID)
            currentPosition = (currentPosition + 1) % len(self.players)
            if (len(self.foldedPlayers) + 1 == len(self.players)):
                remainingPlayer = list(set(self.players) - set(self.foldedPlayers))
                self.winPot(remainingPlayer[0])
                return True
    


        
        
player1 = Player(1000, "Warringloser")
player2 = Player(2000, "The goat")

test = Game(10, 5, [player1, player2])

test.foldPlayer(player1)

test.raisePlayer(player1)

test.callPlayer(player2)

print(str(player1.stack))

test.dealer.collectBlinds()

print(str(player1.stack))
print(str(player2.stack))

test.dealer.winPot(player1)

print(str(player1.stack))

test.dealer.playRound()

# print(test.dealer.foldedPlayers[0].id)

# print(player1.stack)