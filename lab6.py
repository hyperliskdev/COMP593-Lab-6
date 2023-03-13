import requests
import hashlib
import os
import subprocess

def main():

    # Get the expected SHA-256 hash value of the VLC installer
    expected_sha256 = get_expected_sha256()

    # Download (but don't save) the VLC installer from the VLC website
    installer_data = download_installer()

    # Verify the integrity of the downloaded VLC installer by comparing the
    # expected and computed SHA-256 hash values
    if installer_ok(installer_data, expected_sha256):

        # Save the downloaded VLC installer to disk
        installer_path = save_installer(installer_data)

        # Silently run the VLC installer
        run_installer(installer_path)

        # Delete the VLC installer from disk
        delete_installer(installer_path)

def get_expected_sha256():
    # Send GET message to download the file
    file_url = 'http://download.videolan.org/pub/videolan/vlc/3.0.17.4/win64/vlc-3.0.17.4-win64.sha256'
    resp_msg = requests.get(file_url)
    # Check whether the download was successful
    if resp_msg.status_code == requests.codes.ok:
        # Extract text file content from response message
        file_content = resp_msg.text
        
    return file_content


def download_installer():

    # Send GET message to download the file
    file_url = 'http://download.videolan.org/pub/videolan/vlc/3.0.17.4/win64/vlc-3.0.17.4-win64.exe'
    resp_msg = requests.get(file_url)
    # Check whether the download was successful
    if resp_msg.status_code == requests.codes.ok:

        # Extract binary file content from response message
        file_content = resp_msg.content

    return file_content

def installer_ok(installer_data, expected_sha256):

    installer_hash = hashlib.sha256(installer_data).hexdigest()

    if installer_hash == expected_sha256:
        return True

    return False

def save_installer(installer_data):
    # Save the binary file to disk
    with open(os.getenv('TEMP'), 'wb') as file:
        file.write(file_content)

    return os.getenv('TEMP') + "/vlc.exe"

def run_installer(installer_path):
    subprocess.run([installer_path, '/L=1033', '/S'])
    return
    
def delete_installer(installer_path):
    os.remove(installer_path)
    return

if __name__ == '__main__':
    main()