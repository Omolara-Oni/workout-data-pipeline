#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""




@author: omolaraoni
"""
from colorama import Fore,init
import sqlite3
import datetime
import tabulate

init(autoreset=True)

conn = sqlite3.connect('workout_tracker2.db')

def display_menu():
    print(Fore.CYAN + "\nCOMMAND MENU")
    print(Fore.YELLOW + "-" * 50)
    print(Fore.GREEN + "view - View workout by name")
    print(Fore.GREEN + "add - Add a new workout")
    print(Fore.GREEN + "update - Update a workout")
    print(Fore.GREEN + "del - Delete a workout")
    print(Fore.GREEN + "exit - Exit program")
    print(Fore.YELLOW + "-" * 50)
   
#Table for person,workout, set and workout details     
def createTables():
    conn= sqlite3.connect('workout_tracker2.db')
    cur= conn.cursor()
    cur.execute("""CREATE TABLE if not exists Person(
        personID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL UNIQUE
      )
    """)
    
#name is linked to person ID
# #workoutID is linked to evercise put in for that date   
    cur.execute("""CREATE TABLE if not exists Workout(
        workoutID INTEGER PRIMARY KEY AUTOINCREMENT,
        personID INTEGER NOT NULL,
        Category TEXT,
        Exercise TEXT NOT NULL,
        Sets INTEGER,
        Date TEXT DEFAULT (DATE('now')),
        FOREIGN KEY (personID) REFERENCES Person(personID) ON DELETE CASCADE
       )
      """)
# set id is linked to every set for that particular exercise on that date
    cur.execute("""CREATE TABLE if not exists SetTable (
         setID INTEGER PRIMARY KEY AUTOINCREMENT,
         workoutID INTEGER NOT NULL,
         SetNumber INTEGER NOT NULL,
         Weight INTEGER,
         Reps INTEGER NOT NULL,
         FOREIGN KEY (workoutID) REFERENCES Workout(workoutID) ON DELETE CASCADE
         )
    """)
   
    cur.execute("""
        CREATE VIEW IF NOT EXISTS WorkoutDetails AS
        SELECT 
            w.workoutID,
            w.Date,
            p.Name,
            w.Category,
            w.Exercise,
            s.SetNumber,
            s.Weight,
            s.Reps
        FROM Workout w
        JOIN Person p ON p.personID = w.personID
        JOIN SetTable s ON s.workoutID = w.workoutID
    """)

    conn.commit()
    conn.close()
    


def insert_workout():
    conn= sqlite3.connect('workout_tracker2.db')
    cur= conn.cursor()
# add name ( has to be written in letters)   
    while True:
     Name= input("Enter your name: ").strip()
     if all (word.isalpha() for word in Name.split()):
         break
     else:
         print("Invalid input. Please enter letters only.")

#each name has its own unique key which is ther personal id, the same name can't be put in the system again after its been put
#when name is entered,  personID is automatically created for that name 

    cur.execute("SELECT personID FROM Person WHERE Name = ?", (Name,))
#then the system is asked to fetch that name 
    result = cur.fetchone()
# the "result" is the name I assigned to the outcome of the that 
    if result:
        personID = result[0]
    else:
       cur.execute("INSERT INTO Person (Name) VALUES (?)", (Name,))
       conn.commit()
       personID = cur.lastrowid
       print(f"New person '{Name}' added.")  
# asks person what category of workout is being recorded
# only two categories 
    while True:
     Category = input("Is this an Upper Body or Lower Body exercise? ").strip().lower()
     if Category in ["upper body", "lower body"]:
        break
    else:
        print("Invalid input. Please type 'Upper Body' or 'Lower Body'.")        
#then asks for exercise(it should all letters)  
    while True:
     Exercise= input("Enter the exercise: ").strip()
     if all (word.isalpha() for word in Exercise.split()):
         break
     else:
         print("Invalid input. Please enter an exercise using letters only")

# ask the person for date ( can only be in the format YYYY-MM-DD), user can press enter the present date or put in a past date if entering an old workout they havent entered before
    while True:
        custom_date = input("Enter date for this workout (YYYY-MM-DD) or press Enter for today: ").strip()
        if not custom_date:
            date_to_insert = datetime.date.today().isoformat()
            break
        try:
            date_to_insert = datetime.date.fromisoformat(custom_date).isoformat()
            break
        except ValueError:
            print("Wrong. Enter date as YYYY-MM-DD.")

 # info given by person is put into the table
    cur.execute('''
        INSERT INTO Workout (personID, Date ,Category, Exercise)
        VALUES (?, ?, ?, ?)
    ''', (personID, date_to_insert,Category,Exercise))

# then that new workout is found using the workout ID
    workoutID= cur.lastrowid
# then the person put the  number of sets they did for that workout and it has to be greater than 0 
    while True:
     Number_of_sets = input("How many sets did you do for this exercise? ")
     if Number_of_sets.isdigit() and int(Number_of_sets) >0:
        Sets= int(Number_of_sets)
        break
     print("Invalid input. Please put a number greater than 0.")
# the loop is created to link that particular set's weight and reps together 
# for every set they did, the person can put in the weight for it but weight can be 0 or greater than 0 because sometimes you dont use weight for each set

    for SetNumber in range(1, Sets+1):
         while True:
          weight_input = input(f"Enter weight for set {SetNumber}: ")
          if weight_input.isdigit() and int(weight_input) >=0:
            Weight = int(weight_input)
            break
          print("Please enter a valid number.")
# then for every set they did the person put the number of reps 
         while True:
           reps_input = input(f"Enter reps for set {SetNumber}: ")
           if reps_input.isdigit() and int(reps_input) >0:
              Reps = int(reps_input)
              break
           print("Please enter a number greater than 0.")


         cur.execute('''
           INSERT INTO SetTable (workoutID,SetNumber, Weight, Reps)
           VALUES (?, ?, ?, ?)
          ''', (workoutID,SetNumber, Weight, Reps))

   
    conn.commit()
    print(f"Workout added for '{Name}' on {date_to_insert}.\n")
    conn.close()
    
   
def view_workouts_by_name():
    conn = sqlite3.connect('workout_tracker2.db')
    cur = conn.cursor()
 # name first 
 
    Name= input(Fore.CYAN + "Enter the person's name: " ).strip() 
    cur.execute(''' SELECT workoutID,Date, Name, Category, Exercise,SetNumber,Weight, Reps 
            FROM WorkoutDetails
            WHERE Name= ? 
            ORDER BY Date ASC
            ''', (Name,))
 #ordered by date because that how I and my  family look analyze our workouts  
    rows = cur.fetchall()
    if not rows:
        print(Fore.RED + f"No workout data found for this {Name}.\n")
    else:
        print(Fore.YELLOW + f"\nWorkouts for {Name}:\n" )
        headers = ["WorkoutID","Date","Name","Category","Exercise","Set_Number","Weight (lbs)", "Sets", "Reps"]
        print(tabulate.tabulate(rows, headers, tablefmt="fancy_grid", stralign="center", numalign="center"))
    conn.close()

def delete_workouts_by_name():
    conn= sqlite3.connect('workout_tracker2.db')
    cur= conn.cursor()
 # name first     
    Name=input("Enter name of person to delete: ").strip()
    
    cur.execute('''
        DELETE FROM Workout 
        WHERE personID IN (SELECT personID FROM Person WHERE Name=?)
    ''', (Name,))
    
    
    if cur.rowcount ==0:
        print(Fore.RED + f"No workout data found for this {Name}.\n")
    else:
        conn.commit()
        print(f"{Name} and all their workouts have been deleted.\n")
    
    conn.close()
    
  # this deletes all the workouts associated with that person  
    
def update_workout():
    conn= sqlite3.connect('workout_tracker2.db')
    cur= conn.cursor()
# name first    
    Name=input("Enter name to update a workout: ").strip()   
    cur.execute(''' 
        SELECT workoutID, Date, Category, Exercise
        FROM Workout
        WHERE personID IN (SELECT personID FROM Person WHERE Name = ?) 
        ORDER BY Date ASC
    ''', (Name,))
    
    workout= cur.fetchall()
    if not workout:
       print(Fore.RED + f"No workouts found for {Name}.\n")
       conn.close()
       return

    print(f"\nWorkouts for {Name}.\n")
    print(tabulate.tabulate(workout, headers=["ID", "Date", "Category", "Exercise"], tablefmt="grid"))
     
 # so now the person can see a table of all their workouts and the id 
# they enter the ID of the specific workout they want to change   
    workoutID_input= input("\n Enter the ID of the workout to update: ")
    if not workoutID_input.isdigit():
            print("Invalid ID. Try again")
            return
        
    while True:
      Category = input("Is this an Upper Body or Lower Body exercise? ").strip().lower()
      if Category in ["upper body", "lower body"]:
       break
    else:
     print("Invalid input. Please type 'Upper Body' or 'Lower Body'.")
    
    while True:
         Exercise = input("Enter new exercise: ")
         if all (word.isalpha() for word in Exercise.split()):
             break
         else:
             print("Invalid input. Please enter an exercise using letters only")
    while True:
        custom_date = input("Enter date for this workout (YYYY-MM-DD) or press Enter for today: ").strip()
        if custom_date == "":
            date_to_insert = datetime.date.today().isoformat()  # 'YYYY-MM-DD'
            break
        try:
            date_to_insert = datetime.date.fromisoformat(custom_date).isoformat()
            break
        except ValueError:
            print("Wrong. Enter date as YYYY-MM-DD.")
   
    cur.execute('''
        UPDATE Workout
        SET Category = ?, Exercise = ?, Date = ?
        WHERE workoutID = ?
''', (Category, Exercise, date_to_insert, workoutID_input))

    cur.execute('''
     SELECT setID, SetNumber, Weight, Reps
     FROM SetTable
     WHERE workoutID = ?
     ORDER BY SetNumber
''', (workoutID_input,))

    set_list= cur.fetchall()
    
    for s in set_list:
     set_id, SetNumber, old_weight, old_reps = s
     Weight = int(input(f"Enter new weight for set {SetNumber} (old: {old_weight}): "))
     Reps = int(input(f"Enter new reps for set {SetNumber} (old: {old_reps}): "))

     cur.execute('''
        UPDATE SetTable
        SET Weight = ?, Reps = ?
        WHERE setID = ?
     ''', (Weight, Reps, set_id))
     
    conn.commit()
    print(" Workout Updated!")
    conn.close()
 

    
def main():
    createTables()
    display_menu()
    
    while True:
        command = input("Command: ").lower()
        if command == "view":
         view_workouts_by_name()
        elif command == "add":
          insert_workout()
        elif command == "update":
          update_workout()
        elif command == "del":
             delete_workouts_by_name()
        elif command == "exit":
            print('Exiting program........')
            break
        else:
            print("Invalid command. Try again")
        
if __name__ == '__main__':
    main()
                  
             

             
             
        
        