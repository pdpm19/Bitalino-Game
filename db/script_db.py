# Creates the DB
import sqlite3, os
from Crypto.Hash import SHA256

# Pode dar problemas por causa do path onde está a correr

dbPath = os.path.join(os.getcwd(), 'project.db')

conn = sqlite3.connect(dbPath)
c = conn.cursor()

def CreateDB():
    global c

    # Cria as tabelas principais
    # Paciente(paciente_id:PK, paciente_nome:str, paciente_sexo:str, paciente_idade:int)
    c.execute('''CREATE TABLE Paciente
            (paciente_id INTEGER PRIMARY KEY NOT NULL,
            paciente_nome TEXT NOT NULL,
            paciente_sexo TEXT NOT NULL,
            paciente_idade INTEGER NOT NULL)''')

    c.execute('''CREATE TABLE Enfermeiro
            (enfermeiro_id INTEGER PRIMARY KEY NOT NULL,
            enfermeiro_password TEXT NOT NULL)''')

    c.execute('''CREATE TABLE Resultados
            (resultado_id INTEGER PRIMARY KEY NOT NULL,
            resultado_valor INTEGER NOT NULL,
            resultado_timestamp TEXT NOT NULL,
            paciente_id INTEGER NOT NULL)''')

    # Cria as tabelas intermédias
    c.execute('''CREATE TABLE EnfPac
            (enfermeiro_id INTEGER NOT NULL,
            paciente_id INTEGER NOT NULL,
            PRIMARY KEY(enfermeiro_id, paciente_id))''')
    
    c.execute('''CREATE TABLE ResPac
            (resultado_id INTEGER NOT NULL,
            paciente_id INTEGER NOT NULL,
            PRIMARY KEY(resultado_id, paciente_id))''')

def FillsPatient():
    global c, conn
    pacientes = [('João', 'Masculino', 15),
    ('Pedro', 'Masculino', 10),
    ('Catarina', 'Feminino', 12),
    ('Joaquim', 'Masculino', 9),
    ('Rita', 'Feminino', 8),
    ('Andreia', 'Feminino', 9),
    ('Mário', 'Masculino', 11),
    ('Mariana', 'Feminino', 11)]

    c.executemany(
        'INSERT INTO Paciente(paciente_nome, paciente_sexo, paciente_idade) VALUES(?,?,?);', pacientes)

    conn.commit()

def FillsNurse():
    global c, conn
    
    h = SHA256.new()
    pedro_pass = 'pedro123'
    h.update(pedro_pass.encode())
    pedro_pass_sha = h.hexdigest()

    c.execute("INSERT INTO Enfermeiro(enfermeiro_password) VALUES ('" + pedro_pass_sha + "')")

    h = SHA256.new()
    vinicius_pass = 'vini1904'
    h.update(vinicius_pass.encode())
    vinicius_pass_sha = h.hexdigest()

    c.execute("INSERT INTO Enfermeiro(enfermeiro_password) VALUES ('" + vinicius_pass_sha + "')")

    conn.commit()

# Fills Middle tables
def FillsEnfPac():
    global c, conn

    values = [(1,1),
    (1,3),
    (1,5),
    (1,7),
    (2,2),
    (2,4),
    (2,6),
    (2,8),
    ]
    c.executemany("INSERT INTO EnfPac(enfermeiro_id, paciente_id) VALUES(?,?);", values)
    conn.commit()

def FillsDB():
    CreateDB()
    FillsPatient()
    FillsNurse()
    
FillsEnfPac()