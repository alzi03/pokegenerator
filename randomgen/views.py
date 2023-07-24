''' 
Views for Random Pokemon Generator
'''


import os
from typing import Any, Dict

from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe

import random
import requests
import pokebase as pb
import pprint

from .models import GuessStreak

from .forms import GuessForm

# Number of Available Pokemon, established for PokeAPI endpoint
numPokemon = 1010


class IndexView(generic.TemplateView):
    '''
    View for Homepage of Random Generator:
    Methods:
    - get_context_data() to create a context var to pass random pokemon pulled from API
    '''
    template_name = "randomgen/home.html"
    
    id = random.randint(0, numPokemon)
    context = {}
    current_guess = None

    def get_context_data(self, **kwargs):
        self.context = super().get_context_data(**kwargs)

        pokemon = self.get_pokemon_image()
        pokemon['form'] = GuessForm()
        self.context['pokemon'] = pokemon

        # setting current guess streak
        self.set_guess_streak()

        print(self.current_guess.streak)

        return self.context
    def get_pokemon_image(self):
        # arg: id
        pokemon = pb.pokemon(id_or_name=self.id)
        json = {
            'id': pokemon.id,
            'sprite': pokemon.sprites.front_default,
            'name': pokemon.name
        }
        
        return json
    
    def set_guess_streak(self):
        streaks = GuessStreak.objects.all()
        if streaks:
            self.current_guess = streaks.last()
        else:
            self.current_guess = GuessStreak(streak=0)  # default 0 streak
            self.current_guess.save()

    def post(self, request, **kwargs):
        form = GuessForm(request.POST)

        context = self.get_context_data()

        if form.is_valid():
            form_data = form.cleaned_data
            name = context['pokemon']['name']
            valid_guess = name == form_data['guess']

            if not valid_guess:
                q = GuessStreak(streak=0)  # default 0 streak
                q.save()
                return redirect("/randomgen")
            else:
                streak = self.current_guess.streak + 1
                
                # updating streak
                self.current_guess.streak = streak
                self.current_guess.save()
                
                # updating name
                self.current_guess.name = name
                self.current_guess.save()
                     
                return redirect(reverse('randomgen:correct_guess', kwargs={'pk': self.current_guess.pk}))

class CorrectGuess(generic.DetailView):
    
    model = GuessStreak
    template_name = "randomgen/correct_guess.html"
    guess = None
    name = ''
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(CorrectGuess, self).get_context_data(**kwargs)
        
        self.guess = context['guessstreak']
        self.name = self.guess.name
        
        
        pokemon = self.get_pokemon_image()
        context['pokemon'] = pokemon
        
        return context
        
    def get_pokemon_image(self):
        # arg: id
        pokemon = pb.pokemon(id_or_name=self.name)
        json = {
            'sprite': pokemon.sprites.front_default,
            'name': pokemon.name,
            'height': pokemon.height,
            'weight': pokemon.weight,
            'abilities': [{'ability':i.ability.name, 'hidden': i.is_hidden} for i in pokemon.abilities]
        }
        
        return json
    
    
