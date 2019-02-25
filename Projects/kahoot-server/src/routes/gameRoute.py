from flask import Flask, request, json, jsonify
import os
from pathlib import Path

# from ..utils.crypt import encrypt, decrypt
from . import router, baseLocation

from random import randint

# ngambil alamat file 
quizFileLocation = baseLocation / "data" / "quiz-file.json"
questionFileLocation = baseLocation / "data" / "question-file.json"
gameFileLocation = baseLocation / "data" / "game-file.json"

#################################################################################
# CREATE GAME
#################################################################################

@router.route('/game', methods = ['POST'])
def createGame():
    body = request.json
    # manggil info quiz dan generate game pin
    quizFile = open(quizFileLocation)
    quizData = json.load(quizFile)

    for quiz in quizData["quizzes"]:
        if (quiz["quiz-id"] == int(body["quiz-id"])) :
            gameInfo = quiz

    gameInfo["game-pin"] = randint(10000,999999)
    gameInfo["user-list"] = []
    gameInfo["leaderboard"] = []

    # simpan game ini ke history
    gameData = {
        "game-list": []
    }
    if (os.path.exists(gameFileLocation)):
        gameFile = open(gameFileLocation, 'r')
        gameData = json.load(gameFile)
    else:
        gameFile = open(gameFileLocation, 'x')
        
    with open(gameFileLocation,'w') as gameFile:
        gameData["game-list"].append(gameInfo)
        toBeWritten = str(json.dumps(gameData))
        gameFile.write(toBeWritten)

    return jsonify(gameInfo)

#################################################################################
# JOIN GAME
#################################################################################
@router.route('/game/join', methods = ['POST'])
def joinGame():
    body = request.json

    # buka game info
    gameFile = open(gameFileLocation)
    gameData = json.load(gameFile)

    position = 0
    for i in range(len(gameData["game-list"])) : 
        game = gameData["game-list"][i]
        if (game["game-pin"] == int(body["game-pin"])):
            if body["username"] not in game["user-list"] :
                game["user-list"].append(body["username"])
                userData = {
                    "username" : body["username"],
                    "score" : 0
                }
                game["leaderboard"].append(userData)
                gameInfo = game
                position = i
                break
            else :
                return "Username is taken already bos"
            # nanti bikin handling kalau user bikin username yg udah ada
    
    with open(gameFileLocation,'w') as gameFile:
        gameData["game-list"][position] = (gameInfo)
        toBeWritten = str(json.dumps(gameData))
        gameFile.write(toBeWritten)

    return jsonify(request.json)


#################################################################################
# ANSWER GAME
#################################################################################

@router.route('/answer', methods = ['POST'])
def submitAnswer():
    body = request.json

    # ngecek jawaban sambil update skor dan leaderboard
    gameFile = open(gameFileLocation)
    gameData = json.load(gameFile)

    ## nyari game mana yg lagi dimainin dan leaderboard mana yang mau diupdate
    tempLeaderboard = []
    position = 0
    for i in range(len(gameData["game-list"])):
        game = gameData["game-list"][i]
        if game["game-pin"] == body["game-pin"] :
            tempLeaderboard = game["leaderboard"]
            position = i
            break
    
    ### update leaderboard
    questionFile = open(questionFileLocation)
    questionData = json.load(questionFile)

    for question in questionData["questions"] :
        if (question["quiz-id"] == (body["quiz-id"]) and question["question-id"] == (body["question-id"])) : 
            for userData in tempLeaderboard:
                if (userData["username"] == body["username"]):                    
                    if (question["answer"] == body["answer"]):
                        res = "Truuuuuuuu"
                        userData["score"] += 100
                    else:  
                        res = "Y salah"
                        userData["score"] += 0
                    break 

    # \\\\\\\\\\\\\\\\\\\lg di sini update file history game  nya \\\\\\\\\\\\\\\\\\\\\\
    with open(gameFileLocation,'w') as gameFile:
        gameData["game-list"][position]["leaderboard"] = tempLeaderboard
        toBeWritten = str(json.dumps(gameData))
        gameFile.write(toBeWritten)
    
    return res

#################################################################################
# LEADERBOARDS
#################################################################################
@router.route('/game/leaderboard/<gamePin>')
def viewLeaderboard(gamePin):
    gameFile = open(gameFileLocation)
    gameData = json.load(gameFile)

    res = ''
    for game in gameData["game-list"] :
        if game["game-pin"] == int(gamePin):
            res =  (game["leaderboard"])
            break

    nData = len(res)
    sortedLeaderboard = []
    while (len(sortedLeaderboard) != nData):
        biggest = res[0]["score"]
        biggestPosition = 0
        for i in range(len(res)):
            if (res[i]["score"] >= biggest):
                biggest = res[i]["score"]
                data = res[i]
                biggestPosition = i
        sortedLeaderboard.append(data)
        res.pop(biggestPosition)

    return jsonify(sortedLeaderboard)
