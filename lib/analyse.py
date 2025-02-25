import transformers

def summarize(text):
  print("BLAJ 1")
  summarizer = transformers.pipeline("summarization", model="facebook/bart-large-cnn")
  print("BLAJ 2")
  summary = summarizer(text, max_length=150, min_length=10, do_sample=False)
  print("BLAJ 3")
  return summary[0]['summary_text']
