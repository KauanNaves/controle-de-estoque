from flask import Flask, render_template, request, redirect, flash
from database.db import ITENS, CATEGORIAS, MEDIDAS, TAMANHOS
import math

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SECRET_KEY"] = "SUA-CHAVE-SECRETA-AQUI"


# Rota principal
@app.route("/")
def index():
    # Limite de itens por página
    POR_PAGINA = 10

    # Captura da página atual na url
    pagina_atual = request.args.get("pagina", default=1, type=int)

    if pagina_atual < 1:
        pagina_atual = 1

    total_itens = len(ITENS)
    total_paginas = math.ceil(total_itens / POR_PAGINA)

    if pagina_atual > total_paginas and total_paginas > 0:
        pagina_atual = total_paginas

    indice_inicial = (pagina_atual - 1) * POR_PAGINA
    indice_final = indice_inicial + POR_PAGINA

    itens_paginados = ITENS[indice_inicial:indice_final]

    return render_template(
        "pages/index.html",
        itens=itens_paginados,
        pagina_atual=pagina_atual,
        total_paginas=total_paginas
    )


# Rota para adicionar e editar itens
@app.route("/adicionar-item", methods=['GET', 'POST'])
def adicionarItens():
    if request.method == "POST":
        id_item = None
        if request.args.get("id", type=int):
            id_item = request.args.get("id", type=int)

        if not id_item:
            novoId = ITENS[-1]['id'] + 1

        nomeItem = request.form.get("nomeItem").strip().title()
        categoriaItem = request.form.get("categoriaItem")
        quantidade = request.form.get("quantidadeItem")
        unidadeMedida = request.form.get("medidaItem")
        tamanhoItem = request.form.get("tamanhoItem")

        if not id_item:
            for item in ITENS:
                if item['nome'].title() == nomeItem \
                and item['categoria'] == categoriaItem \
                and item['medida'] == unidadeMedida \
                and item['tamanho'] == tamanhoItem:
                    # Não adiciona itens iguais
                    flash(f"Este item já está cadastrado no sistema. ID do item: {item['id']}!")
                    return redirect("/")

        # Adicionando um item que não existe ou atualizando o mesmo
        dictItem = {
            "id": novoId if not id_item else id_item,
            "nome": nomeItem,
            "categoria": categoriaItem,
            "quantidade": quantidade,
            "medida": unidadeMedida,
            "tamanho": tamanhoItem
        }

        if id_item:
            for i, item in enumerate(ITENS):
                if item['id'] == id_item:
                    ITENS[i] = dictItem 

            flash("Item editado com sucesso!")

        else:
            ITENS.append(dictItem)
            flash("Item adicionado com sucesso!")

        return redirect("/")

    if request.method == "GET":
        item = None
        id_item = request.args.get("id", type=int)
        if isinstance(id_item, int) and not isinstance(id_item, bool):
            for dictItem in ITENS:
                if dictItem['id'] == id_item:
                    item = dictItem

        return render_template("pages/adicionarItem.html",
                                item=item,
                                categorias=CATEGORIAS,
                                medidas=MEDIDAS,
                                tamanhos=TAMANHOS,
                                )


# Rota para apagar itens
@app.route("/deletar-item", methods=["POST"])
def deletarItem():
    id_item = request.args.get("id", type=int)
    itemAchado = None
    for item in ITENS:
        if item['id'] == id_item:
            itemAchado = item

    if itemAchado:
        ITENS.remove(itemAchado)
        flash("Item excluído com sucesso!")

    else:
        flash("Item não encontrado para exclusão!")

    return redirect("/")





