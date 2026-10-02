import httpx
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from paper_rag.papers.search.search import SearchHit, hit_to_dict, search


# GET /search?q=...
@require_GET
def search_view(request):
    query: str = request.GET.get("q", "").strip()
    if not query:
        return JsonResponse({"error": "missing 'q'"}, status=400)

    try:
        k: int = int(request.GET.get("k", 5))
    except ValueError:
        return JsonResponse({"error": "'k' must be an integer"}, status=400)
    k = max(1, min(k, 50))

    try:
        hits: list[SearchHit] = search(query, k=k, model=request.GET.get("model"))
    except (ValueError, KeyError) as e:  # Unknown model
        return JsonResponse({"error": str(e)}, status=400)
    except (RuntimeError, httpx.HTTPError) as e:  # Embedder down
        return JsonResponse({"error": f"embedder failed: {e}"}, status=502)

    return JsonResponse({"query": query, "results": [hit_to_dict(h) for h in hits]})
