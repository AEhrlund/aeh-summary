import os
import curses
import json

class EpubBrowser:
    def __init__(self, epub_db_dir):
        self.epub_db_dir = epub_db_dir
        self.toc = self._load_toc()
        self.chapters = self._load_chapters()
        self.current_files = []

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
        curses.wrapper(self._curses_main)

    def _curses_main(self, stdscr):
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        stdscr.clear()
        self._draw_interface(stdscr)
        stdscr.refresh()
        self._main_loop(stdscr)

    def _draw_interface(self, stdscr):
        height, width = stdscr.getmaxyx()
        stdscr.addstr(0, 0, "Chapters", curses.A_BOLD)
        stdscr.addstr(0, width // 3, "Files", curses.A_BOLD)
        stdscr.addstr(0, 2 * width // 3, "Content", curses.A_BOLD)
        self._draw_chapters(stdscr)

    def _draw_chapters(self, stdscr):
        for idx, chapter in enumerate(self.toc):
            stdscr.addstr(idx + 1, 0, chapter['title'])

    def _draw_files(self, stdscr):
        height, width = stdscr.getmaxyx()
        for idx, file in enumerate(self.current_files):
            stdscr.addstr(idx + 1, width // 3, file)

    def _main_loop(self, stdscr):
        current_row = 0
        current_file_row = 0
        pane = 0  # 0 for chapters, 1 for files
        while True:
            self._highlight_row(stdscr, current_row, pane)
            key = stdscr.getch()
            if pane == 0:
                if key == curses.KEY_UP and current_row > 0:
                    self._unhighlight_row(stdscr, current_row, pane)
                    current_row -= 1
                elif key == curses.KEY_DOWN and current_row < len(self.toc) - 1:
                    self._unhighlight_row(stdscr, current_row, pane)
                    current_row += 1
                elif key == curses.KEY_ENTER or key in [10, 13]:
                    self._display_files(stdscr, current_row)
                    current_file_row = 0
                elif key == curses.KEY_RIGHT and self.current_files:
                    pane = 1
            elif pane == 1:
                if key == curses.KEY_UP and current_file_row > 0:
                    self._unhighlight_row(stdscr, current_file_row, pane)
                    current_file_row -= 1
                elif key == curses.KEY_DOWN and current_file_row < len(self.current_files) - 1:
                    self._unhighlight_row(stdscr, current_file_row, pane)
                    current_file_row += 1
                elif key == curses.KEY_ENTER or key in [10, 13]:
                    self._display_content(stdscr, current_file_row)
                elif key == curses.KEY_LEFT:
                    pane = 0
            self._highlight_row(stdscr, current_row if pane == 0 else current_file_row, pane)

    def _highlight_row(self, stdscr, row, pane):
        width = stdscr.getmaxyx()[1]
        if pane == 0:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(row + 1, 0, self.toc[row]['title'])
            stdscr.attroff(curses.color_pair(1))
        elif pane == 1 and self.current_files:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(row + 1, width // 3, self.current_files[row])
            stdscr.attroff(curses.color_pair(1))
        stdscr.refresh()

    def _unhighlight_row(self, stdscr, row, pane):
        width = stdscr.getmaxyx()[1]
        if pane == 0:
            stdscr.addstr(row + 1, 0, self.toc[row]['title'])
        elif pane == 1 and self.current_files:
            stdscr.addstr(row + 1, width // 3, self.current_files[row])
        stdscr.refresh()

    def _display_files(self, stdscr, row):
        chapter = self.toc[row]
        chapter_dir = os.path.join(self.epub_db_dir, chapter['title'])
        if os.path.isdir(chapter_dir):
            self.current_files = os.listdir(chapter_dir)
        else:
            self.current_files = ["No files found in this chapter."]
        self._draw_files(stdscr)

    def _display_content(self, stdscr, row):
        height, width = stdscr.getmaxyx()
        if self.current_files:
            file = self.current_files[row]
            file_path = os.path.join(self.epub_db_dir, file)
            if os.path.isfile(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            else:
                content = "File not found."
            stdscr.addstr(1, 2 * width // 3, content[:width // 3 * (height - 1)])
            stdscr.refresh()

if __name__ == "__main__":
    epub_db_dir = sys.argv[1]
    browser = EpubBrowser(epub_db_dir)
    browser.browse()
