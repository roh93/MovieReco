CREATE VIEW T1_VIEW AS SELECT actorid,mltags.movieid,actor_movie_rank,timestamp,genome_tags.tagid,tag from genome_tags,mltags,movie_actor WHERE  mltags.movieid=movie_actor.movieid AND genome_tags.tagid=mltags.tagid;


select * from t1_view;

select max(actor_movie_rank) from movie_actor;

select * from t1_view where actorid=708940 order by tag;

select count(distinct(actorid)) from t1_view;

select count(distinct(actorid)) from movie_actor;

select count(distinct(tag)), actorid from t1_view where tag="hilarious" group by actorid;


CREATE VIEW T2_VIEW AS SELECT genres,mltags.movieid,timestamp,genome_tags.tagid,tag from genome_tags,mltags,mlmovies WHERE  mltags.movieid=mlmovies.movieid AND genome_tags.tagid=mltags.tagid;

select * from T2_VIEW where genres like '%thriller%';

select count(distinct(movieid)) from t2_view where tag= 'nudity (rear)' and genres like '%drama%';

select * from t2_view;

select count(*) from ml_ratings;

select count(*) from T2_VIEW where genres like '%drama%' OR genres like '%thriller';

select distinct(movieid) from t2_view where genres like '%drama%' OR genres like '%thriller%' and tag='80s';

select count(distinct(tag)) from t2_view where genres like '%drama%' OR genres like '%thriller';





LOAD DATA LOCAL INFILE 'C:\\Users\\Rohit\Desktop\\CSE515\\Phase1\\phase1_dataset\\mlratings.csv' INTO TABLE mlratings
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\r\n;'
IGNORE 1 LINES
(movieid, userid, imbid, rating, timestamp);



select movieid from mlmovies where genres like '%drama%';

select count(distinct(movieid)) from t2_view where genres like '%drama%' OR genres like '%thriller%';

