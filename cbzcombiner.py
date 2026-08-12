import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import zipfile
import shutil

def select_files() -> tuple[str]:
    print("Please select the .cbz files that you would like to combine!")

    # Create Window
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    # PopUp Window for selecting file --> Tuple(Str)
    file_path_tpl = filedialog.askopenfilenames(
        title="Select CBZ File to Unzip",
        filetypes=[("CBZ files", "*.cbz"), ("All files", "*.*")],
    )

    # Destroy PopUp Window
    root.destroy()

    return file_path_tpl

def unzip_files(file_path_tpl : tuple[str]) -> list[str]:
    # List to save the temporal directory created for unzipping
    tmp_dir_list = list()

    for file_to_unzip in file_path_tpl:
        # Path to file to unzip
        cbz_file = Path(file_to_unzip)

        output_dir = cbz_file.parent / f'{cbz_file.stem}_tmp'
        output_dir.mkdir(exist_ok=True, parents=True)

        with zipfile.ZipFile(cbz_file, 'r') as zip_ref:
            zip_ref.extractall(output_dir)

        tmp_dir_list.append(output_dir)


    return tmp_dir_list

def combine_cbz(file_name : str, parent_path : Path, tmp_dir_list : list[Path]) -> None:
    print("Combining")
    combined_cbz_path = parent_path / f'{file_name}.cbz'

    count = 0
    with zipfile.ZipFile(combined_cbz_path, "w", zipfile.ZIP_DEFLATED) as new_cbz:
        for folder in reversed(tmp_dir_list):
            files_in_folder = sorted(folder.rglob("*"))

            for file_path in files_in_folder:
                    if file_path.is_file():
                        count += 1
                        # E.J: page_0001.jpg, page_0002.jpg...
                        arcname = f"page_{count:04d}{file_path.suffix}"
                        new_cbz.write(file_path, arcname=arcname)

            shutil.rmtree(folder)

    print("All files combined succesfully!")


def combine_pipeline(file_path_tpl : tuple[str]):
    print("Selected files: ")
    for file in file_path_tpl:
        file_path = Path(file)
        print(file_path.stem)

    tmp_dir_list = unzip_files(file_path_tpl)

    new_file_name = input('\nType the name for the new file (without .cbz): ')
    first_file_parent = Path(file_path_tpl[0]).parent 
    
    combine_cbz(new_file_name, first_file_parent, tmp_dir_list)



if __name__ == '__main__':

    file_path_tpl = select_files()

    if not file_path_tpl:
        print("No files selected.")
    else:
        combine_pipeline(file_path_tpl)



