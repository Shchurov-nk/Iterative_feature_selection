import pandas as pd
import numpy as np

# TODO возможно стоит воспользоваться готовым решением из numpy
# ma.masked_where или ma.make_mask

# TODO переписать без использования copy и изменить названия переменных (убрать "_", переименовать функцию)
import copy
def IFS(corXX, corXY, level_xx, level_xy):
    mask = np.zeros(corXX.shape[0], dtype=int)
    copy_corXY = copy.copy(corXY)
    while np.max(copy_corXY) > level_xy:
        i_bestXY = np.argmax(copy_corXY)
        # print("Лучший:", i_bestXY, "\nПохожие:")
        mask[i_bestXY] = 1
        copy_corXY[i_bestXY] = 0
        for i in range(corXX.shape[0]):
            if mask[i] == 0:
                if corXX[i_bestXY][i]>level_xx:
                    copy_corXY[i] = 0
                    # print(i)
    return mask


# TODO возможно стоит сделать класс mask с двумя методами: create и save

def create_mask(corXX, corXY, level_xx, level_xy):
    elem_names = [i for i in corXY.columns]
    mask = np.zeros(shape=(corXY.shape[1], corXY.shape[0]))
    for i, element in enumerate(elem_names):
        mask[i] = IFS(corXX, corXY[element].to_numpy(), level_xx, level_xy)
    mask = pd.DataFrame(mask)
    mask = mask.transpose()
    mask.columns = corXY.columns
    mask.index = corXY.index
    mask = mask.astype(int)
    # mask.reindex_like(corXY)
    return mask