import random
from datetime import datetime
from pony.orm import db_session
from fastapi import FastAPI, Cookie, Query, HTTPException
from fastapi.responses import JSONResponse
from modules.database import Utente, Studente, Docente, Segreteria, Corso, Appello
from modules.schemas import (StructCredentials, StructLibretto, NuovoAppello, ModAppello, IdAppello,
                             ListaCorsi, ListaAppelli, ListaUtenti)

SERVER_ADDR = "127.0.0.1"
SERVER_PORT = 4481

app = FastAPI()


@db_session
def get_user(token: str=None) -> Utente:
    # BYPASS TEST
    return Utente.get(id=1)

    if (token is None) or (token == ""):
        raise HTTPException(status_code=401, detail="Session Token mancante.")

    utente = Utente.get(token=token)
    if utente is None:
        raise HTTPException(status_code=401, detail="Session Token non valido.")

    return utente


@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/login")
@db_session
def login(credentials: StructCredentials):
    if not credentials.username or not credentials.password:
        raise HTTPException(status_code=401, detail="Credenziali mancanti.")

    utente = Utente.get(email=credentials.username, password=credentials.password)
    if utente is None:
        raise HTTPException(status_code=401, detail="Credenziali non valide.")

    if not utente.token:
        rand = random.getrandbits(128)
        utente.token = hex(rand)[2:]

    response = JSONResponse(content={"token": utente.token})
    response.set_cookie(key="token", value=utente.token)
    return response


@app.post("/logout")
@db_session
def logout(token: str=Cookie(None)):
    utente = get_user(token)
    utente.token = ""
    return {"result": "ok"}


@app.get("/corsi")
@db_session
def corsi(token: str=Cookie(None), docente: int=Query(None)):
    _ = get_user(token)

    lista_corsi = Corso.select() if docente is None else Corso.select(lambda c: c.docente.id == docente)
    if not lista_corsi:
        raise HTTPException(status_code=404, detail="Nessun corso trovato.")

    return ListaCorsi(lista_corsi)


@app.get("/docenti")
@db_session
def docenti(token: str=Cookie(None)):
    _ = get_user(token)

    lista_docenti = Docente.select()
    if not lista_docenti:
        raise HTTPException(status_code=404, detail="Nessun docente trovato.")

    return ListaUtenti(lista_docenti)


@app.get("/utente")
@db_session
def info_utente(token: str=Cookie(None)):
    utente = get_user(token)
    return {
        "id": utente.id,
        "nome": utente.nome,
        "cognome": utente.cognome,
        "displayName": utente.displayName,
        "email": utente.email,
        "ruolo": utente.ruolo
    }


@app.get("/libretto")
@db_session
def get_libretto(token: str=Cookie(None), matricola: int=Query(None)):
    utente = get_user(token)

    if isinstance(utente, Docente):
        raise HTTPException(status_code=401, detail="Utente non autorizzato.")

    elif isinstance(utente, Segreteria):
        if matricola is None:
            raise HTTPException(status_code=401, detail="Matricola mancante.")

        target = Studente.get(matricola=matricola)
        if target is None:
            raise HTTPException(status_code=404, detail="Studente non trovato.")

    else:
        target = utente

    if not target.libretto:
        raise HTTPException(status_code=404, detail="Nessun corso trovato.")

    return ListaCorsi(target.libretto)


@app.post("/libretto")
@db_session
def post_libretto(libretto: StructLibretto, token: str=Cookie(None)):
    utente = get_user(token)
    if not isinstance(utente, Studente):
        raise HTTPException(status_code=401, detail="Utente non autorizzato.")

    old_libretto = utente.libretto.copy()
    utente.libretto = set()
    for corso_id in libretto.corsi:
        corso = Corso.get(id=corso_id)
        if corso is None:
            utente.libretto = old_libretto
            raise HTTPException(status_code=404, detail="Corso non trovato.")
        utente.libretto.add(corso)

    if not utente.check_libretto():
        utente.libretto = old_libretto
        raise HTTPException(status_code=400, detail="Il libretto non è valido.")

    return {"result": "ok"}


