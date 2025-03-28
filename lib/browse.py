import os
import json
from asciimatics.screen import Screen
from asciimatics.widgets import Frame, ListBox, Layout, Label, Divider
from asciimatics.scene import Scene
from asciimatics.exceptions import StopApplication
from asciimatics.event import KeyboardEvent

class EpubBrowserFrame(Frame):
    def __init__(self, screen, epub_book):
        super().__init__(screen,
                        screen.height,
                        screen.width,
                        title="AEH - Summary Browser",
                        can_scroll=False)

        self.epub_book = epub_book
        chapters = self.epub_book.chapters()
        self.chapters = [(chapter, idx) for idx, chapter in enumerate(chapters)]
        chapter = self.chapters[0][0]
        self.chapter_dir, self.sections = self.epub_book.get_sections(chapter)

        # Calculate dimensions for quadrants
        half_height = screen.height // 2
        half_width = screen.width // 2

        # Layout for all quadrants
        layout = Layout([half_width, half_width], fill_frame=True)
        self.add_layout(layout)

        # Chapters
        self._chapter_listbox = ListBox(
            height=half_height - 4,  # Adjust for borders and padding
            options=self.chapters,
            name="chapter_list",
            on_change=self._update_chapter
        )
        layout.add_widget(Label("Chapters"), 0)
        layout.add_widget(Divider(), 0)
        layout.add_widget(self._chapter_listbox, 0)
        layout.add_widget(Divider(), 0)

        # Sections
        self._section_listbox = ListBox(
            height=half_height - 4,  # Adjust for borders and padding
            options=[],
            name="section_list",
            on_change=self._update_section
        )
        layout.add_widget(Label("Sections"), 0)
        layout.add_widget(Divider(), 0)
        layout.add_widget(self._section_listbox, 0)
        
        # Text
        self._text_label = Label("Select a section to see text",
                                height=half_height - 4,
                                align="^")
        layout.add_widget(Label("Text"), 1)
        layout.add_widget(Divider(), 1)
        layout.add_widget(self._text_label, 1)
        layout.add_widget(Divider(), 1)

        # Summary
        self._summary_label = Label("", height=half_height - 4)
        layout.add_widget(Label("Summary"), 1)
        layout.add_widget(Divider(), 1)
        layout.add_widget(self._summary_label, 1)

        self.fix()

    def _update_chapter(self):
        if self._chapter_listbox.value is not None:
            chapter_index = self._chapter_listbox.value
            chapter = self.chapters[chapter_index][0]
            self.chapter_dir, sections = self.epub_book.get_sections(chapter)
            self._section_listbox.options = [(section, idx) for idx, section in enumerate(sections)]
            self._section_listbox.value = 0
            self._update_section()  # Explicitly call _update_section
            
    def _update_section(self):
        if self._section_listbox.value is not None:
            file = os.path.join(self.chapter_dir, self._section_listbox.options[self._section_listbox.value][0])
            with open(file, 'r', encoding='utf-8') as f:
                selected_content = f.read()
            self._text_label.text = selected_content
            summary_file = os.path.join(self.chapter_dir, f"{self._section_listbox.options[self._section_listbox.value][0]}.mistral.txt")
            print(summary_file)
            with open(summary_file, 'r', encoding='utf-8') as f:
                self._summary_label.text = f.read()

    def process_event(self, event):
        if event and isinstance(event, KeyboardEvent):
            if event.key_code == ord('q'):
                raise StopApplication("User quit")
        return super().process_event(event)

def _epub_browser(screen, epub_book):
    scenes = [
        Scene([EpubBrowserFrame(screen, epub_book=epub_book)], -1, name="Main")
    ]
    screen.play(scenes, stop_on_resize=True)


class EpubBook:
    def __init__(self, epub_db_dir):
        self.epub_db_dir = epub_db_dir
        self.toc = self._read_toc()

    def _read_toc(self):
        toc_file = os.path.join(self.epub_db_dir, "toc.json")
        with open(toc_file, "r") as f:
            return json.load(f)

    def chapters(self):
        chapters = []
        for chapter in self.toc:
            chapters.append(chapter["title"])
        return chapters

    def chapter_to_dirname(self, chapter):
        illegal_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        for char in illegal_chars:
            chapter = chapter.replace(char, '_')
        return chapter

    def get_sections(self, chapter):
        chapter = self.chapter_to_dirname(chapter)
        chapter_dir = os.path.join(self.epub_db_dir, chapter)
        sections = []
        if os.path.exists(chapter_dir):
            sections = [file for file in os.listdir(chapter_dir) if file.endswith('.html')]
        return chapter_dir, sections

class EpubBrowser:
    def __init__(self, epub_db_dir):
        self.epub_db_dir = epub_db_dir

    def browse(self):
        Screen.wrapper(_epub_browser, arguments=[EpubBook(self.epub_db_dir)])
