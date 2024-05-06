from django.urls import path
from .views import CreateView,DetailsView,SearchView,SortView,FilterView,LoginView

urlpatterns=[
    path("",CreateView.as_view()),
    path("login",LoginView.as_view()),
    path("<int:id>",DetailsView.as_view()),
    path("search",SearchView.as_view()),  # ?name=name
    path("sort",SortView.as_view()),   # ?ordering=name
    path("filter",FilterView.as_view())   #  ?search=name&search=email

]