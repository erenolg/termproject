import time
import answerK_func


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __str__(self):
        return self.username

    def remove_account(self):
        """
        Removes user from database

        Returns
        -------
        db: users dictionary after update
        """
        db = answerK_func.csv_to_dict("database.txt")
        counter = 0
        control = input("Enter password: ")
        if control == db[self.username]:
            db.pop(self.username)
            with open("database.txt", "w") as f:
                print("Deleting..")
                for k, v in list(db.items()):
                    if k == list(db.items())[-1][0]:
                        f.write(k + "," + v)
                    else:
                        f.write(k + "," + v + "\n")
            with open("statics.txt", "r") as f1:
                lines = f1.readlines()
                with open("statics.txt", "w") as f2:
                    for i in lines:
                        if i.strip().split(",")[0] != self.username:
                            f2.write(i)
            time.sleep(0.5)
            print("Account is removed successfully..")
            time.sleep(0.5)
            return db
        elif control == "q":
            return 0
        else:
            print("Wrong password!..")
            time.sleep(0.5)
            print("Try again..")
            counter += 1
            if counter > 3:
                print("Give a break..!")
                return 0
            self.remove_account()

    def change_password(self, db):
        """
        Changes password of user

        Parameters
        ----------
        db: the dictionary with key:username and values:password

        Returns
        -------
        db: the dictionary after update
        """
        control = input("Enter your old password: ")
        if control == self.password:
            new_p = input("Enter new password: ")
            if control != new_p:
                db[self.username] = new_p
                with open("database.txt", "w") as f:
                    for k, v in db.items():
                        f.write(k + "," + v + "\n")
                print(f"Password changed successfully..")
                return db
            else:
                print(f"New password can't be same as old one.. Try again!")
                time.sleep(0.5)
                self.change_password(db)
        else:
            print("Wrong password!")
            self.change_password(db)

    def my_grades(self):
        """
        Gets all grades of user  and returns as a list of integers

        Returns
        -------
        my_grades: list of integers with all grades of user
        """
        with open("statics.txt", "r") as f:
            lines = f.readlines()
            my_grades = []
            for i in lines:
                if i.strip().split(",")[0] == self.username:
                    for j in i.strip().split(",")[1:]:
                        my_grades.append(int(j.split("-")[0]))
            return my_grades

    def average_time(self):
        """
        finds average of test times
        Returns
        -------
        ave_time: average of all test times of user
        """
        with open("statics.txt", "r") as f:
            lines = f.readlines()
            my_times = []
            for i in lines:
                if i.strip().split(",")[0] == self.username:
                    for j in i.strip().split(",")[1:]:
                        my_times.append(float(j.split("-")[1]))
            ave_time = sum(my_times) / len(my_times)
            return ave_time
