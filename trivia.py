# -*- coding: utf-8 -*-

import csv
from numpy import random
import re
from time import sleep

class Player:
    
    def __init__(self, id, score):
        self.id = id
        self.score = score
        
    def set_name(self):
        self.name = input(f"Enter Player {self.id + 1}'s Name: \n")
        
    def correct_answer(self):
        self.score += 1
        
    def display_score(self):
        print(f"{self.name} - {self.score} Points.")
        
class Question:
    
    def __init__(self, id, question, A, B, C, Correct):
        self.id = id
        self.question = question
        self.A = A
        self.B = B
        self.C = C
        self.Correct = Correct
        
    def ask_question(self):
        print(self.question)
        print(f"A: {self.A}\nB: {self.B}\nC: {self.C}")
    
        while True:
            try:
                answer = input("Answer: ").upper()
                print()
                if not re.search("[A-C]", answer):
                    raise ValueError
                break
            except ValueError:
                print("Incorrect choice. Please try again.")
                
        if getattr(self, answer) == self.Correct:
            return True
        else:
            return False
        
def initiate_players():
    
    players_list = []
    
    #Get the number of players. Must be between 1 and 4.
    while True:
        try:
            players = int(input("How many people are playing?\n"))
            if players < 1 or players > 4:
                raise ValueError
            break
        except ValueError:
            print("Please enter a number between 1 and 4.")
    
    #Set the name of each player.
    for i in range(players):
        players_list.append(Player(i, 0))
        players_list[i].set_name()
        
    print("\nThis is the list of players: ")
      
    #Print out the list of players      
    for item in players_list:
        print(f"Player {item.id + 1}: {item.name}")
      
    #Ask if players have been input correctly. If not, rerun function to get correct input.
    while True:
        try:
            correct = input("Is this correct? Y/N\n").upper()
            if re.search("^Y(ES)?", correct):
                return players_list
            elif re.search("^N(O)?", correct):
                return initiate_players()
            else:
                raise ValueError
        except ValueError:
            print("Invalid choice. Please try again.")
    
def initiate_questions(reader, players):
    
    questions_list = []
    
    used_numbers = []
    
    while True:
        try:
            questions = int(input("How many questions would you like?\n"))
            print()
            if questions < 3  or questions > 10:
                raise ValueError
            break
        except ValueError:
            print("Please enter a number between 3 and 10.")
    
    id_counter = 0
    
    while len(questions_list) < questions * players:
        #Get a question at random from the database.
        current_number = random.randint(0, 2500)
        
        if current_number not in used_numbers:
            questions_list.append(Question(id_counter, reader[current_number]["Question"],\
                                       reader[current_number]["1"], reader[current_number]["2"],\
                                       reader[current_number]["3"], reader[current_number]["Correct Answer"]))
            used_numbers.append(current_number)
            id_counter += 1

    return questions_list

def display_scores(players_list):
    
    scoreboard = {}
       
    for item in players_list:
        scoreboard[item.name] = item.score

    sorted_scoreboard = sorted(scoreboard.items(), key=lambda x: x[1], reverse = True)
    
    print("------------\nSCOREBOARD\n------------")
    for item in sorted_scoreboard:
        print(f"{item[0]}: {item[1]} points.")
        print("------------")
        continue_game = input("Press Enter to continue...")
    print()
    
    
    return scoreboard
        
     
def main():
    
    data_file = list(csv.DictReader(open("trivia.csv", "r")))
    
    players_list = initiate_players()
    
    questions_list = initiate_questions(data_file, len(players_list))
    
    for i in range(len(questions_list)):
        current_question = questions_list[i].ask_question()
        scoreboard = display_scores(players_list)
            
    return 0

main()


