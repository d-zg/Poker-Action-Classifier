class Features {
    constructor(communityCards, holeCards, pot, amountToPlay, previousBet, lastAction, stack, position) {
        this.communityCards = communityCards
        this.holeCards = holeCards
        this.pot = pot
        this.amountToPlay= amountToPlay
        this.previousBet = previousBet
        this.lastAction = lastAction
        this.stack = stack
        this.position = position
    }
}

export default Features