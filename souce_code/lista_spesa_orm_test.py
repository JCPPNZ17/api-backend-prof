# PER LANCIARE IL TEST USATE IL COMANDO:
# pytest .\souce_code\lista_spesa_orm_test.py -q

# test_app.py
import pytest
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

#
# 1)  ---  FIXTURE DI CONFIGURAZIONE  ----------------------------------------
#
@pytest.fixture(scope="function")
def test_app():
    """
    Restituisce l'istanza di Flask configurata per i test
    e con un database SQLite in-memory isolato.
    """
    # Importiamo qui dentro per non inizializzare subito il DB MySQL
    import lista_spesa_orm as app_module

    # Motore di test in-memory
    engine = sa.create_engine("sqlite:///:memory:", future=True)
    TestingSession = sessionmaker(bind=engine)

    # Colleghiamo i metadati alla nuova engine
    app_module.Base.metadata.create_all(engine)

    # Monkey-patch: usiamo la nuova Session invece di quella MySQL
    app_module.Session = TestingSession

    # Attiviamo la modalità di test di Flask
    app_module.app.config.update(TESTING=True)

    yield app_module.app     # forniamo l'oggetto Flask ai test


@pytest.fixture()
def client(test_app):
    """Fornisce un test-client pronto all'uso (lifetime: function)."""
    return test_app.test_client()

#
# 2)  ---  TEST SULLE VARIE ROTTE  -------------------------------------------
#
def test_aggiungi_utente_success(client):
    resp = client.get("/aggiungi_utente/", query_string={"nome": "Alice"})
    assert resp.status_code == 200
    assert b"Utente Alice creato" in resp.data

    # Verifica che l'utente sia realmente nel DB
    mostra = client.get("/mostra_utenti/")
    assert b"Alice" in mostra.data


def test_cambia_nome_a_utente(client):
    # Arrange: creo un utente
    client.get("/aggiungi_utente/", query_string={"nome": "Bob"})

    # Act: cambio nome
    resp = client.get(
        "/cambia_nome_a_utente/",
        query_string={"vecchio_nome": "Bob", "nuovo_nome": "Robert"},
    )

    # Assert
    assert resp.status_code == 200
    assert b"cambiato" == resp.data

    mostra = client.get("/mostra_utenti/")
    assert b"Robert" in mostra.data and b"Bob" not in mostra.data


def test_rimuovi_utente(client):
    # Arrange: creo un utente da eliminare
    client.get("/aggiungi_utente/", query_string={"nome": "Charlie"})

    # Act: lo elimino
    resp = client.get("/rimuovi_utente/", query_string={"nome": "Charlie"})

    # Assert
    assert resp.status_code == 200
    assert b"Eliminato" == resp.data

    mostra = client.get("/mostra_utenti/")
    assert b"Charlie" not in mostra.data


def test_mostra_utenti_empty_list(client):
    """
    Verifica che la rotta /mostra_utenti/ funzioni anche
    quando il database è vuoto.
    """
    resp = client.get("/mostra_utenti/")
    assert resp.status_code == 200
    # La rappresentazione di una lista vuota è "[]"
    assert resp.data.strip() == b"[]"
