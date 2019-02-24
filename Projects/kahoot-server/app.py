from flask import Flask, request, json, jsonify
import requests, os
from random import randint
app = Flask(__name__)   #buat manggil flask



############## sesi 2 001 ############## nyobain post

@app.route('/quiz', methods = ['POST'])
def createQuiz():
    body = request.json

    quizData = {
        "totalQuizAvailable" : 0,
        "quizzes": []
    }

    if os.path.exists('./quizzes-file.json'):
        print("nambahhh quiz baru ke yg udah ada")
        quizFile = open('quizzes-file.json', 'r')
        quizData = json.load(quizFile)
    else:
        print("bikin quiz aka pertama niy baruu")
        quizFile = open('quizzes-file.json', 'x')

    quizData["quizzes"].append(body)
    quizData["totalQuizAvailable"] += 1
    toBeWritten = str(json.dumps(quizData))
    quizFile = open('./quizzes-file.json','w')
    quizFile.write(toBeWritten)
    
    return jsonify(quizData)

############## 23Feb2019 ###################
@app.route('/quizzes/<quizId>', methods=["PUT", "DELETE"])
def updateDeleteQuiz(quizId):
    quizFile = open('./quizzes-file.json')
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
        print("yaa datanya adaa", position)
        res = str(quizData["quizzes"][position]["quiz-id"]) + " yaaaaaa??? " + str(quizData["quizzes"][position]["quiz-title"])

        # kalau data yg mau di-update atau di-delete udah ketemu, baru deh
        # kalau PUT, berarti quiz-title sama quiz-category di file diganti jd dari yang baru dari body
        if request.method == "PUT" :
            body = request.json
            print("ini bodyyy",body)
            print("ini quizData",quizData)
            quizData["quizzes"][position]["quiz-title"] = body["quiz-title-new"]
            quizData["quizzes"][position]["quiz-category"] = body["quiz-category-new"]
            print("ini Quiz Data updated", quizData)

            # with open('./quizzes-file.json','w') as quizFile:
            #     toBeWritten = str(json.dumps(quizData))
            #     quizFile.write(toBeWritten)

        elif request.method == "DELETE" :
            print("DELLLLL")
            del quizData["quizzes"][position]
            quizData["totalQuizAvailable"] -= 1
            print(quizData)
        
        with open('./quizzes-file.json','w') as quizFile:
            toBeWritten = str(json.dumps(quizData))
            quizFile.write(toBeWritten)

    return res

@app.route('/quizzes/<quizId>/questions/<questionId>', methods=["PUT", "DELETE"])
def updateDeleteQuestion(quizId,questionId):
    questionFile = open('./question-file.json')
    questionData = json.load(questionFile)

    # nyari question yang mau di-update atau di-delete
    position = -1
    print(questionData, "woioiajsoid")
    print(questionData["questions"][0]["quiz-id"],"LOOOOL")
    for i in range(len(questionData["questions"])) :
        if (questionData["questions"][i]["quiz-id"] == int(quizId) and questionData["questions"][i]["question-id"] == int(questionId)):
            position = i
            break

    if (position == -1) :
        res = "ih ga ada datanya ah kak"
        return res
    else : 
        print("yyyy ada nih data question nya", position)
        res = str(questionData["questions"][position]["quiz-id"]) + " yang nomor " + str(questionData["questions"][position]["question-id"])

        # kalau ketemu data nya baru dipisah antara PUT dan DELETE nyaaa
        if request.method == "PUT" :
            body = request.json
            questionData["questions"][position]["question"] = body["question-new"]
            questionData["questions"][position]["answer"] = body["answer-new"]
            questionData["questions"][position]["options"]["A"] = body["options-new"]["A"]
            questionData["questions"][position]["options"]["B"] = body["options-new"]["B"]
            questionData["questions"][position]["options"]["C"] = body["options-new"]["C"]
            questionData["questions"][position]["options"]["D"] = body["options-new"]["D"]

        elif request.method == "DELETE" :
            del questionData["questions"][position]

        with open('./question-file.json','w') as questionFile:
            toBeWritten = str(json.dumps(questionData))
            questionFile.write(toBeWritten)

    return res





