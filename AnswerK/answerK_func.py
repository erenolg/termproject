import datetime
import time
from tabulate import tabulate
import random
from answerK_user import User
import matplotlib.pyplot as plt


def quiz(branch):
    """
    Randomly chooses 7 questions from text file and according to user selections,
    returns grade and time spent during test
    Each question corresponds to 10 point, max grade is 70
    No answers will be graded as pass (0)
    Parameters
    ----------
    branch: The file which contains questions

    Returns
    -------
    grade: Total point taken by user
    total time: spent time during test
    """
    with open(branch, "r", encoding="utf-8") as file:
        questions = random.sample(file.readlines(), k=7)
        grade = 0
        start = time.time()
        true, false, blank = 0, 0, 0
        for num, question in enumerate(questions):
            time.sleep(0.5)
            f = lambda x: "\n".join(x)
            print(f"{num+1}-", f(question.strip().split(",")[:5]))
            answer = input("Your answer: ").lower()
            if answer not in "abcd":
                print("Wrong key, be careful..")
                time.sleep(0.8)
                print(f"{num+1}-", f(question.strip().split(",")[:5]))
                answer = input("Your answer: ").lower()
            if answer == question.strip().split(",")[5]:
                grade += 10
                true += 1
            elif answer == "":
                blank += 1
        end = time.time()
        total_time = f"{end - start:.2f}"
        print(f"True: {true} / False: {7 - true - blank} / Passed: {blank}")
        time.sleep(1)
        print(f"You've completed test in {total_time} seconds\nGrade: {grade}..")
        return grade, total_time


def sketch_graph(user):
    """
    Plots the progress of user
    Parameters
    ----------
    user: The object to be plotted

    """
    grades = user.my_grades()
    plt.plot([i+1 for i in range(len(grades))], grades, marker="D", color="purple", mfc="cyan", mec="purple")
    plt.xticks([i+1 for i in range(len(grades))])
    # determine fontdicts for title and labels
    font1 = {'family': 'serif', 'color': 'red', 'size': 20}
    font2 = {'family': "serif", "color": "green", "size": 13}
    plt.title(user.username, fontdict=font1)
    # y axis will differ from 0 to 70 which represent grade
    plt.ylim(0, 70)
    plt.xlabel("Attempts", fontdict=font2)
    plt.ylabel("Grade", fontdict=font2)
    plt.show()


def greetings():
    """
    Template of main page
    no args
    no returns
    """
    print(datetime.date.today(), end="\t")
    hour = time.localtime()[3]
    if hour <= 6:
        print("Have a nice night!".center(70), end="\n\n")
    elif hour > 18:
        print("Have a nice evening!".center(70), end="\n\n")
    else:
        print("Have a nice day!".center(70), end="\n\n")
    greeting = "Hello, Welcome to AnswerK"
    g = greeting.center(95, "-")
    print("(q) for quit")
    print(g, end="\n\n\n")
    return 0


def csv_to_dict(file):
    """
    Takes csv and convert it to dictionary
    Parameters
    ----------
    file: csv file that contains username,password of users

    Returns
    -------
    db: A dictionary with key of username and value of password
    """
    with open(file, "r") as f:
        usernames = []
        passwords = []
        try:
            for i in f:
                usernames.append(i.split(",")[0])
                passwords.append(i.split(",")[1].strip())
            db = dict(zip(usernames, passwords))
        except IndexError:
            db = {}
    return db


def csv_to_dict_stat():
    """
    Convert csv of stats into TABLE with headers of 'Username', 'Grade(Average)', 'Test Solved'
    Then prints table
    """
    with open("statics.txt", "r") as f:
        grades = {}
        for i in f.readlines():
            how_many = len(i.split(",")) - 1
            if how_many > 0:
                grades[i.split(",")[0]] = f"{sum([float(j.split('-')[0]) for j in i.strip().split(',')[1:]]) / how_many}-{how_many}"
        # Template of table
        table = [[0, 0, 0] for i in range(len(list(grades)))]
        for j in range(len(grades)):
            table[j][0] = list(grades.items())[j][0]
            table[j][1], table[j][2] = list(grades.items())[j][1].split("-")
        add_rank = list(filter(lambda x: int(x[2]) >= 2, table))
        add_rank.sort(key=lambda x: float(x[1]), reverse=True)
        col_names = ["Username", "Grade", "Test Solved"]
        print(tabulate(add_rank, headers=col_names))


def main_menu(db):
    """
    Control if user already has an account
    Parameters
    ----------
    db: A dictionary with keys:username and values:password

    Returns
    -------
    login, if user already has an account
    new_account, if user has no account
    0, 0 for quit
    """
    switch = True
    while switch:
        has_account = input("Do you already have an account? (Y / N): ").lower()
        if has_account == "y":
            return login(db)
        elif has_account == "n":
            return new_account(db)
        elif has_account == "q":
            return 0, 0
        else:
            continue


