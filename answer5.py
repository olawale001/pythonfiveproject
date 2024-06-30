import tkinter as tk
from tkinter import messagebox
import requests

class CurrencyConverter:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = f"https://v6.exchangerate-api.com/v6/{self.api_key}/latest/USD"
        self.rates = self.get_exchange_rates()

    def get_exchange_rates(self):
        try:
            response = requests.get(self.url)
            data = response.json()
            if data['result'] == 'success':
                return data['conversion_rates']
            else:
                raise Exception("Failed to fetch exchange rates")
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching exchange rates: {e}")
            return None

    def convert(self, amount, from_currency, to_currency):
        if self.rates:
            try:
                amount = float(amount)
                if from_currency != "USD":
                    amount = amount / self.rates[from_currency]
                return round(amount * self.rates[to_currency], 2)
            except Exception as e:
                messagebox.showerror("Error", f"Conversion error: {e}")
        return None

class CurrencyConverterApp:
    def __init__(self, root, converter):
        self.converter = converter
        self.root = root
        self.root.title("Currency Converter")
        self.root.geometry("400x200")

        self.amount_label = tk.Label(root, text="Amount:")
        self.amount_label.grid(row=0, column=0, padx=10, pady=10)
        self.amount_entry = tk.Entry(root)
        self.amount_entry.grid(row=0, column=1, padx=10, pady=10)

        self.from_currency_label = tk.Label(root, text="From Currency:")
        self.from_currency_label.grid(row=1, column=0, padx=10, pady=10)
        self.from_currency_entry = tk.Entry(root)
        self.from_currency_entry.grid(row=1, column=1, padx=10, pady=10)

        self.to_currency_label = tk.Label(root, text="To Currency:")
        self.to_currency_label.grid(row=2, column=0, padx=10, pady=10)
        self.to_currency_entry = tk.Entry(root)
        self.to_currency_entry.grid(row=2, column=1, padx=10, pady=10)

        self.convert_button = tk.Button(root, text="Convert", command=self.convert)
        self.convert_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.result_label = tk.Label(root, text="Result:")
        self.result_label.grid(row=4, column=0, padx=10, pady=10)
        self.result = tk.Label(root, text="")
        self.result.grid(row=4, column=1, padx=10, pady=10)

    def convert(self):
        amount = self.amount_entry.get()
        from_currency = self.from_currency_entry.get().upper()
        to_currency = self.to_currency_entry.get().upper()

        if not amount or not from_currency or not to_currency:
            messagebox.showwarning("Input error", "Please fill all fields")
            return

        result = self.converter.convert(amount, from_currency, to_currency)
        if result is not None:
            self.result.config(text=f"{result} {to_currency}")
        else:
            self.result.config(text="")

def main():
    api_key = "79e4d44980d76ad2c5224923"  
    root = tk.Tk()
    converter = CurrencyConverter(api_key)
    app = CurrencyConverterApp(root, converter)
    root.mainloop()

if __name__ == "__main__":
    main()
