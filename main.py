from flask import Flask
from flask import render_template, redirect,request
from chess import WebInterface, Board, InputError,Move,MoveHistory


app = Flask(__name__)
ui = WebInterface()
game = Board()
movehis = MoveHistory()


@app.route('/')
def root():
    return render_template('index.html')

@app.route('/newgame')
def newgame():
    # Note that in Python, objects and variables
    # in the global space are available to
    # top-level functions
    game.start()
    ui.board = game.display()
    ui.inputlabel = f'{game.turn} player: '
    ui.errmsg = None
    ui.btnlabel = 'Move'
    return redirect('/play')

@app.route('/undo',methods=["POST","GET"])
def undo():
    try:
        game.undo(movehis)
    except:
        ui.errmsg = "No more undo allowed"
        return render_template("chess.html",ui=ui)
    game.next_turn()
    ui.inputlabel = f'{game.turn} player: '
    ui.error_msg = None
    ui.board = game.display()
    return render_template('chess.html', ui=ui)

@app.route('/play',methods=["POST","GET"])
def play():
    # TODO: get player move from GET request object
    # TODO: if there is no player move, render the page template
    if request.method == 'POST':
        move_str = request.form["move"]
        try:
            start, end = game.split_input(move_str) 
            move = Move(start, end)
        except InputError:
            ui.errmsg = 'Invalid move format, please try again'
            return render_template('chess.html', ui=ui)
        movetype = game.movetype(start, end)
        if movetype is None:
            ui.errmsg = 'Invalid move for the piece, please try again'
            return render_template('chess.html', ui=ui)
        
        move.storepiece(game)
        movehis.push(move)
        game.update(move.tuple())
        coord = game.check_for_promotion()
        if coord is not None:
            return redirect('/promote')
        game.next_turn()
    ui.board = game.display()
    ui.inputlabel = f'{game.turn} player: '
    ui.errmsg = None
    if game.winner != None:
            ui.inputlabel = game.winner
            return render_template('win.html',ui=ui)
    return render_template('chess.html',ui=ui)

    # TODO: Validate move, redirect player back to /play again if move is invalid
    # If move is valid, check for pawns to promote
    # Redirect to /promote if there are pawns to promote, otherwise 

@app.route('/promote')
def promote():
    pass

app.run('0.0.0.0')