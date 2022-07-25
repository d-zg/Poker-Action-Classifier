
import HomeMenu from "./HomeMenu"
import React, { useState } from 'react'

const Home = (props) => {
    const [gameState, setGameState] = useState("idle")
    if (gameState = "idle") {
        return(
            <div>
               <HomeMenu props={props}></HomeMenu>
         </div>
        )
    }
}

export default Home