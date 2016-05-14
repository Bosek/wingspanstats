import sys
import urllib2


def saveContent(url, dest,
                startCallback=None, progressCallback=None, endCallback=None):
    try:
        response = urllib2.urlopen(url)
    except:
        return False
    destination = open(dest, "wb")
    metainfo = response.info()

    filesize = int(metainfo.getheaders("Content-Length")[0])
    blocksize = 4096
    progress = 0

    if startCallback:
        startCallback(filesize)

    while True:
        buff = response.read(blocksize)
        if not buff:
            break

        progress += len(buff)
        if progressCallback:
            progressCallback(progress, filesize)
        destination.write(buff)

    destination.close()

    if endCallback:
        endCallback()

    return True
