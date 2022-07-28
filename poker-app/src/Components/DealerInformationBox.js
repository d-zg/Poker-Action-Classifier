

const DealerInformationBox = (props) => {
    const cards = []
    props.communityCards.forEach((card) => {
        cards.push(
            <Card value={card.value} suit={card.suit} faceDown={false}></Card>
        )
    })
    return (
        <div>
            {cards}
            <t>Pot: {props.pot}</t>
        </div>
    )
}

export default DealerInformationBox