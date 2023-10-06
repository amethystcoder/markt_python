from PIL import Image
import uuid
import os

class ImageSaver:
    """
    This file contains functions for reducing image file sizes, storing the images in
    the upload folder or storage bucket, and also unlinking(deleting) image files from
    the upload folder or storage bucket. It also contains functions to change the image 
    from one format to another, rasterize and change the image structure and a whole lot of
    other stuff
    """
    @classmethod
    def compressimage(self,image_location):
        """compress an image
        
        Keyword arguments:
        image_location - the directory where the image is located
        Return: a boolean
        """
        filesize = os.path.getsize(image_location)
        if filesize < 5.0:
            try:
                with Image.open(image_location) as image:
                    width,height = image.size
                    new_width = width * 0.3
                    new_height = height * 0.3
                    image.resize((new_width,new_height))
                    image_name = self.generateimagename()
                    image.save("app/routes/"+image_name+".jpg","JPEG",optimize=True,quality=50)
            except OSError:
                return False
            return image_name
        return False

    @classmethod
    def generateimagename(self):
        return str(uuid.uuid5())

    @classmethod
    def deleteimage(self,image_name):
        try:
            os.unlink("app/routes/"+image_name+".jpg")
            return True
        except OSError:
            return False
