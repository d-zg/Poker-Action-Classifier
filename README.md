# Poker-Action-Classifier
Used pokerface to implement a heads-up command line poker game.

Played ~300 hands, recorded 7 features of the pre-action game state: pot, amount to play, equity vs unknown, previous bet, last action, stack, position, and the action (one of 6: raise 1/3 pot, raise pot, raise all in, check, call, fold) I took.

Fit a neural network with 1 hidden layer and 12 neurons to those pre-action state/action pairs. Achieves 21% accuracy on the test set. 

To play poker with the neural network through the command line, run classifierTraining/pokerGameSimulator.py 

To run a web app to see what the neural network would predict given hole cards, community cards, and the rest of those features above, use
### `npm run dev`

To just use the frontend, use
### `npm run client`

For just the backend, use
### `npm run server`

