import pandas as pd


def main():
    training_set_movie_list = []
    labels_list = []
    with open('training.txt') as fp:
        for line in fp:
            a = line.split(' ')
            training_set_movie_list.append(int(a[0]))
            labels_list.append(a[1].strip())
    movies_data = readMovieData()
    training_df = pd.DataFrame(0, index=training_set_movie_list, columns=movies_data.columns)
    for index in training_df.index:
        training_df.loc[index] = movies_data.loc[index]
    training_df = training_df.assign(label=pd.Series(labels_list).values)

    training_mat = training_df.as_matrix()
    tree = build_tree(training_mat, 10, 1)
    for index in movies_data.index:
        print(index, '-->', predict_label(tree, movies_data.loc[index].tolist()))


def readMovieData():
    movies_data = pd.read_csv('u_df.csv')
    movies_data.set_index('movieid', inplace=True)
    return movies_data


def giniIndexCalculate(groups, classes):
    gini = 0.0
    n_instances = float(sum([len(group) for group in groups]))
    for group in groups:
        size = float(len(group))
        if size == 0:
            continue
        score = 0.0
        for class_val in classes:
            p = [row[-1] for row in group].count(class_val) / size
            score += p * p
        gini += (1.0 - score) * (size / n_instances)
    return gini


def splitDataset(index, value, dataset):
    left, right = list(), list()
    for row in dataset:
        if row[index] < value:
            left.append(row)
        else:
            right.append(row)
    return left, right


def getBestSplit(feature_data):
    class_values = list(set(row[-1] for row in feature_data))
    b_index, value, score, groups = 999, 999, 999, None
    for index in range(len(feature_data[0])-1):
        for row in feature_data:
            groups = splitDataset(index, row[index], feature_data)
            gini = giniIndexCalculate(groups, class_values)
            if gini < score:
                b_index, value, score, groups = index, row[index], gini, groups
    return {'index': b_index, 'value': value, 'groups': groups}


def assignLeafLabel(group):
    outcomes = [row[-1] for row in group]
    return max(set(outcomes), key=outcomes.count)


def split(node, max_depth, min_size, depth):
    left, right = node['groups']
    del(node['groups'])
    if not left or not right:
        node['left'] = node['right'] = assignLeafLabel(left + right)
        return
    if depth >= max_depth:
        node['left'], node['right'] = assignLeafLabel(left), assignLeafLabel(right)
        return
    if len(left) <= min_size:
        node['left'] = assignLeafLabel(left)
    else:
        node['left'] = getBestSplit(left)
        split(node['left'], max_depth, min_size, depth+1)
    if len(right) <= min_size:
        node['right'] = assignLeafLabel(right)
    else:
        node['right'] = getBestSplit(right)
        split(node['right'], max_depth, min_size, depth+1)


def build_tree(train, max_depth, min_size):
    root = getBestSplit(train)
    split(root, max_depth, min_size, 1)
    return root


def predict_label(node, row):
    if row[node['index']] < node['value']:
        if isinstance(node['left'], dict):
            return predict_label(node['left'], row)
        else:
            return node['left']
    else:
        if isinstance(node['right'], dict):
            return predict_label(node['right'], row)
        else:
            return node['right']


if __name__ == '__main__':
    main()