@app.get("/appelli")
@db_session
def appelli(token: str=Cookie(None), corso: int=Query(None)):
    _ = get_user(token)
    if not corso:
        raise HTTPException(status_code=400, detail="ID corso mancante.")

    lista_appelli = Appello.select(lambda a: a.corso.id == corso)
    if not lista_appelli:
        raise HTTPException(status_code=404, detail="Nessun appello trovato.")

    return ListaAppelli(lista_appelli)


@app.post("/appelli/iscrizione")
@db_session
def iscrizione_appello(appello: IdAppello, token: str=Cookie(None)):
    utente = get_user(token)
    appello = appello.id
    if not isinstance(utente, Studente):
        raise HTTPException(status_code=401, detail="Utente non autorizzato.")

    if not appello:
        raise HTTPException(status_code=400, detail="ID appello mancante.")

    appello = Appello.get(id=appello)
    if appello is None:
        raise HTTPException(status_code=404, detail="Appello non trovato.")

    if appello.data_inizio_iscrizione > datetime.now():
        raise HTTPException(status_code=400, detail="Iscrizioni non ancora aperte.")

    if appello.data_fine_iscrizione < datetime.now():
        raise HTTPException(status_code=400, detail="Iscrizioni chiuse.")

    if appello in utente.appelli:
        raise HTTPException(status_code=400, detail="Sei già iscritto a questo appello.")

    appello.iscritti.add(utente)
    return {"result": "ok"}


@app.delete("/appelli/iscrizione")
@db_session
def disiscrizione_appello(appello: IdAppello, token: str=Cookie(None)):
    utente = get_user(token)
    appello = appello.id
    if not isinstance(utente, Studente):
        raise HTTPException(status_code=401, detail="Utente non autorizzato.")

    if not appello:
        raise HTTPException(status_code=400, detail="ID appello mancante.")

    appello = Appello.get(id=appello)
    if appello is None:
        raise HTTPException(status_code=404, detail="Appello non trovato.")

    if appello not in utente.appelli:
        raise HTTPException(status_code=400, detail="Non sei iscritto a questo appello.")

    if appello.data_fine_iscrizione < datetime.now():
        raise HTTPException(status_code=400, detail="Iscrizioni chiuse.")

    appello.iscritti.remove(utente)
    return {"result": "ok"}


@app.post("/appelli/inserisci")
@db_session
def inserimento_appello(appello: NuovoAppello, token: str=Cookie(None)):
    utente = get_user(token)
    if not isinstance(utente, Docente):
        raise HTTPException(status_code=401, detail="Utente non autorizzato.")

    corso = Corso.get(id=appello.corso)
    if corso is None:
        raise HTTPException(status_code=404, detail="Corso inesistente.")
    if corso.docente != utente:
        raise HTTPException(status_code=401, detail="Utente non autorizzato.")

    Appello(
        data=appello.data,
        data_inizio_iscrizione=appello.data_inizio_iscrizione,
        data_fine_iscrizione=appello.data_fine_iscrizione,
        aula=appello.aula,
        corso=corso
    )
    return {"result": "ok"}


@app.patch("/appelli/modifica")
@db_session
def modifica_appello(appello: ModAppello, token: str=Cookie(None)):
    utente = get_user(token)
    if not isinstance(utente, Docente):
        raise HTTPException(status_code=401, detail="Utente non autorizzato.")

    target = Appello.get(id=appello.id)
    if target is None:
        raise HTTPException(status_code=404, detail="Appello inesistente.")
    if target.corso.docente != utente:
        raise HTTPException(status_code=401, detail="Utente non autorizzato.")

    target.data = appello.data
    target.data_inizio_iscrizione = appello.data_inizio_iscrizione
    target.data_fine_iscrizione = appello.data_fine_iscrizione
    target.aula = appello.aula
    return {"result": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=SERVER_ADDR, port=SERVER_PORT)
