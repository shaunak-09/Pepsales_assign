from django.urls import path
from .views import CreateView,DetailsView,SearchView,SortView,FilterView

urlpatterns=[
    path("",CreateView.as_view()),
    path("<int:id>",DetailsView.as_view()),
    path("search",SearchView.as_view()),  # ?search=name
    path("sort",SortView.as_view()),   # ?ordering=name&ordering=price
    path("filter",FilterView.as_view())  #  ?search=name&search=category&search=description
]