from PIL import Image
import uuid
from rembg import remove
import os

Image.MAX_IMAGE_PIXELS = 933120000

def generate_image_name():
    return str(uuid.uuid4())


class ImageSaver:
    # images can only be of type image with .jpg, .png and .webp extensions
    allowed_extensions = ['jpg', 'png', 'webp']

    allowed_mimes = ['image/jpeg', 'image/png', 'image/webp']

    # 5mb max file size
    max_file_size = 5 * 1024 * 1024

    """
    This class contains functions for reducing image file sizes, storing the images in
    the upload folder or storage bucket, and also unlinking(deleting) image files from
    the upload folder or storage bucket. It also contains functions to change the image 
    from one format to another, rasterize and change the image structure and a whole lot of
    other stuff
    """

    @classmethod
    def compress_image(cls, image_location):
        """compress an image
        
        Keyword arguments:
        image_location - the directory where the image is located
        Return: a boolean
        """
        try:
            with Image.open(image_location) as image:
                width, height = image.size
                new_width = width * 0.3
                new_height = height * 0.3
                image.resize((int(new_width), int(new_height)))
                image_name = generate_image_name()
                image.save("../uploads/" + image_name + ".jpg", "JPEG", optimize=True, quality=50)
                return image_name
        except OSError as e:
            print(str(e))
            return False

    """compress an image and removes its background

        Keyword arguments:
        image_location - the directory where the image is located
        Return: a boolean
    """
    @classmethod
    def compress_image_and_remove_background(cls, image_location):
        
        try:
            with Image.open(image_location) as image:
                width, height = image.size
                new_width = width * 0.3
                new_height = height * 0.3
                image.resize((int(new_width), int(new_height)))
                image_name = generate_image_name()
                if image.mode in ("RGBA", "P"): image = image.convert('RGB')
                image_with_background_removed = remove(image)
                image_with_background_removed.save("../uploads/" + image_name + ".png", "PNG", optimize=True,
                                                   quality=50)
                return image_name
        except OSError as e:
            print(str(e))
            return False

    @classmethod
    def is_valid_file(cls, name):
        return '.' in name and name.rsplit('.', 1)[1].lower() in cls.allowed_extensions

    @classmethod
    def is_valid_mime(cls, mime_to_check):
        return mime_to_check in cls.allowed_mimes

    @classmethod
    def is_valid_file_size(cls, file_size):
        return file_size < cls.max_file_size

    @staticmethod
    def delete_image(self, image_name):
        try:
            os.unlink("app/routes/" + image_name + ".jpg")
            return True
        except OSError:
            return False

image_saver = ImageSaver()
print(image_saver.compress_image_and_remove_background("C:/Users/Administrator/markt_python/app/utils/samsung-memory-jbmjneY3a6g-unsplash.jpg"))