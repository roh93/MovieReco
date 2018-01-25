from DatabaseConnect import DatabaseConnect
from scipy.spatial.distance import cosine as cosine_dist
import DBOps
import pandas as pd
import numpy as np


def cosine_similarity(tag_vactor_a, tag_vector_b):
    a = [0, 0, 1]
    b = [1, 2, 1]
    print 1 - cosine_dist(a, b)

def personalised_ranking(alpha, seed_vector, data_matix):
    p_not_seed = (1 - alpha)
    for column in data_matix:
        data_matix[column] = data_matix[column].apply(lambda x: (float(x) / a[column].sum()) * p_not_seed if a[column].sum() > 0 else (float(x) * p_not_seed) / 1)

    identity_mat = pd.DataFrame(index=[k for k in data_matix], columns=[k for k in data_matix])
    identity_mat = identity_mat.fillna(0)
    for col in identity_mat:
        identity_mat.set_value(col, col, 1)
    # print identity_mat

    seed_matrix_df = pd.DataFrame(index=[k for k in data_matix], columns=['Value'])
    seed_matrix_df['Value'] = 0.0
    for seed in seed_vector:
        seed_matrix_df.set_value(seed, 'Value', 1.0 / len(seed_vector))
    # print seed_matrix_df

    transformed_mat = identity_mat.subtract(data_matix)
    # print transformed_mat

    for col in transformed_mat:
        transformed_mat[col] = transformed_mat[col].apply(lambda x: x * alpha)

    df_inv = pd.DataFrame(np.linalg.pinv(transformed_mat.values), transformed_mat.columns, transformed_mat.index)
    inverse = df_inv.dot(transformed_mat)
    # print(inverse)

    final_mat = inverse.dot(seed_matrix_df)
    final_mat = final_mat.sort_values('Value', ascending=False)
    # print final_mat

    for items in range(len(seed_vector), len(seed_vector) + 10):
        print DBOps.getActorName(str(final_mat.iloc[items].name),cursor)



#tag_mapping = pd.read_csv('C:\\Users\\Rohit\\Desktop\\CSE515\\Phase2_data\\genome-tags.csv')
tag_mapping = pd.read_csv('C:\\Users\\Rohit\\Desktop\\Phase2_mwd\\Code\\Task 1\\Code_t1\\genome-tags.csv')
tag_mapping_dict = dict([(i, j) for i, j in zip(tag_mapping.tagId, tag_mapping.tag)])
#print tag_mapping_dict.values()

db_obj = DatabaseConnect()
cursor = db_obj.getCursorForDatabase()

total_actors = DBOps.getActorCount(cursor)[0][0]
#print total_actors
#print len(total_actors)

actor_matrix = {}
for a in DBOps.getListOfActors(cursor):
    cursor.callproc('mwdb.GetActorTags', (a[0],))
    for result in cursor.stored_results():
        lis = result.fetchall()
        actor_matrix[a[0]] = {}
        actor_matrix[a[0]] = dict.fromkeys(tag_mapping_dict.values(), 0)
        for l in lis:
            actor_matrix[a[0]][tag_mapping_dict[l[0]]] += 1.0/len(lis)

actor_matrix_df = pd.DataFrame.from_dict(actor_matrix,orient='index')

actor_matrix_df_transpose = pd.DataFrame.transpose(actor_matrix_df)

a = actor_matrix_df.dot(actor_matrix_df_transpose)

alpha = 0.3

seedno = int(raw_input("Enter number of seed actors "))
seed_vector= [0 for i in range(seedno)]

for i in range(seedno):
    actorno = int(raw_input("Enter seed actor "+str(i+1) +" "))
    seed_vector[i] = actorno

print("")
print("The 10 most related actors to the actors given in the seed set are:")  
print("")
    
personalised_ranking(alpha, seed_vector, a)
