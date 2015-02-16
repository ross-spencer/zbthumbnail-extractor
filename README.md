zbthumbnail-extractor
=====================

Zoom Browser Thumbnail Extractor

Accepts --info <filename> as an argument.

<filename> should point to a ZBThumbnail.info file. 

    Example:
    >python zbextractor.py --info ZbThumbnail.info
    
If zbextractor.py accurately discovers thumbnail files then it will a folder with the following name '{filename}-{uuid4}/' under which it will put the stored images, e.g. image-0001.jpg, image-0002.jpg.

More information here: http://fileformats.archiveteam.org/wiki/ZoomBrowser_Ex_thumbnail_cache

**NOTE:** This may also work on Thumbs.db files created by Microsoft Windows.
