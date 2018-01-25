import pandas as pd
import math
import sys
import numpy as np
import datetime as dt
import lda
import print_genre_vector_rtr as pgv
import print_genre_vector2_rtr as pgv2
pd.set_option('display.max_colwidth', -1)

def p2t1a(g,m):
    #data importing and cleaning
    df_g=pd.read_csv('mlmovies.csv')
    df_t=pd.read_csv('genome-tags.csv')
    t=list(df_t['tag'].unique())
    a=list(df_g['genres'].str.split('|', expand=True).stack().unique())
    index=a
    columns=t
    actor_tm=pd.DataFrame(index=index,columns=columns)
    actor_tm=actor_tm.fillna(0)
    doc_tm=pd.DataFrame(index=index,columns=columns)
    doc_tm=doc_tm.fillna(0)

    #matrix construction
    for i in a:
        c=pgv.print_genre_vector(i,'tfidf')
        d=pgv2.print_genre_vector(i,'tf')
        actor_tm.loc[i]=c
        doc_tm.loc[i]=d

    #droping empty rows and columns
    actor_tm=actor_tm.dropna(axis=1,how='all')
    actor_tm=actor_tm.dropna(axis=0,how='all')
    actor_tm=actor_tm.fillna(0)
    ind_a=actor_tm.index.copy()
    col_a=actor_tm.columns.copy()
    doc_tm=doc_tm.dropna(axis=1,how='all')
    doc_tm=doc_tm.dropna(axis=0,how='all')
    doc_tm=doc_tm.fillna(0)
    vocab=doc_tm.columns.copy().tolist()
    vocab=tuple(vocab)
    ind_g=doc_tm.index.copy()

    if m=='svd':
        U,C,V=np.linalg.svd(actor_tm,full_matrices=False)
        C=np.diag(C)
        U=U.dot(C)
        U_df = pd.DataFrame(U[:,0:4], index=a,columns=['l0','l1','l2','l3'])
        V_df = pd.DataFrame(V[0:4,:], columns=t,index=['l0','l1','l2','l3'])
        print(U_df.loc[g])
        print(V_df)


    if m=='pca':
        X_std=actor_tm
        mean_vec = np.mean(X_std, axis=0)
        cov_mat = (X_std - mean_vec).T.dot((X_std - mean_vec)) / (X_std.shape[0]-1)
        U_p,C_p,V_p= np.linalg.svd(cov_mat,full_matrices=False)
        U_p=U_p[:,0:4]
        new_U=X_std.as_matrix().dot(U_p)
        U_p=pd.DataFrame(U_p,index=col_a,columns=['l0','l1','l2','l3'])
        new_U=pd.DataFrame(new_U,index=a,columns=['l0','l1','l2','l3'])
        print(new_U.loc[g])
        print(U_p.T)

    if m=='lda':
        doc_tm1=doc_tm.as_matrix()
        doc_tm1=doc_tm1.astype(int)
        model = lda.LDA(n_topics=4, n_iter=1500, random_state=1)
        model.fit(doc_tm1)
        topic_word = model.topic_word_
        n_top_words = 5
        for i, topic_dist in enumerate(topic_word):
            topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
            print('Topic {}: {}'.format(i, ','.join(topic_words)))
        c=model.transform(doc_tm1)
        c=pd.DataFrame(c,index=ind_g,columns=['t0','t1','t2','t3'])
        print(c.loc[g])

    else:
        print('pca/svd/lda')


p2t1a(sys.argv[1],sys.argv[2])
