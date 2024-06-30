import tkinter as tk
from tkinter import messagebox
from google.cloud import translate_v2 as translate
import os

class Translator:
    def __init__(self, api_key_path):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = api_key_path
        self.client = translate.Client()

    def translate_text(self, text, target_language):
        try:
            result = self.client.translate(text, target_language=target_language)
            return result['translatedText']
        except Exception as e:
            messagebox.showerror("Error", f"Translation error: {e}")
            return None

class TranslatorApp:
    def __init__(self, root, translator):
        self.translator = translator
        self.root = root
        self.root.title("Text Translator")
        self.root.geometry("400x300")

        self.text_label = tk.Label(root, text="Text to Translate:")
        self.text_label.grid(row=0, column=0, padx=10, pady=10)
        self.text_entry = tk.Text(root, height=5, width=40)
        self.text_entry.grid(row=0, column=1, padx=10, pady=10)

        self.target_language_label = tk.Label(root, text="Target Language (e.g., es, fr, de):")
        self.target_language_label.grid(row=1, column=0, padx=10, pady=10)
        self.target_language_entry = tk.Entry(root)
        self.target_language_entry.grid(row=1, column=1, padx=10, pady=10)

        self.translate_button = tk.Button(root, text="Translate", command=self.translate)
        self.translate_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.result_label = tk.Label(root, text="Translated Text:")
        self.result_label.grid(row=3, column=0, padx=10, pady=10)
        self.result = tk.Text(root, height=5, width=40)
        self.result.grid(row=3, column=1, padx=10, pady=10)

    def translate(self):
        text = self.text_entry.get("1.0", tk.END).strip()
        target_language = self.target_language_entry.get().strip()

        if not text or not target_language:
            messagebox.showwarning("Input error", "Please fill all fields")
            return

        result = self.translator.translate_text(text, target_language)
        if result is not None:
            self.result.delete("1.0", tk.END)
            self.result.insert(tk.END, result)

def main():
    api_key_path = "path/to/your/service-account-file.json"
    root = tk.Tk()
    translator = Translator(api_key_path)
    app = TranslatorApp(root, translator)
    root.mainloop()

if __name__ == "__main__":
    main()
