import requests
from dotenv import load_dotenv
import os
import pprint

input = "Q: Information/File Manager I'm looking for a file manager application which helps to organize a large amount of movies, pictures, music, text documents, databases, audio-books and ebooks. Right now I only use the Finder which doesn't work well, because I really need a function to put single files into multiple categories. Simply using the file system for this creates a confusing nesting of files. A: Depending on the number of categories you require to handle, you could always use a combination of the finder with the built in label functionality, thus a movie can be held in one area (movies directory, for example), but \"tagged\" as something else. Using smart directories and saved searches you can view your files by a combination of the attributes (location, label, media type) to create custom views. All without purchasing software. Cheap and cheerful, but may be suitable to your needs. A: Maybe use a file manager that supports Open Meta. Or use symbolic links for organizing all your media files. Or even use hardlinked files if you dare."

load_dotenv()
HF_API_KEY = os.getenv('HF_API_KEY')

# internal server error :(
# API_URL = "https://api-inference.huggingface.co/models/mhenrichsen/context-aware-splitter-1b-english"

# does classification instead :(
# API_URL = "https://api-inference.huggingface.co/models/BlueOrangeDigital/distilbert-cross-segment-document-chunking"

# works, but kinda sucks. Produces chunks of uneven size
API_URL = "https://api-inference.huggingface.co/models/ish97/bert-finetuned-chunking-for-echo-reading"

headers = {"Authorization": f"Bearer {HF_API_KEY}"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

output = query({
	"inputs": input,
})

pp = pprint.PrettyPrinter()
pp.pprint(output)
