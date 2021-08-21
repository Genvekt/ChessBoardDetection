import requests
import zipfile
from pathlib import Path
from typing import Union
from tqdm import tqdm 
import argparse


def download_file(url:str, output_file:str):
    """
    Download file with progressbar
    Args:
        url (str): url used to download file
        output_file(str): path to the output file
    """
    # Make sure dirs for output file exist
    Path(output_file).parent.mkdir(exist_ok=True, parents=True)

    # Retrieve all information for verbose
    r = requests.get(url, stream=True)
    file_size = int(r.headers['Content-Length'])
    chunk_size=1024
    num_bars = int(file_size / chunk_size)

    # Download file by chanks
    with open(output_file, 'wb') as fp:
        for chunk in tqdm(
                r.iter_content(chunk_size=chunk_size),
                total= num_bars,
                unit = 'KB',
                desc = output_file,
                leave = True):

            fp.write(chunk)


def unzip_file(zip_path:str, output_dir:Union[str, Path]=None):
    """
    Unzip file into directory
    Args:
        zip_path (str):
    """
    if output_dir is None:
        output_dir = Path(zipfile).parent

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(output_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download and unzip file')
    parser.add_argument('url', type=str,
                        help='url to file to download')
    parser.add_argument('output_file', type=str,
                        help='File path for downloaded zip. Files from \
                            zip will be extracted in the same directory.')

    args = parser.parse_args()

    url = args.url
    out_path = args.output_file

    print(f"Downloading file into {out_path}")
    download_file(url=url, output_file=out_path)

    unzipping_dir = Path(out_path).parent
    print(f"Unzipping file into {unzipping_dir}...")
    unzip_file(out_path, unzipping_dir)

    print("Done.")
