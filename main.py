import requests, json, os
from os.path import exists


def check(city):
   
    if has_city_file(city):
        # Check if the file is not older than 180 minutes
        return True
    else:
        return False


def has_env_file():
    return exists(".env")


def get_api_key():
    return input("Please enter your OpenWeather API key:\n")


def save_to_env(key):
    with open(".env", "w") as f:
        f.write(f"KEY={key}")


def read_env():
    with open(".env", "r") as f:
        for line in f.readlines():
            key, value = line.split('=')
    return value


def get_city_name():
    return input("Enter name of city:\n")


def has_city_file(city):
    files = os.listdir("data")

    for file in files:
        if city in file:
            return True
    return False


def get_coordinates(city, key):
    result = requests.get(
        f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={key}"
    ).text
    
    if len(result) < 3:
        return (0,0)
    
    lat = json.loads(result)[0]["lat"]
    lon = json.loads(result)[0]["lon"]
    
    return (lat, lon)


def get_current_weather(key, lat_lon):
    result = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?lat={lat_lon[0]}&lon={lat_lon[1]}&appid={key}&units=metric"
    ).text
    current_temp = json.loads(result)["main"]["temp"]
    description = json.loads(result)["weather"][0]["description"]
    return f"Temp: {current_temp}\nDescription: {description}"


def get_3_hourly_forecast(lat_lon, key):
    result = requests.get(
        f"https://api.openweathermap.org/data/2.5/forecast?lat={lat_lon[0]}&lon={lat_lon[1]}&cnt=5&appid={key}&units=metric"
    ).text
    data = json.loads(result)["list"]
    
    first = {"Temp": data[0]["main"]["temp"],
             "Description": data[0]["weather"][0]["description"],
             "Time": data[0]["dt_txt"]}
    
    second = {"Temp": data[0]["main"]["temp"],
             "Description": data[0]["weather"][0]["description"],
             "Time": data[0]["dt_txt"]}
    
    third =  {"Temp": data[0]["main"]["temp"],
             "Description": data[0]["weather"][0]["description"],
             "Time": data[0]["dt_txt"]}
    
    return (first, second, third)


def save_to_file(city, current_weather, three_hour_forecast):

    print("Save to file")
    pass


def update_city_file(city, current_weather, five_day_weather):
    print("Update city file")
    pass


def display_data():
    print("Display data :D")
    pass


def main():
    key, city = "", ""

    if not has_env_file():

        while True:
            key = get_api_key()

            if not len(key) == 32:
                continue
            else:
                break

        save_to_env(key)

    key = read_env()
    city = get_city_name()

    if not check(city):
        lat_lon = get_coordinates(city, key)
        current_weather = get_current_weather(key, lat_lon)
        three_hour_forecast = get_3_hourly_forecast(lat_lon, key)
        save_to_file(city, current_weather, three_hour_forecast)
    
    print(current_weather)
    print(three_hour_forecast)
    display_data()


if __name__ == '__main__':
    main()