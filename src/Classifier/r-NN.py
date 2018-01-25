import pandas as pd
import numpy as np
import sys

def main():
    if len(sys.argv) == 2:
        r = int(sys.argv[1])
        training_set_movie_list = []
        labels_list = []
        with open('training.txt') as fp:
            for line in fp:
                a = line.split(' ')
                training_set_movie_list.append(int(a[0]))
                labels_list.append(a[1].strip())

        label_dict = dict(zip(training_set_movie_list, labels_list))

        movies_data = readMovieData()
        training_df = pd.DataFrame(0, index=training_set_movie_list, columns=movies_data.columns)
        for index in training_df.index:
            training_df.loc[index] = movies_data.loc[index]
        movies_data.drop(training_set_movie_list, inplace=True)
        distance_matrix = movies_data.dot(training_df.T)

        order = np.argsort(-distance_matrix.values, axis=1)
        for i in range(0, len(distance_matrix.index)):
            rNN_labels_list = [label_dict[distance_matrix.columns[order[i][k]]] for k in range(r)]
            print(distance_matrix.iloc[i].name, '-->', max(set(rNN_labels_list), key=rNN_labels_list.count))
    else:
        print('Not Enough Paramaeters')


def readMovieData():
    movies_data = pd.read_csv('mtvlda.csv')
    movies_data.set_index('movieid', inplace=True)
    return movies_data

if __name__ == '__main__':
    main()
