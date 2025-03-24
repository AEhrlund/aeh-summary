import ollama

# ollama pull mistral

class Mistral:
  def name(self):
    return "mistral"

  def summarize(self, text):
    num_words = int(0.1 * self._word_count(text))
    prompt = f"Your task is to summarize the following text into maximum {num_words} words. Extract the most important information. Only output the summary without any additional text."
    response = ollama.chat(model=self.name(), messages=[
      {
        "role": "system",
        "content": prompt
      },
      {
        "role": "user",
        "content": text
      }
    ])
    
    summary = response["message"]["content"]
    return summary

  def _word_count(self, text):
    return len(text.split())
