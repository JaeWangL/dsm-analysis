import earthpy.plot as ep
import matplotlib.pyplot as plt
import numpy as np
import rioxarray

def calculate_diff_std(reference_path: str, target_path: str) -> None:
    reference_array = rioxarray.open_rasterio(reference_path)
    target_array = rioxarray.open_rasterio(target_path)
    
    # NOTE: Make same shape for subtracting with each array
    target_array = target_array.rio.reproject_match(reference_array)
    
    # for make difference range in 0 ~ 1
    # diff = (target_dsm.astype(float) - reference_dsm.astype(float))/(target_dsm + reference_dsm)
    diff = (target_array.astype(float) - reference_array.astype(float)).to_numpy()
    diff_without_nan = diff[~np.isnan(diff)]
    
    ep.plot_bands(diff,
        cmap='viridis',
        title="Difference Height Model\nby reference data")
    plt.show()

    ep.hist(diff_without_nan,
        bins=100,
        title="Distribution of Difference DSM Height Model Pixels")
    plt.show()

    print('Diff minimum value: ', diff_without_nan.min())
    print('Diff max value: ', diff_without_nan.max())
    print('Diff standard deviation: ', np.std(np.abs(diff_without_nan)))
    