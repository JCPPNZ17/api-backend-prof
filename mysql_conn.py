import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, declarative_base

db = sa.create_engine("sqlite:///:memory:")
# db = sa.create_engine("mysql+pymysql://thomas:Th0M4s!@localhost/db_spesa")
Session = sessionmaker(bind=db)
Base = declarative_base()


class User(Base):
    __tablename__ = "utenti"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(sa.String(100))
    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.nome}>"


def main() -> None:
    Base.metadata.create_all(db)
    nome_utente = input("Inserisci il nome: ")
    user = User(nome=nome_utente)

    with Session() as session:
        session.add(user)
        session.commit()
        print(session.query(User).all())


if __name__ == "__main__":
    main()
