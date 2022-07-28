// wraps the player control options in a box for formatting
import PlayerControl from "./PlayerControl";
import Container from 'react-bootstrap/Container';

const PlayerControlMenu = (props) => {
    //function here to handle the raw data and make it readable for playercontrol
    //something that maps Raise X to You Can Raise X or something like that
    //haven't chosen representation of data yet so idk lol
    const foldOption = 'Fold'
    const raiseOption = 'Raise'
    const checkOption = 'Check'
    const callOption = 'Call'
    return(
        <div>
            <Container>
                <PlayerControl active={props.active} raiseOption={raiseOption} checkOption={checkOption} callOption={callOption} foldOption={foldOption}></PlayerControl>
            </Container>
        </div>
    )
}

export default PlayerControlMenu