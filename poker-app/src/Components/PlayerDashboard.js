import PlayerControl from "./PlayerControl"
import StackDisplay from "./StackDisplay"

const PlayerDashboard= (props) => {
    const menu = <PlayerControl active={props.yourTurn}></PlayerControl>
    const cards = []
    props.playerHand.forEach((card) => {
        cards.push(
            <Card value={card.value} suit={card.suit} faceDown={false}></Card>
        )
    })
    return(
        <div>
          <StackDisplay></StackDisplay>
          {cards}
          {menu}
        </div>
    )
}

export default PlayerDashboard