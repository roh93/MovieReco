import pandas as pd
import math
import sys
import numpy as np
import datetime as dt
import lda


def svd500lf():
    df=pd.read_csv("mtvnew.csv").set_index("movieid")
    ind_m=list(df.index).copy()
    col_t=list(df.columns).copy()
    print("svd start")
    U,C,V = np.linalg.svd(df,full_matrices=False)
    print("svd end")
    u_df=pd.DataFrame(U,index=ind_m)
    u_df=u_df.ix[:,:499]
    print(u_df.head())
    u_df.to_csv("u_df.csv")

    return
svd500lf()
