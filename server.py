import time
from flask import Flask
from flask_cors import CORS, cross_origin
from flask import request
import glob
import os
import json
from flask.helpers import send_from_directory

from src import DynaProgLatestVersionProb1
from src import DynaProgLatestVersionProb2

from src import dataExtractor

from src import VNSLatestVersionProblem1
from src import VNSLatestVersionProblem2

from src import HodsonMoore

server = Flask(__name__, static_folder="ui/build", static_url_path='')
cors = CORS(server, resources={r"/*": {"origins": "*"}})


@server.route("/addInstance", methods=["POST"], strict_slashes=False)
@cross_origin(server)
def addInstance():
    instances = {}

    os.chdir("./Instances")
    data = json.loads(request.data.decode('utf-8'))

    nbTaches = data['nbTaches']
    problem = data['problem']
    fichier = data['fichierData']

    for file in glob.glob("*.txt"):
        instances[file[:2]] = []

    for file in glob.glob("*.txt"):
        instances[file[:2]].append(file)

    nomFichier = problem.upper() + "_n" + str(nbTaches) + ".txt"

    cpt = 0

    while nomFichier in instances[problem.upper()]:
        cpt += 1
        nomFichier = problem.upper() + "_n" + str(nbTaches) + "_" + str(cpt) + ".txt"

    print(nomFichier)

    fd = open("./"+nomFichier, "w+")
    fichier = fichier.replace("\r", "")
    fd.write(fichier)
    #fichier = fichier.split("\n")
    #print("afterMod", fichier)
    fd.close()

    fd = open("./"+nomFichier, "r")
    print(fd.readline())
    fd.close()

    error = False

    if problem.upper() == "P1":

        filee = open(nomFichier, "r")

        line1 = filee.readline()
        line2 = filee.readline()
        line3 = filee.readline()

        filee.close()

        line1 = line1.replace("\t", " ")
        n = int(line1.split(" ")[0])

        line2 = line2.replace("\t", " ")
        line2 = line2.replace("\n", " ")
        line2 = line2.split(" ")
        try:
            while "" in line2:
                line2.remove("")
        except:
            pass

        line3 = line3.replace("\t", " ")
        line3 = line3.replace("\n", " ")
        line3 = line3.split(" ")
        try:
            while "" in line3:
                line3.remove("")
        except:
            pass

        if (n != int(nbTaches)) or (len(line2) != n) or (len(line3) != n):
            print("n", n)
            print("nb", nbTaches, "type", type(nbTaches))
            print("line2", line2, "len", len(line2))
            print("line3", line3, "len", len(line3))
            error = True

        else:
            error = False

    else:

        filee = open(nomFichier, "r")

        line1 = filee.readline()
        line2 = filee.readline()
        line3 = filee.readline()
        line4 = filee.readline()
        line5 = filee.readline()

        filee.close()

        line1 = line1.replace("\t", " ")
        n = int(line1.split(" ")[0])

        line2 = line2.replace("\t", " ")
        line2 = line2.replace("\n", " ")
        line2 = line2.split(" ")
        try:
            while "" in line2:
                line2.remove("")
        except:
            pass

        line3 = line3.replace("\t", " ")
        line3 = line3.replace("\n", " ")
        line3 = line3.split(" ")
        try:
            while "" in line3:
                line3.remove("")
        except:
            pass

        line4 = line4.replace("\t", " ")
        line4 = line4.replace("\n", " ")
        line4 = line4.split(" ")
        try:
            while "" in line4:
                line4.remove("")
        except:
            pass

        line5 = line5.replace("\t", " ")
        line5 = line5.replace("\n", " ")
        line5 = line5.split(" ")
        try:
            while "" in line5:
                line5.remove("")
        except:
            pass

        if (n != int(nbTaches)) or (len(line2) != n) or (len(line3) != n) or (len(line3) != n) or (len(line4) != n) or (len(line5) != n):
            print("n", n)
            print("nb", nbTaches, "type", type(nbTaches))
            print("line2", line2, "len", len(line2))
            print("line3", line3, "len", len(line3))
            print("line4", line4, "len", len(line4))
            print("line5", line5, "len", len(line5))
            error = True
        else:
            error = False

    if error == True:
        os.remove(nomFichier)
        res = "echec"
    else:
        res = "success"

    os.chdir("..")
    return res


@server.route("/getInstances", methods=["GET"], strict_slashes=False)
def nbInstances():
    instances = {}

    os.chdir("./Instances")

    for file in glob.glob("*.txt"):
        instances[file[:2]] = []

    cpt = 0
    deleteFiles = False

    for file in glob.glob("*.txt"):
        cpt += 1

        if cpt < 20:
            instances[file[:2]].append(file)
        else:
            deleteFiles = True
            break

    if deleteFiles == True:
        for file in glob.glob("*.txt"):
            os.remove(file)

    os.chdir("..")

    return instances


@server.route('/poly', methods=['GET'])
def poly():

    os.chdir("./Instances")
    # problem = request.args.get("problem")

    instance = request.args.get("instance")

    start = time.time()
    res = HodsonMoore.moore(instance)

    data2 = res["data"]

    data = [data2[0][1]]

    for i in range(1, len(data2)):
        data.append(data[i-1] + data2[i][1])

    data2.clear()

    os.chdir("..")

    return {"sequance": res["sequance"],
            "temps": time.time()-start,
            "data": data,
            "valeur": res["valeur"]}


@server.route('/dyna', methods=['GET'])
def dyna():

    os.chdir("./Instances")

    problem = request.args.get("problem")

    instance = request.args.get("instance")

    if problem == "p1":
        res = DynaProgLatestVersionProb1.dynamiqueP1(instance)

    else:
        res = DynaProgLatestVersionProb2.dynamiqueP2(instance)

    os.chdir("..")

    return {"sequance": res}


@server.route('/meta', methods=['GET'])
def meta():

    os.chdir("./Instances")

    problem = request.args.get("problem")

    instance = request.args.get("instance")

    if problem == "p1":
        res = VNSLatestVersionProblem1.metaP1(instance)
    else:
        res = VNSLatestVersionProblem2.metaP2(instance)

    os.chdir("..")

    return {"sequance": res}


@server.route('/')
def serve():
    return send_from_directory(server.static_folder, 'index.html')


if __name__ == "__main__":
    server.run()
