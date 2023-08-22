from google_images_search import GoogleImagesSearch
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from mycarapp import cache


@cache.memoize(86400)
def get_image_link(car):
    """
    This is Google search api that uses a key word to get the link of image,
    it is used here to get car image based on its name. the API then stores
    the car image for 1 day
    :param car: dict
    :return: image link for car
    """
    try:
        # Replace "your Google API key" and "your Google API CX" with your own values
        gis = GoogleImagesSearch('AIzaSyD8xTkz6wkPCznYTq2mflpf8C-5P1UwvoY', 'c342f53d0d7674732')

        # Replace "parado tx" with your query string
        query = f"picture of Car {car['name']} Manufactured in {car['mfg_year']} body colour {car['body_color']}"
        print(query)
        # Set the search parameters and send the search request
        gis.search({'q': query, 'num': 1})

        # Get the search results and print the first image URL
        for image in gis.results():
            result = image.url
            print(result)

    except Exception as e:
        print(e)
        result = "https://i.ytimg.com/vi/cDGM76Ig9zM/maxresdefault.jpg"
    return result


if __name__ == '__main__':
    car = {'id': 29, 'name': 'Subaru Ascent', 'rent_price': 29.0, 'year': 2019, 'model': 'Base', 'engine_number': '29SU020',
     'cylinder_count': '4', 'body_color': 'Green', 'mfg_year': '2018', 'seating_capacity': '8',
     'horse_power_cc': '2600', 'maker_name': 'Subaru', 'status': 'available'}
    get_image_link(car)
