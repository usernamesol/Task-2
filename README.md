How to use app:
Create .env with fiels:
  PG_USER - postgres username.
  PG_PASSWORD - postgres username password.
  PG_SERVER - postgres server.
  PG_PORT - postgres port.
  PG_DB_NAME - postgres database name.
  PG_TEST_DB_NAME - postgres database name for tests.
  
  SECRET_KEY - secret key for jwt token.
  ALGORITHM - algorithm for jwt token.
  
  USER_FILES_PATH - path to users files.
  TEST_FILES_PATH - path to users files for tests.
  TEST_FILE - path to file for tests.

Create python environment
Use python unvironment
Make revisions by alembic (alembic revision)
Use upgrade by alembic (alembic upgrade head)
Start uvicorn server (uvicorn main:app)
