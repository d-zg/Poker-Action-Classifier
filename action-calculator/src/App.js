import React, { useState, useEffect } from "react"
import "./App.css"
import Header from "./components/Header"
import CardInstructions from "./components/CardInstructions"
import CommunalContainer from "./containers/CommunalContainer"
import TableContainer from "./containers/TableContainer"
import OddsDisplay from "./components/OddsDisplay"
import cards from "./helpers/cardData"
import calculateOdds from "./helpers/pokerCalculator"
import { areas, areaKeys } from "./helpers/areaData"
import Button from 'react-bootstrap/Button'
import TextField from "@material-ui/core/TextField"
import Features from "./featureVector"

const initialState = {
  cards,
  ...areas,
  selectedKey: areaKeys[0],
  odds: null,
}

const App = () => {
  const [state, setState] = useState(initialState)
  const [bigBlind, setPosition] = useState(false)
  const { cards, selectedKey, odds } = state

  const selectedCards = () => [...areaKeys.map(key => state[key].cards)]

  const availableCards = () =>
    cards.filter(card => !selectedCards().flat().includes(card))

  const addCard = selectedCard => {
    let currentArea = state[selectedKey]
    if (currentArea.cards.length < currentArea.limit) {
      return setState({
        ...state,
        [selectedKey]: {
          ...currentArea,
          cards: [...currentArea.cards, selectedCard],
        },
      })
    }
    alert("You can't add any more cards to this area!")
  }

  const removeCard = (selectedCard, areaKey) => {
    let currentArea = state[areaKey]
    setState({
      ...state,
      [areaKey]: {
        ...currentArea,
        cards: currentArea.cards.filter(card => card !== selectedCard),
      },
    })
  }

  const setSelectedKey = selectedKey => setState({ ...state, selectedKey })

  const enableCalcButton = () => selectedCards().flat().length >= 2

  const getAndShowOdds = () => {
    const odds = calculateOdds(...selectedCards())
    setState({ ...state, odds })
  }

  const resetTable = () => setState(initialState)

  const disableApp = () => !!odds

  const renderTableAreas = (keys, props = {}) =>
    keys.map(key => {
      const { cards, areaName } = state[key]
      return (
        <TableContainer areaKey={key} {...{ key, cards, areaName, ...props }} />
      )
    })

  const { areaName } = state[selectedKey]

  const communalCards = availableCards()

  const enable = enableCalcButton()

  const disable = disableApp()

  const tableProps = { disable, removeCard, setSelectedKey, selectedKey }

  // const getString = cards => cards.map(card => card.code).join("")

  // const getGroup = cards => CardGroup.fromString(getString(cards))

  // const calculateOddsTest = (player1, table, player2) => {
  //   const groups = [[getGroup(player1), getGroup(player2)], getGroup(table)]
  //   console.log(groups)
  // }
  const onClick = () => setPosition(!bigBlind)

  const [potSize, setPotSize] = useState(0)

  const [stackSize, setStackSize] = useState(0)

  const [previousBet, setPreviousBet] = useState(0)
  // const onPotUpdate = (value) => setPotSize(value)
  const actionList = ['Posted Big', 'Posted Small', 'Check', 'Call', 'Fold', 'Raise all in', 'Raise pot', 'Raise 1/3 pot']
  
  const [lastAction, setLastAction] = useState(0)

  const onChangeLastAction = () => setLastAction((lastAction + 1)%8)

  const [amountToPlay, setAmountToPlay] = useState(0)

  const position = (bigBlind) ? 'Big Blind' : 'Small Blind'

  const getAction = async (url, data) => {
    console.log('Sending request')
    console.log(JSON.stringify(data))
    const newData = await fetch(url, { 
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json'
      },
      body: JSON.stringify(data)
    })
    return newData
  }
  
  const testGet = async (value) => {
    const vector = new Features([], ['2h', '2d'], 100, 10, 10, 'Posted big', 1000, 1)
    console.log('here')
    console.log(vector.position)
    getAction('/', vector)
  }

  const calculateAction = async () => {
    const cards = calculateOdds(...selectedCards())
    const hand = cards.hand
    const community = cards.community
    var modelPosition =- -9
    if (bigBlind) {
      modelPosition = -10
    }
    const vector = new Features(community, hand, potSize, amountToPlay, previousBet, lastAction, stackSize, modelPosition)
    const odds = await getAction('/', vector).then(res => res.json(), res => console.log(`req failed: ${res}`))
    console.log(odds)
    setState({ ...state, odds })
  }

  return (
    <div>
      <Header />
      <CommunalContainer {...{ communalCards, disable, addCard }} />
      <CardInstructions {...{ areaName }} />
      <div className="table-containers">
        {renderTableAreas(areaKeys, tableProps)}
      </div>
      <div>
        <Button onClick={onClick}>Position: {position}</Button>
      </div>
      <div>
        <Button onClick={onChangeLastAction}>Last action: {actionList[lastAction]}</Button>
      </div>
      <div>
        <Button onClick={testGet}>testGet: {actionList[lastAction]}</Button>
      </div>
      <div>
        <Button onClick={calculateAction}>testCalc: {actionList[lastAction]}</Button>
      </div>
      <div>
      <TextField
          label="Enter pot size (pre bet)"
          onSubmit={(e) => setPotSize(e)}
        />
      </div>
      <div>
      <TextField
          label="Enter amount to play"
          onSubmit={(e) => setAmountToPlay(e)}
        />
      </div>
      <div>
      <TextField
          label="Enter stack size"
          onSubmit={(e) => setStackSize(e)}
        />
      </div>
      <div>
      <TextField
          label="Enter previous bet"
          onSubmit={(e) => setPreviousBet(e)}
        />
      </div>
      
      <OddsDisplay {...{ enable, getAndShowOdds, resetTable, odds }} />
    </div>
  )
}

export default App
