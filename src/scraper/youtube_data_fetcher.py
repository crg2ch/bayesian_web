import os
import argparse
import pandas as pd
from googleapiclient.discovery import build
from dotenv import load_dotenv

def fetch_youtube_data(file_path, channel_id='UCee1MvXr6E8qC_d2WEYTU5g', maxResults=100):
   load_dotenv()
   api_key = os.getenv('YOUTUBE_API_KEY')

   youtube = build('youtube', 'v3', developerKey=api_key)

   ids=[]
   titles=[]
   descriptions=[]
   thumbnails=[]

   request = youtube.search().list(
       part='snippet',
       channelId=channel_id,
       type='video',
       maxResults=min(maxResults, 50),  # 첫 번째 요청에서 최대 50개의 결과 가져오기
       videoDuration='medium'
   )

   response = request.execute()

   for item in response['items']:
       ids.append(item['id']['videoId'])
       titles.append(item['snippet']['title'])
       descriptions.append(item['snippet']['description'])
       thumbnails.append(item['snippet']['thumbnails']['high']['url'])
  
   # 다음 페이지에서 추가적인 결과 가져오기
   while len(ids) < maxResults and 'nextPageToken' in response:
       next_page_token = response['nextPageToken']

       request = youtube.search().list(
           part='snippet',
           channelId=channel_id,
           type='video',
           maxResults=min(maxResults - len(ids), 50),  # 남은 결과 수만큼 가져오기
           videoDuration='medium',
           pageToken=next_page_token
       )

       response = request.execute()       
      
       for item in response['items']:
           ids.append(item['id']['videoId'])
           titles.append(item['snippet']['title'])
           descriptions.append(item['snippet']['description'])
           thumbnails.append(item['snippet']['thumbnails']['high']['url'])
  
   # DataFrame 생성 후 CSV 파일로 저장
   data = {'video_id': ids, 'video_title': titles, 'video_description': descriptions, 'video_thumbnail': thumbnails}
   df = pd.DataFrame(data)
   df.to_csv(file_path, sep='\t', index=False)

if __name__ == '__main__':
   parser = argparse.ArgumentParser(description='fetch_youtube_data 파라미터')
   parser.add_argument('--file_path', dest='arg1', type=str, help='저장할 파일 경로')
   parser.add_argument('--channel_id', dest='arg2', type=str, help='유튜브 채널 아이디')
   parser.add_argument('--maxResults', dest='arg3', type=int, help='불러올 아이템 개수')
   args = parser.parse_args()

   # 파라미터 검증 및 기본값 설정
   file_path = args.arg1 if args.arg1 else os.path.join(os.path.dirname(__file__), '..', 'data', 'youtube_data.tsv')
   channel_id = args.arg2 if args.arg2 else 'UCee1MvXr6E8qC_d2WEYTU5g'
   maxResults = args.arg3 if args.arg3 else 100

   print('run fetch_youtube_data...')
   print('file_path:', file_path)
   fetch_youtube_data(file_path, channel_id, maxResults)
   print('fetch_youtube_data has been completed.')