import csv
import random
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

@app.route("/") #displays the home page when the website is first opened
def home():
    return render_template("home.html")

@app.route("/register",methods=["GET","POST"]) #runs the register function on the register page
def register():
    if request.method == "POST":
        username = request.form["username"] #inputs are taken as request forms
        password = request.form["password"]
        userFile = open("student.csv", "r") #opens the csv file to be read from
        datareader = csv.reader(userFile, delimiter=",")
        users = []
        num = 0
        exist = False
        for row in datareader:
            if row: #only appends row if row is not empty
                users.append(row) #appends all the rows in the csv file to the array users
        if len(users) > 0: #only checks csv array if it is not empty
            for i in range(len(users)):
                if users[i][1].lower() == username.lower(): #compares the username inputted to the usernames in the csv file
                    exist = True
                    return redirect(url_for("login")) #user redirected to login page
                num = num + 1

        if exist == False:
            num = str(num)
            new_row = [num, username, password, 3, 0] #defines the user's details and all the fields necessary
            with open ("student.csv", "a") as csvfile: #opens the csv file to be written to
                my_writer = csv.writer(csvfile, delimiter = ",") #adds the user's details as a new row in the csv file
                my_writer.writerow(new_row)
        return redirect(url_for("home"))
    return render_template("register.html")

@app.route("/login",methods=["GET","POST"]) #runs the login function on the login page
def login():
    if request.method == "POST":
        username = request.form["username"] #inputs are taken as request forms
        password = request.form["password"]
        userFile = open("student.csv", "r") #opens the csv file to be read from
        datareader = csv.reader(userFile, delimiter=",")
        users = []
        for row in datareader:
            if row: #only appends row if row is not empty
                users.append(row) #appends all the rows in the csv file to the array users
        for i in range(len(users)):
            if users[i][1].lower() == username.lower() and users[i][2] == password: #needs to check if usernames matches and if password is exactly the same
                session["ID"] = int(users[i][0]) #ID is stored as a session to be used in every page on the website when the user is logged in
                return redirect(url_for("home"))
        return redirect(url_for("register"))
    return render_template("login.html")

app.secret_key = "devkey" #used to hash the session cookie

@app.route("/quiz/start", methods=["GET", "POST"]) #runs the quizSart function on the quizStart page
def quizStart(): #page to allow the user to coose the number of questions before the quiz
    if "ID" not in session: #redirects the user to log in if they try and access the quiz without logging in
        return redirect(url_for("login"))
    if request.method == "GET": #gets input from quizStart.html
        return render_template("quizStart.html")
    session["limit"] = int(request.form["limit"]) #gets input from quizStart.html and stores as session to be used in quizPage()
    ID = session["ID"] #session variables defined to be used in quizPage()
    session["points"] = 0
    session["correct"] = 0
    session["number"] = 0
    userFile = open("student.csv", "r")
    datareader = csv.reader(userFile, delimiter=",")
    users = []
    for row in datareader:
        users.append(row)
    level = users[ID][3] #stores the user's level to use when selecting questions
    level = int(level)
    
    quizFile = open("quiz.csv", "r")
    datareader = csv.reader(quizFile, delimiter=",")
    quiz = []
    for row in datareader:
        quiz.append(row)
    questionsID = [[],[]] #defining 2D array where questions will be sorted based on level
    for i in range(len(quiz)):
        if int(quiz[i][1]) == level:
            questionsID[0].append(i) #fisrt index stores questions with the same level as the user's level
        else:
            questionsID[1].append(i) #second index holds questions of all other levels

    session["normal"] = questionsID[0] #the two arrays are stored as separate sessions to be used in quizPage()
    session["other"] = questionsID[1]

    return redirect(url_for("quizPage"))


