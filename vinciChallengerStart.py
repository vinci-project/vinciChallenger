from mongoChallenger import mongoChallenger
from flask import Flask, abort, request
import json


class flaskServer():
    def __init__(self):
        self.app = Flask(__name__)
        self.mc = mongoChallenger()

        @self.app.route("/createChallenge", methods=['POST'])
        def createChallenge():
            if not request:
                abort(400)
            try:
                user = request.form.get("user")
                descr = request.form.get("descr")
                reward = float(request.form.get("reward"))
                ch_id = self.mc.createChallenge(challengeText=descr, currentUserId=user, rewardCount=reward)
                return json.dumps({"code": 0, "challenge": ch_id})
            except:
                return json.dumps({"code": -1})

        @self.app.route("/removeChallenge", methods=['POST'])
        def removeChallenge():
            if not request:
                abort(400)

            try:
                user = request.form.get("user")
                challengeid = request.form.get("challengeid")
                self.mc.removeChallenge(challengeId=challengeid, currentUserId=user)
            except:
                return json.dumps({"code": -1})


        @self.app.route("/getChallenges", methods=['POST'])
        def getChallenges():
            if not request:
                abort(400)
            try:
                offset = request.form.get("offset")
                limit = request.form.get("limit")
                self.mc.getChallenges(pageOffset=offset, pageLimit=limit)
            except:
                return json.dumps({"code": -1})

        @self.app.route("/addMedia", methods=['POST'])
        def addMedia():
            if not request:
                abort(400)
            try:
                user = request.form.get("user")
            except:
                return json.dumps({"code": -1})
        @self.app.route("/removeMedia", methods=['POST'])
        def removeMedia():
            if not request:
                abort(400)
            try:
                user = request.form.get("user")
            except:
                return json.dumps({"code": -1})
        @self.app.route("/getMediaList", methods=['POST'])
        def getMediaList():
            if not request:
                abort(400)
            try:
                user = request.form.get("user")
            except:
                return json.dumps({"code": -1})
        @self.app.route("/getMedia", methods=['POST'])
        def getMedia():
            if not request:
                abort(400)
            try:
                user = request.form.get("user")
            except:
                return json.dumps({"code": -1})
        @self.app.route("/setLike", methods=['POST'])
        def setLike():
            if not request:
                abort(400)
            try:
                user = request.form.get("user")
                mediaid = request.form.get("mediaid")
                challengeid = request.form.get("challengeid")
                self.mc.upDownLike(challengeId=challengeid, mediaId=mediaid, currentUserId=user)
            except:
                return json.dumps({"code": -1})
        @self.app.route("/getLikes", methods=['POST'])
        def getLikes():
            if not request:
                abort(400)
            try:
                mediaid = request.form.get("mediaid")
                self.mc.likeCount(mediaId=mediaid)
            except:
                return json.dumps({"code": -1})

    def run(self):
        self.app.run(host='0.0.0.0', port=18900)


if __name__ == "__main__":
    fl = flaskServer()
    fl.run()

