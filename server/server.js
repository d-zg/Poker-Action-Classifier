const express = require('express') // creates express server
const socketio = require('socket.io');
const gameSocket = require('./socket/index');
const bodyParser = require('body-parser')
const cors = require('cors')

const app = express();
// app.use(express.static(path.join('server', 'public')));

app.use(bodyParser.json({}))
app.use(cors())

const API_PORT = process.env.PORT || 5000

const server = app.listen(API_PORT, () => {
    console.log(
      `Server is listening on port ${API_PORT}...`,
    );
});

const io = socketio(server);

io.on('connection', (socket) => gameSocket.init(socket, io));

process.on('unhandledRejection', (err) => {
    db.disconnect();
  
    console.error(`Error: ${err.message}`);
    server.close(() => {
      process.exit(1);
    });
});