import React from 'react';
import WebSocketProvider from './websocket/WebsocketProvider';
import GameState from './game/GameState';

const Providers = ({ children }) => (
    <WebSocketProvider>
        <GameState>
            {children}
        </GameState>
    </WebSocketProvider>
);

export default Providers;