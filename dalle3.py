# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 13:51:45 2023

@author: ming
"""

# import cv2 as cv
import random
import os
import re
import requests
import openai

openai.api_base = 'http://openai-proxy.diandian.info/v1'
openai.api_key = 'wuming.cli'

def auto_save_file(path):
    directory, file_name = os.path.split(path)
    while os.path.isfile(path):
        pattern = '(\d+)\)\.'
        if re.search(pattern, file_name) is None:
            file_name = file_name.replace('.', '(0).')
        else:
            current_number = int(re.findall(pattern, file_name)[-1])
            new_number = current_number + 1
            file_name = file_name.replace(f'({current_number}).', f'({new_number}).')
        path = os.path.join(directory + os.sep + file_name)
    return path, file_name

def generateByDalle3(pic_prompt):
    
    response = openai.Image.create(
      model="dall-e-3",
      prompt=pic_prompt,
      size="1024x1792",
      quality="standard",
      n=1,
    )
    image_url = response.data[0].url
    actual_prompt = response.data[0].revised_prompt
    return image_url, actual_prompt


elements = ['fire', 'water', 'earth', 'wind', 'steam', 'lava', 'firestorm', 'mud', 'waves', 'dust']
# elements = ['phoenix', 'wildfire']
for element in elements:
    img_title = element
    pic_prompt = 'imagery of ' + element + ', Legends of Runeterra style, epic illusion by Noami, concept art, full landscape, no human, no card frame, no text'

    for i in range(3):
        seed = random.random()
        extra = ', generate with seed of ' + str(seed)
        pic_prompt += extra
        
        save_path = r'D:/wuming/dalle3 pic/'
        prompt_file = save_path + 'prompt.txt'
        pic_file = save_path + img_title +'.png'
        
        img, actual_prompt= generateByDalle3(pic_prompt)
        print(img)
        path, file_name = auto_save_file(pic_file)
        with open(path, 'wb') as file_obj:
            file_obj.write(requests.get(img).content)
        with open(prompt_file, 'a') as f:
            f.write('\n' + file_name + ' :\n' 
                    + 'seed:' + str(seed) +'\n'
                    + 'prompt: ' + pic_prompt + '\n'
                    + 'actual prompt: ' + actual_prompt + '\n')