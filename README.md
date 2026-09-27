# hep-rag

Semantic search & RAG over scientific papers (INSPIRE-HEP first), with a Django REST API and an MCP server.

Status: work in progress — learning project (Django, embeddings, RAG, MCP).


## Init Environment

```bash
# to use a specific version
poetry env use python3.11

# create environment
python -m venv .venv

# activate the environment
poetry env activate

# install the librairies
poetry install
```

## Migration

Création du fichier de migration :
```bash
python manage.py makemigrations model
```

- 1 faire des ingestions
     - récupérer depuis une source avec leur métadonnées
     - créer des embedding pour le titre+abstract
     - stocker les infos dans la base de données
