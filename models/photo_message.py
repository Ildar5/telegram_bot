import urllib.request
import requests
import cv2
import ssl
import numpy as np
from urllib.request import urlopen
from env import environment
from postgres_command import command
from models import check_user as chu


class PhotoMessage:

    def __init__(self):
        self.env = environment.Environment().get_env()
        self.cd = command.Command()
        self.chu = chu.CheckUser()

    def get_photo(self, file_id):
        print('get_photo')
        url = self.env['TELEGRAM_FILE_URL'].format(self.env['TELEGRAM_API_TOKEN'], file_id)
        request = requests.get(url, verify=False)
        if request.status_code == 200:
            print('Success')
            json = request.json()
            file_path = json['result']['file_path']
            image_url = self.env['TELEGRAM_IMAGE_URL'].format(self.env['TELEGRAM_API_TOKEN'], file_path)
            print('image_url')
            print(image_url)
            return [request.status_code, image_url]
        else:
            return [request.status_code, '']

    def url_to_image(self, url, readFlag=cv2.IMREAD_COLOR):
        resp = urlopen(url)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, readFlag)

        # return the image
        return image

    def image_recognition(self, image_url):
        print('image_recognition')
        print(image_url)
        # Load the cascade
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Open the input image from url
        ssl._create_default_https_context = ssl._create_unverified_context
        req = urlopen(image_url)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        img = cv2.imdecode(arr, -1)  # 'Load it as it is'
        # img = cv2.imread(image_url)

        # Convert into grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        if len(faces):
            return 1
        else:
            return 0

    def save_image(self, image_url, save_url):
        urllib.request.urlretrieve(image_url, save_url)

    def photo(self, update, type):
        if type == 'photo':
            file_id = update.message.photo[-1].file_id
        else:
            file_id = update.message.document.thumb.file_id

        user_id = update.message.chat.id
        image_url = self.get_photo(file_id)
        if image_url[0] == 200:
            check_image_recognition = self.image_recognition(image_url[1])
            if check_image_recognition == 1:
                print('Image Has Face/s')
                file_name = 'storage/photo_{0}.{1}'.format(file_id, image_url[1].split('.')[-1])
                save_url = './' + file_name
                self.save_image(image_url[1], save_url)
                self.chu.check_user_exist(user_id)
                add_image = ['image', file_name, user_id]
                self.cd.run_command(add_image)
            else:
                print('There Are No Face/s On The Photo')

        else:
            print('Problem with getting the image: {0}'.format(image_url[0]))
