from pydantic import BaseModel
from pony.orm import db_session


class StructCredentials(BaseModel):
    username: str
    password: str


class StructLibretto(BaseModel):
    corsi: list[int]


class StructAppello(BaseModel):
    data: str
    data_inizio_iscrizione: str
    data_fine_iscrizione: str
    aula: str
    corso: int


@db_session
def ListaCorsi(corsi) -> dict:
    return {
        "corsi": [{
            "id": corso.id,
            "nome": corso.nome,
            "crediti": corso.crediti,
            "docente": corso.docente.displayName
        } for corso in corsi]
    }


@db_session
def ListaAppelli(appelli) -> dict:
    return {
        "appelli": [{
            "id": appello.id,
            "data": appello.data,
            "data_inizio_iscrizione": appello.data_inizio_iscrizione,
            "data_fine_iscrizione": appello.data_fine_iscrizione,
            "aula": appello.aula,
            "corso": appello.corso.nome,
        } for appello in appelli]
    }


@db_session
def ListaUtenti(utenti) -> dict:
    return {
        "utenti": [{
            "id": utente.id,
            "nome": utente.nome,
            "cognome": utente.cognome,
            "displayName": utente.displayName,
            "email": utente.username,
            "ruolo": utente.ruolo
        } for utente in utenti]
    }
