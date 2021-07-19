import psycopg2


class Artigos:

    def __init__(self):
        self.reset()

    def reset(self):
        self.id = None  # Número do produto
        self.category = None  # Categoria
        self.brand = None  # Marca
        self.description = None  # Descrição
        self.price = None  # Preço
        self.reference = None  # Referência
        self.ean = None  # European Article Number
        self.stock = None  # Quantidade de artigos
        self.created = None  # Data de criação
        self.updated = None  # Data de alteração
        ficheiro = self.herokudb()
        db = ficheiro.cursor()
        db.execute('CREATE TABLE IF NOT EXISTS categorias (id SERIAL PRIMARY KEY, category TEXT)')
        db.execute('CREATE TABLE IF NOT EXISTS marca (id SERIAL PRIMARY KEY, brand TEXT)')
        db.execute('CREATE TABLE IF NOT EXISTS artigos (id SERIAL PRIMARY KEY, category INT, brand INT,'
                   'description TEXT, price NUMERIC,reference TEXT, ean TEXT, stock INT, created DATE, updated DATE,'
                   'FOREIGN KEY (category) REFERENCES categorias(id), FOREIGN KEY (brand) REFERENCES marca(id))')
        ficheiro.commit()
        ficheiro.close()

    def herokudb(self):
        from db import Database
        mydb = Database()
        return psycopg2.connect(host=mydb.Host, database=mydb.Database, user=mydb.User, password=mydb.Password,
                                sslmode='require')

    def select(self, id):
        erro = None
        try:
            ficheiro = self.herokudb()
            db = ficheiro.cursor()
            db.execute("select * from artigos where id = %s", (id,))
            valor = db.fetchone()
            ficheiro.close()
            self.id = valor[0]  # Número do produto
            self.category = valor[1]  # Categoria
            self.brand = valor[2]  # Marca
            self.description = valor[3]  # Descrição
            self.price = valor[4]  # Preço
        except:
            self.reset()
            erro = "The article does not exist!"  # O artigo não existe!
        return erro

    def inserirA(self, category, brand, description, price):
        ficheiro = self.herokudb()
        db = ficheiro.cursor()

        catId = self.existeC(category)
        if not catId:
            self.inserirC(category)
            catId = self.existeC(category)
        marId = self.existeM(brand)
        if not marId:
            self.inserirM(brand)
            marId = self.existeM(brand)
        db.execute("INSERT INTO artigos VALUES (DEFAULT ,%s, %s, %s, %s)", (catId, marId, description, price,))
        ficheiro.commit()
        ficheiro.close()

    def inserirC(self, category):
        ficheiro = self.herokudb()
        db = ficheiro.cursor()
        db.execute("INSERT INTO categorias VALUES (DEFAULT ,%s)", (category,))
        ficheiro.commit()
        ficheiro.close()

    def inserirM(self, brand):
        ficheiro = self.herokudb()
        db = ficheiro.cursor()
        db.execute("INSERT INTO marca VALUES (DEFAULT ,%s)", (brand,))
        ficheiro.commit()
        ficheiro.close()

    def apagarusr(self):
        try:
            ficheiro = self.herokudb()
            db = ficheiro.cursor()
            db.execute("drop table usr")
            ficheiro.commit()
            ficheiro.close()
        except:
            erro = "The table does not exist."  # A tabela não existe.
        return erro

    def existe(self, login):
        try:
            ficheiro = self.herokudb()
            db = ficheiro.cursor()
            db.execute("SELECT * FROM usr WHERE login = %s", (login,))
            valor = db.fetchone()
            ficheiro.close()
        except:
            valor = None
        return valor

    def existeC(self, category):
        try:
            ficheiro = self.herokudb()
            db = ficheiro.cursor()
            db.execute("SELECT id FROM categorias WHERE category = %s", (category,))
            valor = db.fetchone()
            ficheiro.close()
        except:
            valor = None
        return valor

    def existeM(self, brand):
        try:
            ficheiro = self.herokudb()
            db = ficheiro.cursor()
            db.execute("SELECT id FROM marca WHERE brand = %s", (brand,))
            valor = db.fetchone()
            ficheiro.close()
        except:
            valor = None
        return valor

    def log(self, login, password):
        ficheiro = self.herokudb()
        db = ficheiro.cursor()
        db.execute("SELECT * FROM usr WHERE login = %s and password = %s", (login, self.code(password),))
        valor = db.fetchone()
        ficheiro.close()
        return valor

    def alterar(self, id, price):
        ficheiro = self.herokudb()
        db = ficheiro.cursor()
        db.execute("UPDATE artigos SET price = %s WHERE id = %s", (price, id))
        ficheiro.commit()
        ficheiro.close()

    def apaga(self, id):
        ficheiro = self.herokudb()
        db = ficheiro.cursor()
        db.execute("DELETE FROM artigos WHERE id = %s", (id,))
        ficheiro.commit()
        ficheiro.close()

    @property
    def campos(self):
        return [('número',), ('categorias',), ('marca',), ('descrição',), ('preço',)]

    @property
    def lista(self):
        try:
            ficheiro = self.herokudb()
            db = ficheiro.cursor()
            db.execute('SET lc_monetary TO "pt_PT.utf8"')
            db.execute("SELECT artigos.id, c.category, m.brand, description,"
                       "price::MONEY FROM artigos JOIN categorias c ON artigos.category = c.id JOIN marca m ON m.id = artigos.brand")

            valor = db.fetchall()
            ficheiro.close()
        except:
            valor = ""
        return valor

    @property
    def listaC(self):
        try:
            ficheiro = self.herokudb()
            db = ficheiro.cursor()
            db.execute("select category from categorias")
            valor = db.fetchall()
            ficheiro.close()
        except:
            valor = ""
        return valor

    @property
    def listaM(self):
        try:
            ficheiro = self.herokudb()
            db = ficheiro.cursor()
            db.execute("select brand from marca")
            valor = db.fetchall()
            ficheiro.close()
        except:
            valor = ""
        return valor

    @staticmethod
    def code(passe):
        import hashlib
        return hashlib.sha3_256(passe.encode()).hexdigest()
