import React, { useState } from "react";
import { Chessboard } from "react-chessboard";
import axios from "axios";

function App() {
    const [fen, setFen] = useState("start");
    const [gameId, setGameId] = useState(null);

    const startNewGame = async () => {
        const response = await axios.post("http://localhost:5000/new_game");
        setFen(response.data.fen);
        setGameId(response.data._id);
    };

    const onDrop = async (sourceSquare, targetSquare) => {
        const move = `${sourceSquare}${targetSquare}`;
        const response = await axios.post("http://localhost:5000/make_move", {
            game_id: gameId,
            move: move,
        });
        if (response.data.error) {
            alert("Invalid Move");
            return false;
        }
        setFen(response.data.fen);
    };

    return (
        <div>
            <h1>AI Chess Game</h1>
            <button onClick={startNewGame}>New Game</button>
            <Chessboard position={fen} onPieceDrop={onDrop} />
        </div>
    );
}

export default App;
