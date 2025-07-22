from flask import Flask, request
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, declarative_base
from sqlalchemy.exc import IntegrityError

# db = sa.create_engine("sqlite:///dati.db", echo=False, future=True)
db = sa.create_engine("mysql+pymysql://thomas:Th0M4s!@localhost/db_spesa")
Session = sessionmaker(bind=db)
Base = declarative_base()

app = Flask(__name__)

class User(Base):
    __tablename__ = "utenti"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(sa.String(100))
    def __repr__(self) -> str:
        return f"<Utente(id={self.id}, username={self.nome}>"

Base.metadata.create_all(db)

@app.route("/aggiungi_utente/")
def aggiungi_utente():
    nome = request.args.get('nome')
    user = User(nome=nome)
    try:
        with Session() as session:
            session.add(user)
            session.commit()
    except IntegrityError:
            session.rollback()
            return f"Errore: impossibile creare utente {nome}", 409

    return f"Utente {nome} creato"

@app.route("/rimuovi_utente/")
def rimuovi_utente():
    nome = request.args.get('nome')
    # metodo 1:
    with Session() as session:
        utente = session.query(User).filter(User.nome == nome).one()
        session.delete(utente)
        session.commit()
    # metodo 2:
    '''
    with Session() as session:
        session.query(User).filter(User.nome == nome).delete()
        session.commit()
    '''
    return 'Eliminato'

@app.route("/cambia_nome_a_utente/")
def cambia_nome_a_utente():
    vecchio_nome = request.args.get('vecchio_nome')
    nuovo_nome = request.args.get('nuovo_nome')
    # metodo 1:
    with Session() as session:
        utente = session.query(User).filter(User.nome == vecchio_nome).one()
        utente.nome = nuovo_nome
        session.commit()
    # metodo 2:
    '''
    with Session() as session:
        session.query(User).filter(User.nome == vecchio_nome).update(
            {User.nome: nuovo_nome}
        )
        session.commit()
    '''
    return 'cambiato'

@app.route("/mostra_utenti/")
def mostra_utenti():
    with Session() as session:
        utenti = session.query(User).all()
        return utenti.__repr__()
    return 'Errore', 400

if __name__ == '__main__':
    app.debug = True
    app.run()    