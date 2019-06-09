import os
from urllib.parse import unquote
from helpers import Encoder
from gtts import gTTS


class GttsService:
    config = {}

    def __init__(self, settings):
        self.config = settings

    def text_handler(self, text, limit=20):
        # 字元限制
        text = text[0:limit]
        return text

    def auto_choice_lang(self, text: str) -> str:
        # 字串預處理判斷
        text = unquote(text)
        text = text.replace(" ", "")

        # 全英文時使用英文
        if text.encode('UTF-8').isalpha():
            return 'en'

        # 無法判斷時使用中文
        return 'zh-tw'

    def get_file(self, text, lang=''):

        lang = lang and lang or self.auto_choice_lang(text)
        text = self.text_handler(text)

        tts = gTTS(text=text, lang=lang)

        # 檔名轉 md5
        text_encoded = Encoder.to_md5(text)
        filename = '{}.mp3'.format(text_encoded)

        path = self.config['PROJECT']['STORAGES_VOICE']
        voice_path = os.path.join(path, filename)

        # 存在則直接返回
        if os.path.exists(voice_path):
            return voice_path

        # 不存在則寫入後回傳
        tts.save(voice_path)
        return voice_path
