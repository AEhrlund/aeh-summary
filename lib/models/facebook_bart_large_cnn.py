import transformers
from transformers import BartTokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

def extractive_summary(text):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, 30)
    return " ".join(str(sentence) for sentence in summary)

def summarize(text):
  summarizer = transformers.pipeline("summarization", model="facebook/bart-large-cnn")
  print(f"Summarizing text: size = {len(text)}")
  tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
  tokens = tokenizer.encode(text, return_tensors="pt")
  if len(tokens[0]) > 1024:
    print("Text too long, summarizing extractively")
    text = extractive_summary(text)
  summary = summarizer(text, max_length=250, min_length=10, do_sample=False)
  return summary[0]['summary_text']
