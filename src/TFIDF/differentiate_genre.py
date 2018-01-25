import sys
import math

import operator

import DatabaseOperations
from DatabaseConnect import DatabaseConnect
from Utils import sortedDict


def main():
    if len(sys.argv) == 4:
        genre1 = sys.argv[1]
        genre2 = sys.argv[2]
        model = sys.argv[3]
        db_obj = DatabaseConnect()
        cursor = db_obj.getCursorForDatabase()

        if model == 'tf-idf-diff':
            tfidfdiffCalculation(cursor, genre1, genre2)
        elif model == 'p-diff1':
            pdiff1(cursor, genre1, genre2)
        elif model == 'p-diff2':
            pdiff2(cursor, genre1, genre2)

        cursor.close()
        db_obj.closeDatabaseConnection()
    else:
        print "Options-> Argument 1 is genre1 and  Argument 2 is genre2 and Argument 3 is model"


def tfidfdiffCalculation(cursor, genre1, genre2):
    genre1_result = DatabaseOperations.getGenreDetails(cursor, genre1)
    genre2_result = DatabaseOperations.getGenreDetails(cursor, genre2)
    genre1_dict = {}
    genre2_dict = {}

    genre1_tags_num = len(genre1_result)
    genre2_tags_num = len(genre2_result)
    for genre1_tuple in genre1_result:
        if genre1_tuple[4] not in genre1_dict.keys():
            genre1_dict[genre1_tuple[4]] = 1.0/genre1_tags_num
        else:
            genre1_dict[genre1_tuple[4]] += 1.0/genre1_tags_num

    for genre2_tuple in genre2_result:
        if genre2_tuple[4] not in genre2_dict.keys():
            genre2_dict[genre2_tuple[4]] = 1.0/genre2_tags_num
        else:
            genre2_dict[genre2_tuple[4]] += 1.0/genre2_tags_num

    idf_dict ={}
    tags_result = DatabaseOperations.getTagsForCombinedGenres(cursor, genre1, genre2)
    max_count = DatabaseOperations.getCombinedMovieList(cursor, genre1, genre2)[0][0]
    for tag in tags_result:
        if tag[0] in genre1_dict:
            idf_dict[tag[0]] = math.log(max_count/float(DatabaseOperations.getTagsCountForGenreMovies(cursor, tag, genre1, genre2)[0][0])) * genre1_dict[tag[0]] * 1000

    a = sorted(idf_dict.items(), key=operator.itemgetter(1), reverse=True)
    for b, c in a:
        print b, '-->', c


def pdiff1(cursor,genre1,genre2):
    movie_tuple_genre1 = DatabaseOperations.getMovieListForGenre(cursor, genre1)
    movie_list_genre1 = list()
    for a in movie_tuple_genre1:
        movie_list_genre1.append(a[0])
    R = len(movie_list_genre1)
    movie_tuple_genre2 = DatabaseOperations.getMovieListForGenre(cursor, genre2)
    movie_list_genre2 = list()
    for a in movie_tuple_genre2:
        movie_list_genre2.append(a[0])
    finalMovieSet = list()
    for movie in movie_list_genre1:
        if movie not in finalMovieSet:
            finalMovieSet.append(movie)
    for movie in movie_list_genre2:
        if movie not in finalMovieSet:
            finalMovieSet.append(movie)
    M = len(finalMovieSet)
    genre1_tags = DatabaseOperations.getTagFromMovieDictionary(cursor, movie_list_genre1)
    genre2_tags = DatabaseOperations.getTagFromMovieDictionary(cursor, movie_list_genre2)
    genre1_genre2_tags = DatabaseOperations.getTagFromMovieDictionary(cursor, finalMovieSet)
    final_tag_dict = dict()
    for tag in genre1_genre2_tags:
        if tag not in genre1_tags:
            rij = 0
        else:
            rij = genre1_tags[tag]

        if tag not in genre2_tags:
            count_genre2 = 0
        else:
            count_genre2 = genre2_tags[tag]

        if M == R or genre1_genre2_tags[tag] == rij or R == rij:
            final_tag_dict[tag] = float(genre1_tags[tag] - count_genre2) / M
        elif rij == 0:
            final_tag_dict[tag] = float(genre1_genre2_tags[tag]) / (M - R)
        else:
            log_val = (float(rij) * (M - R + float(rij) - genre1_genre2_tags[tag])) / (
            (R - rij) * (float(genre1_genre2_tags[tag]) - rij))
            modulus_term = abs(rij / R) - (float((genre1_genre2_tags[tag] - rij)) / (M - R))
            final_tag_dict[tag] = abs((math.log(log_val)) * modulus_term)
    sortedDict(final_tag_dict, cursor)


def pdiff2(cursor, genre1, genre2):
    movie_tuple_genre1 = DatabaseOperations.getMovieListForGenre(cursor, genre1)
    movie_list_genre1 = list()
    for a in movie_tuple_genre1:
        movie_list_genre1.append(a[0])
    movie_tuple_genre2 = DatabaseOperations.getMovieListForGenre(cursor, genre2)
    movie_list_genre2 = list()
    for a in movie_tuple_genre2:
        movie_list_genre2.append(a[0])
    R = len(movie_list_genre2)
    finalMovieSet = list()
    for movie in movie_list_genre1:
        if movie not in finalMovieSet:
            finalMovieSet.append(movie)
    for movie in movie_list_genre2:
        if movie not in finalMovieSet:
            finalMovieSet.append(movie)
    M = len(finalMovieSet)
    genre2_tags = DatabaseOperations.getTagFromMovieDictionary(cursor, movie_list_genre2)
    # computing the number of movies without tag
    for tag in genre2_tags:
        genre2_tags[tag] = R - genre2_tags[tag]

    genre1_genre2_tags = DatabaseOperations.getTagFromMovieDictionary(cursor, finalMovieSet)
    # computing the number of movies without tag
    for tag in genre1_genre2_tags:
        genre2_tags[tag] = M - genre1_genre2_tags[tag]
    final_tag_dict = dict()
    for tag in genre1_genre2_tags:
        if tag not in genre2_tags:
            rij = 0
        else:
            rij = genre1_genre2_tags[tag]

        if M == R or genre1_genre2_tags[tag] == rij or R == rij:
            final_tag_dict[tag] = float(R - rij) / R
        elif rij == 0:
            final_tag_dict[tag] = float(genre1_genre2_tags[tag]) / (M - R)
        else:
            log_term = (float(rij) * (M - R + float(rij) - genre1_genre2_tags[tag])) / (
            (R - rij) * (float(genre1_genre2_tags[tag]) - rij))
            modulus_term = abs(rij / R) - (float((genre1_genre2_tags[tag] - rij)) / (M - R))
            final_tag_dict[tag] = abs((math.log(log_term)) * modulus_term)
    sortedDict(final_tag_dict, cursor)


if __name__ == '__main__':
    main()