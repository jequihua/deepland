import numpy as np
import causalnex
import rasterio

from misc_functions import multiple_file_types
from misc_functions import swap_values
from misc_functions import filename

PATHRASTERS='./data/mapbiomas/'
PATHRASTERSFLAT='./data/mapbiomas_remapped/'

files=multiple_file_types(PATHRASTERS,["*.tif"],recursive=True)
files_=list(files)
file=files_[0]
print(file)

with rasterio.open(file) as dataset:
    cols=dataset.width
    rows=dataset.height
    profile = dataset.profile.copy()
    data=dataset.read().flatten()
 
    # Remap raster values.
    data=swap_values(data,
    # From:

    # Forest
    # Forest Formation 3
    # Savanna Formation 4
    # Mangrove 5
    # Wooded Sandbank Vegetation 49
    [[3,4,5,49],

    # Non forest
    # Wetland 11
    # Grassland 12
    # Salt Flat 32
    # Rocky Outcrop 29
    # Herbaceous Sandbank Vegetation 50
    # Other non Forest Formations 13
    [11,12,32,29,50,13],

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
    [15,18,19,39,20,40,62,41,36,46,47,48,9,21],

    # Non vegetated
    # Beach, Dune and Sand Spot 23
    # Urban Area 24
    # Mining 30
    # Other non Vegetated Areas 25
    [23,24,30,25],

    # Water
    # River, Lake and Ocean 33
    # Aquaculture 31
    [33,31],

    # None
    # Non Observed 27
    [27]],

    # To
    # Forest 1
    # Non forest 2
    # Farming 3
    # Non vegetated 4
    # Water 5
    # None 6
    [1,2,3,4,5,6])

    # Return to original 2D-size.
    data = np.reshape(data,(rows,cols))

    # Save remapped raster.
    with rasterio.open(PATHRASTERSFLAT + filename(file) + '.tif', 'w', **profile) as dataset:
            dataset.write(data, indexes = 1)
