## Database (local)

### Installation

1. Create virtual environment.

```bash
python3.13 -m venv db-venv
```

2. Install dependencies.

```bash
pip install -r requirements-db.txt
```

### Deploy MySQL

You need Docker.

```bash
./db/deploy_db_local.sh
```

### Create & Populate Database

```bash
./db/populate_db_local.py
```

### Check contents (very dirty)

(number of rows, columns names, example data)

```bash
./db/check_db_contents.py
```

## Cache load (local)

1. Run database (as explained before).
2. Create virtual environment with backend dependencies.

```bash
python3.13 -m venv backend-venv
```

3. Activate virtual environment.

```bash
source backend-venv/bin/activate
```

4. Install backend dependencies.

```bash
pip install -r requirements-backend.txt
```

4. Run flask server.

```bash
python3 backend/server.py
```

5. Run example client.

(Asks for database data and loads it into local IndexedDB).

Client -> Flask -> DB -> Flask -> Client -> IndexedDB

```bash
firefox cache/basic-web-server.html
```

