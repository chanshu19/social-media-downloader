import youtube_dl

class CTube:

    def __init__(self, url):
        self.url = url
        self.extractor = self.results('extractor')
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
    
    def getDownloadUrlForYoutube(self):
        streams = self.results('formats')
        title = self.results('title')
        filtered_stream = []
        verbose = True
        for stream in streams:
            if stream['height']!='none' and stream['vcodec']=='none' and verbose:
                video_stream = {
                'title':title + ".mp4",
                'url':stream['url'],
                'height':stream['height']
                }
                filtered_stream.append(video_stream)
                verbose = False
                # print(f" * {stream['filesize']} , {stream['height']}, {stream['acodec']}, {stream['vcodec']}, {stream['ext']} ,{stream['url']}")
                
            elif stream['height']!='none' and stream['vcodec']!='none' and stream['acodec']!='none':
                audio_stream = {
                'title':title + ".mp3",
                'url':stream['url'],
                'height':stream['height'],
                'ext':stream['ext']
                }
                filtered_stream.append(audio_stream)
        return filtered_stream
    
    def getDownloadUrlForFacebook(self):
        try:
            video = self.results('formats')
            return video[-1]['url']
        except Exception as e:
            return e

          

if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=aS4slsNv89A"
    ct = CTube(url)
    # print(ct.results('title'))
    print("\n")
    # print(ct.extractor)
    # print(ct.results('thumbnail'))
    print(ct.getDownloadUrlForYoutube())

        
    
