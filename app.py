from flask import Flask, render_template, request, jsonify
from c_tube import CTube
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        recieved_url = request.form['video_url']
        recieved_filetype = request.form['options']
        url = ''
        ct = CTube(recieved_url)
        thumbnail = 'not available'
        if recieved_filetype == 'Video':
            t = ct.getDownloadUrlForYoutube()
            try:
                url = t['v720']
                return render_template('index.html', thumbnail=thumbnail, url=url)
            except:
                url = t['v360']
                return render_template('index.html', thumbnail=thumbnail, url=url)
        elif recieved_filetype == 'Audio':
            t = ct.getDownloadUrlForYoutube(only_audio=True)
            url = t['audio']
            return render_template('index.html',thumbnail=thumbnail, url=url)
        else:
            return "Pls choose valid type"
    else:
       return render_template('index.html',url='')

@app.route('/tags', methods=['GET','POST'])
def tags():
    if request.method == 'POST':
        rcvd_url = request.form['video_url']
        ct = CTube(rcvd_url)
        res = ct.results('tags')
        return render_template('tags.html',tags=res)
    else:
        return render_template('tags.html',tags=['empty'])

@app.route('/api', methods=['POST'])
def api():
    data = request.get_json()
    ct = CTube(data['url'])
    extractor = ct.extractor
    title = ct.results('title')

    if data['type'] == 'Video':
        # for Youtube
        if(extractor=="youtube"):
            try:
                t = ct.getDownloadUrlForYoutube()
                url = t['v720']
                return jsonify({'url':url, 'title':f"{title}.mp4"})
            except:
                t = ct.getDownloadUrlForYoutube()
                url = t['v360']
                return jsonify({'url':url, 'title':f"{title}.mp4"})
        elif(extractor=="facebook"):
            print(extractor)
            url = ct.getDownloadUrlForFacebook()
            # print(url)
            # return jsonify({'url':'not......'})
            return jsonify({'url':url, 'title':title + '.mp4'})
    elif data['type'] == 'Audio':
        try:
            t = ct.getDownloadUrlForYoutube(only_audio=True)
            url = t['audio']
            return jsonify({'url':url, 'title':f"{title}.mp3"})
        except:
            return jsonify({'message':'(:something went wrong'})
    else:
        return jsonify({'error':'Something went wrong'})

        
@app.route('/api/tags', methods=['POST'])
def api_tags():
    rcvd_url = request.get_json()
    ct = CTube(rcvd_url['url'])
    res = ct.results('tag')
    return jsonify({'tags':res})   

if __name__ == "__main__":
    app.run(host='0.0.0.0')
