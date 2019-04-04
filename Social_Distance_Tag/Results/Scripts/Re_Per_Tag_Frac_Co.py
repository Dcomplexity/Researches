import numpy as np
import pandas as pd
import os


abspath = os.path.abspath(os.path.join(os.getcwd(), "../"))
dirname = abspath + "Re_Per_Tag_Frac_Co/"
filename = dirname + "Re_Per_Tag_10_uniform_Gs_8_Dp_1.2_t_1.0.csv"
data = pd.read_csv(filename, index_col=0)
print(data.iloc[0])