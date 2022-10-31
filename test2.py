from gtts import gTTS

amh = "selam"
obj = gTTS(text = amh, slow= False, lang = 'am')
obj.save('amh.mp3')
