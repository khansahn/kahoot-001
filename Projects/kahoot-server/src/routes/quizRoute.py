from flask import Flask, request, json, jsonify
import os
from pathlib import Path

# from ..utils.crypt import encrypt, decrypt
from . import router, baseLocation

# ngambil alamat file 
quizFileLocation = baseLocation / "data" / "quiz-file.json"
questionFileLocation = baseLocation / "data" / "question-file.json"

#################################################################################
# CREATE QUIZ
#################################################################################
@router.route('/quiz', methods = ['POST'])
def createQuiz():
    body = request.json

    quizData = {
        "total-quiz-available" : 0,
        "quizzes": []
    }

    if os.path.exists(quizFileLocation):
        quizFile = open(quizFileLocation, 'r')
        quizData = json.load(quizFile)
    else:
        quizFile = open(quizFileLocation, 'x')

    quizData["quizzes"].append(body)
    quizData["total-quiz-available"] += 1
    toBeWritten = str(json.dumps(quizData))
    quizFile = open(quizFileLocation,'w')
    quizFile.write(toBeWritten)
    
    return jsonify(quizData)

#################################################################################
# GET ALL QUIZ
#################################################################################
@router.route('/quiz/seeAllQuizAvailable')
def getAllQuiz():
    quizFile = open(quizFileLocation)
    quizData = json.load(quizFile)

    return jsonify(quizData["quizzes"])

#################################################################################
# GET QUESTION(S) PER QUIZ-ID
#################################################################################
@router.route('/quiz/<quizId>')
def getQuiz(quizId):
    quizFile = open(quizFileLocation)
    quizData = json.load(quizFile)

    # nyari kuis nya ada atau engga
    position = -1
    for i in range(len(quizData["quizzes"])) :
        if (quizData["quizzes"][i]["quiz-id"] == int(quizId)):
            position = i
            break
    if (position == -1) :
        res = "wah mas ga ada data nya, kuis yang mana ya?"
        return res
    else:

        for quiz in quizData["quizzes"] :
            # quiz = json.loads(quiz)
            if (quiz["quiz-id"] == int(quizId)):
                quizDataTemp = quiz
                break
        
        #nyari questionnya
        questionFile = open(questionFileLocation)
        questionData = json.load(questionFile)

        for question in questionData["questions"] :
            # question = json.loads(question)
            if (question["quiz-id"] == int(quizId)):
                quizDataTemp["question-list"].append(question)

    return jsonify(quizDataTemp)

#################################################################################
# UPDATE DELETE QUIZ
#################################################################################
@router.route('/quiz/<quizId>', methods=["PUT", "DELETE"])
def updateDeleteQuiz(quizId):
    quizFile = open(quizFileLocation)
    quizData = json.load(quizFile)

    # nyari quiz yg mau di-update atau di-delete dl
    position = -1
    for i in range(len(quizData["quizzes"])) :
        if (quizData["quizzes"][i]["quiz-id"] == int(quizId)):
            position = i
            break

    if (position == -1) :
        res = "wah mas ga ada data nya, kuis yang mana ya?"
        return res
    else:
        res = str(quizData["quizzes"][position]["quiz-id"]) + " yaaaaaa??? " + str(quizData["quizzes"][position]["quiz-title"])

        # kalau data yg mau di-update atau di-delete udah ketemu, baru deh
        # kalau PUT, berarti quiz-title sama quiz-category di file diganti jd dari yang baru dari body
        if request.method == "PUT" :
            body = request.json
            quizData["quizzes"][position] = {**quizData["quizzes"][position], **body}

        elif request.method == "DELETE" :   
            # ngehapus question di quiz ybs dl
            questionFile = open(questionFileLocation)
            questionData = json.load(questionFile)
            
            # tapi ini delete nya masih ga sempurna, kalau ada question-id yang sama dia bakal nge-delete yang muncul pertama kali aja
            lenQL = 0
            QLInd = []
            for question in questionData["questions"] :
                i = questionData["questions"].index(question) #ini maksud komen di atas ku hue tp kalau question-id nya unik semua gapapa sih (kayaknya lol he he)
                if (question["quiz-id"] == int(quizId)):
                    lenQL += 1
                    QLInd.append(i)
            
            currentDeletingIndex = 0
            deleted = 0
            for i in range(lenQL):
                currentDeletingIndex = QLInd[i] - deleted
                del questionData["questions"][currentDeletingIndex]
                deleted += 1

            with open(questionFileLocation,'w') as questionFile:
                toBeWritten = str(json.dumps(questionData))
                questionFile.write(toBeWritten)

            # ngehapus quiz nya
            del quizData["quizzes"][position]
            quizData["total-quiz-available"] -= 1
        
        with open(quizFileLocation,'w') as quizFile:
            toBeWritten = str(json.dumps(quizData))
            quizFile.write(toBeWritten)

    return res
