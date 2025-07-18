from flask import Flask, request
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, declarative_base

# db = sa.create_engine("sqlite:///:memory:")
db = sa.create_engine("mysql+pymysql://utente:password@host/database")
Session = sessionmaker(bind=db)
Base = declarative_base()

app = Flask(__name__)

@app.route("/aggiungi_utente/")
def aggiungi_utente():
    raise NotImplemented

@app.route("/rimuovi_utente/")
def rimuovi_utente():
    raise NotImplemented

@app.route("/cambia_nome_a_utente/")
def cambia_nome_a_utente():
    raise NotImplemented

@app.route("/mostra_utenti/")
def mostra_utenti():
    raise NotImplemented

if __name__ == '__main__':
    app.debug = True
    app.run()