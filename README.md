# Poker-Action-Classifier
Trained a neural network to play heads-up poker like me. Also created a web app that returns the neural network's prediction given a situation.

Used tensorflow + keras to train the classifier. React for the web app frontend, node for the backend. Full game app in progress 

To play poker with the neural network through the command line, run classifierTraining/pokerGameSimulator.py 

To run a web app to see what the neural network would predict given hole cards, community cards, and the rest of those features above, use
### `npm run dev`

To just use the frontend, use
### `npm run client`

For just the backend, use
### `npm run server`

Played ~300 hands, recorded 7 features of the pre-action game state: pot, amount to play, equity vs unknown, previous bet, last action, stack, position, and the action (one of 6: raise 1/3 pot, raise pot, raise all in, check, call, fold) I took.

Fit a neural network with 1 hidden layer and 12 neurons to those pre-action state/action pairs. Achieves 21% accuracy on the test set. 
