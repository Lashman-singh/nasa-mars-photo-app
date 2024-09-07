from requests import get
from PIL import Image
from io import BytesIO
from menu import Menu

# NASA API Key
API_KEY = "6kVdihE5jRgDkJgsw3aQrIkreW3HF4Zt7SN3UjUO"

# Base URL for the Mars Rover API
url_rovers = f"https://api.nasa.gov/mars-photos/api/v1/rovers?api_key={API_KEY}"

def display_photo(url):
    """Displays the photo found at url."""
    try:
        img_resp = get(url)
        img_resp.raise_for_status()  # Check for HTTP errors
        img = Image.open(BytesIO(img_resp.content))
        img.show()
    except Exception as e:
        print(f"Error displaying photo: {e}")

def get_rover_photos(rover_name, date=None, sol=None, camera=None):
    """Fetches and returns photos for the given rover and date/sol/camera."""
    url_photos = f"https://api.nasa.gov/mars-photos/api/v1/rovers/{rover_name}/photos?"
    params = {"api_key": API_KEY}

    if date:
        params["earth_date"] = date
    if sol:
        params["sol"] = sol
    if camera:
        params["camera"] = camera

    try:
        response = get(url_photos, params=params)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()
        print(f"Fetching photos from: {url_photos}")

        if "photos" not in data:
            print("Unexpected response structure:", data)
            return []
        
        if not data["photos"]:
            print(f"No photos found for {rover_name} on {date or 'sol ' + str(sol)}.")
            return []
        
        return data["photos"]
    except Exception as e:
        print(f"Error fetching photos for {rover_name}: {e}")
        return []

def show_photos_for_rover(rover):
    """Prompts the user for date, sol, camera, and displays photos for the chosen rover."""
    while True:
        print(f"\nOptions for {rover}:")
        date = input("Enter a date (YYYY-MM-DD) or press Enter to skip: ")
        sol = input("Enter a Martian sol or press Enter to skip: ")
        camera = input("Enter a camera abbreviation (FHAZ, RHAZ, MAST, CHEMCAM, MAHLI, MARDI, NAVCAM, PANCAM, MINITES) or press Enter to skip: ")

        photos = get_rover_photos(rover, date if date else None, sol if sol else None, camera if camera else None)

        if not photos:
            print(f"No photos available for {rover} with the given criteria. Please try again.")
            continue
        
        paginate_photos(photos, rover, date, sol)

        if input("\nWould you like to search for another rover? (y/n): ").lower() != 'y':
            break

def paginate_photos(photos, rover, date, sol, page=1):
    """Paginate the photos and allow the user to view them."""
    per_page = 10
    total_pages = (len(photos) + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page

    current_page_photos = photos[start:end]
    if not current_page_photos:
        print("No photos available on this page.")
        return
    
    menu_options = [(f"Photo {i + 1}: {photo['img_src']}", lambda url=photo['img_src']: display_photo(url)) for i, photo in enumerate(current_page_photos)]
    
    # Pagination controls
    if page > 1:
        menu_options.append(("Previous Page", lambda: paginate_photos(photos, rover, date, sol, page - 1)))
    if page < total_pages:
        menu_options.append(("Next Page", lambda: paginate_photos(photos, rover, date, sol, page + 1)))

    menu_options.append(("Back to rover selection", choose_rover))
    
    menu = Menu(options=menu_options, title=f"{rover} Photos (Page {page}/{total_pages})")
    menu.open()

def choose_rover():
    """Displays a menu to select a rover and view its photos."""
    rovers = ["Curiosity", "Perseverance"] 
    rover_options = [(rover, lambda rover=rover: show_photos_for_rover(rover)) for rover in rovers]
    rover_options.append(("Exit", Menu.CLOSE))

    menu = Menu(options=rover_options, title="Choose a Mars Rover")
    menu.open()

if __name__ == "__main__":
    choose_rover()

# TEST CASES
"""
1. Curiosity: "2022-08-25" "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&api_key=6kVdihE5jRgDkJgsw3aQrIkreW3HF4Zt7SN3UjUO"
2. Perseverance: "2021-04-20", "100", "https://api.nasa.gov/mars-photos/api/v1/rovers/perseverance/photos?sol=100&api_key=6kVdihE5jRgDkJgsw3aQrIkreW3HF4Zt7SN3UjUO"
"""



# #6kVdihE5jRgDkJgsw3aQrIkreW3HF4Zt7SN3UjUO


# """
# Description: Fetches random dog pictures from Dog CEO's Dog API.
# Author: MGA
# Date: Sep/2024
# """
# from requests import get
# from PIL import Image
# from io import BytesIO

# # Base URL for the Dog API
# url_random_dog = "https://dog.ceo/api/breeds/image/random"

# def fetch_dog_picture() -> None:
#     """Fetches a random dog picture and displays it."""
#     response = get(url_random_dog)  # Make an API request to fetch a random dog image
#     data = response.json()  # Parse the JSON response to get the image URL
#     img_url = data["message"]

#     # Display the fetched dog picture
#     img_resp = get(img_url)  # Make another request to get the image content
#     img = Image.open(BytesIO(img_resp.content))  # Open the image using PIL
#     img.show()  # Display the image
#     img.close()

# if __name__ == "__main__":
#     fetch_dog_picture()  # Call the function to fetch and show a dog picture


