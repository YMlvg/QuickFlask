from flask import Flask
from flask import render_template, redirect,request
from chess import WebInterface, Board, InputError


app = Flask(__name__)
ui = WebInterface()
game = Board()

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

@app.route('/play',methods=["POST","GET"])
def play():
    # TODO: get player move from GET request object
    # TODO: if there is no player move, render the page template
    if request.method == 'POST':
        move = request.form["move"]
        try:
            start, end = game.split_input(move) 
        except InputError:
            ui.errmsg = 'Invalid move format, please try again'
            return render_template('chess.html', ui=ui)
        movetype = game.movetype(start, end)
        #import pdb;pdb.set_trace()
        if movetype is None:
            ui.errmsg = 'Invalid move for the piece, please try again'
            return render_template('chess.html', ui=ui)
        #import pdb; pdb.set_trace()
        game.update(start, end)
        coord = game.check_for_promotion()
        if coord is not None:
            return redirect('/promote')
        game.next_turn()
    ui.board = game.display()
    ui.inputlabel = f'{game.turn} player: '
    ui.errmsg = None
    return render_template('chess.html',ui=ui)
    
    # TODO: Validate move, redirect player back to /play again if move is invalid
    # If move is valid, check for pawns to promote
    # Redirect to /promote if there are pawns to promote, otherwise 

@app.route('/promote')
def promote():
    pass

app.run('0.0.0.0')