import calculate_difference as diff
import crop_test_region as cropping

def main():
    reference_data = r"./testData/dsm_reference.tif"
    input_data = r"./testData/dsm_target.tif"
    minx, miny = 153963, 366588
    maxx, maxy = 154617, 365774
    
    cropped_target_path = cropping.crop_raster_by_coordinates(input_data, minx, miny, maxx, maxy)
    cropped_reference_path = cropping.crop_raster_by_coordinates(reference_data, minx, miny, maxx, maxy)
    diff.calculate_diff_std(cropped_reference_path, cropped_target_path)

if __name__ == '__main__':
    main()
