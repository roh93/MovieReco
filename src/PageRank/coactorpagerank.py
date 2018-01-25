# -*- coding: utf-8 -*-
"""
Created on Mon Oct 02 20:08:48 2017

@author: venka
"""

from __future__ import division
import sys
import mysql.connector
import numpy
from math import*

#import routines

def main():
    createCoActorCoActorMatrix()
    
def createAllActorsVector(cur):
    cur.execute("select id from imdb_actor_info")
    result=cur.fetchall()
    listOfActors=list()
    for item in result:
        listOfActors.append(item[0])
    return listOfActors

def getcountofmovies(actor1,actor2,cur):
    if actor1 == actor2:
        return 0
    else:
        cur.execute("select count(*) from movie_actor m1, movie_actor m2 where m1.movieid=m2.movieid and m1.actorid = %s and m2.actorid = %s",(actor1,actor2))
        result=cur.fetchall()[0]
    return result[0]

def getActorName(actor1,cur):
    cur.execute("Select name from imdb_actor_info where id = %s",(actor1,))
    result=cur.fetchall()[0]
    return result[0]

def getadjmtx(w,h,Matrix):

    coltotalmatrix = [0.0 for x in range(w)] 
     
    
    for i in range(w):    
        for j in range(h):
#             print(Matrix[j][i])
             coltotalmatrix[i] = coltotalmatrix[i] + Matrix[j][i]
#            print(str(i) + str(j)+str(Matrix[j][i]))
#        print(coltotalmatrix[i])
           
    for i in range(w):    
        for j in range(h):
            if coltotalmatrix[i] != 0:    
                Matrix[j][i] =  Matrix[j][i]/ coltotalmatrix[i]
    return Matrix

    

def createCoActorCoActorMatrix():
    cnx = mysql.connector.connect(user='root', password='root',host='127.0.0.1',database='mwdb')
    cur = cnx.cursor()
    seedno = int(raw_input("Enter number of seed actors "))
    
    actorseeds= [0 for i in range(seedno)]
    
    c = 0.30
    
    for i in range(seedno):
        actorno = int(raw_input("Enter seed actor "+str(i+1) +" "))
        actorseeds[i] = actorno
        
    print("")
    print("The 10 most related actors to the actors given in the seed set are:")  
    print("")
    
    AllActors=createAllActorsVector(cur)
    
    
    actornumber = 0
    actorcount = {}
    for actor in sorted(AllActors):
        actorcount.update({actor:actornumber})
        actornumber = actornumber+1
    
    matrix =[[0 for i in range(actornumber)] for j in range(actornumber)]
    
    for actor1 in sorted(AllActors):
        for actor2 in sorted(AllActors):
             matrix[actorcount[actor1]][actorcount[actor2]]=getcountofmovies(actor1,actor2,cur)
 #             coactorcoactorsimmtx[CoactorDict[coactor1]][CoactorDict[coactor2]]=
              
    actorlist = '    '
    for actor1 in sorted(AllActors):
        actorlist= actorlist+str(actor1)+' '
        
#    print actorlist         
    
    adjmatrix =[[0 for i in range(actornumber)] for j in range(actornumber)]
    
    adjmatrix = getadjmtx(actornumber, actornumber, matrix)
             
#    for k,i in sorted(actorcount.iteritems()):
#          print str(k)+' '+str(matrix[i])
 
#    print(adjmatrix[1])
    
    identitymtx = [[0 for i in range(actornumber)] for j in range(actornumber)]
    
    for i in range(actornumber):
        for j in range(actornumber):
            if i==j:
                identitymtx[i][j] = 1
    vectorq = [0 for i in range(actornumber)] 
    for k in range(seedno):
        vectorq[actorcount[actorseeds[k]]] = 1/seedno;
    
    cc= 1-c
    
    mtxtemp = [[0 for i in range(actornumber)] for j in range(actornumber)]
    mtxtemp2 = [[0 for i in range(actornumber)] for j in range(actornumber)]
    
    for i in range(actornumber):
        for j in range(actornumber):
           mtxtemp[i][j] = identitymtx[i][j]- (cc * adjmatrix[i][j])  
    
    mtxtemp2 = numpy.linalg.inv(mtxtemp)
    
    for i in range(actornumber):
        for j in range(actornumber):
            mtxtemp2[i][j] = c * mtxtemp2[i][j]
    
    
#    print(mtxtemp2)
#    print(vectorq)
    

    finalmtx = numpy.dot(mtxtemp2,vectorq)
    
#    for i in range(actornumber):
#        print(finalmtx[i])
    
    cpymtx = [0 for i in range(actornumber)]
    
    cpymtx = sorted(finalmtx, reverse=True) 
    
    sortedActors = sorted(AllActors)
#    print(finalmtx)
#    print(cpymtx)
    actornumber1=actornumber    

    for i in range(seedno):
        sortedActors.remove(actorseeds[i])
        actornumber1=actornumber1-1
 
   # print("The 10 most related actors to the actors given in the seed set are:")  
#    for i in range(10):
    i=0
    p=0
    while p<10 and cpymtx[i] != 0:
#        print(i)
#        print(cpymtx[i])
        if cpymtx[i]!=0:
            k = cpymtx[i]
            for j in range(actornumber1):
                if finalmtx[j] == k:
                    print(getActorName(sortedActors[j],cur))
#                    print(i)
                    sortedActors.remove(sortedActors[j])
                    actornumber1=actornumber1-1
                    i=i+1
                    p=p+1
                    break
                else:
#                     print("Hi")
                     if j==actornumber1-1:
                        
                         i=i+1
                     
                         
 #                   m = 0
 #                   for actor1 in sorted(AllActors):
 #                       if m == j:
 #                           print(actor1)
 #                           break
 #                       m = m + 1
                        
                    
    
    
  #  print(vectorq)   
  #  a1 = int(raw_input("Enter actor 1"))
   # a2 = int(raw_input("Enter actor 2"))    
    
  #  print( matrix[actorcount[a1]][actorcount[a2]])


    cnx.close()


if __name__ == "__main__":
    main()