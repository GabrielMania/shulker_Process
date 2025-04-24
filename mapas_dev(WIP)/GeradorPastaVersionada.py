import os

def create_folders(start_version, end_version, base_path="."):
    """
    Creates a series of folders named according to a versioning scheme,
    incrementing from start_version to end_version.

    Args:
        start_version (str): The initial version number (e.g., "0.0.0").
        end_version (str): The final version number (e.g., "9.9.9").
        base_path (str, optional): The base directory where the folders will be created. Defaults to the current directory.
    """

    start_nums = list(map(int, start_version.split(".")))
    end_nums = list(map(int, end_version.split(".")))

    current_nums = start_nums[:]  # Start with a copy of the start version

    while current_nums <= end_nums:
        folder_name = "v" + ".".join(map(str, current_nums))
        folder_path = os.path.join(base_path, folder_name)

        try:
            os.makedirs(folder_path, exist_ok=True)  # Create the folder, no error if it exists
            print(f"Created folder: {folder_path}")
        except Exception as e:
            print(f"Error creating folder {folder_path}: {e}")
            return  # Exit if there's an error

        # Increment the version numbers
        current_nums[2] += 1
        if current_nums[2] > 9:
            current_nums[2] = 0
            current_nums[1] += 1
            if current_nums[1] > 9:
                current_nums[1] = 0
                current_nums[0] += 1
        if current_nums[0] > 9:
            print("Alcançado o limite máximo de versão.")
            break

# Example usage:
if __name__ == "__main__":
    create_folders("0.0.0", "0.3.3")