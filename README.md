# hep-rag

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



- 1 faire des ingestions
     - récupérer depuis une source avec leur métadonnées
     - créer des embedding pour le titre+abstract
     - stocker les infos dans la base de données
- résoudre l'erreur : ERROR    | paper_rag.ingester.ingester | Paper 311 failed (5422 chars): Ollama error 400: {"error":"the input length exceeds the context length"}
- Ajoute de la doc Baptiste
## ingestion

```bash
python manage.py ingest --title "dark matter" --limit
```

