import sqlite3

# Database connection (or creation, if it doesn't exist)
conn = sqlite3.connect("../contratos_publicos.db")
print("Database created/connected successfully!")
cur = conn.cursor()

# CPV
cur.execute("""
    CREATE TABLE IF NOT EXISTS CPVs (
        codigoCPV TEXT PRIMARY KEY,
        descricaoCPV TEXT NOT NULL
    );
    """)

cur.execute("""
    CREATE TABLE IF NOT EXISTS CPVContratos (
        idContrato INTEGER NOT NULL,
        codigoCPV TEXT NOT NULL,
        PRIMARY KEY (idContrato, codigoCPV),
        FOREIGN KEY(idContrato) REFERENCES Contratos(idContrato),
        FOREIGN KEY(codigoCPV) REFERENCES CPVs(codigoCPV)
    );
    """)

# descricao acordo quadro
#TODO identificador TEXT,
cur.execute("""
    CREATE TABLE IF NOT EXISTS DescrAcordoQuadro (
        idAcordoQuadro INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao TEXT NOT NULL
    );
    """)

cur.execute("""
    CREATE TABLE IF NOT EXISTS AcordoQuadroContratos (
        idContrato INTEGER NOT NULL,
        idAcordoQuadro INTEGER NOT NULL,
        PRIMARY KEY (idcontrato, idAcordoQuadro),
        FOREIGN KEY(idContrato) REFERENCES Contratos(idContrato),
        FOREIGN KEY(idAcordoQuadro) REFERENCES DescrAcordoQuadro(idAcordoQuadro)
    );
    """)

# procedimentos
cur.execute("""
    CREATE TABLE IF NOT EXISTS TiposProcedimentos (
        idProcedimento INTEGER PRIMARY KEY AUTOINCREMENT,
        procedimento TEXT NOT NULL
    );
    """)

# tiposContratos
cur.execute("""
    CREATE TABLE IF NOT EXISTS TiposContratos (
        idTipoContrato INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT NOT NULL
    );
    """)

cur.execute("""
    CREATE TABLE IF NOT EXISTS ClassificacaoContratos (
        idContrato INTEGER NOT NULL,
        idTipoContrato INTEGER NOT NULL,
        PRIMARY KEY (idContrato, idTipoContrato),
        FOREIGN KEY(idContrato) REFERENCES Contratos(idContrato),
        FOREIGN KEY(idTipoContrato) REFERENCES TiposContratos(idTipoContrato)
    );
    """)

# fundamentacoes
cur.execute("""
    CREATE TABLE IF NOT EXISTS Fundamentacoes (
        idFundamentacao INTEGER PRIMARY KEY AUTOINCREMENT,
        artigo TEXT NOT NULL,
        numero INTEGER,
        alinea TEXT,
        subalinea TEXT,
        referenciaLegislativa TEXT NOT NULL
    );
    """)

cur.execute("""
    CREATE TABLE IF NOT EXISTS FundamentacaoContratos (
        idContrato INTEGER NOT NULL,
        idFundamentacao INTEGER NOT NULL,
        PRIMARY KEY (idContrato, idFundamentacao),
        FOREIGN KEY(idContrato) REFERENCES Contratos(idContrato),
        FOREIGN KEY(idFundamentacao) REFERENCES Fundamentacoes(idFundamentacao)
    );
    """)

# local de execucao
cur.execute("""
    CREATE TABLE IF NOT EXISTS Paises (
        idPais INTEGER PRIMARY KEY AUTOINCREMENT,
        pais TEXT NOT NULL
    );
    """)

cur.execute("""
    CREATE TABLE IF NOT EXISTS Distritos (
        idDistrito INTEGER PRIMARY KEY AUTOINCREMENT,
        distrito TEXT,
        idPais INTEGER NOT NULL,
        FOREIGN KEY(idPais) REFERENCES Paises(idPais)
    );
    """)

cur.execute("""
    CREATE TABLE IF NOT EXISTS Municipios (
        idMunicipio INTEGER PRIMARY KEY AUTOINCREMENT,
        municipio TEXT,
        idDistrito INTEGER NOT NULL,
        FOREIGN KEY(idDistrito) REFERENCES Distritos(idDistrito)
    );
    """)

cur.execute("""
    CREATE TABLE IF NOT EXISTS LocaisDeExecucao (
        idContrato INTEGER NOT NULL,
        idMunicipio INTEGER NOT NULL,
        PRIMARY KEY (idContrato, idMunicipio),
        FOREIGN KEY(idContrato) REFERENCES Contratos(idContrato),
        FOREIGN KEY(idMunicipio) REFERENCES Municipios(idMunicipio)
    );
    """)

# entidades
cur.execute("""
    CREATE TABLE IF NOT EXISTS Entidades (
        idEntidade INTEGER PRIMARY KEY AUTOINCREMENT,
        nif TEXT NOT NULL,
        entidade TEXT NOT NULL
    );
    """)

cur.execute("""
    CREATE TABLE IF NOT EXISTS Adjudicatarios (
        idContrato INTEGER NOT NULL,
        idEntidade INTEGER NOT NULL,
        PRIMARY KEY (idContrato, idEntidade),
        FOREIGN KEY(idContrato) REFERENCES Contratos(idContrato),
        FOREIGN KEY(idEntidade) REFERENCES Entidades(idEntidade)
    );
    """)

# contratos
cur.execute("""
    CREATE TABLE IF NOT EXISTS Contratos (
        idContrato INTEGER PRIMARY KEY,
        objetoContrato TEXT NOT NULL,
        dataPublicacao DATE NOT NULL,
        dataCelebracaoContrato  DATE NOT NULL,
        precoContratual REAL NOT NULL,
        procedimentoCentralizado INTEGER NOT NULL,
        prazoExecucao INTEGER NOT NULL,
        idProcedimento INTEGER NOT NULL,
        idAdjudicante INTEGER,
        FOREIGN KEY(idProcedimento) REFERENCES Procedimentos(idProcedimento),
        FOREIGN KEY(idAdjudicante) REFERENCES Entidades(idEntidade)
    );
    """)


conn.close()
print("Database disconnected successfully!")