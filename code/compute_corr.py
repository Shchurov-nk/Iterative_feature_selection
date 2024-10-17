import pandas as pd
import numpy as np

def pearson_corr(df_X, df_Y):
    X_names = [i for i in df_X.columns]
    Y_names = [i for i in df_Y.columns]
    # XY_result = np.array([])
    XY_result = []
    for Y_name in Y_names:
        Y = df_Y[Y_name]
        X = df_X
        corXY = X.corrwith(Y, axis=0, drop=False, method='pearson')
        corXY = corXY.to_numpy()
        corXY = np.absolute(corXY)
        corXY = np.array(corXY)
        XY_result.append(corXY)

    XY_result = np.around(XY_result, decimals=5)
    XY_result = pd.DataFrame(XY_result)
    XY_result = XY_result.transpose()
    XY_result.index = X_names
    XY_result.columns = Y_names

    corXX = X.corr()
    corXX = corXX.to_numpy()
    corXX = np.absolute(corXX)
    corXX = np.around(corXX, decimals=5)
    # заполняем диагональ нулями (т.к корреляция элемента с самим собой = 1)
    corXX[np.diag_indices(len(corXX))] = 0
    XX_result = pd.DataFrame(corXX, index=X_names, columns=X_names)
    # file_XX_name = f'{result_path}/corrXX.csv'
    # np.savetxt(file_XX_name, corXX, fmt='%s', delimiter=",")
    return XX_result, XY_result
# TODO: Добавить больше функций (например, энтропию и веса нейронных сетей)

X_path = "data/raw/salts_water_basic_IR.csv"
Y_path = "data/raw/salts_water_basic_output_i.csv"
result_path = "../data/corr/"
df_X = pd.read_csv(X_path, delimiter = ",", header = 0, index_col = 0)
df_Y = pd.read_csv(Y_path, delimiter = ",", header = 0, index_col = 0)[1:]

XX_dist, XY_dist = pearson_corr(df_X, df_Y)

XX_dist.to_csv("data/corr/XX_dist.csv")
XY_dist.to_csv("data/corr/XY_dist.csv")