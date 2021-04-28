import youtube_dl

class CTube:

    def __init__(self, url):
        self.url = url
        self.extractor = self.results('extractor')
        self.media_stream = {}

    def allOptions(self):
        ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})
        with ydl:
            result = ydl.extract_info(url=self.url,download=False)
            return result

    def results(self,option):
        ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})
        with ydl:
            result = ydl.extract_info(url=self.url,download=False)
            return result[option]
    
    def getDownloadUrlForYoutube(self, only_audio=False):
        video = self.results('formats')
        for i, stream in enumerate(video):
            if stream['height']==None and only_audio:
                # returns a list of audio urls
                self.media_stream[f'audio'] = stream['url']
            elif stream['height']!=None and only_audio==False:
                # returns a list of video urls
                self.media_stream[f'v{stream["height"]}'] = stream['url']
        return self.media_stream
    
    def getDownloadUrlForFacebook(self):
        try:
            video = self.results('formats')
            return video[-1]['url']
        except Exception as e:
            return e

          

if __name__ == "__main__":

    ct = CTube('https://www.facebook.com/ShareChatApp/videos/3930092723689373/')
    print(ct.results('title'))

    print("\n")
    print(ct.extractor)
    print(ct.getDownloadUrlForFacebook())
        
    
