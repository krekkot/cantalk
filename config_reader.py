from pydantic_settings import BaseSettings
from pydantic import SecretStr

class Settings(BaseSettings):
    bot_token: SecretStr

config = Settings(bot_token="6337428893:AAFFWOQRUTi-3U_FVM_TE4Izz-VJpRuH6ws")
payment_token ='1661751239:TEST:730B-zL4k-deSl-n1xK'