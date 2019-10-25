from random import choice
from telegram import ReplyKeyboardMarkup, KeyboardButton
from emoji import emojize

from clarifai.rest import ClarifaiApp

import settings

def get_user_emo(user_data):
    if 'emo' in user_data:
        return user_data['emo']
    else: 
        user_data['emo'] = emojize(choice(settings.USER_EMOJI), use_aliases=True)
        return user_data['emo']

def get_keyboard():
    contact_button = KeyboardButton('Прислать контакты', request_contact=True)
    location_button = KeyboardButton('Прислать координаты', request_location=True)
    my_keyboard = ReplyKeyboardMarkup([
                                        ['Прислать носорожку','Сменить аватарку'],
                                        [contact_button, location_button]
                                    ], resize_keyboard=True
                                    )
    return my_keyboard

def is_rhino(file_name):
    image_has_rhino = False
    app = ClarifaiApp(api_key=settings.CLARIFAI_API_KEY)
    model = app.public_models.general_model
    response = model.predict_by_filename(file_name, max_concepts=5)
    if response['status']['code'] == 10000:
        for concept in response['outputs'][0]['data']['concepts']:
            if concept['name'] == 'rhinoceros':
                image_has_rhino = True
    return image_has_rhino
    
if __name__ == "__main__":
    print(is_rhino('images/rhino_not.jpg'))