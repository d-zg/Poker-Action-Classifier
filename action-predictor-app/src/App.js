import './App.css';
import { useState } from "react"
import deck from './helpers/cardData';
import CommunalCardContainer from './components/CommunalCardContainer';



const initialState = {
  cards: deck,
  communalCards: [],
  disable:false,
  myHand: [],
  amountToPlay: null,
  lastAction: null,
  stack: null,
  pot: null, 
  previousBet: null,
  position: null,
  action: null,
}
function App() {
  const [state, setState] = useState(initialState)
  const { cards, disable, action } = state

  const addCard = (val) => {
    console.log('adding card')
  }
  // const 
  return (
   <div>
     
 
      <CommunalCardContainer communalCards={cards} disable={disable} addCard={addCard}>
      </CommunalCardContainer>
    
   </div>
  );
}

export default App;
