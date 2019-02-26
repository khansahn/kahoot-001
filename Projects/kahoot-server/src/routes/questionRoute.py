from flask import Flask, request, json, jsonify
import os
from pathlib import Path

from . import router, baseLocation
from ..utils.file import readFile, createFile, writeFile


# ngambil alamat file 
quizFileLocation = baseLocation / "data" / "quiz-file.json"
questionFileLocation = baseLocation / "data" / "question-file.json"

#################################################################################
# CREATE QUESTION
#################################################################################
@router.route('/question', methods = ['POST']) #default method itu GET
def createQuestion():
    body = request.json

    questionData = {
        "questions": []
    }

    if os.path.exists(questionFileLocation):
        # 2602
        # questionFile = open(questionFileLocation, 'r')
        # questionData = json.load(questionFile)
        questionData = readFile(questionFileLocation)
    # else:
        # 2602
        # questionFile = open(questionFileLocation, 'x')
        # questionFile = createFile(questionFileLocation)

    questionData["questions"].append(body)
    toBeWritten = str(json.dumps(questionData))
    # 2602
    # questionFile = open(questionFileLocation,'w')
    # questionFile.write(toBeWritten)
    writeFile(questionFileLocation,toBeWritten)

    return jsonify(questionData)

#################################################################################
# GET QUESTION IN SPECIFIC QUIZ-ID 
#################################################################################
@router.route('/quiz/<quizId>/question/<questionId>')
def getThatQuestion(quizId,questionId):
    # 2602
    # questionFile = open(questionFileLocation)
    # questionData = json.load(questionFile)
    questionData = readFile(questionFileLocation)

    for question in questionData["questions"] :
        if (question["question-id"] == int(questionId) and question["quiz-id"] == int(quizId)) :
            return jsonify(question)

    return "heu ga ketemu mz mb"

#################################################################################
# UPDATE DELETE QUESTION
#################################################################################
@router.route('/quiz/<quizId>/question/<questionId>', methods=["PUT", "DELETE"])
def updateDeleteQuestion(quizId,questionId):
    # 2602
    # questionFile = open(questionFileLocation)
    # questionData = json.load(questionFile)
    questionData = readFile(questionFileLocation)

    # nyari question yang mau di-update atau di-delete
    position = -1
    for i in range(len(questionData["questions"])) :
        if (questionData["questions"][i]["quiz-id"] == int(quizId) and questionData["questions"][i]["question-id"] == int(questionId)):
            position = i
            break

    if (position == -1) :
        res = "ih ga ada datanya ah kak"
        return res
    else : 
        res = str(questionData["questions"][position]["quiz-id"]) + " yang nomor " + str(questionData["questions"][position]["question-id"])

        # kalau ketemu data nya baru dipisah antara PUT dan DELETE nyaaa
        if request.method == "PUT" :
            body = request.json
            questionData["questions"][position] = {**questionData["questions"][position], **body}

        elif request.method == "DELETE" :
            del questionData["questions"][position]

        # 2602
        # with open(questionFileLocation,'w') as questionFile:
        #     toBeWritten = str(json.dumps(questionData))
        #     questionFile.write(toBeWritten)
        toBeWritten = str(json.dumps(questionData))
        writeFile(questionFileLocation,toBeWritten)

    return res

#################################################################################
# GET QUESTION IN SPECIFIC QUIZ-ID ((deprecated krn fungsinya di file quizRoute))
#################################################################################
# @router.route('/quiz/<quizId>/question2/<questionId>')
# def getThatQuestion2(quizId, questionId):
#     quizData = getQuiz(int(quizId)).json
    
#     for question in quizData["question-list"] :
#         if (question["question-id"] == int(questionId)):
#             return jsonify(question)

#     return "hmm maz ko ga ada yh"