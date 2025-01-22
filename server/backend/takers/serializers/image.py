from concurrent.futures import ThreadPoolExecutor
from google.oauth2.service_account import Credentials
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from typing import BinaryIO
from PIL import Image
import mimetypes
import tempfile
import shutil
import socket
import os


class ImageSerializer:
    def save(self, id, files: BinaryIO):
        return {"file_key": id, "url": "abc"}

    def load(self, id, size):
        return {id: id, size: size}


class ImageToLocalSerializer(ImageSerializer):
    def save(self, host, id, files):
        baseDir = settings.BASE_DIR + os.sep
        images = settings.MEDIA_URL.replace('/', '') + os.sep
        folder = os.path.join(os.sep, baseDir, images, id)

        if not os.path.exists(folder):
            os.makedirs(folder)

        res = []
        for file in files:
            image = Image.open(file)
            web_name = "web_" + file.name
            mob_name = "mob_" + file.name
            image.thumbnail((1300, 720))
            image.save(folder + os.sep + web_name)
            image.thumbnail((360, 720))
            image.save(folder + os.sep + mob_name)

            web_url = host + settings.MEDIA_URL + id + "/" + web_name
            mob_url = host + settings.MEDIA_URL + id + "/" + mob_name
            res.append({"key": id, "name": file.name, "web_url": web_url, "mob_url": mob_url})

        """
        res = []
        fs = FileSystemStorage(location=folder, base_url=id)
        for file in files:
            filename = fs.save(file.name, file)
            file_url = fs.url(filename)
            url = host + settings.MEDIA_URL + file_url
            res.append({"key": id, "name": filename, "url": url})
        """

        return res

    def load(self, id, size):
        # file = default_storage.open(file_name)
        # file_url = default_storage.url(file_name)
        return {id: id, size: size}

    def remove(self, id):
        baseDir = settings.BASE_DIR + os.sep
        images = settings.MEDIA_URL.replace('/', '') + os.sep
        folder = os.path.join(os.sep, baseDir, images, str(id))

        if os.path.exists(folder):
            # os.removedirs(folder)
            shutil.rmtree(folder, ignore_errors=True)

        return True


class ImageToGoogleDriveSerializer(ImageSerializer):
    def __init__(self):
        # Set timeout to 10 minutes to upload to Google Drive
        socket.setdefaulttimeout(60*10)
        self.credentials = Credentials.from_service_account_file(
            settings.SERVICE_ACCOUNT_FILE, scopes=settings.SCOPES
        )
        self.drive_service = build('drive', 'v3', credentials=self.credentials)

    def __del__(self):
        # print("I'm being automatically destroyed. Goodbye!")
        # However, this is a hacky solution because this a low level setting
        # could also impact other http clients. so, set it back
        socket.setdefaulttimeout(None)

    def upload_to_drive(self, file_path, file_name, folder_id=None):
        # print(f"Uploading file: {file_path}\{file_name}")
        mime_type, _ = mimetypes.guess_type(file_path)
        file_metadata = {'name': file_name}
        if folder_id:
            file_metadata['parents'] = [folder_id]

        # Chulk upload
        # media = MediaFileUpload(file_path, mimetype=mime_type, chunksize=1024*1024, resumable=True)
        media = MediaFileUpload(file_path, mimetype=mime_type)
        uploaded_file = self.drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        # Set timeout to 10 minutes
        #uploaded_file.http.timeout = 600

        # Chulk upload
        # response = None
        # while response is None:
        #     status, response = uploaded_file.next_chunk()
        #     # if status:
        #     # print(f"Uploaded {int(status.progress() * 100)}%.")
        # print("Upload complete.")

        # Set file to be publicly accessible
        self.drive_service.permissions().create(
            fileId=uploaded_file.get('id'),
            body={'role': 'reader', 'type': 'anyone'}
        ).execute()

        file_url = f"https://drive.google.com/thumbnail?id={uploaded_file.get('id')}"
        print(f"Uploaded file: {file_path}\{file_name}")
        return file_url

    def process_file(self, file, id, temp_dir, folder_id):
        image = Image.open(file)

        # Web image
        web_name = f"web_{file.name}"
        web_path = os.path.join(temp_dir, web_name)
        image.thumbnail((1300, 720))
        image.save(web_path)

        # Mobile image
        mob_name = f"mob_{file.name}"
        mob_path = os.path.join(temp_dir, mob_name)
        image.thumbnail((360, 720))
        image.save(mob_path)

        # Upload to Google Drive
        web_url = self.upload_to_drive(web_path, web_name, folder_id)
        mob_url = self.upload_to_drive(mob_path, mob_name, folder_id)

        return {
            "key": id,
            "name": file.name,
            "web_url": f"{web_url}&sz=w1300",
            "mob_url": f"{mob_url}&sz=w360"
        }

    def save(self, host, id, files, folder_id=None):
        res = []
        try:
            temp_dir = os.path.join(os.path.dirname(tempfile.mktemp()), 'takeandgive')
            # Ensure the directory exists
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            # Upload by multithreading
            # with ThreadPoolExecutor() as executor:
            #     futures = [
            #         executor.submit(self.process_file, file, id, temp_dir, folder_id)
            #         for file in files
            #     ]
            #     for future in futures:
            #         res.append(future.result())
            for file in files:
                res.append(self.process_file(file, id, temp_dir, folder_id))
            # Removes the directory and its contents
            shutil.rmtree(temp_dir)
        except Exception as e:
            print(f"Error occurred: {e}")
            #print(f"Temp directory path: {temp_dir}")

        return res

    def load(self, id, size):
        # file = default_storage.open(file_name)
        # file_url = default_storage.url(file_name)
        return {id: id, size: size}

    def remove(self, id):
        baseDir = settings.BASE_DIR + os.sep
        images = settings.MEDIA_URL.replace('/', '') + os.sep
        folder = os.path.join(os.sep, baseDir, images, str(id))

        if os.path.exists(folder):
            # os.removedirs(folder)
            shutil.rmtree(folder, ignore_errors=True)

        return True


class ImageToAzureSerializer(ImageSerializer):
    def save(self, id, files: BinaryIO):
        return {"file_key": id, "url": "abc"}

    def load(self, id, size):
        return {id: id, size: size}
