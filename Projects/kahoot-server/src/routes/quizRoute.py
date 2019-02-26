from flask import Flask, request, json, jsonify, g
import os
from pathlib import Path

from . import router, baseLocation
from ..utils.file import readFile, createFile, writeFile
from ..utils.authorisation import verifyLogin


# ngambil alamat file 
quizFileLocation = baseLocation / "data" / "quiz-file.json"
questionFileLocation = baseLocation / "data" / "question-file.json"

#################################################################################
# CREATE QUIZ
#################################################################################
@router.route('/quiz', methods = ['POST'])
@verifyLogin
def createQuiz():
    username = g.username
    body = request.json
    print("======IS NOW LOGGING INNNN======", g.username)
    quizData = {
        "total-quiz-available" : 0,
        "quizzes": []
    }

    if os.path.exists(quizFileLocation):
        quizData = readFile(quizFileLocation)

    quizData["quizzes"].append(body)
    quizData["total-quiz-available"] += 1
    # quizData["quiz-creator"] = username
    toBeWritten = str(json.dumps(quizData))
    writeFile(quizFileLocation,toBeWritten)

    return jsonify(quizData)

#################################################################################
# GET ALL QUIZ
#################################################################################
@router.route('/quiz/seeAllQuizAvailable')
def getAllQuiz():
    quizData = readFile(quizFileLocation)

    return jsonify(quizData["quizzes"])

#################################################################################
# GET QUESTION(S) PER QUIZ-ID
#################################################################################
@router.route('/quiz/<quizId>')
def getQuiz(quizId):
    quizData = readFile(quizFileLocation)

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
            if (quiz["quiz-id"] == int(quizId)):
                quizDataTemp = quiz
                break
        
        #nyari questionnya
        questionData = readFile(questionFileLocation)

        for question in questionData["questions"] :
            if (question["quiz-id"] == int(quizId)):
                quizDataTemp["question-list"].append(question)

    return jsonify(quizDataTemp)

#################################################################################
# UPDATE DELETE QUIZ
#################################################################################
@router.route('/quiz/<quizId>', methods=["PUT", "DELETE"])
@verifyLogin
def updateDeleteQuiz(quizId):
    print("======IS NOW LOGGING INNNN======", g.username)
    quizData = readFile(quizFileLocation)

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
            questionData = readFile(questionFileLocation)

            # kayaknya sih ini ngedelete nya udah semua meski question-id nya sama
            lenQL = 0
            QLInd = []
            for question in questionData["questions"] :
                i = questionData["questions"].index(question) 
                if (question["quiz-id"] == int(quizId)):
                    lenQL += 1
                    QLInd.append(i)
            
            currentDeletingIndex = 0
            deleted = 0
            for i in range(lenQL):
                currentDeletingIndex = QLInd[i] - deleted
                del questionData["questions"][currentDeletingIndex]
                deleted += 1

            toBeWritten = str(json.dumps(questionData))
            writeFile(questionFileLocation,toBeWritten)            

            # ngehapus quiz nya
            del quizData["quizzes"][position]
            quizData["total-quiz-available"] -= 1
        
        toBeWritten = str(json.dumps(quizData))
        writeFile(quizFileLocation,toBeWritten)

    return res
