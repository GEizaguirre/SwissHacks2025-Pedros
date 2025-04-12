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

