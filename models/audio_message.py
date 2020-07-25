import librosa
from models import check_user as chu
import ssl
import urllib.request
from postgres_command import command as cd
from env import environment


class AudioMessage:

    def __init__(self):
        self.cd = cd.Command()
        self.chu = chu.CheckUser()
        self.env = environment.Environment().get_env()

    def decode_audio(self, filepath, user_id, **input_kwargs):
        print('decode_audio')
        print(filepath)
        temp = '../storage/temp.oga'
        file_name = 'storage/audio_message_' + filepath.split('/')[-1].split('.')[0] + '.wav'
        ssl._create_default_https_context = ssl._create_unverified_context
        urllib.request.urlretrieve(filepath, temp)
        y, s = librosa.load(temp, sr=int(self.env['SAMPLERATE']))
        # y, s = librosa.load(temp, sr=16000)
        write_wav = librosa.output.write_wav('./' + file_name, y, s)

        # if we don't have this user, we will add it.
        self.chu.check_user_exist(user_id)

        add_audio = ['audio', file_name, user_id]
        self.cd.run_command(add_audio)
        print(write_wav)

    def audio(self, update, type):
        print('Voice Message or Audio File')
        # file = update.message.voice.get_file().download_as_bytearray()
        print(update.message)
        user_id = update.message.chat.id
        if type == 'voice_message':
            file_path = update.message.voice.get_file()['file_path']
        else:
            file_path = update.message.audio.get_file()['file_path']
        self.decode_audio(file_path, user_id)
