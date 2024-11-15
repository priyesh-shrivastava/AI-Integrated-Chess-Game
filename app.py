from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import chess
import chess.engine

app = Flask(__name__)
CORS(app)

# MongoDB connection
client = MongoClient("your_mongodb_connection_string")
db = client.chess_game

# Initialize chess engine (Stockfish AI)
engine_path = "path_to_stockfish_executable"
engine = chess.engine.SimpleEngine.popen_uci(r"C:\Users\HP\Downloads\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe")

@app.route("/new_game", methods=["POST"])
def new_game():
    board = chess.Board()
    game = {"board": board.fen(), "moves": [], "result": None}
    db.game_history.insert_one(game)
    return jsonify({"fen": board.fen()})

@app.route("/make_move", methods=["POST"])
def make_move():
    data = request.json
    game_id = data["game_id"]
    move = data["move"]
    game = db.game_history.find_one({"_id": game_id})
    board = chess.Board(game["board"])
    if chess.Move.from_uci(move) in board.legal_moves:
        board.push_uci(move)
        game["board"] = board.fen()
        game["moves"].append(move)

        # AI's turn
        result = engine.play(board, chess.engine.Limit(time=1))
        ai_move = result.move.uci()
        board.push(result.move)
        game["board"] = board.fen()
        game["moves"].append(ai_move)

        db.game_history.update_one({"_id": game_id}, {"$set": game})
        return jsonify({"fen": board.fen(), "ai_move": ai_move})
    return jsonify({"error": "Invalid move"}), 400

if __name__ == "__main__":
    app.run(debug=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