@app.route("/quiz", methods=["GET", "POST"]) #runs the quizPage function on the question and feedback pages
def quizPage():
    if "ID" not in session:
        return redirect(url_for("login"))
    
    quizFile = open("quiz.csv", "r")
    datareader = csv.reader(quizFile, delimiter=",")
    quiz = []
    for row in datareader:
        quiz.append(row)
    
    feedback = session.pop("feedback", None)
    was_correct = session.pop("was_correct", None)

    if request.method == "POST":
        answer = request.form["answer"]
        questionID = session["questionID"]

        if answer == quiz[questionID][4]: #adds points if user inputs correct answer
            session["correct"] = session["correct"] + 1
            session["points"] = session["points"] + int(quiz[questionID][1]) #points awarded for a questions matches the question's level
            was_correct = True
        else:
            was_correct = False
        
        session["feedback"] = quiz[questionID][5] #feedback page is shown
        session["was_correct"] = was_correct
        session["number"] = session["number"] + 1

        return redirect(url_for("quizPage"))

    if request.method == "GET":
        if feedback is not None: #only runs GET bock if a question is shown instead of also runnning when feedback is shown
            questionID = session["questionID"]
        else:
            if session["number"] >= session["limit"]: #redirects to quizEnd page if number of questions inputted is reached
                return redirect(url_for("quizEnd"))
            if not session["normal"] and not session["other"]: #question is only searched for using probability function if both lists are not empty
                return redirect(url_for("quizEnd"))
            
            temp = random.randint(1,5)
            if session["normal"] and session["other"]:
                if temp > 0 and temp < 5: #there is an 80% chance of the user getting a question that matches their level
                    questionID = random.choice(session["normal"])
                    session["normal"].remove(questionID)
                else:
                    questionID = random.choice(session["other"])
                    session["other"].remove(questionID)
            elif not session["other"]: #if the second list is empty, only select questions from the first list
                questionID = random.choice(session["normal"])
                session["normal"].remove(questionID) #if the first list is empty, only select questions from the second list
            elif not session["normal"]:
                questionID = random.choice(session["other"])
                session["other"].remove(questionID)
            else:
                return redirect(url_for("quizEnd"))

        session["questionID"] = questionID
        questionDetails = quiz[questionID]

        return render_template( #question display returned
            "quizPage.html",
            number=session["number"]+1,
            question=questionDetails[2],
            options=questionDetails[3].split("/"), #split string by the "/" to get the 4 options as 4 separate strings in an array
            feedback=feedback,
            was_correct=was_correct
        )

    return render_template( #feedback returned
        "quizPage.html",
        number=session["number"]+1,
        question=None,
        options=None,
        feedback=feedback,
        was_correct=was_correct
    )

@app.route("/quiz/end") #runs the quizEnd function on the quizEnd page
def quizEnd():
    if "ID" not in session:
        return redirect(url_for("login"))
    
    ID = session["ID"]
    correct = session["correct"]
    number = session["number"]

    saveScore() #runs the saving score and level functions
    saveLevel()

    return render_template( #returns the user's score
        "quizEnd.html",
        correct = correct,
        total = number
    )

def saveScore():
    ID = session["ID"] #variables defined as sessions rather than being passed as parameters
    correct = session["correct"]
    number = session["number"]
    score = round((correct/number)*100) #round the score to the nearest whole number
    userFile = open("student.csv", "r")
    datareader = csv.reader(userFile, delimiter=",")
    users = []
    for row in datareader:
        users.append(row)
    scores = users[ID][4].split("/") #finds the user's string of scores in the 2D array using the ID and converts it into an array
    scores.append(str(score)) #adds the new score to this array
    users[ID][4] = "/".join(scores) #the array is converted into a string again and replaces the old string
    with open("student.csv", "w", newline="", encoding='utf-8') as file:
        writer = csv.writer(file) #the whole 2D array containing the entire database is rewritten into the csv file
        writer.writerows(users)

def saveLevel():
    ID = session["ID"] #variables defined as sessions rather than being passed as parameters
    points = session["points"]
    number = session["number"]
    level = round(points/number) #round the level to the nearest whole number
    if level<1: #if statement ensures the user's level is between 1 and 5 inlcusive
        level = 1
    elif level>5:
        level = 5
    userFile = open("student.csv", "r")
    datareader = csv.reader(userFile, delimiter=",")
    users = []
    for row in datareader:
        users.append(row)
    users[ID][3] = str(level) #find the user's old level in the 2D array using ID and replace it with the new level
    with open("student.csv", "w", newline="", encoding='utf-8') as file:
        writer = csv.writer(file) #the whole 2D array containing the entire database is rewritten into the csv file
        writer.writerows(users)

@app.route("/analytics") #runs the analytics function on the analytics page
def graph():
    if "ID" not in session: #user has to be logged in if they want to see their score graph
        return redirect(url_for("login")) #user redirected to login page if not logged in
    ID = session["ID"]
    xPoints = []
    yPoints = []
    userFile = open("student.csv", "r")
    datareader = csv.reader(userFile, delimiter=",")
    users = []
    for row in datareader:
        users.append(row)
    scores = users[ID][4].split("/") #string of scores converted to array
    for i in range(len(scores)):
        xPoints.append(i) #i can be used as quiz number as it starts at 0 and is incremented by 1
        yPoints.append(int(scores[i])) #scores are converted to integers and appended to the y-coordinates
    plt.clf()
    plt.plot(xPoints, yPoints, marker="*") #graph is plotted using x and y arrays
    plt.title("Score evolution")
    plt.savefig("static/graph.png") #graph is exported as a png file
    plt.close()
    return render_template("analytics.html")

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)