def new_account(db):
    """
    Wants user to enter username and password for new account.
    If everything is OK, save user to database

    Parameters
    ----------
    db: dictionary with keys:username and values:password

    Returns
    -------
    new db: dictionary after added new user
    user: the User object
    """
    with open("database.txt", "a") as f:
        print("Sign-up".center(40, "-"))
        username = input("Create an username: ")
        password = input("Create a password: ")
        confirm = input("Confirm your password: ")
        if username in db.keys():
            print("This username was taken, please try new one..")
            time.sleep(0.5)
            new_account(db)
        else:
            if password != confirm:
                print("Passwords don't match, please try again!..")
                time.sleep(0.5)
                new_account(db)
            elif len(password) < 6 or len(password) > 15:
                print("Length of password should between 6-15, try again..")
                time.sleep(0.5)
                new_account(db)
            else:
                print(f"Registration complteted successfully, welcome {username}")
                user = User(username, password)
                with open("statics.txt", "a") as f1:
                    if len(db) != 0:
                        f1.write(f"\n{username}")
                    else:
                        f1.write(f"{username}")
                    time.sleep(1)
                    f.write(username + "," + password + "\n")
                    new_db = csv_to_dict("database.txt")
                    return new_db, user



def login(db):
    """
    If user information are true, directs user to application

    Parameters
    ----------
    db: dictionary with keys:username and values:password

    """
    counter = 0
    while True:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        if username not in db.keys():
            print("Username can't be found, please try again!")
            continue
        else:
            if password == db[username]:
                print(f"Welcome back {username}..")
                user = User(username, password)
                return db, user
            else:
                counter += 1
                if counter == 3:
                    print("You've made many attempts, give a break!")
                    break
                print("Wrong password, try again!")


def main_page(db, user):
    """
    Menu of application

    Parameters
    ----------
    db: dictionary with keys:username and values:password
    user: an object of User class
    """
    if db == 0:
        return 0
    print(f"""
    a) Test yourself
    b) Rank Table
    c) My Stats
    d) Settings
    q) Log out
    """)
    selection = input("Selection: ").lower()
    if selection == "a":
        print(f"""
        a) Sport
        b) Culture
        c) Programming
        d) Menu
        """)
        selection1 = input("Selection: ").lower()
        if selection1 in "abc":
            print(f"Test is starting at 2 seconds")
            time.sleep(2)
            if selection1 == "a":
                statistics(user, *quiz("sport.txt"))
            elif selection1 == "b":
                statistics(user, *quiz("culture.txt"))
            else:
                statistics(user, *quiz("programming.txt"))
            time.sleep(1)
            print("You're hosting to main page..")
            time.sleep(1)
            main_page(db, user)
        elif selection1 == "d":
            main_page(db, user)
    elif selection == "b":
        csv_to_dict_stat()
        selection1 = input("\nAny key for main menu\n").lower()
        if selection1:
            main_page(db, user)
    elif selection == "c":
        sketch_graph(user)
        if len(user.my_grades()) == 0:
            print(f"Applied Tests: {len(user.my_grades())}\nNo data found!")
        else:
            print(f"Average Grade: {(sum(user.my_grades()) / len(user.my_grades())):.2f}")
            print(f"Average Time: {user.average_time():.2f}")
            print(f"Applied Tests: {len(user.my_grades())}")
        selection1 = input("\nAny key for main menu\n").lower()
        if selection1:
            plt.close()
            main_page(db, user)
    elif selection == "d":
        print("""
        a) Change password
        b) Remove account
        c) Back to menu
        """)
        selection2 = input("Selection: ").lower()
        if selection2 == "a":
            user.change_password(db)
            time.sleep(1)
            print("You are returning to menu..")
            time.sleep(1)
            main_page(db, user)
        elif selection2 == "b":
            key = user.remove_account()
            time.sleep(0.5)
            if type(key) == dict:
                print("\n" * 3)
                greetings()
                main_page(*main_menu(csv_to_dict("database.txt")))
            else:
                main_page(db, user)
        elif selection2 == "c":
            main_page(db, user)
        else:
            print("Wrong key, you are hosting to menu..")
            main_page(db, user)
    elif selection == "q":
        greetings()
        main_page(*main_menu(csv_to_dict("database.txt")))
    else:
        print("Wrong key..")
        main_page(db, user)


def statistics(user, grade, t_time):
    """
    Writes data of quiz to database for statistics

    Parameters
    ----------
    user: User object
    grade: Grade of user in quiz
    t_time: time spent during test
    """
    with open("statics.txt", "r") as f:
        file = f.readlines()
        to_change = ""
        with open("statics.txt", "w") as f1:
            for i in file:
                if i.strip().split(",")[0] != user.username:
                    f1.write(i)
                else:
                    if file.index(i) != len(file)-1:
                        to_change = f"\n{i.strip()},{grade}-{t_time}"
                    else:
                        to_change = f"{i.strip()},{grade}-{t_time}"
            with open("statics.txt", "w") as f2:
                f1.write(to_change)
    return 0