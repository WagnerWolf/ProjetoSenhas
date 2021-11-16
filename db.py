import sqlite3

dbname = 'db/senha'
try:
    con = sqlite3.connect(dbname)
except sqlite3.Error as e:
    print(e)
    exit(1)
def gerarSenha():
    cur = con.cursor()
    row = None
    try:
        cur.execute('INSERT INTO senha default values')
        row = cur.lastrowid
        print('senha gerada ' ,row)
        if row == None:
                raise sqlite3.Error('erro gerando senha')
    except sqlite3.Error as e:
        print(e)
        exit(1)
    cur.close()
    con.commit()
def chamarSenha(guichecall):
    cur = con.cursor()
    guiche = guichecall
    senha = None
    try:
        cur.execute('select * from senha where atendido = 0 order by time()')
        senha = cur.fetchone()
        if senha is not None:
            cur.execute('update senha set atendido = 1 where idSenha = ?', (senha[0],))
            cur.execute('insert into guiche_atende_senha (guiche_guicheID, senha_senhaID) values(? , ?) ',
                    (guiche, senha[0]))
        elif senha is None:
            print('Nenhuma senha Disponível')
    except sqlite3.Error as e:
        print('erro chamando senha guiche ', e)
        exit(1)
    cur.close()
    con.commit()
    if senha is not None:
        print('senha '+ str(senha[0]) + ' ' 'chamada guiche ', guiche)
def ultimosChamados():
    from datetime import datetime
    import pytz
    localdata = pytz.timezone('America/Santarem')
    cur = con.cursor()
    query = None
    try:
        cur.execute(
            'select guiche_guicheID, senha_senhaID, datetime(horaAtendido,\'localtime\') from guiche_atende_senha,guiche'
            ' where guiche_guicheID = guiche.guicheId order by atendimentoId desc')
        query = cur.fetchmany(4)
        if query == None:
            raise sqlite3.Error('erro na query')
    except sqlite3.Error as e:
        print(e)
        exit(1)
    cur.close()
    print('Senha na Tela: ' + str(query[0][1]) + ' Guichê: ' + str(query[0][0]) + ' Hora: ' + str(query[0][2]))
    print('última senha: ' + str(query[1][1]) + ' Guichê: ' + str(query[1][0]) + ' Hora: ' + str(query[1][2]))
    print('penúltima senha: ' + str(query[2][1]) + ' Guichê: ' + str(query[2][0]) + ' Hora: ' + str(query[2][2]))
    print('antepenúltima senha: ' + str(query[3][1]) + ' Guichê: ' + str(query[3][0]) + ' Hora: ' + str(query[3][2]))


