import operator

import math
import pandas as pd
import sys

from DatabaseConnect import DatabaseConnect
from DatabaseOperations import getMoviesForUser, fetchTagForMovies, fetchTagForUser, fetchNumberofUserForTag
from Utils import dateWeightGenerator

number_of_users = pd.read_csv("C:\\Users\\Rohit\Desktop\\CSE515\\Phase1\\phase1_dataset\\mlusers.csv").shape[0]


def main():
    if len(sys.argv) == 3:
        db_obj = DatabaseConnect()
        user_id = sys.argv[1]
        model = sys.argv[2]
        cursor = db_obj.getCursorForDatabase()
        if model == 'tf':
            tfForUser(cursor,user_id)
        elif model == 'tfidf':
            tfidf(cursor,user_id)


    else:
        print "Options-> Argument 1 is userid and Argument 2 is model"


def tfForUser(cursor, user_id):
    movies = getMoviesForUser(cursor, user_id)
    movies_list = list()
    for a in movies:
        movies_list.append(a[0])
    tagCount = 0
    tagVector = dict()
    for movie in movies_list:
        tagList = fetchTagForMovies(movie, cursor)
        for tag in tagList:
            if tag in tagVector:
                tagVector[tag] = tagVector[tag] + 1
            else:
                tagVector[tag] = 1
        tagCount = tagCount + len(tagList)
    for tag in tagVector:
        tagVector[tag] = float(tagVector[tag]) / tagCount

    timvector = {}
    count = {}
    for movie in movies_list:
        tagTime = fetchTagForUser(movie, cursor)
        for single_tag in tagTime:
            if single_tag[0] not in timvector.keys():
                timvector[single_tag[0]] = dateWeightGenerator(single_tag[1])
                count[single_tag[0]] = 1
            else:
                timvector[single_tag[0]] += dateWeightGenerator(single_tag[1])
                count[single_tag[0]] += 1
    for tag in tagVector:
        tagVector[tag] = tagVector[tag] * timvector[tag]

    a = sorted(tagVector.items(), key=operator.itemgetter(1), reverse=True)
    for b, c in a:
        print b, ' ', c



def tfidf(cursor, user_id):
    movies = getMoviesForUser(cursor, user_id)
    movies_list = list()
    for a in movies:
        movies_list.append(a[0])
    tagCount = 0
    tagVector = dict()
    for movie in movies_list:
        tagList = fetchTagForMovies(movie, cursor)
        for tag in tagList:
            if tag in tagVector:
                tagVector[tag] = tagVector[tag] + 1
            else:
                tagVector[tag] = 1
        tagCount = tagCount + len(tagList)
    for tag in tagVector:
        tagVector[tag] = float(tagVector[tag]) / tagCount

    timvector = {}
    count = {}
    for movie in movies_list:
        tagTime = fetchTagForUser(movie, cursor)
        for single_tag in tagTime:
            if single_tag[0] not in timvector.keys():
                timvector[single_tag[0]] = dateWeightGenerator(single_tag[1])
                count[single_tag[0]] = 1
            else:
                timvector[single_tag[0]] += dateWeightGenerator(single_tag[1])
                count[single_tag[0]] += 1
    for tag in tagVector:
        tagVector[tag] = tagVector[tag] * timvector[tag]

    for key in tagVector:
        users_tags = fetchNumberofUserForTag(key, cursor)
        tagVector[key] = tagVector[key] * math.log(float(number_of_users) / users_tags)
    a = sorted(tagVector.items(), key=operator.itemgetter(1), reverse=True)
    for b, c in a:
        print b, ' ', c


if __name__ == '__main__':
    main()