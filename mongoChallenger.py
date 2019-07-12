from pymongo import MongoClient
from bson import ObjectId
import time


class mongoChallenger():
    def __init__(self):
        self.mongo_host = 'localhost'
        self.mongo_port = 27017
        self.mongo_conn = MongoClient(self.mongo_host, self.mongo_port)
        self.mongo = self.mongo_conn.vinciChallenger

    def createChallenge(self, currentUserId, challengeText, rewardCount):
        '''
        :param currentUserId - str - user creater challenge:
        :param challengeText - str - challenge description:
        :param rewardCount - float - complete challenge reward:
        :return ObjectId - challenge ID:
        '''

        challengeId = self.mongo.challenges.insert_one({"user": currentUserId, "description": challengeText, "reward": rewardCount, "complete": False, "winner": None})
        return challengeId

    def countOfChallenges(self, deactive=False):
        '''
        :param deactive - bool - get only active count of challenges:
        :return int - count of challenges:
        '''

        challengesCount = self.mongo.challenges.count({"complete": deactive})
        return challengesCount

    def getChallenges(self, pageOffset=1, pageLimit=20, active=True, deactive=False):
        '''
        :param active - bool - get active challenges:
        :param deactive - bool - get deactive challenges:
        :param pageOffset - int - page number:
        :param pageLimit - int - challenges on page:
        :return list of dicts:
        '''

        challenges = self.mongo.challenges.find().limit(pageLimit).skip((pageOffset - 1)*pageLimit)
        return challenges

    def getMyChallenges(self, currentUserId, active=True, deactive=False):
        '''
        :param active - bool - get active challenges:
        :param deactive - bool - get deactive challenges:
        :param currentUserId:
        :return list of dicts:
        '''

        challenges = self.mongo.challenges.find({"user": currentUserId})
        return challenges

    def removeChallenge(self, challengeId, currentUserId):
        '''
        :param challengeId:
        :param currentUserId:
        :return bool - result of operation:
        '''

        challenge = self.mongo.challenges.find_one({"_id": ObjectId(challengeId), "user": currentUserId})
        if challenge is None:
            return False
        else:
            self.mongo.remove_one({"_id": ObjectId(challengeId), "user": currentUserId})
        return True

    def addMedia(self, challengeId, media, currentUserId):
        '''
        :param challengeId:
        :param media - byte of file:
        :param currentUserId:
        :return media id or None:
        '''

        challenge = self.mongo.challenges.find_one({"_id": ObjectId(challengeId), "complete": False})
        if challenge is None:
            return None

        mediaId = self.mongo.media.insert_one({"user": currentUserId, "file": media, "challenge": challengeId})
        return mediaId

    def removeMedia(self, challengeId, mediaId, currentUserId):
        '''
        :param challengeId:
        :param mediaId:
        :param currentUserId:
        :return:
        '''

        isMedia = self.mongo.media.count({"user": currentUserId, "_id": mediaId, "challenge": challengeId})
        if isMedia != 0:
            self.mongo.media.remove_one({"user": currentUserId, "_id": mediaId, "challenge": challengeId})
        return True

    def upDownLike(self, challengeId, mediaId, currentUserId):
        '''
        :param challengeId:
        :param mediaId:
        :param currentUserId:
        :return bool:
        '''

        isLike = self.mongo.mediaLikes.find_one({"user": currentUserId, "challenge": ObjectId(challengeId), "media": mediaId})
        if isLike is None:
            self.mongo.mediaLikes.insert_one({"user": currentUserId, "challenge": ObjectId(challengeId), "media": ObjectId(mediaId), "dt": int(time.time())})
        else:
            self.mongo.mediaLikes.remove_one({"user": currentUserId, "challenge": ObjectId(challengeId), "media": ObjectId(mediaId), "dt": int(time.time())})
        return True

    def likeCount(self, mediaId):
        '''
        :param mediaId:
        :return int:
        '''

        lcount = self.mongo.mediaLikes.count({"media": mediaId})
        return lcount