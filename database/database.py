# Integração do app.py com o sqlite3

# Querys em funções para facilitação do uso do Banco de Dados sqlite3

import sqlite3

def createDb(local: str):
    conn = sqlite3.connect(local + '/estoque.db')
    conn.row_factory = sqlite3.Row 
    return conn


def createCursor(connection):
    cursor = connection.cursor()
    return cursor


def createTables():
    
    
