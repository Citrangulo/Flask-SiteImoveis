from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db = SQLAlchemy(app)

class cadastrado(db.Model):
    __tablename__="imóvel"
    i_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo = db.Column(db.String)
    area = db.Column(db.String)
    ende = db.Column(db.String)

    def __init__(self, i_id, tipo, area, ende):
        self.i_id = i_id
        self.tipo = tipo
        self.area = area
        self.ende = ende

db.create_all()

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/cadastrar")
def cadastrar():
    return render_template("cadastro.html")

@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    if request.method == "POST":
           i_id = request.form.get("i_id")
           tipo = request.form.get("tipo")
           area = request.form.get("area")
           ende = request.form.get("ende")
    if i_id and tipo and area and ende:
        c = cadastrado(i_id, tipo, area, ende)
        db.session.add(c)
        db.session.commit()

    return redirect(url_for("index"))

@app.route("/lista")
def lista():
    cadastrados = cadastrado.query.all()
    return render_template("lista.html", cadastrados=cadastrados)

@app.route("/excluir/<int:id>")
def excluir(id):
    cadastrado = cadastrado.query.filter_by(i_id=id).first()

    db.session.delete(cadastrado)
    db.session.commit()

    cadastrados = cadastrado.query.all()
    return render_template("lista.html", cadastrados=cadastrados)


def voltar():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
