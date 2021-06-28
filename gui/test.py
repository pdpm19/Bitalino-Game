# Testes à BD
import os, sqlite3
from commands_db import Query, Add, Search

workingDirectory = os.path.join(os.getcwd(), 'db', 'project.db')
conn = sqlite3.connect(workingDirectory)

c = conn.cursor()

# SELECT * FROM Paciente
s = Query('*', 'Paciente', [''], '','', 1)
# print(s)

# SELECT * FROM Paciente WHERE paciente_sexo = Masculino
s = Query('*', 'Paciente', ['', 'Masculino'], 'paciente_sexo', '', 0)
print(s)

# SELECT enfermeiro_password FROM Enfermeiro WHERE enfermeiro_id = 1 
s = Query('enfermeiro_password', 'Enfermeiro',['', '1'], 'enfermeiro_id', '' ,0)
print(s)

# SELECT paciente_id FROM EnfPac WHERE enfermeiro_id = 2
s = Query('paciente_id', 'EnfPac', ['', '2'], 'enfermeiro_id', '', 0)
print(s)

print('VAMOS!')
s1 = Query('paciente_nome', 'Paciente', s, 'paciente_id', 'OR', 0)
print(s1)
