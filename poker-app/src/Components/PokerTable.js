import OpponentInformationBox from "./OpponentInformationBox"
import DealerInformationBox from "./DealerInformationBox"
import PlayerDashboard from "./PlayerDashboard"
import PlayerControlMenu from "./PlayerControlMenu"
const PokerTable = (props) => {
    return(
        <div>
            <OpponentInformationBox></OpponentInformationBox>
            <DealerInformationBox></DealerInformationBox>
            <PlayerDashboard></PlayerDashboard>
            <PlayerControlMenu></PlayerControlMenu>
        </div>
    )
}

export default PokerTable