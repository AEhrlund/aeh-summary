import sys
from lib.epub import EpubDb
from lib.browse import EpubBrowser

epub_dir = sys.argv[1]
epub_db = EpubDb(epub_dir)
browse = EpubBrowser(epub_db.epub_db_dir)
browse.browse()
