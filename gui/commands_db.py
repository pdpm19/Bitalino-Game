# Comandos BD
import os, sqlite3

workingDirectory = os.path.join(os.getcwd(), 'db', 'project.db')
conn = sqlite3.connect(workingDirectory)

c = conn.cursor()

# Makes queries to DB and lists the output
def Query(headerOutput, tableName, restrictor, headerInput, operator, option):
    global c
    ret = ['']
    # Removes 1st position, empty value
    restrictor.pop(0)
    if option == 1:
        query = 'SELECT ' + headerOutput + ' FROM ' + tableName
    else:
        if headerOutput != 'pro_name' and len(restrictor) == 0:
            return None
        if len(restrictor) == 0:
            query = 'SELECT ' + headerOutput + ' FROM ' + tableName
        elif len(restrictor) == 1:
            query = 'SELECT ' + headerOutput + ' FROM ' + tableName + \
                ' WHERE ' + headerInput + ' = "' + str(restrictor[0]) + '"'
        else:
            query = 'SELECT ' + headerOutput + ' FROM ' + tableName + ' WHERE '
            # Gets the last value of the restrictor
            lastValuePox = len(restrictor)-1
            for value in range(len(restrictor)):
                if value == lastValuePox:
                    query = query + headerInput + ' = "' + \
                        str(restrictor[value]) + '"'
                else:
                    query = query + headerInput + ' = "' + \
                        str(restrictor[value]) + '" ' + operator + ' '
    if headerOutput == '*':
        for row in c.execute(query):
            # 0 -> id, 1 -> name, 2-> ....
            ret.append(row[1:])
    else:
        for row in c.execute(query):
            ret.append(row[0])
    return ret

# Makes searchs in the middle-tables of DB
def Search(index, name_id):
    global c
    if name_id == 'product_id':
        restrictor = [' ', str(index)]
        return(Query('category_id', 'ProCat', restrictor, name_id, '', 0))
    elif name_id == 'category_id':
        restrictor = [' ', str(index)]
        return (Query('brand_id', 'CatBra', restrictor, name_id, '', 0))
    elif name_id == 'brand_id':
        restrictor = [' ', str(index)]
        return (Query('model_id', 'BraMod ', restrictor, name_id, '', 0))
    elif name_id == 'model_id':
        restrictor = ['', str(index)]
        return (Query('version_id', 'ModVer', restrictor, name_id, '', 0))
    # Erro
    else:
        exit(-3)

# Adds entries
def Add(tableName, inputs):
    if tableName == 'Category' and len(inputs) == 1:
        query = 'INSERT INTO Category(cat_name) VALUES (?);'
    elif tableName == 'Brand' and len(inputs) == 1:
        query = 'INSERT INTO Brand(bra_name) VALUES (?);'
    elif tableName == 'Model' and len(inputs) == 4:
        query = 'INSERT INTO Model(mod_name, mod_factoryName, mod_startYear, mod_finishYear) VALUES(?,?,?,?);'
    elif tableName == 'Version' and len(inputs) == 8:
        query = 'INSERT INTO Version(ver_name, ver_fuel, ver_engineSize, ver_doors, ver_seats, ver_horsepower, ver_weigth, ver_price) VALUES(?,?,?,?,?,?,?,?);'
    else:
        return -1 
    c.execute(query, inputs)
    conn.commit()
