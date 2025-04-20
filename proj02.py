#!/usr/bin/python3

from jinja2 import Environment, FileSystemLoader
import requests
import json
import os
import shutil


#Delete and remake the old build dir
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

build_dir = os.path.join(parent_dir, 'build')

shutil.rmtree(build_dir, ignore_errors=True)

os.makedirs(build_dir, exist_ok=True)


#make sub dir's
css_dir = os.path.join(build_dir, 'css')
img_dir = os.path.join(build_dir, 'img')

os.makedirs(css_dir, exist_ok=True)
os.makedirs(img_dir, exist_ok=True)


#remake downalods folder
downloads_dir = os.path.join(os.path.dirname(__file__), '..', 'downloads')
shutil.rmtree(downloads_dir, ignore_errors=True)

os.makedirs(downloads_dir, exist_ok=True)





API_FILE_PATH="/home/kscrivnor/key"
with open(API_FILE_PATH, 'r') as keyfile:
    API_KEY = keyfile.read().rstrip()

print("Read the secret key, it is: " + API_KEY)


# setup some information
secret_key = API_KEY
nasa_url = 'https://api.nasa.gov/planetary/apod?api_key=' + API_KEY + '&count=3'


# make the GET request
r = requests.get(nasa_url)

# did we get back some JSON?
print("Got a response from NASA!")
print(r.text)
print()

# load the data as json data
data = json.loads(r.text)


nasa_stuff = []


for entry in data:
    entry_data = {
        'date': entry['date'],
        'title': entry['title'],
        'explanation': entry['explanation'],
        'url': entry['url']
        }
        

    nasa_stuff.append(entry_data)

# download the image into the downloads folder
    print("Downloading...")
    os.system("wget -P /home/kscrivnor/421/comp_421_24s_jogg/proj02/downloads " + entry['url'])

# extract the filename, might be useful later
    print("Downloaded file: " + entry['url'].split('/')[-1])

  



# Determine the path to the templates directory
templates_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')

# Load the Jinja2 environment
env = Environment(loader=FileSystemLoader(templates_dir))

# Load the template
template = env.get_template('newsletter.html.j2')


# Prepare data (assuming `entries` is your JSON structure)
data = {
    'entries': nasa_stuff
}






output = template.render(data)


build_dir = os.path.join(os.path.dirname(__file__), '..', 'build')

#make html file
with open(os.path.join(build_dir, 'newsletter.html'), 'w') as f:
    f.write(output)


downloads_dir = os.path.join(os.path.dirname(__file__), '..', 'downloads')
build_img_dir = os.path.join(os.path.dirname(__file__), '..', 'build', 'img')


# copy pics from downlaods to build/img
for file_name in os.listdir(downloads_dir):

      if os.path.isfile(os.path.join(downloads_dir, file_name)):
             shutil.copy(os.path.join(downloads_dir, file_name), build_img_dir)





#Download bootstrap.css and put into /build/css
url = "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"

css_file_path = "/home/kscrivnor/421/comp_421_24s_jogg/proj02/build/css/bootstrap.css"

response = requests.get(url)

if response.status_code == 200:
    with open(css_file_path, "wb") as file:
        file.write(response.content)
    
else:
    print(f"Failed to download bootstrap.css file.")

