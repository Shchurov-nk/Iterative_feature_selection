import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns



# TODO сделать файл visualisation, который будет рисовать эти графики
def plot_xy_corr(corXY):
    for col_name in corXY.columns:
        plt.title(col_name)
        plt.plot(corXY[col_name])
        plt.show()

# TODO сделать нормальное отображение оси абцисс (сейчас выводятся все числа, причем)
def plot_mask(mask, spectrum, i, row):
    plt.plot(spectrum.iloc[row, :])
    arr = mask[i]*(spectrum.iloc[row, :].T).to_numpy()
    arr[arr == 0] = np.nan
    plt.plot(arr, '.', color = 'red')


