import logging
import os
import re
import urllib
import shutil
import multiprocessing
from wand.image import Image

from flickrsync import general
from flickrsync.log import Log

PICTURE_TYPES = ('.jpg', '.png', '.gif')
DELETED = '1'
UNDEFINED = None
UNDELETED = None
IMAGE_ERROR = 1

logger = logging.getLogger(Log.NAME)

def search_photos(picturepath):
    assert picturepath, "picturepath not supplied"
    logger.debug('picturepath<%s>' % picturepath)

    newsearch = []

    for directory, __dirs, files in os.walk(picturepath):
        for filename in files:
            if filename.lower().endswith(PICTURE_TYPES) :
                newsearch.append({
                    'directory' : directory
                   , 'filename'  : filename
                })

    logger.debug("Number of photos found: %d" % len(newsearch))

    return newsearch

def search_deleted(allfiles):
    deletedfiles = []

    for afile in allfiles:
        pathname = os.path.join(afile['directory'], afile['filename'])

        if os.path.isfile(pathname):
            if afile['deleted']:
                deletedfiles.append({'directory' : afile['directory'], 'filename' : afile['filename'], 'deleted' : UNDELETED})
                logger.debug('un-delete, %s, %s, %s' % (afile['directory'], afile['filename'], afile['deleted']))

        elif not afile['deleted']:
            deletedfiles.append({'directory' : afile['directory'], 'filename' : afile['filename'], 'deleted' : DELETED})
            logger.debug('delete, %s, %s, %s' % (afile['directory'], afile['filename'], afile['deleted']))

    logger.debug("Number of deleted / undeleted photos found: %d" % len(deletedfiles))

    return deletedfiles

def image_worker(data):
    directory, filename = data
    assert directory, "directory not supplied<%s>" % directory
    assert filename, "filename not supplied<%s>" % filename

    datetimeoriginal = UNDEFINED
    flickrid, flickrsecret, flickrtitle, flickrextension = _get_flickr_id_secret_title_extension(filename)
    signature = UNDEFINED
    dateflat = UNDEFINED
    imageerror = IMAGE_ERROR
    pathname = os.path.join(directory, filename)
    shortname = general.get_short_name(filename, flickrtitle)

    try :
        with Image(filename = pathname) as img:
            try :
                datetimeoriginal = img.metadata['exif:DateTimeOriginal']
                dateflat = general.get_flat_date(datetimeoriginal)
            except Exception as e :
                logger.warning('DateTimeOriginal not available: %s' % (pathname))

            signature = img.signature
            imageerror = None

    except Exception as e:
        logger.error('Not a valid picture file: %s' % (pathname))

    photo = {
          'directory'        : directory
        , 'filename'         : filename
        , 'datetimeoriginal' : datetimeoriginal
        , 'flickrid'         : flickrid
        , 'flickrsecret'     : flickrsecret
        , 'flickrtitle'      : flickrtitle
        , 'flickrextension'  : flickrextension
        , 'signature'        : signature
        , 'dateflat'         : dateflat
        , 'shortname'        : shortname
        , 'imageerror'       : imageerror
    }

    logger.debug('%s' % (photo))
    return (photo)

def download_photos(directory, flickrphotos, dryrun=True):
    downloadphotos = []
    for flickrphoto in flickrphotos:
        filename = _get_flickr_filename(flickrphoto['id'], flickrphoto['originalsecret'],
                                       flickrphoto['title'], flickrphoto['originalformat'])
        downloadphotos.append(
            (directory, filename, flickrphoto['url_o'])
        )
    if dryrun:
        logger.info('Dry run, not downloading')
    else:
        with multiprocessing.Pool(processes=10) as pool:
            pool.map(_download_image, iterable=downloadphotos)

def _download_image(data):
    directory, filename, url = data
    pathname = os.path.join(directory, filename)

    try:
        out_file = open(pathname, 'xb')
        # Download the file from `url` and save it locally under `pathname`:
        with urllib.request.urlopen(url) as response:
            shutil.copyfileobj(response, out_file)
            logger.info('Downloaded <{name}>'.format(name=out_file.name))

    except OSError as e:
        logger.error('File can not be opened %s, %s' % (pathname, e))

    except Exception as e:
        logger.error('Failed to download from Flickr: %s, %s' % (url, e))

def _get_flickr_filename(id, secret, title, extension):
    return '{app}_{id}_{secret}_o_{title}.{extension}'.format(
        app=general.APPLICATION_NAME, id=id, secret=secret, title=title, extension=extension)

def _get_flickr_id_secret_title_extension(filename):
    id = UNDEFINED
    secret = UNDEFINED
    title = UNDEFINED
    extension = UNDEFINED
    try:
        id, secret, title, extension = re.match('^'+general.APPLICATION_NAME+'_([0-9]+)_([a-z0-9_]+)_o_(.+)\.(.+)', filename).group(1,2,3,4)
    except AttributeError as e:
        logger.debug('Not found')

    logger.debug('<{filename}>, <{id}>, <{secret}>, <{title}>, <{extension}>'.format(
        filename=filename, id=id, secret=secret, title=title, extension=extension))
    return id, secret, title, extension
