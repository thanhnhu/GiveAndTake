from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import mimetypes
from django.conf import settings
from typing import BinaryIO
from PIL import Image
import shutil
import os
import tempfile


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
        #file = default_storage.open(file_name)
        #file_url = default_storage.url(file_name)
        return {id: id, size: size}

    def remove(self, id):
        baseDir = settings.BASE_DIR + os.sep
        images = settings.MEDIA_URL.replace('/', '') + os.sep
        folder = os.path.join(os.sep, baseDir, images, str(id))
        
        if os.path.exists(folder):
            #os.removedirs(folder)
            shutil.rmtree(folder, ignore_errors=True)

        return True


class ImageToGoogleDriveSerializer(ImageSerializer):
    def __init__(self):
        self.credentials = Credentials.from_service_account_file(
            settings.SERVICE_ACCOUNT_FILE, scopes=settings.SCOPES
        )
        print(f"settings.SERVICE_ACCOUNT_FILE {settings.SERVICE_ACCOUNT_FILE}")
        print(f"settings.SCOPES {settings.SCOPES}")
        self.drive_service = build('drive', 'v3', credentials=self.credentials)

    def upload_to_drive(self, file_path, file_name, folder_id=None):
        mime_type, _ = mimetypes.guess_type(file_path)
        file_metadata = {'name': file_name}
        if folder_id:
            file_metadata['parents'] = [folder_id]
        
        media = MediaFileUpload(file_path, mimetype=mime_type)
        uploaded_file = self.drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        # Set file to be publicly accessible
        self.drive_service.permissions().create(
            fileId=uploaded_file.get('id'),
            body={'role': 'reader', 'type': 'anyone'}
        ).execute()

        file_url = f"https://drive.google.com/thumbnail?id={uploaded_file.get('id')}"
        return file_url

    def save(self, host, id, files, folder_id=None):
        res = []
        with tempfile.TemporaryDirectory() as temp_dir:
            for file in files:
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

                res.append({
                    "key": id, "name": file.name,
                    "web_url": f"{web_url}&sz=w1300",
                    "mob_url": f"{mob_url}&sz=w360"
                })
        return res

    def load(self, id, size):
        #file = default_storage.open(file_name)
        #file_url = default_storage.url(file_name)
        return {id: id, size: size}

    def remove(self, id):
        baseDir = settings.BASE_DIR + os.sep
        images = settings.MEDIA_URL.replace('/', '') + os.sep
        folder = os.path.join(os.sep, baseDir, images, str(id))
        
        if os.path.exists(folder):
            #os.removedirs(folder)
            shutil.rmtree(folder, ignore_errors=True)

        return True


class ImageToAzureSerializer(ImageSerializer):
    def save(self, id, files: BinaryIO):
        return {"file_key": id, "url": "abc"}

    def load(self, id, size):
        return {id: id, size: size}
