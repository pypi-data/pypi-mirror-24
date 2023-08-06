import os
import shutil
import unittest
from glob import glob

from omrdatasettools.downloaders import DatasetDownloader
from omrdatasettools.downloaders.HomusDatasetDownloader import HomusDatasetDownloader


class DatasetDownloaderTest(unittest.TestCase):
    def test_download_and_extract_homus_v1_dataset_expect_folder_to_be_created(self):
        destination_directory = "HOMUS"
        downloader = HomusDatasetDownloader(".", version=1)
        zip_file = downloader.get_dataset_filename()
        number_of_samples_in_the_dataset = 15200
        target_file_extension = "*.txt"

        self.download_dataset_and_verify_correct_extraction(destination_directory, number_of_samples_in_the_dataset,
                                                            target_file_extension, zip_file,
                                                            downloader)

    def test_download_and_extract_homus_v2_dataset_expect_folder_to_be_created(self):
        destination_directory = "HOMUS"
        downloader = HomusDatasetDownloader(".", version=1)
        zip_file = downloader.get_dataset_filename()
        number_of_samples_in_the_dataset = 15200
        target_file_extension = "*.txt"

        self.download_dataset_and_verify_correct_extraction(destination_directory, number_of_samples_in_the_dataset,
                                                            target_file_extension, zip_file,
                                                            downloader)

    def download_dataset_and_verify_correct_extraction(self, destination_directory: str,
                                                       number_of_samples_in_the_dataset: int,
                                                       target_file_extension: str, zip_file: str,
                                                       dataset_downloader: DatasetDownloader):
        # Arrange and Cleanup
        if os.path.exists(zip_file):
            os.remove(zip_file)
        shutil.rmtree(destination_directory, ignore_errors=True)

        # Act
        dataset_downloader.download_and_extract_dataset()

        # Assert
        all_files = [y for x in os.walk(destination_directory) for y in glob(os.path.join(x[0], target_file_extension))]
        actual_number_of_files = len(all_files)
        self.assertEqual(number_of_samples_in_the_dataset, actual_number_of_files)
        self.assertTrue(os.path.exists(zip_file))

        # Cleanup
        os.remove(zip_file)
        shutil.rmtree(destination_directory, ignore_errors=True)


if __name__ == '__main__':
    unittest.main()
