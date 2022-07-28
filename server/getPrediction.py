from pokerface import *
import sys
sys.path.insert(0, '../classifierTraining')
import json

hand = sys.argv[1]
communityCards = sys.argv[2]
holeCards = sys.argv[3]
pot = sys.argv[4]
amountToPlay = sys.argv[5]
previousBet = sys.argv[6]
lastAction = sys.argv[7]
stack = sys.argv[8]
position = sys.argv[9]

from loadModel import getPrediction


def situationPredictor(hand, communityCards, holeCards, pot, amountToPlay, previousBet, lastAction, stack, position):
    evaluator = StandardEvaluator()
    riversWon = 0
    for i in range(3000):
        potentialDeck = StandardDeck()
        potentialDeck.draw(holeCards)
        potentialDeck.draw(communityCards)
        opponentHand = potentialDeck.draw(2)
        potentialRiver = communityCards + potentialDeck.draw(5 - len(communityCards))
        if (evaluator.evaluate_hand(hand, potentialRiver) >= evaluator.evaluate_hand(opponentHand, potentialRiver)):
            riversWon = riversWon + 1
    equityVsUnKnown = riversWon/3000
    features = [amountToPlay, previousBet, lastAction, position, pot, stack, equityVsUnKnown]
    return getPrediction(features)

print(json.dumps(situationPredictor(hand, communityCards, holeCards, pot, amountToPlay, previousBet, lastAction, stack, position)))
sys.stdout.flush()