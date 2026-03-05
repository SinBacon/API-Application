# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # This is a modified version of the previous code

    def print_hi(name):
        # Use a breakpoint in the code line below to debug your script.
        print(f'Hi, {name}')


    if __name__ == '__main__':
        import datetime
        from googleapiclient.discovery import build
        from googleapiclient.errors import HttpError
        import requests
        from translate import Translator
        import nltk
        import string
        import time

        nltk.download('averaged_perceptron_tagger')
        num = 0

        # 設定 API 金鑰
        API_KEY = 'AIzaSyARGhmvVSGZYNNjxeYq-gRYSQP7E6h5Sv8'

        # 建立 YouTube API 服務
        youtube = build('youtube', 'v3', developerKey=API_KEY)

        # 取得七天前的日期
        seven_days_ago = datetime.date.today() - datetime.timedelta(days=7)

        try:
            # 初始化變數
            videos = []
            next_page_token = None

            # 循環進行分頁查詢，直到沒有下一頁為止
            while True:
                # 執行搜尋影片的 API 呼叫
                response = youtube.search().list(
                    part='snippet',
                    q='美食',
                    type='video',
                    publishedAfter=f'{seven_days_ago}T00:00:00Z',
                    publishedBefore=f'{datetime.date.today()}T23:59:59Z',
                    maxResults=50,
                    pageToken=next_page_token
                ).execute()

                # 獲取搜尋結果中的影片資訊
                videos.extend(response['items'])

                # 檢查是否還有下一頁
                next_page_token = response.get('nextPageToken')
                if not next_page_token:
                    break

            print(f"過去七天有 {len(videos)} 個包含 '美食' 的影片：")

            # 初始化變數
            video_data = []
            video_ids = set()

            for video in videos:
                video_title = video['snippet']['title']
                video_id = video['id']['videoId']

                if video_id in video_ids:
                    continue

                video_ids.add(video_id)

                try:
                    # 執行影片資訊的 API 呼叫，獲取觀看次數
                    video_response = youtube.videos().list(
                        part='statistics',
                        id=video_id
                    ).execute()

                    if 'items' in video_response and len(video_response['items']) > 0:
                        view_count = int(video_response['items'][0]['statistics'].get('viewCount', 0))
                    else:
                        view_count = 0
                except KeyError:
                    view_count = 0

                video_data.append({
                    'title': video_title,
                    'videoId': video_id,
                    'viewCount': view_count
                })

            # 根據觀看次數進行排序
            sorted_videos = sorted(video_data, key=lambda x: x['viewCount'], reverse=True)

            print("觀看次數前 10 名的影片：")
            for i in range(10):
                video = sorted_videos[i]
                video_title = video['title']
                video_id = video['videoId']
                view_count = video['viewCount']
                print(f"{i + 1}. 影片標題：{video_title}，影片ID：{video_id}，觀看次數：{view_count}")


            def translate_sentence(sentence):
                translator = Translator(to_lang='en', from_lang='zh')
                translation = translator.translate(sentence)
                return translation


            def search_recipes_by_ingredient(ingredient):
                api_key = '51d858fc7d28434f98449c3d3ee6bd03'
                url = f'https://api.spoonacular.com/recipes/findByIngredients?apiKey={api_key}'

                payload = {
                    'ingredients': ingredient,
                    'number': 5  # Specify the number of recipes to return
                }

                response = requests.get(url, params=payload)
                if response.status_code == 200:
                    data = response.json()
                    recipes = [recipe['title'] for recipe in data]
                    return recipes
                else:
                    print('Error:', response.status_code)


            def extract_food_keywords(sentence):
                    tokens = nltk.word_tokenize(sentence)
                    food_keywords = []

                    for token in tokens:
                        if token.isalpha() and token not in string.punctuation:
                            tag = nltk.pos_tag([token])[0][1]
                            if tag.startswith('NN') and len(token) > 2 and not tag.startswith(
                                    'NNP') and not tag.startswith(
                                    'VB') and token.lower() != 'eat' and token.lower() != 'food':
                                recipes = search_recipes_by_ingredient(token)
                                time.sleep(1)
                                if recipes and token not in food_keywords:
                                    food_keywords.append(token)
                    return food_keywords


            print()
            print("前3名影片的食物相關詞彙和食譜：")
            for i in range(4):
                video = sorted_videos[i]
                video_title = video['title']
                view_count = video['viewCount']

                translated_sentence = translate_sentence(video_title)
                keywords = extract_food_keywords(translated_sentence)
                if keywords:
                    print(f"影片標題：{video_title}")
                    print("食物相關詞彙:", keywords)
                    print("觀看次數:", view_count)
                    print("相關食譜：")
                    for keyword in keywords:
                        recipes = search_recipes_by_ingredient(keyword)
                        if recipes:
                            for recipe in recipes:
                                print(recipe)
                    print()

        except HttpError as e:
            print(f"發生錯誤：{e}")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
