import sys
from lib.epub import EpubDb
from lib.browse import EpubBrowser

epub_file = sys.argv[1]
epub_db = EpubDb(epub_file)
browse = EpubBrowser(epub_db.epub_db_dir)
browse.browse()
