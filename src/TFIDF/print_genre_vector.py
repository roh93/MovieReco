from __future__ import division
from DatabaseConnect import DatabaseConnect
import sys
import math
import DatabaseOperations
import operator
from Utils import dateWeightGenerator


def main():
    if len(sys.argv) == 3:
        db_obj = DatabaseConnect()
        genre = sys.argv[1]
        model = sys.argv[2]
        cursor = db_obj.getCursorForDatabase()
        results = DatabaseOperations.getGenreDetails(cursor, genre)

        genre_information = {"genres": results}
        tag_names = dict()
        tag_names["tf"] = {}
        tag_names["weight_ts"] = {}
        tag_names["weight_rank"] = {}
        tag_names["idf"] = {}

        for tuple_list in genre_information["genres"]:
            tuple_list = list(tuple_list)
            tuple_list[2] = dateWeightGenerator(tuple_list[2].split(' ')[0])
            if tuple_list[4] not in tag_names["tf"].keys():
                tag_names["tf"][tuple_list[4]] = 1
                tag_names["weight_ts"][tuple_list[4]] = tuple_list[2]
                tag_names["idf"][tuple_list[4]] = math.log(float(17)/DatabaseOperations.getTagsForIdfGenres(cursor, tuple_list[4],genre)[0][0])
            else:
                tag_names["tf"][tuple_list[4]] += 1
                tag_names["weight_ts"][tuple_list[4]] += tuple_list[2]

        genre_vector_mapping_dict = {}
        genre_vector_mapping_tfidf = {}

        for tag in tag_names["tf"].keys():
            tag_names["weight_ts"][tag] = float(tag_names["weight_ts"][tag])/float(tag_names["tf"][tag])
            tag_names["tf"][tag] = float(tag_names["tf"][tag])/len(genre_information["genres"])
            genre_vector_mapping_dict[tag] = str(tag_names["tf"][tag] * tag_names["weight_ts"][tag])
            genre_vector_mapping_tfidf[tag] = str(tag_names["tf"][tag] * tag_names["weight_ts"][tag] * tag_names["idf"][tag])

        if model == "tf":
            a = sorted(genre_vector_mapping_dict.items(), key=operator.itemgetter(1), reverse=True)
            for b,c in a:
                print b, '-->', c

        if model == "tfidf":
            a = sorted(genre_vector_mapping_tfidf.items(), key=operator.itemgetter(1), reverse=True)
            for b, c in a:
                print b, '-->', c

        cursor.close()
        db_obj.closeDatabaseConnection()
    else:
        print "Options-> Argument 1 is genre and Argument 2 is model"

if __name__ == '__main__':
    main()
