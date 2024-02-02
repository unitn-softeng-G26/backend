from pony.orm import Database, PrimaryKey, Discriminator, Required, Optional, Set
from datetime import datetime

db = Database("sqlite", "../ci4.db", create_db=True)


class Utente(db.Entity):
    ruolo = Discriminator(int)
    _discriminator_ = 0

    id = PrimaryKey(int, auto=True, size=64)
    email = Required(str, unique=True)
    password = Required(str)
    token = Optional(str)

    nome = Required(str)
    cognome = Required(str)

    @property
    def displayName(self) -> str:
        return f"{self.nome} {self.cognome}"


class Studente(Utente):
    _discriminator_ = 1
    matricola = Required(int, unique=True)

    libretto = Set("Corso", reverse="studenti")
    appelli = Set("Appello", reverse="iscritti")

    def check_libretto(self) -> bool:
        return sum([corso.crediti for corso in self.libretto]) == 180


class Docente(Utente):
    _discriminator_ = 2
    insegnamenti = Set("Corso", reverse="docente")

    @property
    def displayName(self) -> str:
        return f"Prof. {self.cognome}"


class Segreteria(Utente):
    _discriminator_ = 3


class Corso(db.Entity):
    id = PrimaryKey(int, auto=True, size=64)
    nome = Required(str, unique=True)
    crediti = Required(int, default=6, unsigned=True)

    docente = Required(Docente)
    studenti = Set("Studente", reverse="libretto")
    appelli = Set("Appello", reverse="corso")


class Appello(db.Entity):
    id = PrimaryKey(int, auto=True, size=64)
    data = Required(datetime)
    data_inizio_iscrizione = Required(datetime)
    data_fine_iscrizione = Required(datetime)
    aula = Required(str)

    corso = Required(Corso)
    iscritti = Set("Studente", reverse="appelli")


db.generate_mapping(create_tables=True)


if __name__ == "__main__":
    from pony.orm import db_session
    with db_session:
        # Crea studenti se non esistono
        if not Studente.exists():
            print("[DB] Creo studenti di esempio: ", end="")
            Studente(email="filippo.pesavento@studenti.unitn.it",
                     password="5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
                     nome="Filippo", cognome="Pesavento", matricola=123100)
            Studente(email="alessandro.bettale@studenti.unitn.it",
                     password="5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
                     nome="Alessandro", cognome="Bettale", matricola=123101)
            Studente(email="luca.cola@studenti.unitn.it",
                     password="5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
                     nome="Luca", cognome="Cola", matricola=123102)
            print("Fatto.")

        # Crea docenti se non esistono
        if not Docente.exists():
            print("[DB] Creo docenti di esempio: ", end="")
            d1 = Docente(email="paolo.giorgini@unitn.it",
                         password="5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
                         nome="Paolo", cognome="Giorgini")
            d2 = Docente(email="antonio.bucchiarone@unitn.it",
                         password="5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
                         nome="Antonio", cognome="Bucchiarone")
            d3 = Docente(email="alessandro.tomasi@unitn.it",
                         password="5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
                         nome="Alessandro", cognome="Tomasi")
            d4 = Docente(email="marco.patrignani@unitn.it",
                         password="5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
                         nome="Marco", cognome="Patrignani")
            d5 = Docente(email="alberto.montresor@unitn.it",
                         password="5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
                         nome="Alberto", cognome="Montresor")
            d6 = Docente(email="romeo.brunetti@unitn.it",
                         password="5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
                         nome="Romeo", cognome="Brunetti")
            print("Fatto.")

        # Crea segreteria se non esiste
        if not Segreteria.exists():
            print("[DB] Creo segreteria di esempio: ", end="")
            Segreteria(email="segreteria@unitn.it",
                       password="5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
                       nome="Segreteria", cognome="UniTN")
            print("Fatto.")

        # Crea corsi se non esistono
        if not Corso.exists():
            print("[DB] Creo corsi di esempio: ", end="")
            Corso(nome="Analisi 1", crediti=60, docente=d6)
            Corso(nome="Analisi 2", crediti=60, docente=d6)
            Corso(nome="Fisica", crediti=60, docente=d6)
            Corso(nome="Programmazione 1", crediti=60, docente=d5)
            Corso(nome="Programmazione 2", crediti=60, docente=d5)
            Corso(nome="Ingegneria del Software", crediti=60, docente=d1)
            Corso(nome="Algoritmi e Strutture Dati", crediti=60, docente=d5)
            Corso(nome="Basi di Dati", crediti=60, docente=d3)
            Corso(nome="Reti", crediti=60, docente=d2)
            Corso(nome="Sistemi Operativi", crediti=60, docente=d2)

            Corso(nome="Probabilità e Statistica", crediti=30, docente=d1)
            Corso(nome="Programmazione Funzionale", crediti=30, docente=d1)
            Corso(nome="Algebra Lineare", crediti=30, docente=d6)
            Corso(nome="Fondamenti Matematici", crediti=30, docente=d3)
            Corso(nome="Calcolatori", crediti=30, docente=d5)
            Corso(nome="Logica", crediti=30, docente=d3)
            Corso(nome="Sistemi Informativi", crediti=30, docente=d2)
            Corso(nome="Sviluppo Web", crediti=30, docente=d4)
            Corso(nome="Human-Conputer Interaction", crediti=30, docente=d4)
            Corso(nome="Network Security", crediti=30, docente=d4)

            print("Fatto.")

        # Crea appelli se non esistono
        if not Appello.exists():
            print("[DB] Creo appelli di esempio: ", end="")
            Appello(data=datetime(2024, 1, 1, 9, 0), data_inizio_iscrizione=datetime(2023, 12, 15, 0, 0),
                    data_fine_iscrizione=datetime(2024, 12, 31, 23, 59), aula="A101", corso=Corso[1])
            Appello(data=datetime(2024, 1, 1, 9, 0), data_inizio_iscrizione=datetime(2023, 12, 15, 0, 0),
                    data_fine_iscrizione=datetime(2024, 12, 31, 23, 59), aula="A102", corso=Corso[2])
            Appello(data=datetime(2024, 1, 1, 9, 0), data_inizio_iscrizione=datetime(2023, 12, 15, 0, 0),
                    data_fine_iscrizione=datetime(2024, 12, 31, 23, 59), aula="A103", corso=Corso[3])
            Appello(data=datetime(2024, 1, 1, 9, 0), data_inizio_iscrizione=datetime(2023, 12, 15, 0, 0),
                    data_fine_iscrizione=datetime(2024, 12, 31, 23, 59), aula="A104", corso=Corso[4])
            Appello(data=datetime(2024, 1, 1, 9, 0), data_inizio_iscrizione=datetime(2023, 12, 15, 0, 0),
                    data_fine_iscrizione=datetime(2024, 12, 31, 23, 59), aula="A105", corso=Corso[5])
            Appello(data=datetime(2024, 1, 1, 9, 0), data_inizio_iscrizione=datetime(2023, 12, 15, 0, 0),
                    data_fine_iscrizione=datetime(2024, 12, 31, 23, 59), aula="A106", corso=Corso[6])

            print("Fatto.")
