const express = require("express");
const spawn = require("child_process").spawn;
const cors = require("cors");
const app = express();
const PORT = 8080;


const runGetPrediction = (position, communityCards, holeCards, pot, amountToPlay, previousBet, lastAction, stack) => {
    console.log('Loading model and getting prediction')
    let process = spawn("python3", ['./server/getPrediction.py', position, communityCards, holeCards, pot, amountToPlay, previousBet, lastAction, stack])

    let result = ""
    process.stdout.on("data", (data) => {
        result += data.toString();
    });   
    
    process.on("close", (code) => {
        console.log(`Python process exited with code ${code}`)
    });

    return result
}

app.use(express.json());
app.use(cors());

app.post("/", (req, res) => {
    communityCards = req.communityCards
    holeCards = req.holeCards
    pot = req.pot
    amountToPlay = req.amountToPlay
    previousBet = req.previousBet
    lastAction = req.lastAction
    stack = req.stack
    position = req.position
    action = runGetPrediction(position, communityCards, holeCards, pot, amountToPlay, previousBet, lastAction, stack)
    console.log(position)
    if (action == null) {
        // If action is null, the python script hasn't finished so send status 425
        console.log('null')
        res.status(425).send("Scraper has not yet finished running");
    } else {
        // If scrapedData is populated, send it with status 200
        res.status(200).send(action);
    }
});

app.get("/api", (req, res) => {
    console.log('test')
})

app.listen(PORT, () => {
    console.log(`Backend active on http://localhost:${PORT}`);
});