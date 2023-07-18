''' 
Views for Random Pokemon Generator
'''


import os

from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe

# Number of Available Pokemon, established for PokeAPI endpoint
numPokemon = 1010


class IndexView(generic.TemplateView):

    '''
    View for Homepage of Random Generator:
    Methods:
    - get_context_data() to create a context var to pass random pokemon pulled from API
    '''
    template_name = "randomgen/home.html"
    
    def get_context_data(self, **kwargs):
        context = self.get_context_data()
        return context
