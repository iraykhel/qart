import requests
import shutil
import skimage
from skimage import io, metrics
import numpy as np
import time
import traceback

class Image:
    def __init__(self,filename=None):
        self.filename = None
        if filename is not None:
            self.filename = filename
            self.filename_name,self.filename_ext = filename.split(".")
            self.image = io.imread('data/'+self.filename)
            print(filename,self.image.shape)

    @classmethod
    def download(cls,url,filename=None):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'}
        if filename is None:
            filename = url[url.rfind('/')+1:]

        success = False
        while not success:
            try:
                r = requests.get(url, stream=True, headers=headers)

                if r.status_code == 200:
                    r.raw.decode_content = True
                    with open('data/'+filename, 'wb') as f:
                        shutil.copyfileobj(r.raw, f)
                    success = True
            except:
                print("Failed to download image",url,traceback.format_exc(),"will retry")
                time.sleep(10)

        return Image(filename)


    def crop(self,yfrom,yto,xfrom,xto,outfile):
        crop = self.image[xfrom:xto,yfrom:yto]
        io.imsave('data/'+outfile,crop)
        # h = np.sum(crop)
        # h1 = np.sum(crop < 100)
        # print(h)
        # crop.flags.writeable = False
        # h = hash(crop.data.tobytes())
        return crop




# image = Image('0.png')
# image.crop(200,500,200,500,'0_crop.png')
# image.download('https://gateway.pinata.cloud/ipfs/QmVqMYxaEkifE7FoMkdNtryXhPNgHwA89msFQUBQbEYwKE/images/0.png')