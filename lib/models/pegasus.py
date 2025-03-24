from transformers import PegasusTokenizer, PegasusForConditionalGeneration

class Pegasus:
  def __init__(self):
    self.model_name = "google/pegasus-xsum"
    self.tokenizer = PegasusTokenizer.from_pretrained(self.model_name)
    self.model = PegasusForConditionalGeneration.from_pretrained(self.model_name)

  def name(self):
    return "pegasus"

  def summarize(self, text):
    inputs = self.tokenizer(text, truncation=True, padding="longest", return_tensors="pt")

    summary_ids = self.model.generate(
        inputs["input_ids"],
        num_beams=8,            # Beam search for better quality
        max_length=200,          # Maximum length of the summary
        early_stopping=False
    )

    summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary
