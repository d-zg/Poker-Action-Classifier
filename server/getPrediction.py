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
    for card in holeCards.split(','):
        convertedHand.append(parse_card(card))
    if len(communityCards) > 0:
        for card in communityCards.split(','):
            convertedCommunityCards.append(parse_card(card))
    for i in range(3000):
        potentialDeck = StandardDeck()
        potentialDeck.draw(convertedHand)
        if len(communityCards) != 0:
            potentialDeck.draw(convertedCommunityCards)
        opponentHand = potentialDeck.draw(2)
        potentialRiver = convertedCommunityCards + potentialDeck.draw(5 - len(communityCards))
        if (evaluator.evaluate_hand(convertedHand, potentialRiver) >= evaluator.evaluate_hand(opponentHand, potentialRiver)):
            riversWon = riversWon + 1
    equityVsUnKnown = riversWon/3000
    features = [amountToPlay, previousBet, lastAction, position, pot, stack, equityVsUnKnown]
    return runInference(features)

# for card in holeCards:
#     sys.stdout.write(card)
#     sys.stdout.write('\n')

# sys.stdout.write(str(holeCards.split(',')))
sys.stdout.write(json.dumps(situationPredictor(communityCards, holeCards, pot, amountToPlay, previousBet, lastAction, stack, position)))
sys.stdout.flush()

sys.exit(0)