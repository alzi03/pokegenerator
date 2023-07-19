''' 
Views for Random Pokemon Generator
'''


import os

from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe

import random
import requests
import pokebase as pb
import pprint

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
        context = super().get_context_data(**kwargs)
        
        pokemon = self.get_pokemon_image()
        print(context)
        return context

    def get_pokemon_image(self):
        id = random.randint(0, numPokemon)
        # Argument: id
        pokemon = pb.pokemon(id_or_name=id)
        
        json = {
            'id': pokemon.id,
            'sprite': pokemon.sprites.front_default
        }
        
        return json
        
        
        
    def post(self, request, **kwargs):
        return