@app.route('/quizzes/<quizId>')
def getQuiz(quizId):
    quizFile = open('./quizzes-file.json')
    quizData = json.load(quizFile)

    for quiz in quizData["quizzes"] :
        # quiz = json.loads(quiz)
        if (quiz["quiz-id"] == int(quizId)):
            quizDataTemp = quiz
            break

    
    #nyari questionnya
    questionFile = open('./question-file.json')
    questionData = json.load(questionFile)

    for question in questionData["questions"] :
        # question = json.loads(question)
        if (question["quiz-id"] == int(quizId)):
            quizDataTemp["question-list"].append(question)

    return jsonify(quizDataTemp)



# load  V dump daaan loads V dumps
# loads itu dari string ke json
# dumps itu dari singlequotes ke doublequotes
@app.route('/question', methods = ['POST']) #default method itu GET
def createQuestion():
    body = request.json

    questionData = {
        "questions": []
    }

    if os.path.exists('./question-file.json'):
        print("nambahhh dr yg udah ada")
        questionFile = open('question-file.json', 'r')
        questionData = json.load(questionFile)
    else:
        print("bikin baruu")
        questionFile = open('question-file.json', 'x')

    questionData["questions"].append(body)
    toBeWritten = str(json.dumps(questionData))
    questionFile = open('./question-file.json','w')
    questionFile.write(toBeWritten)

    return jsonify(questionData)



# manfaatin fungsi getQuiz yg udah ada
@app.route('/quizzes/<quizId>/questions/<questionId>')
def getThatQuestion(quizId, questionId):
    quizData = getQuiz(int(quizId)).json
    
    for question in quizData["question-list"] :
        if (question["question-id"] == int(questionId)):
            return jsonify(question)

    return "hmm maz ko ga ada yh"

# sama aja tp cuma ngakses satu file database (question aja)
@app.route('/quizzes/<quizId>/questions2/<questionId>')
def getThatQuestion2(quizId,questionId):
    questionFile = open('./question-file.json')
    questionData = json.load(questionFile)

    for question in questionData["questions"] :
        # question = json.loads(question)
        if (question["question-id"] == int(questionId) and question["quiz-id"] == int(quizId)) :
            return jsonify(question)

    return "heu ga ketemu mz mb"


######################### sesi 3 nyoba ngejawab #####################

'''
leaderboard pas user join game, mereka diappend ke leaderboard dengan skor awal 0

nanti tiap answer diupdate semua skor dr tiap usernya

'''

@app.route('/answer', methods = ['POST'])
def submitAnswer():
    body = request.json

    ''' pending dl ya kak
    questionFile = open('./question-file.json')
    questionData = json.load(questionFile)

    for question in questionData["questions"] :
        question = json.loads(question)
        if (question["quiz-id"] == (body["quiz-id"]) and question["question-id"] == (body["question-id"])) : 
            if (question["answer"] == body["answer"]):
                res = "Truuuuuuuu"
            else:
                res = "Y salah"
            break
    '''

    # ngecek jawaban sambil update skor dan leaderboard
    gameFile = open('./history-game-file.json')
    gameData = json.load(gameFile)
    # print(gameData, body["game-pin"])

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
    questionFile = open('./question-file.json')
    questionData = json.load(questionFile)

    for question in questionData["questions"] :
        # question = json.loads(question)
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
    with open('./history-game-file.json','w') as gameFile:
        gameData["game-list"][position]["leaderboard"] = tempLeaderboard
        toBeWritten = str(json.dumps(gameData))
        gameFile.write(toBeWritten)
    
    return res


@app.route('/game', methods = ['POST'])
def createGame():
    body = request.json
    # manggil info quiz dan generate game pin
    quizFile = open('./quizzes-file.json')
    quizData = json.load(quizFile)

    for quiz in quizData["quizzes"]:
        # quiz = json.loads(quiz)
        if (quiz["quiz-id"] == int(body["quiz-id"])) :
            gameInfo = quiz

    gameInfo["game-pin"] = randint(10000,999999)
    gameInfo["user-list"] = []
    gameInfo["leaderboard"] = []

    # simpan game ini ke history
    gameData = {
        "game-list": []
    }
    if (os.path.exists('./history-game-file.json')):
        gameFile = open('./history-game-file.json', 'r')
        gameData = json.load(gameFile)
    else:
        gameFile = open('./history-game-file.json', 'x')
        
    with open('./history-game-file.json','w') as gameFile:
        gameData["game-list"].append(gameInfo)
        toBeWritten = str(json.dumps(gameData))
        gameFile.write(toBeWritten)

    return jsonify(gameInfo)


