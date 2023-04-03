# url - #view - template

from django.urls import path, include
from.views import homepage, contato

urlpatterns = [
    path('', homepage),
    path('contato', contato),

]
