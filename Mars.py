import requests
import gradio as gr

# Function to fetch Mars Rover photos
def fetch_mars_rover_photos(api_key, sol=None, earth_date=None, page=1):
    base_url = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos"
   
    params = {
        'api_key': api_key,
        'page': page
    }
   
    if sol is not None:
        params['sol'] = sol
    elif earth_date is not None:
        params['earth_date'] = earth_date
   
    print(params)
   
    response = requests.get(base_url, params=params)
   
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Gradio interface setup
def mars_rover_photo_interface(search_by, sol, earth_date, page):
    api_key = "36PJ0s4qF2bak3DEzoaxMidn7tYjYtyA55xBVDik" # API KEY
    if search_by == "sol":
        data = fetch_mars_rover_photos(api_key, sol=sol, page=page)
    else:
        data = fetch_mars_rover_photos(api_key, earth_date=earth_date, page=page)
   
    print(data)
    if data:
        photos = data.get('photos', [])
        photo_urls = [photo['img_src'] for photo in photos]
        print(photo_urls)
        return photo_urls
    else:
        return []

# Define the input components for the Gradio interface
search_by_input = gr.Radio(label="Search By", choices=["sol", "earth_date"], value="sol")
sol_input = gr.Number(label="Martian Sol", value=None)
earth_date_input = gr.Textbox(label="Earth Date (YYYY-MM-DD)", value=None)
page_input = gr.Number(label="Page", value=1)

# Create the Gradio interface
gr.Interface(fn=mars_rover_photo_interface,
        inputs=[search_by_input, sol_input, earth_date_input, page_input],
        outputs=gr.Gallery(label="Mars Rover Photos")).launch()