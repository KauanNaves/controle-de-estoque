from flask import Flask, render_template, request, redirect
from database.db import ITENS

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SECRET_KEY"] = "SUA-CHAVE-SECRETA-AQUI"

# Rotas
@app.route("/")
def index():
    return render_template("pages/index.html")

@app.route("/adicionar-item", methods=['GET', 'POST'])
def adicionarItens():
    if request.method == "GET":
        return render_template("pages/adicionarItem.html")

    return redirect("/")