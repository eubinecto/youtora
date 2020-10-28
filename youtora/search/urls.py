from django.urls import path

from youtora.search import views

urlpatterns = [
    # api for searching on general doc
    path('general_doc/', views.srch_general_doc),
    # add this later
    # re_path('idiom_doc/', views.srch_idiom_doc)
]
