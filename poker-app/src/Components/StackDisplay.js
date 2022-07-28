const StackDisplay = (props) => {
    const stack = props.playerToDisplay === 'opponent' ? props.opponentStack : props.playerStack
    return(
        <div>
            <t>Current Stack: {stack}</t>
        </div>
    )
}

export default StackDisplay
