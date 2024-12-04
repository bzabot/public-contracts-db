import sqlite3

# Database connection (or creation, if it doesn't exist)
conn = sqlite3.connect("contratos_publicos.db")
print("Database created/connected successfully!")
cur = conn.cursor()

# creating table "procedimentos"
cur.execute("""
    CREATE TABLE IF NOT EXISTS procedimentos (
        codigo INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao TEXT NOT NULL
    );
    """)

# creating table "contratoTipoClassificacoes"
cur.execute("""
    CREATE TABLE IF NOT EXISTS contratoTipoClassificacoes (
        codigo INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao TEXT NOT NULL
    );
    """)

# creating table "classificacoesCpv"
cur.execute("""
    CREATE TABLE IF NOT EXISTS classificacoesCpv (
        codigo TEXT PRIMARY KEY,
        descricao TEXT NOT NULL
    );
    """)

# creating table "fundamentacoes"
cur.execute("""
    CREATE TABLE IF NOT EXISTS fundamentacoes (
        codigo INTEGER PRIMARY KEY AUTOINCREMENT,
        fundamentacao TEXT NOT NULL
    );
    """)

# creating table "paises"
cur.execute("""
    CREATE TABLE IF NOT EXISTS paises (
        codigo INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
    );
    """)

# creating table "distritos"
cur.execute("""
    CREATE TABLE IF NOT EXISTS distritos (
        codigo INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        pais INTEGER NOT NULL,
        FOREIGN KEY(pais) REFERENCES paises(codigo)
    );
    """)

# creating table "municipios"
cur.execute("""
    CREATE TABLE IF NOT EXISTS municipios (
        codigo INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        distrito INTEGER NOT NULL,
        FOREIGN KEY(distrito) REFERENCES distritos(codigo)
    );
    """)

cur.execute("""
    CREATE TABLE IF NOT EXISTS municipioDeExecucao (
        contrato INTEGER NOT NULL,
        municipio INTEGER NOT NULL,
        PRIMARY KEY (contrato, municipio),
        FOREIGN KEY(contrato) REFERENCES contratos(idContrato),
        FOREIGN KEY(municipio) REFERENCES municipios(codigo)
    );
    """)

cur.execute("""
    CREATE TABLE IF NOT EXISTS paisDeExecucao (
        contrato INTEGER NOT NULL,
        pais INTEGER NOT NULL,
        PRIMARY KEY (contrato, pais),
        FOREIGN KEY(contrato) REFERENCES contratos(idContrato),
        FOREIGN KEY(pais) REFERENCES paises(codigo)
    );
    """)

# creating table "contratos"
cur.execute("""
    CREATE TABLE IF NOT EXISTS contratos (
        idContrato INTEGER PRIMARY KEY,
        objetoContrato TEXT NOT NULL,
        dataPublicacao DATETIME NOT NULL,
        dataCelebracaoContrato  DATETIME NOT NULL,
        precoContratual REAL NOT NULL,
        prazoExecucao INTEGER NOT NULL,
        procedimentoCentralizado INTEGER NOT NULL,
        tipoProcedimento INTEGER NOT NULL,
        fundamentacao INTEGER,
        FOREIGN KEY(tipoProcedimento) REFERENCES procedimentos(codigo),
        FOREIGN KEY(fundamentacao) REFERENCES fundamentacoes(codigo)
    );
    """)

# creating table "entidades"
cur.execute("""
    CREATE TABLE IF NOT EXISTS entidades (
        codigo INTEGER PRIMARY KEY AUTOINCREMENT,
        nif TEXT NOT NULL,
        designacao TEXT NOT NULL
    );
    """)

# creating table "adjudicatarios"
cur.execute("""
    CREATE TABLE IF NOT EXISTS adjudicatarios (
        contrato INTEGER NOT NULL,
        entidade INTEGER NOT NULL,
        PRIMARY KEY (contrato, entidade),
        FOREIGN KEY(contrato) REFERENCES contratos(idContrato),
        FOREIGN KEY(entidade) REFERENCES entidades(codigo)
    );
    """)

# creating table "adjudicantes"
cur.execute("""
    CREATE TABLE IF NOT EXISTS adjudicantes (
        contrato INTEGER NOT NULL,
        entidade INTEGER NOT NULL,
        PRIMARY KEY (contrato, entidade),
        FOREIGN KEY(contrato) REFERENCES contratos(idContrato),
        FOREIGN KEY(entidade) REFERENCES entidades(codigo)
    );
    """)

cur.execute("""
    CREATE TABLE IF NOT EXISTS tiposContrato (
        contrato INTEGER NOT NULL,
        tipoContrato INTEGER NOT NULL,
        PRIMARY KEY (contrato, tipoContrato),
        FOREIGN KEY(contrato) REFERENCES contratos(idContrato),
        FOREIGN KEY(tipoContrato) REFERENCES contratoTipoClassificacoes(codigo)
    );
    """)

cur.execute("""
    CREATE TABLE IF NOT EXISTS cpvContratos (
        contrato INTEGER NOT NULL,
        cpv INTEGER NOT NULL,
        PRIMARY KEY (contrato, cpv),
        FOREIGN KEY(contrato) REFERENCES contratos(idContrato),
        FOREIGN KEY(cpv) REFERENCES classificacoesCpv(codigo)
    );
    """)

conn.close()
print("Database disconnected successfully!")