@app.route('/game/join', methods = ['POST'])
def joinGame():
    body = request.json

    # buka game info
    gameFile = open('./history-game-file.json')
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
            # nanti bikin handling kalau user bikin username yg udah ada
    
    with open('./history-game-file.json','w') as gameFile:
        gameData["game-list"][position] = (gameInfo)
        toBeWritten = str(json.dumps(gameData))
        gameFile.write(toBeWritten)

    return jsonify(request.json)

@app.route('/game/leaderboard/<gamePin>')
def viewLeaderboard(gamePin):
    # body = request.json

    gameFile = open('./history-game-file.json')
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


##################################### sesi 3 #####################################  
@app.route('/register', methods=['POST'])
def registerUser():
    body = request.json

    if body["todo"] == "encrypt":
        body["password"] = encrypt(body["password"])
    elif body["todo"] == "decrypt":
        body["password"] = decrypt(body["password"])

    registeredUserData = {
        "registeredUsers" : []
    }

    if os.path.exists('./registered-user-file.json'):
        registeredUserFile = open('registered-user-file.json', 'r')
        registeredUserData = json.load(registeredUserFile)

         # cek username nya udah pernah dipake belum
        res = ''
        position = -1
        for i in range(len(registeredUserData["registeredUsers"])) :
            registeredUser = registeredUserData["registeredUsers"][i]
            if (registeredUser["username"] == body["username"]) :
                print("uname sama")
                res = "Username nya udah dipake maz"
                position = i
                break
            if (registeredUser["email"] == body["email"]):
                print("email sama")
                res = "Km udah pernah daftar pake email ini loh"
                position = i
                break
        if (position == -1):
            with open('./registered-user-file.json','w') as registeredUserFile:
                registeredUserData["registeredUsers"].append(body) 
                toBeWritten = str(json.dumps(registeredUserData))
                registeredUserFile.write(toBeWritten)
                res = jsonify(registeredUserData)
        else : 
            res = res
    else:
        registeredUserFile = open('registered-user-file.json', 'x')
       
        with open('./registered-user-file.json','w') as registeredUserFile:
            registeredUserData["registeredUsers"].append(body) 
            toBeWritten = str(json.dumps(registeredUserData))
            registeredUserFile.write(toBeWritten)
        res = jsonify(registeredUserData)

    return res


# login user
@app.route('/login', methods = ['POST'])
def loginUser():
    body = request.json

    # ngebuka file yang udah pernah regist
    registeredUserFile = open('./registered-user-file.json')
    registeredUserData = json.load(registeredUserFile)

    # nyari yang di-login udah ada di regist atau belum
    res = ''
    position = -1
    for i in range(len(registeredUserData["registeredUsers"])) :
        registeredUser = registeredUserData["registeredUsers"][i]
        if (registeredUser["username"] == body["username"]) :
            position = i
            print(decrypt(registeredUser["password"]), body["password"])
            if (decrypt(registeredUser["password"]) == body["password"]) :
                res = "Login berhasssil"
                break
            else:
                res = "Passwordnya salah ih"
    
    # kalau user yang di login ga ada di registered user
    if (position == -1) :
        res = "Regist dl ah"
    
    return res

############### fungsi freelance ##########################
defaultCaesarMove = 7
def encrypt(string):
    caesarMove = defaultCaesarMove
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    number = '0123456789'
    initial = alphabet+number
    listInitial = list(initial)
    allMove = len(listInitial)
  
    listString = list(string)     
    for i in range(len(listString)) :
        tobe = listInitial.index(listString[i])
        en = (tobe + caesarMove) % allMove
        listString[i] = listInitial[en]
    
    return ''.join(listString)

def decrypt(string):
    caesarMove = defaultCaesarMove
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    number = '0123456789'
    initial = alphabet+number
    listInitial = list(initial)
    allMove = len(listInitial)
    
    listString = list(string)  
    for i in range(len(listString)) :
        tobe = listInitial.index(listString[i])
        en = (tobe - caesarMove) % allMove
        listString[i] = listInitial[en]
        
    return ''.join(listString)


# masuk ke development mode tanpa setting environment, biar aman taro paling bawah ajaaa abis td nyobain di atas ga jalan heu
if __name__ == "__main__":
    app.run(debug=True, port = 5000)