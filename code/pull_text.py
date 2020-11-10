import pandas as pd
import pytesseract
import requests
from PIL import Image
from io import BytesIO
from tqdm import tqdm

cares_bot = pd.read_csv("project_2/data/cares_bot_image_urls.csv", names=["images"],
                        skiprows=1)

image_requests = cares_bot["images"].apply(requests.get)

respondent_info = []

# Catch the index of image that failed to be opened or extracted
errors = []

# This will likely take awhile so we'll use tqdm to print a progress bar to see
# what iteration I'm on
for index, image in tqdm(enumerate(image_requests)):
    try:
        opened_image = Image.open(BytesIO(image.content))
        image_text = pytesseract.image_to_string(opened_image).replace("\n", " ")
        respondent_info.append(image_text)
    # Doing a general catch-all exception as I'm not entirely sure what errors I could expect
    except:
        errors.append(index)
        continue

# Convert the text data into a DataFrame then write out to a CSV
cares_bot_survey_data = pd.DataFrame(respondent_info)
cares_bot_survey_data.to_csv("C:/Users/Rober/DATS_6103/project_2/data/cares_bot_survey_data.csv", index=False)
