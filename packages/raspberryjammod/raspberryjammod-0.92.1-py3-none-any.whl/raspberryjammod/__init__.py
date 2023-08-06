import os.path
import zipfile
import platform

try:
    # Python 3
    from urllib.request import urlopen
    from io import BytesIO
except ImportError:
    # Python 2
    from urllib2 import urlopen
    import StringIO as BytesIO

def getVersion():
    dir = os.path.dirname(__file__)
    with open(os.path.join(dir, 'VERSION'), encoding="ASCII") as f:
        return f.read().strip()   

def install():
    url = ("https://github.com/arpruss/raspberryjammod/releases/download/{}/mods.zip"
           .format(getVersion()))

    print("Downloading", url)
    with urlopen(url) as stream:
        zipdata = BytesIO()
        zipdata.write(stream.read())

    mods_dir = os.path.join(getMinecraftDir(), "mods")
    print("Extracting into", mods_dir)
    with zipfile.ZipFile(zipdata) as zip:
        zip.extractall(mods_dir)
    
    print("Done!")

def getMinecraftDir():
    # https://minecraft.gamepedia.com/.minecraft
    if platform.system() == "Windows":
        return os.path.join(os.environ["APPDATA"], ".minecraft")
    elif platform.system() == "Darwin":
        return os.path.expanduser("~/Library/Application Support/minecraft")
    else:
        return os.path.expanduser("~/.minecraft")
        
