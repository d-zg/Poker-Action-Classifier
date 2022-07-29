const express = require("express");
const spawn = require("child_process").spawn;
const exec = require("child_process").exec;
const cors = require("cors");
const app = express();
const PORT = 8080;

currentAction = null

const runGetPrediction =   (position, communityCards, holeCards, pot, amountToPlay, previousBet, lastAction, stack) => {
    console.log('Loading model and getting prediction')
    return new Promise((resolve, reject) => {
        let process = spawn("python", ['./server/getPrediction.py', position, communityCards, holeCards, pot, amountToPlay, previousBet, lastAction, stack])

        let result = []
        process.stdout.on("data", (data) => { // these are returning fucking promises
            result.push(data.toString());
        });   
        process.stderr.on("data", data => {
            console.error(`stderr: ${data}`)
        })
        process.on("close", (code) => {
            console.log(`Python process exited with code ${code}`)
            if (code === 0) {
                resolve(result.at(-1))
            } else {
                reject(`Process failed with code ${code}`)
            }
        })
        process.on('error', (err) => {
            reject(err)
        })
    })
    
    // the problem is that we have no idea when/whether this returns anything
    // so .on is basically entirely promise based
    // we want to find a way to say, wait a certain amount of time until exit code 0
    // if that time elapses, or we get a different exit code, resolve the promise with a fail
    // this func should probably also be asynchronous 
}

app.use(express.json());
app.use(cors());

app.post("/",  async (req, res) => {
    communityCards = req.body.communityCards
    holeCards = req.body.holeCards
    pot = req.body.pot
    amountToPlay = req.body.amountToPlay
    previousBet = req.body.previousBet
    lastAction = req.body.lastAction
    stack = req.body.stack 
    position = req.body.position
    try {
        action = await runGetPrediction(position, communityCards, holeCards, pot, amountToPlay, previousBet, lastAction, stack)
        console.log(action)
        res.status(200).send(action)
    }
    catch (err) {
        console.error(err)
        res.status(425).send('Inference failed')
    }
    
    // then here, we have to figure out how to say, now that we have this either resolved or failed promise, do something with it
    // which as far as i know should be thru await but this bullshit below is going off instantly
    
    // action.then((data) => {
    //     console.log(data)
    //     res.status(200).send(data)
    // })
    // res.status(200).send(action)
    // if (action == null) {
    //     // If action is null, the python script hasn't finished so send status 425
    //     console.log('null')
    //     res.status(425).send("Inference failed");
    // } else {
    //     // If scrapedData is populated, send it with status 200
    //     res.status(200).send(action);
    //     console.log(action)
    // }
});


app.listen(PORT, () => {
    console.log(`Backend active on http://localhost:${PORT}`);
});