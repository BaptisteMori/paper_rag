from django.urls import include, path

from paper_rag.papers.views.search import search_view

urlpatterns: list = [
    path("", include("paper_rag.papers.urls")),
    path("search/", search_view, name="search"),
]
