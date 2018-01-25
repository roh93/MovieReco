def getListOfActors(cursor):
    cursor.execute('SELECT ACTORID FROM MOVIE_ACTOR')
    return cursor.fetchall()

def getTags(cursor):
    cursor.execute('SELECT tagid from mltags m inner join (select movieid from mltags) as mov on m.movieid = mov.movieid')
    return cursor.fetchall()

def getActorCount(cursor):
    cursor.execute('select count(distinct(actorid)) from movie_actor')
    return cursor.fetchall()

def getAllMovies(cursor):
    cursor.execute('select distinct(movieid) from movie_actor')
    return cursor.fetchall()

def getAllRatings(cursor):
    cursor.execute('select distinct(rating) from mlratings')
    return cursor.fetchall()

def getAllTags(cursor):
    cursor.execute('select distinct(tagid) from mltags')
    return cursor.fetchall()

def getActorName(actor1,cursor):
    cursor.execute("Select name from imdb_actor_info where id = %s",(actor1,))
    result=cursor.fetchall()[0]
    return result[0]
