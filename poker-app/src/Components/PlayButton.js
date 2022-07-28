const PlayButton = (props) => {
    return (
        <button onClick={props.setGameState('start')}>Play</button>
    )
}

export default PlayButton