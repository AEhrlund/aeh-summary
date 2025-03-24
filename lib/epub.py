import os
import ebooklib
import ebooklib.epub
import bs4
import json

class EpubDb:
  def __init__(self, epub_file):
    if os.path.isdir(epub_file):
      self._load_epub_db(epub_file)
    else:
      self._create_epub_db(epub_file)

  def _load_epub_db(self, epub_db_dir):
      self.epub_db_dir = epub_db_dir
      self.toc = self._load_get_toc(self.epub_db_dir)

  def _create_epub_db(self, epub_file):
    root_dir = os.path.join(os.path.dirname(__file__), '../../epub_db')
    epub_name = os.path.basename(epub_file)
    epub_name = os.path.splitext(epub_name)[0]
    self.epub_db_dir = os.path.join(root_dir, epub_name)
    self.toc = self._epub_to_text_chapters(epub_file, self.epub_db_dir)

  def _epub_to_text_chapters(self, epub_file, epub_db_dir):
    os.makedirs(epub_db_dir)
    book = ebooklib.epub.read_epub(epub_file)
    toc = self._epub_get_toc(book)
    self._save_toc(toc, epub_db_dir)
    for item in book.get_items():
      if item.get_type() == ebooklib.ITEM_DOCUMENT:
        if self._find_toc_item(toc, item.get_name()):
          toc_item = self._find_toc_item(toc, item.get_name())
        self._save_chapter(item, toc_item, epub_db_dir)
    return toc

  def _load_get_toc(self, epub_db_dir):
    toc_filename = os.path.join(epub_db_dir, 'toc.json')
    with open(toc_filename, 'r', encoding='utf-8') as f:
      toc = json.load(f)
    return toc

  def _epub_get_toc(self, book):
    toc = []
    for item in book.toc:
      if not isinstance(item, ebooklib.epub.Link):
        raise Exception('TOC item is not a Link')
      chapter = {
        'title': item.title,
        'href': item.href,
        'uid': item.uid
      }
      toc.append(chapter)
    return toc

  def _find_toc_item(self, toc, href):
    for item in toc:
      if item['href'] == href:
        return item
    return None

  def _save_toc(self, toc, output_dir):
    toc_filename = os.path.join(output_dir, 'toc.json')
    os.makedirs(output_dir, exist_ok=True)
    for index, item in enumerate(toc, start=1):
      item['title'] = f"{index} - {item['title']}"
    with open(toc_filename, 'w', encoding='utf-8') as f:
      json.dump(toc, f, ensure_ascii=False, indent=4)

  def _chapter_to_dirname(self, chapter):
    illegal_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in illegal_chars:
      chapter = chapter.replace(char, '_')
    return chapter

  def _save_chapter(self, chapter, toc_item, output_dir):
    text_content = self._chapter_to_text(chapter)
    if not text_content.strip():
      return
    text_content = '\n'.join(line.strip() for line in text_content.splitlines() if line.strip())

    toc_title = self._chapter_to_dirname(toc_item["title"])
    chapter_name = chapter.get_name()

    filename = os.path.join(output_dir, toc_title, chapter_name)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text_content)
    
  def _chapter_to_text(self, chapter):
    soup = bs4.BeautifulSoup(chapter.get_content(), 'html.parser')
    return soup.get_text()
