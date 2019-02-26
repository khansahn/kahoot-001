from flask import Flask, request, json, jsonify
import os
from pathlib import Path
from random import randint

from . import router, baseLocation
from ..utils.file import readFile, createFile, writeFile

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
    # 2602
    # quizFile = open(quizFileLocation)
    # quizData = json.load(quizFile)
    quizData = readFile(quizFileLocation)

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
        # 2602
        # gameFile = open(gameFileLocation, 'r')
        # gameData = json.load(gameFile)
        gameData = readFile(gameFileLocation)
    # else:
        # 2602
        # gameFile = open(gameFileLocation, 'x')
        # gameFile = createFile(gameFileLocation)
        
    gameData["game-list"].append(gameInfo)
    # 2602
    # with open(gameFileLocation,'w') as gameFile:
        # toBeWritten = str(json.dumps(gameData))
        # gameFile.write(toBeWritten)
    toBeWritten = str(json.dumps(gameData))
    writeFile(gameFileLocation,toBeWritten)

    return jsonify(gameInfo)

#################################################################################
# JOIN GAME
#################################################################################
@router.route('/game/join', methods = ['POST'])
def joinGame():
    body = request.json

    # buka game info
    # 2602
    # gameFile = open(gameFileLocation)
    # gameData = json.load(gameFile)
    gameData = readFile(gameFileLocation)

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
    
    
    gameData["game-list"][position] = gameInfo
    # 2602
    # with open(gameFileLocation,'w') as gameFile:
        # toBeWritten = str(json.dumps(gameData))
        # gameFile.write(toBeWritten)
    writeFile(gameFileLocation,toBeWritten)

    return jsonify(request.json)


#################################################################################
# ANSWER GAME
#################################################################################

@router.route('/answer', methods = ['POST'])
def submitAnswer():
    body = request.json

    # ngecek jawaban sambil update skor dan leaderboard
    # 2602
    # gameFile = open(gameFileLocation)
    # gameData = json.load(gameFile)
    gameData = readFile(gameFileLocation)

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
    # 2602
    # questionFile = open(questionFileLocation)
    # questionData = json.load(questionFile)
    questionData = readFile(questionFileLocation)

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
    # 2602
    # with open(gameFileLocation,'w') as gameFile:
        # gameData["game-list"][position]["leaderboard"] = tempLeaderboard
        # toBeWritten = str(json.dumps(gameData))
        # gameFile.write(toBeWritten)
    gameData["game-list"][position]["leaderboard"] = tempLeaderboard
    toBeWritten = str(json.dumps(gameData))
    writeFile(gameFileLocation,toBeWritten)
    
    return res

#################################################################################
# LEADERBOARDS
#################################################################################
@router.route('/game/leaderboard/<gamePin>')
def viewLeaderboard(gamePin):
    # 2602
    # gameFile = open(gameFileLocation)
    # gameData = json.load(gameFile)
    gameData = readFile(gameFileLocation)

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
