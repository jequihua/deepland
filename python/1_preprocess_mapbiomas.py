import numpy as np
import rioxarray
import xarray

from misc_functions import multiple_file_types
from misc_functions import swap_values
from misc_functions import filename
from misc_functions import lc_overlay

PATHREFGRID = '../data/reference_grids/ref_grid_30by100.tif'
PATHRASTERS = '../data/mapbiomas/'
PATHOUTPUT = '../data/training_tables/mapbiomas_lcc_v1.csv'

nanvalue = 0
newlcclasses = [1, 2, 3, 4, 5, 6]

def main():

    # TODO only processes the first two years of mapbiomas, add a loop here for all time steps.
    ref_grid = xarray.open_dataarray(PATHREFGRID)

    files = multiple_file_types(PATHRASTERS, ["*.tif"], recursive=True)
    files_ = list(files)
    file1 = files_[0]

    raster = xarray.open_dataarray(file1)
    lat = raster['y'].values
    lon = raster['x'].values
    data = raster.values
    nan_mask = data == nanvalue
    data = data.flatten()

    # Remap raster values.
    data1 = swap_values(data,
                       # From:
                       # Forest
                       # Forest Formation 3
                       # Savanna Formation 4
                       # Mangrove 5
                       # Wooded Sandbank Vegetation 49
                       [[3, 4, 5, 49],

                        # Non forest
                        # Wetland 11
                        # Grassland 12
                        # Salt Flat 32
                        # Rocky Outcrop 29
                        # Herbaceous Sandbank Vegetation 50
                        # Other non Forest Formations 13
                        [11, 12, 32, 29, 50, 13],

                        # Farming
                        # Pasture 15
                        # Agriculture 18
                        # Temporary Crop 19
                        # Soybean 39
                        # Sugar cane 20
                        # Rice 40
                        # Cotton (beta) 62
                        # Other Temporary Crops 41
                        # Perennial Crop 36
                        # Coffee 46
                        # Citrus 47
                        # Other Perennial Crops 48
                        # Forest Plantation 9
                        # Mosaic of Uses 21
                        [15, 18, 19, 39, 20, 40, 62, 41, 36, 46, 47, 48, 9, 21],

                        # Non vegetated
                        # Beach, Dune and Sand Spot 23
                        # Urban Area 24
                        # Mining 30
                        # Other non Vegetated Areas 25
                        [23, 24, 30, 25],

                        # Water
                        # River, Lake and Ocean 33
                        # Aquaculture 31
                        [33, 31],

                        # None
                        # Non Observed 27
                        [27]],

                       # To:
                       # Forest 1
                       # Non forest 2
                       # Farming 3
                       # Non vegetated 4
                       # Water 5
                       # None 6
                       newlcclasses)

    # Return to original 2D-size.
    data1 = np.reshape(data, (1, len(lat), len(lon))).astype(np.float32)

    # Calculate class proportions overlay.
    data_df1 = lc_overlay(data1, raster, ref_grid, newlcclasses, nanmask=nan_mask)

    file2 = files_[1]

    raster = xarray.open_dataarray(file2)
    lat = raster['y'].values
    lon = raster['x'].values
    data = raster.values
    nan_mask = data == nanvalue
    data = data.flatten()

    # Remap raster values.
    data = swap_values(data,
                       # From:
                       # Forest
                       # Forest Formation 3
                       # Savanna Formation 4
                       # Mangrove 5
                       # Wooded Sandbank Vegetation 49
                       [[3, 4, 5, 49],

                        # Non forest
                        # Wetland 11
                        # Grassland 12
                        # Salt Flat 32
                        # Rocky Outcrop 29
                        # Herbaceous Sandbank Vegetation 50
                        # Other non Forest Formations 13
                        [11, 12, 32, 29, 50, 13],

                        # Farming
                        # Pasture 15
                        # Agriculture 18
                        # Temporary Crop 19
                        # Soybean 39
                        # Sugar cane 20
                        # Rice 40
                        # Cotton (beta) 62
                        # Other Temporary Crops 41
                        # Perennial Crop 36
                        # Coffee 46
                        # Citrus 47
                        # Other Perennial Crops 48
                        # Forest Plantation 9
                        # Mosaic of Uses 21
                        [15, 18, 19, 39, 20, 40, 62, 41, 36, 46, 47, 48, 9, 21],

                        # Non vegetated
                        # Beach, Dune and Sand Spot 23
                        # Urban Area 24
                        # Mining 30
                        # Other non Vegetated Areas 25
                        [23, 24, 30, 25],

                        # Water
                        # River, Lake and Ocean 33
                        # Aquaculture 31
                        [33, 31],

                        # None
                        # Non Observed 27
                        [27]],

                       # To:
                       # Forest 1
                       # Non forest 2
                       # Farming 3
                       # Non vegetated 4
                       # Water 5
                       # None 6
                       newlcclasses)

    # Return to original 2D-size.
    data2 = np.reshape(data, (1, len(lat), len(lon))).astype(np.float32)

    # Create data set which is 1 when in t_{n} the class was forest and in t_{n+1} the class is farming or nonvegetated.
    data2 = np.logical_and(data1 == 1, np.logical_or(data2 == 3, data2 == 4))*1.0

    # Calculate class proportions overlay.
    data_df2 = lc_overlay(data2, raster, ref_grid, lcids=[1], lclabels=['forestloss'], nanmask=nan_mask)

    # Add forest loss variable to data set.
    data_df1['forestloss'] = data_df2['forestloss']

    # Drop NaNs and save to disk.
    data_df1.dropna(inplace=True)

    data_df1.to_csv(PATHOUTPUT, encoding='utf-8', index=False)

if __name__ == "__main__":
    main()
