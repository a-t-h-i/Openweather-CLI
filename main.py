import requests, json, os, time
from os.path import exists
from prettytable import PrettyTable


def should_update(city):
    if has_city_file(city):
        for file in os.listdir("data"):
            if city in file:
                file_time = os.path.getmtime(f"data/{file}")
                now = time.time()
                # Returns either true or false.
                return (now - file_time) > (3 * 3600)
    else:
        return True


def has_env_file():
    return exists(".env")


def get_api_key():
    return input("Please enter your OpenWeather API key:\n")


def save_to_env(key):
    with open(".env", "w") as f:
        f.write(f"KEY={key}")


def set_env_variable():
    with open(".env", "r") as f:
        for line in f.readlines():
            key, value = line.split("=")
            os.environ[key] = value


def get_city_name(key):
    while True:
        os.system("clear")
        city = input("Enter name of city:\n").upper()
        result = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}"
        ).json()

        if result["cod"] == "404":
            continue
        else:
            break
    return city.upper()


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

    lat = json.loads(result)[0]["lat"]
    lon = json.loads(result)[0]["lon"]

    return (lat, lon)


def get_current_weather(key, lat_lon):
    result = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?lat={lat_lon[0]}&lon={lat_lon[1]}&appid={key}&units=metric"
    ).text

    current_temp = json.loads(result)["main"]["temp"]
    description = json.loads(result)["weather"][0]["description"]

    return {"Temp": current_temp, "Description": description}


def get_3_hourly_forecast(lat_lon, key):
    result = requests.get(
        f"https://api.openweathermap.org/data/2.5/forecast?lat={lat_lon[0]}&lon={lat_lon[1]}&cnt=5&appid={key}&units=metric"
    ).text

    data = json.loads(result)["list"]

    first = {
        "Temp": data[0]["main"]["temp"],
        "Description": data[0]["weather"][0]["description"],
        "Time": data[0]["dt_txt"].split(" ")[1],
    }

    second = {
        "Temp": data[1]["main"]["temp"],
        "Description": data[1]["weather"][0]["description"],
        "Time": data[1]["dt_txt"].split(" ")[1],
    }

    third = {
        "Temp": data[2]["main"]["temp"],
        "Description": data[2]["weather"][0]["description"],
        "Time": data[2]["dt_txt"].split(" ")[1],
    }

    return (first, second, third)


def save_to_file(city, lat_lon, data):
    formatted_name = f"{city.upper()}_{lat_lon[0]}_{lat_lon[1]}.txt"

    if has_city_file(city):
        for item in os.listdir("data"):
            if city in item:
                f = open(f"data/{item}", "w")
                f.write(data)
                f.close()
    else:
        with open(f"data/{formatted_name}", "w") as f:
            f.write(data)


def prettify_data(city, current_weather, three_hour_forecast):
    table = PrettyTable()

    table.field_names = ["Time", "Temperature", "Description"]
    table.add_row(["Now", current_weather["Temp"], current_weather["Description"]])
    table.add_row(
        [
            three_hour_forecast[0]["Time"],
            three_hour_forecast[0]["Temp"],
            three_hour_forecast[0]["Description"],
        ]
    )

    table.add_row(
        [
            three_hour_forecast[1]["Time"],
            three_hour_forecast[1]["Temp"],
            three_hour_forecast[1]["Description"],
        ]
    )

    table.add_row(
        [
            three_hour_forecast[2]["Time"],
            three_hour_forecast[2]["Temp"],
            three_hour_forecast[2]["Description"],
        ]
    )

    return f"Today's weather in {city}\n{str(table)}"


def display(city):
    files = os.listdir("data")

    for file in files:
        if city in file:
            with open(f"data/{file}", "r") as f:
                for line in f.readlines():
                    print(line, end="")
                print()


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

    set_env_variable()

    key = os.environ["KEY"]
    city = get_city_name(key)

    if should_update(city):
        lat_lon = get_coordinates(city, key)
        current_weather = get_current_weather(key, lat_lon)
        three_hour_forecast = get_3_hourly_forecast(lat_lon, key)
        pretty_data = prettify_data(city, current_weather, three_hour_forecast)
        save_to_file(city, lat_lon, pretty_data)

    os.system("clear")
    display(city)


if __name__ == "__main__":
    main()
