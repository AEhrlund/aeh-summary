import sys
from lib.generate_summary import EpubGenerateSummary
from lib.models.mistral import Mistral

epub_file = sys.argv[1]
epub_db = EpubGenerateSummary(epub_file)
epub_db.generate_summary(Mistral())
