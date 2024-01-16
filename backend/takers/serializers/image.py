from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from typing import BinaryIO
from PIL import Image
import shutil
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
