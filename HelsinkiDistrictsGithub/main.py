from geopy.geocoders import Nominatim
import requests 
from bs4 import BeautifulSoup
import json

response = requests.get("https://fi.wikipedia.org/wiki/Helsingin_alueellinen_jako") 
soup = BeautifulSoup(response.content, 'html.parser') 
tag = soup.select('td')

geolocator = Nominatim(user_agent="")

def city_checker(cityname):
    print(cityname)
    first_location_data = geolocator.geocode(cityname, exactly_one=True)
    location_data_list = str(first_location_data).split(",")

    try:
        if location_data_list[3] == " Helsinki" or location_data_list[2] == " Helsinki" or location_data_list[4] == " Helsinki":
            location = geolocator.geocode(cityname)
            json_wirter(cityname, location.latitude, location.longitude, False)
        else:
            all_locations_data = geolocator.geocode(cityname, exactly_one=False)
            for city_district in all_locations_data: 
                all_locations_data_list = str(city_district).split(",")
                try:
                    if all_locations_data_list[3] == " Helsinki" or all_locations_data_list[2] == " Helsinki" or all_locations_data_list[4] == " Helsinki":
                        #sleep(randint(1,10))
                        location = geolocator.geocode(cityname)
                        json_wirter(cityname, location.latitude, location.longitude, False)
                        break
                    else:
                        pass
                except IndexError:
                    print(all_locations_data_list)
                    print(f"Error in: {cityname}")                   
    except IndexError:
        print(location_data_list)
        print(f"Error in: {cityname}")
        
def json_wirter(cityname, latitude, longitude, error):
    with open("boroughs_full_data.json", encoding="utf8") as f:
        data = json.load(f)
    json_data = data[suurpiiri][suurpiiri_list[suurpiiri]][peruspiiri]['subdivisions']

    if error == False:
        json_data.append({
        "name": cityname.replace("\n", ""),
        "latitude": latitude,
        "longitude": longitude
        })

    else:
        json_data.append({
        "name": cityname.replace("\n", ""),
        "error": error,
        "latitude": 0,
        "longitude": 0
        })

    with open('data.json', 'w', encoding="utf8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


if __name__=="__main__":
    if input("Start scraping?") == "y":
        names_datafile = open("boroughs_names.txt", "r", encoding="utf8")
        suurpiiri_list = ["ETELÄINEN SUURPIIRI", "LÄNTINEN SUURPIIRI", "KESKINEN SUURPIIRI", "POHJOINEN SUURPIIRI", "KOILLINEN SUURPIIRI", "KAAKKOINEN SUURPIIRI", "ITÄINEN SUURPIIRI", "ÖSTERSUNDOMIN SUURPIIRI"]
        peruspiiri = -1
        suurpiiri = -1

        for name in names_datafile:
            splitted_name = list(name.split(" "))
            length = len(splitted_name)

            if "SUURPIIRI" in splitted_name[length-1]:
                suurpiiri += 1
                peruspiiri = -1
            elif "peruspiiri" in splitted_name[length-1]:
                peruspiiri += 1
            else:
                city_checker(name)
        names_datafile.close
