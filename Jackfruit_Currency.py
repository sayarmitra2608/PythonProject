import wx
import requests
from datetime import datetime

class CurrencyConverterFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Currency Converter - Real-Time Rates", size=(500, 600))
        
        # Multiple API sources for fallback
        self.api_sources = [
            {
                "name": "ExchangeRate-API",
                "url": "https://api.exchangerate-api.com/v4/latest/",
                "format": "standard"
            },
            {
                "name": "Exchangerate.host",
                "url": "https://api.exchangerate.host/latest?base=",
                "format": "host"
            },
            {
                "name": "FreeForexAPI",
                "url": "https://api.freeforexapi.com/v1/latest?base=",
                "format": "freeforex"
            }
        ]
        
        # Popular currencies
        self.currencies = [
            "USD", "EUR", "GBP", "JPY", "AUD", "CAD", "CHF", "CNY", 
            "INR", "MXN", "BRL", "ZAR", "SGD", "HKD", "NOK", "SEK",
            "DKK", "NZD", "KRW", "TRY", "RUB", "AED", "SAR", "PKR"
        ]
        
        self.init_ui()
        self.Centre()
        
    def init_ui(self):
        panel = wx.Panel(self)
        panel.SetBackgroundColour(wx.Colour(236, 240, 241))
        
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Title
        title = wx.StaticText(panel, label="Currency Converter",style=wx.ALIGN_CENTRE_HORIZONTAL)
        title_font = wx.Font(18, wx.FONTFAMILY_SCRIPT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD,faceName="Segoe Script")
        title.SetFont(title_font)
        title.SetForegroundColour(wx.WHITE)
        title.SetBackgroundColour(wx.Colour(186,104 ,200))
        
        title_sizer = wx.BoxSizer(wx.HORIZONTAL)
        title_sizer.Add(title, 1, wx.ALIGN_CENTRE | wx.ALL, 20)
        main_sizer.Add(title_sizer, 0, wx.EXPAND)
        
        # Content panel
        content_panel = wx.Panel(panel)
        content_panel.SetBackgroundColour(wx.Colour(236, 240, 241))
        content_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Amount section
        amount_box = wx.BoxSizer(wx.HORIZONTAL)
        amount_label = wx.StaticText(content_panel, label="Amount:")
        amount_label.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        amount_box.Add(amount_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        
        self.amount_text = wx.TextCtrl(content_panel, value="1", size=(250, -1))
        self.amount_text.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        amount_box.Add(self.amount_text, 1, wx.EXPAND)
        content_sizer.Add(amount_box, 0, wx.EXPAND | wx.ALL, 10)
        
        # From currency section
        from_box = wx.BoxSizer(wx.HORIZONTAL)
        from_label = wx.StaticText(content_panel, label="From:")
        from_label.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        from_box.Add(from_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 33)
        
        self.from_choice = wx.Choice(content_panel, choices=self.currencies, size=(250, -1))
        self.from_choice.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.from_choice.SetSelection(self.currencies.index("USD"))
        from_box.Add(self.from_choice, 1, wx.EXPAND)
        content_sizer.Add(from_box, 0, wx.EXPAND | wx.ALL, 10)
        
        # To currency section
        to_box = wx.BoxSizer(wx.HORIZONTAL)
        to_label = wx.StaticText(content_panel, label="To:")
        to_label.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        to_box.Add(to_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 50)
        
        self.to_choice = wx.Choice(content_panel, choices=self.currencies, size=(250, -1))
        self.to_choice.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.to_choice.SetSelection(self.currencies.index("EUR"))
        to_box.Add(self.to_choice, 1, wx.EXPAND)
        content_sizer.Add(to_box, 0, wx.EXPAND | wx.ALL, 10)
        
        # Buttons
        button_box = wx.BoxSizer(wx.HORIZONTAL)
        
        self.convert_btn = wx.Button(content_panel, label="Convert", size=(140, 50))
        self.convert_btn.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.convert_btn.SetBackgroundColour(wx.Colour(39, 174, 96))
        self.convert_btn.SetForegroundColour(wx.WHITE)
        self.convert_btn.Bind(wx.EVT_BUTTON, self.on_convert)
        button_box.Add(self.convert_btn, 0, wx.RIGHT, 10)
        
        self.swap_btn = wx.Button(content_panel, label="Swap", size=(140, 50))
        self.swap_btn.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.swap_btn.SetBackgroundColour(wx.Colour(52, 152, 219))
        self.swap_btn.SetForegroundColour(wx.WHITE)
        self.swap_btn.Bind(wx.EVT_BUTTON, self.on_swap)
        button_box.Add(self.swap_btn, 0)
        
        content_sizer.Add(button_box, 0, wx.ALIGN_CENTER | wx.ALL, 20)
        
        # Result panel
        result_panel = wx.Panel(content_panel)
        result_panel.SetBackgroundColour(wx.WHITE)
        result_sizer = wx.BoxSizer(wx.VERTICAL)
        
        result_title = wx.StaticText(result_panel, label="Result:")
        result_title.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        result_title.SetForegroundColour(wx.Colour(44, 62, 80))
        result_sizer.Add(result_title, 0, wx.ALL, 10)
        
        self.result_text = wx.StaticText(result_panel, label="Enter amount and click Convert")
        self.result_text.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.result_text.SetForegroundColour(wx.Colour(52, 73, 94))
        result_sizer.Add(self.result_text, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        
        self.rate_text = wx.StaticText(result_panel, label="")
        self.rate_text.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.rate_text.SetForegroundColour(wx.Colour(127, 140, 141))
        result_sizer.Add(self.rate_text, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        
        self.timestamp_text = wx.StaticText(result_panel, label="")
        self.timestamp_text.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL))
        self.timestamp_text.SetForegroundColour(wx.Colour(149, 165, 166))
        result_sizer.Add(self.timestamp_text, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        
        result_panel.SetSizer(result_sizer)
        content_sizer.Add(result_panel, 1, wx.EXPAND | wx.ALL, 10)
        
        content_panel.SetSizer(content_sizer)
        main_sizer.Add(content_panel, 1, wx.EXPAND | wx.ALL, 20)
        
        panel.SetSizer(main_sizer)
        
    def fetch_rate_from_api(self, api_source, from_curr, to_curr):
        #ry to fetch rate from a specific API source
        try:
            if api_source["format"] == "standard":
                url = f"{api_source['url']}{from_curr}"
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                data = response.json()
                
                if to_curr in data.get('rates', {}):
                    rate = data['rates'][to_curr]
                    timestamp = data.get('time_last_updated', data.get('date', ''))
                    return rate, timestamp, api_source['name']
                    
            elif api_source["format"] == "host":
                url = f"{api_source['url']}{from_curr}"
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                data = response.json()
                
                if to_curr in data.get('rates', {}):
                    rate = data['rates'][to_curr]
                    timestamp = data.get('date', '')
                    return rate, timestamp, api_source['name']
                    
            elif api_source["format"] == "freeforex":
                url = f"{api_source['url']}{from_curr}"
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                data = response.json()
                
                rates = data.get('rates', {})
                if to_curr in rates:
                    rate_data = rates[to_curr]
                    rate = rate_data.get('rate', rate_data) if isinstance(rate_data, dict) else rate_data
                    timestamp = data.get('updated_date', '')
                    return rate, timestamp, api_source['name']
                    
        except Exception:
            return None, None, None
            
        return None, None, None
    
    def on_convert(self, event):
        try:
            amount = float(self.amount_text.GetValue())
            from_curr = self.currencies[self.from_choice.GetSelection()]
            to_curr = self.currencies[self.to_choice.GetSelection()]
            
            # Show loading message
            self.result_text.SetLabel("Fetching real-time rates...")
            self.result_text.SetForegroundColour(wx.Colour(52, 152, 219))
            self.rate_text.SetLabel("")
            self.timestamp_text.SetLabel("")
            self.Update()
            
            # Try each API source until one succeeds
            rate = None
            timestamp = None
            source_name = None
            
            for api_source in self.api_sources:
                rate, timestamp, source_name = self.fetch_rate_from_api(api_source, from_curr, to_curr)
                if rate is not None:
                    break
            
            if rate is not None:
                converted = amount * rate
                
                # Update result
                result_text = f"{amount:,.2f} {from_curr} = {converted:,.2f} {to_curr}"
                self.result_text.SetLabel(result_text)
                self.result_text.SetForegroundColour(wx.Colour(39, 174, 96))
                self.result_text.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
                
                rate_text = f"Exchange Rate: 1 {from_curr} = {rate:.6f} {to_curr}"
                self.rate_text.SetLabel(rate_text)
                
                # Format timestamp
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if timestamp:
                    timestamp_text = f"Rate updated: {timestamp} | Data from: {source_name}"
                else:
                    timestamp_text = f"Retrieved at: {current_time} | Data from: {source_name}"
                self.timestamp_text.SetLabel(timestamp_text)
            else:
                wx.MessageBox("Could not fetch exchange rates from any source.\nPlease check your internet connection.", 
                            "Error", wx.OK | wx.ICON_ERROR)
                self.result_text.SetLabel("Conversion failed")
                self.result_text.SetForegroundColour(wx.Colour(231, 76, 60))
                
        except ValueError:
            wx.MessageBox("Please enter a valid number!", "Error", wx.OK | wx.ICON_ERROR)
            self.result_text.SetLabel("Invalid input")
            self.result_text.SetForegroundColour(wx.Colour(231, 76, 60))
        except Exception as e:
            wx.MessageBox(f"An error occurred: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)
            self.result_text.SetLabel("Error occurred")
            self.result_text.SetForegroundColour(wx.Colour(231, 76, 60))
    
    def on_swap(self, event):
        from_idx = self.from_choice.GetSelection()
        to_idx = self.to_choice.GetSelection()
        
        self.from_choice.SetSelection(to_idx)
        self.to_choice.SetSelection(from_idx)


def main():
    app = wx.App()
    frame = CurrencyConverterFrame()
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    main()
