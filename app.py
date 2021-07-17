from flask import Flask, render_template, request, redirect
from user import User
from artigos import Artigos

app = Flask(__name__)
usr = User()
art = Artigos()


@app.route('/inserirA', methods=['GET', 'POST'])
def inserirA():
    erro = None
    if request.method == 'POST':
        v1 = request.form['category']
        v2 = request.form['brand']
        v3 = request.form['description']
        v4 = request.form['price']
        art.inserirA(v1, v2, v3, v4)
        erro = "Article successfully inserted."
    return render_template('artigos/inserirA.html', erro=erro, usr=usr, art=art)


@app.route('/editarA', methods=['GET', 'POST'])
def editarA():
    erro = None
    if request.method == 'POST':
        if art.id:
            if "cancel" in request.form:
                art.reset()
            elif "delete" in request.form:
                art.apaga(art.id)
                erro = "Artigo eliminado com sucesso"
            elif "edit" in request.form:
                v1 = request.form['price']
                art.alterar(art.id, v1)
                art.select(art.id)  # Atualizar os dados na classe
                erro = "Preço alterado com sucesso"
        else:
            v1 = request.form['id']
            erro = art.select(v1)
    return render_template('artigos/editarA.html', erro=erro, usr=usr, art=art)


@app.route('/eliminarA', methods=['GET', 'POST'])
def eliminarA():
    if request.method == 'POST':
        v1 = request.form['id']
        title = "Eliminação do seu Artigo"
        return render_template('accounts.html', title=title, accounts=art.listaA(v1), campos=art.campos, usr=usr)
    erro = "Indique o id do seu Artigo a eliminar."
    return render_template('artigos/eliminarA.html', erro=erro, usr=usr, art=art)


@app.route('/accounts')
def accounts():
    title = "User Accounts 📂"
    return render_template('accounts.html', title=title, accounts=usr.lista, campos=usr.campos, usr=usr)


@app.route('/consultarA')
def consultarA():
    title = "Article List 🛒"
    return render_template('accounts.html', title=title, accounts=art.lista, campos=art.campos, usr=usr)


@app.route('/register', methods=['GET', 'POST'])
def route():
    erro = None
    if request.method == 'POST':
        v1 = request.form['utilizador']
        v2 = request.form['email']
        v3 = request.form['passe']
        v4 = request.form['cpasse']
        if usr.existe(v1):
            erro = 'The user already exists.'
        elif v3 != v4:
            erro = 'Password does not match.'
        else:
            erro = 'User created with Success.'
            usr.gravar(v1, v2, v3)
    return render_template('utilizadores/register.html', erro=erro, usr=usr)


@app.route('/')
def index():
    return render_template('index.html', usr=usr)


@app.route('/login', methods=['GET', 'POST'])
def login():
    erro = None
    if request.method == 'POST':
        v1 = request.form['utilizador']
        v2 = request.form['passe']
        if not usr.existe(v1):
            erro = 'User does not exist.'
        elif not usr.log(v1, v2):
            erro = 'The password is wrong.'
        else:
            usr.login = v1
            erro = 'Welcome!'
    return render_template('utilizadores/login.html', erro=erro, usr=usr)


@app.route('/logout')
def logout():
    usr.reset()
    return redirect('/')


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    erro = None
    if request.method == 'POST':
        v1 = request.form['utilizador']
        v2 = request.form['passe']
        if not usr.existe(v1):
            erro = 'User does not exist.'
        elif not usr.log(v1, v2):
            erro = 'The password is wrong.'
        else:
            usr.apaga(v1)
            erro = 'Account Deleted Successfully.'
    return render_template('utilizadores/delete.html', erro=erro, usr=usr)


@app.route('/newpasse', methods=['GET', 'POST'])
def newpasse():
    erro = None
    if request.method == 'POST':
        v1 = request.form['utilizador']
        v0 = request.form['apasse']
        v2 = request.form['passe']
        v3 = request.form['cpasse']
        if not usr.existe(v1):
            erro = 'User does not exist.'
        elif not usr.log(v1, v0):
            erro = 'The password is wrong.'
        elif v2 != v3:
            erro = 'Password does not match.'
        else:
            usr.alterar(v1, v2)
    return render_template('utilizadores/newpasse.html', erro=erro, usr=usr)


@app.route('/drones')
def drones():
    return render_template('drones.html', usr=usr)


@app.route('/company')
def company():
    return render_template('company.html', usr=usr)


@app.route('/about me')
def me():
    return render_template('about me.html', usr=usr)


@app.route('/contact us')
def contact():
    return render_template('contact us.html', usr=usr)


@app.route('/testimonials')
def testimonials():
    return render_template('testimonials.html', usr=usr)


if __name__ == '__main__':
    app.run(debug=True)