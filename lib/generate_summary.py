import os
from lib.epub import EpubDb

class EpubGenerateSummary(EpubDb):
  def __init__(self, epub_file):
    super().__init__(epub_file)

  def generate_summary(self, model):
    print(f"Generating summary for {model.name()} model")
    for chapter in self.toc:
      print(f"Generating summary for chapter: {chapter['title']}")
      chapter_dir = os.path.join(self.epub_db_dir, self._chapter_to_dirname(chapter['title']))
      if not os.path.exists(chapter_dir):
        continue
      for section in os.listdir(chapter_dir):
        print(f"  Generating summary for section: {section}")
        section_file = os.path.join(chapter_dir, section)
        with open(section_file, 'r', encoding='utf-8') as f:
          text = f.read()
        summary = model.summarize(text)
        summary_file = os.path.join(chapter_dir, f"{section}.{model.name()}.txt")
        with open(summary_file, 'w', encoding='utf-8') as f:
          f.write(summary)
