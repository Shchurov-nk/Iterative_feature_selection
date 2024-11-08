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
    return mask.tolist()


# TODO возможно стоит сделать класс mask с двумя методами: create и save

def create_masks(corXX, corXY):
    elem_names = [i for i in corXY.columns]
    # mask = np.zeros(shape=(corXY.shape[1], corXY.shape[0]))
    mask = []
    for element in elem_names:
        for level_xx in range(900, 1000, 5):
            level_xx = level_xx / 1000
            for level_xy in range(0, 30, 5):
                level_xy = level_xy / 100
                ifs_result = IFS(corXX, corXY[element].to_numpy(), level_xx, level_xy)
                mask.append([element, level_xx, level_xy, sum(ifs_result)] + ifs_result)
    mask = pd.DataFrame(mask)
    # mask = mask.astype(bool)
    mask.columns = ["Element", "T_xx", "T_xy", "Num_of_selected"] + corXY.index.tolist()
    return mask

XX_dist = pd.read_csv("data/corr/XX_dist.csv", index_col=0)
XY_dist = pd.read_csv("data/corr/XY_dist.csv", index_col=0)

mask_result = create_masks(XX_dist.to_numpy(), XY_dist)
mask_result.to_csv("data/masks/masks.csv")