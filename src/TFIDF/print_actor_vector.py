from __future__ import division

import operator

from DatabaseConnect import DatabaseConnect
import sys
import math
import DatabaseOperations
from Utils import dateWeightGenerator


def main():
    if len(sys.argv) == 3:
        db_obj = DatabaseConnect()
        actor_id = sys.argv[1]
        model = sys.argv[2]
        cursor = db_obj.getCursorForDatabase()
        results = DatabaseOperations.getActorDetails(cursor, actor_id)
        max_rating_val = DatabaseOperations.getMaxRatingsOfActors(cursor)[0][0]

        actor_information = {"movies": results}
        tag_names = dict()
        tag_names["tf"] = {}
        tag_names["weight_ts"] = {}
        tag_names["weight_rank"] = {}
        tag_names["idf"] = {}

        max_actor_count = 17306 #DatabaseOperations.getTotalActorCount(cursor)[0][0]

        for tuple_list in actor_information["movies"]:
            tuple_list = list(tuple_list)
            tuple_list[2] = (max_rating_val - tuple_list[2])/max_rating_val
            tuple_list[3] = dateWeightGenerator(tuple_list[3])
            if tuple_list[5] not in tag_names["tf"].keys():
                tag_names["tf"][tuple_list[5]] = 1
                tag_names["weight_ts"][tuple_list[5]] = tuple_list[3]
                tag_names["weight_rank"][tuple_list[5]] = tuple_list[2]
                tag_names["idf"][tuple_list[5]] = math.log(float(max_actor_count)/len(DatabaseOperations.getTagsForIdfWeighting(cursor,tuple_list[5])))
            else:
                tag_names["tf"][tuple_list[5]] += 1
                tag_names["weight_ts"][tuple_list[5]] += tuple_list[3]
                tag_names["weight_rank"][tuple_list[5]] += tuple_list[2]

        actor_vector_mapping_dict = {}
        actor_vector_mapping_tfidf = {}

        for tag in tag_names["tf"].keys():
            #print tag, tag_names["weight_ts"][tag], tag_names["weight_rank"][tag], tag_names["tf"][tag]
            tag_names["weight_ts"][tag] = float(tag_names["weight_ts"][tag])/float(tag_names["tf"][tag])
            tag_names["weight_rank"][tag] = float(tag_names["weight_rank"][tag])/float(tag_names["tf"][tag])
            tag_names["tf"][tag] = float(tag_names["tf"][tag])/len(actor_information["movies"])
            actor_vector_mapping_dict[tag] = str(tag_names["tf"][tag] * tag_names["weight_rank"][tag] * tag_names["weight_ts"][tag])
            actor_vector_mapping_tfidf[tag] = str(tag_names["tf"][tag] * tag_names["weight_rank"][tag] * tag_names["weight_ts"][tag] * tag_names["idf"][tag])

        if model == "tf":
            a = sorted(actor_vector_mapping_dict.items(), key=operator.itemgetter(1), reverse=True)
            for b, c in a:
                print b, '-->', c

        if model == "tfidf":
            a = sorted(actor_vector_mapping_tfidf.items(), key=operator.itemgetter(1), reverse=True)
            for b, c in a:
                print b, '-->', c

        cursor.close()
        db_obj.closeDatabaseConnection()

    else:
        print "Options-> Argument 1 is actor_id and Argument 2 is model"

if __name__ == '__main__':
    main()
