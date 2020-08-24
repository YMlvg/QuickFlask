from flask import Flask
from flask import render_template, redirect,request
from chess import WebInterface, Board


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
 
        prompt_result = game.prompt(move) 
        #it return string if there is error, return a tuple(start,end)when the move is valid
        if type(prompt_result) == str:
            ui.errmsg = prompt_result
        elif type(prompt_result) == tuple:
            start, end = prompt_result
        try:
            game.update(start, end)
        except :
            ui.errmsg = (f'Invalid move ({game.printmove(start, end)})')
        else:
            game.next_turn()
            ui.board = game.display()
            ui.inputlabel = f'{game.turn} player: '
    return render_template('chess.html',ui=ui)
    valid,output = game.prompt(move)
    
  
    if valid:
        if game.promotepawns():
            return redirect('/promote')      
        else: 
            start, end = output
            game.update(start, end)
            return render_template('chess.html', ui=ui)
    else:
        return render_template('chess.html', ui=ui)
#
    
    
    # TODO: Validate move, redirect player back to /play again if move is invalid
    # If move is valid, check for pawns to promote
    # Redirect to /promote if there are pawns to promote, otherwise 

@app.route('/promote')
def promote():
    pass

app.run('0.0.0.0')