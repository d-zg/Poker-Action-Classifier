import { CardGroup, OddsCalculator } from "poker-odds-calculator"

const getString = cards => cards.map(card => card.code).join("")

const getGroup = cards => CardGroup.fromString(getString(cards))

const calculateOdds = (player1, table, player2) => {
  const myHand = getGroup(player1)
  const communityCards = getGroup(table)
  // clubs are 1, diamonds 2, hearts are 3 , spades 4
  const suits = ['c', 'd', 'h', 's']
  const ranks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']
  const pokerfaceHand = []
  const pokerfaceCommunity = []
  for (var i = 0; i < myHand.length; ++i) {
    pokerfaceHand.push(ranks[myHand[i].rank - 1] + suits[myHand[i].suit - 1])
  }

  

  for (var j = 0; j < communityCards.length; ++j) {
    pokerfaceCommunity.push(ranks[communityCards[j].rank - 1] + suits[communityCards[j].suit - 1])
  }

  console.log(pokerfaceCommunity)
  console.log(pokerfaceHand)
  return({hand: pokerfaceHand, community: pokerfaceCommunity})


  // const { equities } = OddsCalculator.calculate(...groups)

  // const [p1, p2] = equities.map(equity => equity.getEquity())

  // const tie = 100 - p1 - p2

  // return { p1, p2, tie }
}

export default calculateOdds
