from Phase2.DBOps import getAllMovies, getAllRatings, getAllTags
from Phase2.DatabaseConnect import DatabaseConnect
import numpy as np
import tensorly.decomposition as td

db_obj = DatabaseConnect()
cursor1 = db_obj.getCursorForDatabase()
cursor2 = db_obj.getCursorForDatabase()
movie_list = getAllMovies(cursor1)
ratings_list = getAllRatings(cursor1)
tags_list = getAllTags(cursor1)

movie_list = [a[0] for a in movie_list]
ratings_list = [a[0] for a in ratings_list]
tags_list = [a[0] for a in tags_list]

data_array = np.zeros((len(tags_list), len(movie_list), len(ratings_list)), dtype=int)

for tag in tags_list:
    cursor1.callproc('mwdb_p2.GetMovies', (tag,))
    for result in cursor1.stored_results():
        lis = result.fetchall()
        for movie in lis:
            cursor2.callproc('mwdb_p2.GetAvgRating', (movie[0],))
            for res in cursor2.stored_results():
                ratl = res.fetchall()
                for r in ratl:
                    for ratin in ratings_list:
                        if r[0] <= ratin:
                            data_array[tags_list.index(tag)][movie_list.index(movie[0])][ratings_list.index(ratin)] = 1
print type(data_array)

for i in range(0,79):
    for j in range(0,86):
        print data_array[i][j]
a = td.parafac(data_array, 5, 200, it, random_state=None, verbose=False)
#print a[1]