

def getActorDetails(cursor, actor_id):
    cursor.execute("SELECT * FROM T1_VIEW WHERE ACTORID=%s", (actor_id,))
    return cursor.fetchall()


def getMaxRatingsOfActors(cursor):
    cursor.execute("SELECT max(actor_movie_rank) FROM MOVIE_ACTOR")
    return cursor.fetchall()

def getTotalActorCount(cursor):
    cursor.execute("select count(distinct(actorid)) from t1_view")
    return cursor.fetchall()

def getTagsForIdfWeighting(cursor, tag):
    cursor.execute("select count(distinct(tag)), actorid from t1_view where tag=%s group by actorid",(tag,))
    return cursor.fetchall()


def getTagsForIdfGenres(cursor, tag, genre):
    var = '%' + genre + '%'
    cursor.execute("select count(distinct(movieid)) from t2_view where tag=%s and genres like %s", (tag,var))
    return cursor.fetchall()

def getGenreDetails(cursor, genre):
    var = '%'+genre+'%'
    cursor.execute("select * from T2_VIEW where genres like %s", (var,))
    return cursor.fetchall()

def getMoviesForUser(cursor, userid):
    cursor.execute("select movieid from mlratings where userid = %s",(userid,))
    return cursor.fetchall()

def getTagFromMovie(cursor, movieid):
    cursor.execute("select tagid from mltags where movieid=%s",(movieid,))
    return cursor.fetchall()


def fetchTagForMovies(movieid,cursor):
    mov_list=list()
    cursor.execute("select tagid from mltags where movieid=%s",(movieid,))
    for item in cursor.fetchall():
        mov_list.append(item[0])
    return mov_list

def fetchTagForUser(movieid,cursor):
    cursor.execute('select tagid, timestamp from mltags where movieid= %s',(movieid,))
    return cursor.fetchall()

def fetchNumberofUserForTag(tag,cursor):
    cursor.execute('select mlratings.userid,mltags.userid from mltags,mlratings where tagid=%s and mltags.movieid=mlratings.movieid',(tag,))
    userData=cursor.fetchall()
    userList=list()
    for touple in userData:
        if touple[0] not in userList:
            userList.append(touple[0])
        if touple[1] not in userList:
            userList.append(touple[1])
    return len(userList)

def getTagsForCombinedGenres(cursor, genre1, genre2):
    var1 = '%' + genre1 + '%'
    var2 = '%' + genre2 + '%'
    cursor.execute("select distinct(tag) from T2_VIEW where genres like %s OR genres like %s", (var1,var2))
    return cursor.fetchall()

def getCombinedMovieList(cursor, genre1, genre2):
    var1 = '%' + genre1 + '%'
    var2 = '%' + genre2 + '%'
    cursor.execute("select distinct(movieid) from T2_VIEW where genres like %s OR genres like %s", (var1,var2))
    return cursor.fetchall()

def getTagsCountForGenreMovies(cursor, tag, genre1, genre2):
    tag =str(tag)
    var1 = '%' + genre1 + '%'
    var2 = '%' + genre2 + '%'
    cursor.execute("select count(distinct(movieid)) from T2_VIEW where genres like %s OR genres like %s and tag=%s", (var1,var2,tag))
    return cursor.fetchall()

def getMovieListForGenre(cursor, genre):
    var = '%' + genre + '%'
    cursor.execute("select movieid from mlmovies where genres like %s",(var,))
    return cursor.fetchall()

def getTagFromMovieDictionary(cursor, movie_list):
    tagVector = dict()
    for movie in movie_list:
        movie_tag_count = dict()
        cursor.execute('select tagid from mltags where movieid=%s', (movie,))
        result = cursor.fetchall()
        for tag in result:
            if (tag[0] not in tagVector) and (tag[0] not in movie_tag_count):
                movie_tag_count[tag[0]] = 1
                tagVector[tag[0]] = 1
            elif (tag[0] in tagVector) and (tag[0] not in movie_tag_count):
                movie_tag_count[tag[0]] = 1
                tagVector[tag[0]] = 1 + tagVector[tag[0]]
    return tagVector

def getTagname(tagid,cursor):
    cursor.execute("SELECT tag from genome_tags where tagid=%s",(tagid,))
    return cursor.fetchall()[0]