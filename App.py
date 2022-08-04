
from flask import Flask
from youtube_transcript_api import YouTubeTranscriptApi
from flask import request
from transformers import pipeline
import validators
from flask_cors import CORS



app = Flask(__name__)
CORS(app)




@app.route('/api/summarize', methods=['GET'])
def get_transcript():
    print("Request generated...")
    print(request)
    youtube_url = request.args.get('youtube_url', '')
    print(youtube_url)
    #validate the url
    valid=validators.url(youtube_url)
    if valid==False:
        return "No response, pls check the url :)"

    try:
        video_id = youtube_url.split('?')[1].split('=')[1]
    except:
        return "No response, pls check the url :)" 
    
    
    YouTubeTranscriptApi.get_transcript(video_id)
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    result = ""
    for i in transcript:
        result += ' ' + i['text']

    summarizer = pipeline('summarization')

    num_iters = int(len(result)/1000)
    summarized_text = []
    for i in range(0, num_iters + 1):
        start = 0
        start = i * 1000
        end = (i + 1) * 1000
        out = summarizer(result[start:end])
        out = out[0]
        out = out['summary_text']
        summarized_text.append(out)
    return str(summarized_text)
     


if __name__ == '__main__':
    app.run(debug=True)