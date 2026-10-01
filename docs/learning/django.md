
# Structure

```mermaid
flowchart TD
    A["curl /search/?q=..."] --> B["wsgi.py<br/>(point d'entrée du serveur)"]
    B --> C["middleware<br/>(CommonMiddleware)"]
    C --> D["urls.py<br/>« quelle fonction pour cette URL ? »<br/>→ search_view"]
    D --> E["papers/views.py<br/>lit les paramètres HTTP,<br/>appelle la logique, fabrique la réponse"]

    H["python manage.py search --query ..."] --> I["Command"]
    I --> F

    E --> F["core/search/...<br/>logique métier : embedder, requête, tri"]
    F --> G["core/model/models.py<br/>ORM : les tables PostgreSQL"]
```


## Middleware

Exemple :
```python
# paper_rag/common_middlewares.py

import time

def timing_middleware(get_response):
    def middleware(request):
        start = time.perf_counter()
        response = get_response(request)
        response["X-Duration"] = f"{time.perf_counter() - start:.3f}s"
        return response
    return middleware
```

```python
# paper_rag/settings.py
MIDDLEWARE = [
    "paper_rag.middleware.timing_middleware",
]
```
La fonction `timing_middleware` sera appelé pour chaque requête.


## URLS
- urls.py : associe un chemin à une fonction. Aucune logique.
    -> api blueprint de flask