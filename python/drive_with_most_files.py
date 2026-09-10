import unittest

def getDriveWithMostFiles(absoluteFilePathList) -> list[str | int]:
    """Get Windows drive with the most files.

    Given a list of absolute file paths, this function identifies the Windows
    drive with the most number of files. by returning a list of 3 items:
    [ Windows drive name, number of folders, number of files]

    Args:
        absoluteFilePathList: a list of absolute file paths, e.g. 
                        paths = [
                        "C:\\folder1\\folder2\\folder3\\folder4\\file1.txt",
                        "D:\\folder2\\folder21\\folder22\\file2.txt",
                        "D:\\folder2\\folder21\\folder22\\file3.txt"
                    ]

    Returns:
        A list of 3 items: 
            [ Windows drive name, number of folders, number of files]
            e.g. ["D:", 1, 2] for the example above, where 
                    "D:" is the drive name with the most files,
                    1 is the number of folders in that drive, and 
                    2 is the number of files in that drive.
            if two drives have the same number of most files, the drive with the most folders is returned.
            if two drives have the same number of most files and the same number of folders,
            the first drive in the sorted ascending order is returned.
    Raises:
        ValueError: If `absoluteFilePathList` is invalid.
    """

    folders_to_files = {} # Dictionary of set, key: folder, value: set of absoluteFilePaths
    folders_to_subfolders = {} # Dictionary of set, key: folder, value: set of subfolders
    drive_filenames = {}   # Dictionary of set, key: drivename, value: set of files
    drive_folders = {} # Dictionary of set, key: drivename, value: set of folders
    for absoluteFilePath in absoluteFilePathList:
        # Split the path into components using backslash as the separator
        drive_name = absoluteFilePath.split("\\")[0]  # Get the drive name (e.g., "C:")
        drive_filenames.setdefault(drive_name, set()).add(absoluteFilePath)

        components = absoluteFilePath.split("\\")

        if len(components) < 2:
            continue  # Skip if the path doesn't have enough components

        for component in components[1:-1]:  # Exclude drive name and file name
            folder_path = "\\".join(components[1:components.index(component)+1])  # Get the full folder path up to the current component
            drive_folders.setdefault(drive_name, set()).add(folder_path)  # Add the folder to the set for the corresponding drive
    max_files = 0
    max_folders = 0
    drive_with_most_files = None
    num_folders_in_drive_with_most_files = 0

    for drivename, files in drive_filenames.items():
        num_files = len(files)
        if num_files > max_files:
            max_files = num_files
            drive_with_most_files = drivename
            num_folders_in_drive_with_most_files = len(drive_folders[drivename])
        elif num_files == max_files:
            # If the number of files is the same, check the number of folders
            num_folders = len(drive_folders[drivename])
            if num_folders > num_folders_in_drive_with_most_files:
                drive_with_most_files = drivename
                num_folders_in_drive_with_most_files = num_folders
            elif num_folders == num_folders_in_drive_with_most_files:
                # If the number of folders is also the same, choose the drive with the lexicographically smaller name
                if drivename < drive_with_most_files:
                    drive_with_most_files = drivename

    if drive_with_most_files is None:
        return []

    return [ drive_with_most_files, num_folders_in_drive_with_most_files, max_files ]

class TestgetDriveWithMostFiles(unittest.TestCase):
    def test_1(self):
        paths = [
            "C:\\folder1\\folder2\\folder3\\folder4\\file1.txt",
        ]
        self.assertEqual(getDriveWithMostFiles(paths), ["C:", 4, 1])

    def test_2(self):
        paths = [
            "C:\\folder1\\folder2\\folder3\\folder4\\file1.txt",
            "C:\\folder1\\folder2\\folder3\\folder4\\file2.txt",
        ]
        self.assertEqual(getDriveWithMostFiles(paths), ["C:", 4, 2])

    def test_3(self):
        paths = [
            "C:\\folder1\\file1.txt",
            "D:\\folder1\\file1.txt",
            "D:\\folder2\\file2.txt"
        ]
        self.assertEqual(getDriveWithMostFiles(paths), ["D:", 2, 2])

    def test_4(self):
        paths = [
            "C:\\folder1\\file1.txt",
            "C:\\folder1\\file2.txt",
            "D:\\folder1\\file1.txt",
            "D:\\folder2\\file2.txt"
        ]
        self.assertEqual(getDriveWithMostFiles(paths), ["D:", 2, 2])

    def test_4(self):
        paths = [
            "C:\\folder1\\file1.txt",
            "C:\\folder1\\folder2\\folder3\\file1.txt",
            "D:\\folder3\\file1.txt",
            "D:\\folder3\\folder4\\folder5\\file1.txt",
        ]
        self.assertEqual(getDriveWithMostFiles(paths), ["C:", 3, 2])

    def test_5(self):
        paths = [
            "E:\\folder1\\file1.txt",
            "E:\\folder1\\folder2\\folder3\\file1.txt",
            "D:\\folder3\\file1.txt",
            "D:\\folder3\\folder4\\folder5\\file1.txt",
        ]
        self.assertEqual(getDriveWithMostFiles(paths), ["D:", 3, 2])     

if __name__ == "__main__":
    unittest.main(verbosity=2)

