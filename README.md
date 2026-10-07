# paper_rag

Semantic search & RAG over scientific papers (INSPIRE-HEP first), with a Django REST API and an MCP server.

Status: work in progress — learning project (Django, embeddings, RAG, MCP).


## Init Environment

```bash
# create environment
python -m venv .venv

# to use a specific version
poetry env use python3.12

# activate the environment
poetry env activate

# install the librairies
poetry install
```

## Database

```bash
# the compose file is ready to use 
docker compose --env-file .env up -d 

```

```bash
# To stop it:
docker compose down
# use the -v to clean volume if needed
```


## Migration

Création du fichier de migration :
```bash
python manage.py makemigrations model
python manage.py migrate model
```

## ingestion

```bash
python manage.py ingest --title "dark matter" --limit
```

