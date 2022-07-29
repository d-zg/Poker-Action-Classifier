from pokerface import *
import sys
import json

position = sys.argv[1]
communityCards = sys.argv[2]
holeCards = sys.argv[3]
pot = sys.argv[4]
amountToPlay = sys.argv[5]
previousBet = sys.argv[6]
lastAction = sys.argv[7]
stack = sys.argv[8]

from loadModel import runInference


def situationPredictor(communityCards, holeCards, pot, amountToPlay, previousBet, lastAction, stack, position):
    evaluator = StandardEvaluator()
    riversWon = 0
    convertedHand = []
    convertedCommunityCards = []
    print('here are hole : \n\nn\n\n\nn\n\n')
    print(holeCards)
    for card in holeCards:
        convertedHand.append(parse_card(card))
    for card in communityCards:
        convertedCommunityCards.append(parse_card(card))
    print(convertedCommunityCards)
    print(convertedHand)
    for i in range(3000):
        potentialDeck = StandardDeck()
        potentialDeck.draw(holeCards)
        if len(communityCards) != 0:
            potentialDeck.draw(communityCards)
        opponentHand = potentialDeck.draw(2)
        potentialRiver = communityCards + potentialDeck.draw(5 - len(communityCards))
        if (evaluator.evaluate_hand(holeCards, potentialRiver) >= evaluator.evaluate_hand(opponentHand, potentialRiver)):
            riversWon = riversWon + 1
    equityVsUnKnown = riversWon/3000
    features = [amountToPlay, previousBet, lastAction, position, pot, stack, equityVsUnKnown]
    return runInference(features)

print(json.dumps(situationPredictor(communityCards, holeCards, pot, amountToPlay, previousBet, lastAction, stack, position)))
sys.stdout.flush()