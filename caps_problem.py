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
import random
import pandas as pd

def read_caps(path):
    caps = []
    caps_df = pd.read_csv(path)
    for i in range(len(caps_df)):
        persona = caps_df.iloc[i]
        caps.append(cap(persona["nom"], persona["sexe"], str(persona["preferencia"]).split(","), str(persona["persones_si"]).split(","), str(persona["persones_no"]).split(",")))
    return caps

def caps_to_csv(llista):
    caps = []
    for cap in llista:
        caps.append([cap.nom, cap.sexe, ",".join(cap.pref_unit), ",".join(cap.pers_si), ",".join(cap.pers_no)])
    df = pd.DataFrame(caps, columns=["nom", "sexe", "preferencia", "persones_si", "persones_no"])
    df.to_csv("caps_2.csv", index=False)


COLORS = [(245, 147, 66), (171, 171, 171), (255, 255, 54), (18, 101, 255), (255, 0, 47), (17, 145, 0)]

def draw_best_unitats(best):
        # Initialize pygame
        pygame.init()

        # Set the width and height of the screen (width, height)
        size = (700, 700)
        screen = pygame.display.set_mode(size)

        # Loop until the user clicks the close button
        done = False

        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()

        # -------- Main Program Loop -----------
        while not done:
            # --- Main event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

            # --- Game logic should go here

            # --- Drawing code should go here
            # First, clear the screen to white. Don't put other drawing commands
            # above this, or they will be erased with this command
            screen.fill((255, 255, 255))

            # Define the font
            font = pygame.font.Font(None, 25)

            # Draw the "unitats"
            for i, uni in enumerate(best.unitats):
                # Choose a color
                color = COLORS[i % len(COLORS)]

                # Calculate the height of the rectangle based on the number of "caps"
                rect_height = len(uni.caps) * 30 + 50 + 10

                # Draw a rectangle
                pygame.draw.rect(screen, color, [50, 50 + i * 115, 200, rect_height])  # Increased space between rectangles here

                # Draw the "caps"
                for j, capos in enumerate(uni.caps):
                    # Create a text object
                    text = font.render(capos.nom, True, (0, 0, 0))

                    # Calculate the y-position of the text
                    text_y = 50 + i * 115 + j * 30  # Increased space between rectangles here

                    # Draw the text object
                    screen.blit(text, [60, text_y])
            # draw the heuristic value
            text = font.render("Heuristic: " + str(best.heuristic()), True, (0, 0, 0))
            screen.blit(text, [400, 300])
            # --- Go ahead and update the screen with what we've drawn
            pygame.display.flip()
        
            # --- Limit to 60 frames per second
            clock.tick(60)

        # save the image 
        pygame.image.save(screen, "Best_unitats/unitats"+str(random.randint(0,100))+".png")
        pygame.quit()

class CapsProblem(Problem):

    def  __init__(self, initial_state:proposta):
        super().__init__(initial_state)
        
    
    def actions(self, state: proposta) -> Generator[Swap, None, None]:
        return state.generate_actions()

    def result(self, state: proposta, action: CapsOperator) -> proposta:
        return state.apply_actions(action)

    def value(self, state: proposta) -> float:
        return -state.heuristic()

    def goal_test(self, state: proposta) -> bool:
        return False

if __name__ == '__main__':

    llista_caps = [cap("Edu","M",["pic","truc","ring","llid","enx","cill"],["Pere"],["Victor"]),
                   cap("Berta","F",["ring","pic","llid","truc","enx","cill"],["Josemi"],["Marc Mateos","Hector F"]),
                   cap("Anna","F",["ring","llid","enx","pic","cill","truc"],["Paula"],["Victor"]),
                   cap("Paula","F",["ring","llid","enx","pic","cill","truc"],["Gerard"],["Hector F","Marc Mateos"]),
                   cap("Ramon","M",["cill","ring","pic","llid","enx","truc"],["Gerard"],["Victor"]),
                   cap("Gerard","M",["cill","enx","llid","ring","pic","truc"],["Ramon"],[]),
                   cap("Marti","M",["pic","truc","ring","llid","enx","cill"],["Ramon"],["Victor"]),
                   cap("Marc Mateos","M",["ring","pic","llid","truc","enx","cill"],["Anna"],["Edu","Paula","Berta","Ramon"]),
                   cap("Marc Rodriguez","M",["enx","cill","llid","ring","pic","truc"],["Berta","Gerard"],[]),
                   cap("Josemi","M",["ring","llid","pic","enx","cill","truc"],["Berta","Edu"],["Victor","Marc Mateos"]),
                   cap("Hector F","M",["ring","llid","pic","enx","cill","truc"],["Berta M"],["Elna"]),
                   cap("Berta M","F",["cill","enx","llid","ring","pic","truc"],["Pere"],[]),
                   cap("Mario","M",["pic","ring","llid","enx","cill","truc"],["Neus"],["Victor","Marc Mateos"]),
                   cap("Neus","F",["ring","llid","enx","cill","pic","truc"],["Paula","Ramon"],["Marc Martinez"]),
                   cap("Pere","M",["pic","truc","ring","llid","enx","cill"],["Elna"],["Hector I"]),
                   cap("Elna","F",["pic","truc","ring","llid","enx","cill"],["Pere"],["Victor","Hector I"]),
                   cap("Marc Martinez","M",["ring","cill","llid","pic","enx","truc"],["Berta M"],["Victor","Neus"]),
                   cap("Victor","M",["truc","pic","ring","llid","enx","cill"],["Hector I"],["Elna","Josemi"]),
                   cap("Hector I","M",["truc","pic","ring","llid","enx","cill"],["Victor","Pere"],["Victor"]),
                   cap("Ligia","F",["cill","enx","llid","ring","truc","pic"],["Gerard"],["Marc Mateos"]),
                   cap("Mysa","F",["llid","enx","cill","ring","truc","pic"],[],[])]
    

    llista_caps = read_caps("caps_33.csv")
    print(llista_caps)
    best = []
    lowest = 10000000
    for i in tqdm(range(100), desc="Processing"):
        a=proposta(n=21,caps_predeterminats=llista_caps, rand_seed=i)
        a.crear_unitats()
        n=hill_climbing(CapsProblem(a))
        best.append((n, n.heuristic()))
    
    best = sorted(best, key=lambda x: x[1])
    
    print("Unitats finals:")
    print(best[0][0].unitats)
    print("Heuristic final: ",best[0][1])

    
    #plt.plot(n.afinitat_persones,n.afinitat_unitats,n.unitats_mixtes)

    unitats = best[0][0].afinitat_unitats()
    persones = best[0][0].afinitat_persones()
    mixtes = best[0][0].unitats_mixtes()

    # barplot of the scores
    plt.figure(figsize=(10, 5))
    plt.bar("Unitats", unitats, width=0.5)
    plt.bar("Persones", persones, width=0.5)
    plt.bar("Mixtes", mixtes, width=0.5)
    plt.title("Puntacions")
    plt.ylabel("Puntuació")
    plt.xlabel("Tipus de puntuació")
    plt.show()    
    for i in range(7):
        draw_best_unitats(best[i][0])


