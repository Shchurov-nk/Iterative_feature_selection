import pandas as pd
import numpy as np

from mask_utils.masking import create_mask

XX_dist = pd.read_csv("data/corr/XX_dist.csv", index_col=0)
XY_dist = pd.read_csv("data/corr/XY_dist.csv", index_col=0)

level_xx = 0.95
level_xy = 0.0
mask_result = create_mask(XX_dist.to_numpy(), XY_dist, level_xx, level_xy)
mask_result.to_csv("data/masks/95_00_masks.csv")