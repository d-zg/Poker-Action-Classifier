const PlayerControl = (props) => {
    return(
        <div>
            <button disabled={props.active}>{props.raiseOption}</button> 
            <button disabled={props.active}>{props.checkOption}</button> 
            <button disabled={props.active}>{props.callOption}</button> 
            <button disabled={props.active}>{props.foldOption}</button> 
        </div>
    )
}

export default PlayerControl