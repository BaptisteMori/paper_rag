from django.urls import include, path

urlpatterns: list = [
    path("", include("paper_rag.papers.urls")),
]
