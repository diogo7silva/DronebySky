from flask import Flask, render_template, request
from user import User

app = Flask(__name__)
db = User()


@app.route('/tabela')
def tabela():
    dados = db.lista()
    return render_template('tabela.html', tabela=dados, max=len(dados))

@app.route('/registo', methods=['GET', 'POST'])
def route():
    erro = None
    if request.method == 'POST':
        v1 = request.form['utilizador']
        v2 = request.form['email']
        v3 = request.form['passe']
        v4 = request.form['cpasse']
        if db.existe(v1):
            erro = 'O Utilizador já existe.'
        elif v3 != v4:
            erro = 'A palavra passe não coincide.'
        else:
            db.gravar(v1, v2, v3)
    return render_template('registo.html', erro=erro)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    erro = None
    if request.method == 'POST':
        v1 = request.form['utilizador']
        v2 = request.form['passe']
        if not db.existe(v1):
            erro = 'O Utilizador não existe.'
        elif not db.log(v1, v2):
            erro = 'A palavra passe está errada.'
        else:
            erro = 'Bem-Vindo.'
    return render_template('login.html', erro=erro)


@app.route('/apagar', methods=['GET', 'POST'])
def apagar():
    erro = None
    if request.method == 'POST':
        v1 = request.form['utilizador']
        v2 = request.form['passe']
        if not db.existe(v1):
            erro = 'O Utilizador não existe.'
        elif not db.log(v1, v2):
            erro = 'A palavra passe está errada.'
        else:
            db.apaga(v1)
            erro = 'Conta Eliminada com Sucesso.'
    return render_template('apagar.html', erro=erro)


@app.route('/newpasse', methods=['GET', 'POST'])
def newpasse():
    erro = None
    if request.method == 'POST':
        v1 = request.form['utilizador']
        v0 = request.form['apasse']
        v2 = request.form['passe']
        v3 = request.form['cpasse']
        if not db.existe(v1):
            erro = 'O Utilizador não existe.'
        elif not db.log(v1, v0):
            erro = 'A palavra passe está errada.'
        elif v2 != v3:
            erro = 'A palavra passe não coincide.'
        else:
            db.alterar(v1, v2)
    return render_template('newpasse.html', erro=erro)


if __name__ == '__main__':
    app.run(debug=True)
