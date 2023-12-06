# Ci4 Backend
Server code for the Ci4 backend, APIs and database.

# Technologies used
- Server code: Python 3.11
- Database: SQLite3 (+ ORM library)
- API Server: FastAPI, Uvicorn engine
- API Documentation: Swagger UI
- Other: nginx (reverse proxy)

# Dati di test
Per creare e popolare il database con alcuni dati di test (studenti, docenti, segreteria ed esami), eseguire il seguente comando:
```bash
python3.11 modules/database.py
```
