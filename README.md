## Database (local)

### 1. Install dependencies

1. Create virtual environment.

```bash
python3.13 -m venv db-venv
```

2. Activate the venv.

```bash
source db-venv/bin/activate
```

3. Install dependencies.

```bash
pip install -r requirements-db.txt
```

### 2. Deploy MySQL

You need Docker.

```bash
./db/deploy_db_local.sh
```

### 3. Create & Populate Database

```bash
./db/populate_db_local.py
```

### 4. Check contents (very dirty)

(number of rows, columns names, example data)

```bash
./db/check_db_contents.py
```

