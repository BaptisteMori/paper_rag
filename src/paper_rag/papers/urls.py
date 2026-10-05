from django.urls import path

from paper_rag.papers.views.search import search_view

urlpatterns: list = [
    path("search/", search_view, name="search"),
]
