
import HomeMenu from "./HomeMenu"
import React, { useState } from 'react'
import PokerTable from "./PokerTable"

const Home = (props) => {
    const [gameState, setGameState] = useState("idle")
    if (gameState === "idle") {
        return(
            <div>
               <HomeMenu setGameState={setGameState}></HomeMenu>
            </div>
        )
    }
    else if (gameState === "start") {
        return(
            <div>
                <PokerTable></PokerTable>
            </div>
        )
    }
}

export default Home