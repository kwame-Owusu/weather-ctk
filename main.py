import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from PIL import Image, ImageTk
import requests


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("500x500")
        self.title("Weather")
        self.resizable(False, False)
        self.iconbitmap("icon.ico")
        self.config(bg="#151515")
        self
        # Create the labels and buttons
        self.search_img_button = ctk.CTkImage(light_image=Image.open("search.png"), dark_image=Image.open("search.png"), size=(30,30))
        
        # Create the labels and buttons
        self.search = ctk.CTkEntry(self, placeholder_text="Search", width=300, height=30, font=("Arial", 16, "bold"))
        self.weather_label = ctk.CTkLabel(self, text="", bg_color="#151515")
        self.temperature_label = ctk.CTkLabel(self, text="Temperature:",font=("Arial", 20, "bold"), bg_color="#151515")#373A40
        self.description_label = ctk.CTkLabel(self, text="Description:",font=("Arial", 20, "bold"), bg_color="#151515")
        self.search_button = ctk.CTkButton(self,text="", command=self.search_weather, image=self.search_img_button,bg_color="#151515" ,width=80,fg_color="#151515", hover_color="#373A40")
        self.location = ctk.CTkLabel(self)

      
   
   
        

        # Place the search entry in the middle of the screen
        self.search.grid(column=0, row=0, padx=20, pady=50)
        self.search_button.grid(column=1, row=0,)
        self.weather_label.grid(column=0, row=1, pady=50 )
        self.temperature_label.grid(column=0, row=2,padx=20,)
        self.description_label.grid(column=0, row=3, padx=20, pady=20)

    def show_info(self) -> None:
        CTkMessagebox(title="Warning Message!", message="Unable to find city",
                      icon="warning", option_1="Cancel", option_2="Retry")

    def get_weather(self:any, city: str) -> str:
        self.API_KEY = "your_own_api_key"
        self.url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.API_KEY}"
        self.res = requests.get(self.url)
        if self.res.status_code == 404:
            self.show_info()
        try:
            self.weather = self.res.json()
            self.icon_id = self.weather['weather'][0]['icon']
            self.temperature = self.weather['main']['temp'] - 273.15
            self.description = self.weather['weather'][0]['description']
            self.country = self.weather['sys']['country']
        except KeyError:
            self.show_info()
        else:
            print("Enter a city in the search field")

        # Get the icon URL and return all weather information
        self.icon_url = f"https://openweathermap.org/img/wn/{self.icon_id}@2x.png"
        return self.icon_url, self.temperature, self.description, city, self.country

    def search_weather(self) -> None:
        city = self.search.get()
        result = self.get_weather(city)
        if result:
            icon_url, temperature, description, city, country = result
            self.temperature_label.configure(text=f"Temperature: {temperature:.2f} °C")
            self.description_label.configure(text=f"Description: {description}")
            self.location.configure(text=f"{city}, {country}")
            
            # Get weather icon image from URL and update icon label
            image = Image.open(requests.get(icon_url, stream=True).raw)
            icon = ImageTk.PhotoImage(image)
            self.weather_label.configure(image=icon)
            self.weather_label.image = icon  # Keep a reference to the image


app = App()
app.mainloop()
