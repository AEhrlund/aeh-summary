import os
import json
from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem, SubmenuItem

class EpubBrowser:
    def __init__(self, epub_db_dir):
        self.epub_db_dir = epub_db_dir
        self.toc = self._load_toc()
        self.chapters = self._load_chapters()

    def _load_toc(self):
        toc_filename = os.path.join(self.epub_db_dir, 'toc.json')
        with open(toc_filename, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _load_chapters(self):
        chapters = {}
        for root, _, files in os.walk(self.epub_db_dir):
            for file in files:
                if file.endswith('.html'):
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        chapters[file] = f.read()
        return chapters

    def browse(self):
        menu = ConsoleMenu("EPUB Browser", "Select a chapter and file to view content")
        for chapter in self.toc:
            submenu = ConsoleMenu(chapter['title'])
            chapter_dir = os.path.join(self.epub_db_dir, chapter['title'])
            if os.path.isdir(chapter_dir):
                files = os.listdir(chapter_dir)
                for file in files:
                    file_path = os.path.join(chapter_dir, file)
                    submenu.append_item(FunctionItem(file, self._display_content, [file_path]))
            menu.append_item(SubmenuItem(chapter['title'], submenu, menu))
        menu.show()

    def _display_content(self, file_path):
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            input(f"\n{content}\n\nPress Enter to return to the menu...")
        else:
            input("File not found. Press Enter to return to the menu.")

if __name__ == "__main__":
    epub_db_dir = sys.argv[1]
    browser = EpubBrowser(epub_db_dir)
    browser.browse()
