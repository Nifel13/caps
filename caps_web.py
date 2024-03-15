from flask import Flask, render_template, request, redirect, url_for
from caps_problem import CapsProblem
from tqdm import tqdm
from random import randint
from caps_operators import CapsOperator,Swap
from caps_state import proposta,cap,unitat
from typing import Generator
from aima.search import Problem, hill_climbing,simulated_annealing, exp_schedule, astar_search
import pygame
import matplotlib.pyplot as plt
import tempfile
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    solution = None
    if request.method == 'POST':
        # Get the initial state from the form
        initial_state = request.form.get('initial_state')

        # Create an instance of CapsProblem
        problem = CapsProblem(initial_state)

        # Solve the problem
        solution = problem.solve()

    # Render the template
    return render_template('index.html', solution=solution)

if __name__ == '__main__':
    app.run(debug=True)
