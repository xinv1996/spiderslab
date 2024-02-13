# -*- coding:utf-8 -*-
# @project: SH4NH4I
# @software: PyCharm
# desc:

import datetime
import json
from loguru import logger as logging
import re
from json import load, dumps
from os import path
from re import findall

import pymongo
import requests
import scrapy
from pymongo.errors import DuplicateKeyError

cwd = path.dirname(path.abspath(__file__))


class VideoError(Exception):
    def __init__(self, vid):
        self.message = f'Invalid video ID. Are you sure "{vid}" is a valid URL?'
        super().__init__(self.message)


class PlaylistError(Exception):
    def __init__(self, pid):
        self.message = f'Invalid Playlist ID. Are you sure "{pid}" is a valid URL and available?'
        super().__init__(self.message)


def fetch_and_save_video_info():
    gMongoClient = pymongo.MongoClient()
    gMongoDb = gMongoClient['crawlers']
    gMongoCollection = gMongoDb['youtube']

    docs = gMongoCollection.find({})
    for doc in docs:
        videoId = doc['videoId']
        url = f"https://www.youtube.com/watch?v={videoId}"
        title = doc['title']
        shortViewCountText = doc['shortViewCountText']
        channelTitle = doc['channelTitle']
        channelId = doc['channelId']
        canonicalBaseUrl = doc['canonicalBaseUrl']
        subscriberCount = doc['subscriberCount']
        videosCount = doc['videosCount']
        headers = {
            'user-agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'),
            'referer': 'https://youtube.com'}

        vid = "".join([i for i in findall(r"v=(.*?)&|youtu.be\/(.*?)&", url + "&")[0]])
        logging.info(vid)
        json_file = load(open(cwd + "/tube_dl_config.json", "rb"))

        headers["x-youtube-client-version"] = json_file['cver']
        headers["x-youtube-client-name"] = json_file['cname']
        y_data = requests.get(url=f"https://youtube.com/watch?v={vid}&pbj=1", headers=headers,
                              ).json()
        yt_data = [i for i in y_data if "playerResponse" in i.keys()][0]["playerResponse"]
        if yt_data["playabilityStatus"]["status"] == "ERROR":
            raise VideoError(vid)

        shortDescription = yt_data['videoDetails']['shortDescription']
        logging.info(dumps(y_data))
        # logging.info(shortDescription)

        # "label": "102,293 likes"
        likes = re.findall('"defaultText": \{"accessibility": \{"accessibilityData": \{"label": "(.*?) likes"\}\}',
                           dumps(y_data))[0]
        try:
            if likes:
                # 格式化成数字
                likes = int(likes.replace(',', ''))
        except Exception as e:
            logging.info(e)
            likes = 0
        publishDate = yt_data['microformat']['playerMicroformatRenderer']['publishDate']  # 2023-11-04T16:00:11-07:00
        publishDateDay = publishDate.split('T')[0]  # 2023-11-04

        viewCount = re.findall('"allowRatings": true, "viewCount": "(.*?)",', dumps(y_data))[0]

        if '万 个视频' in videosCount:
            videosCount = videosCount.replace('万 个视频', '')
            videosCount = float(videosCount) * 10000
        if '万位订阅者' in subscriberCount:
            subscriberCount = subscriberCount.replace('万位订阅者', '')
            subscriberCount = float(subscriberCount) * 10000

        item = {
            'videoId': videoId,
            'title': title,
            'viewCount': viewCount,
            'channelTitle': channelTitle,
            'channelId': channelId,
            'canonicalBaseUrl': canonicalBaseUrl,
            'subscriberCount': subscriberCount,
            'videosCount': videosCount,
            'shortDescription': shortDescription,
            'likes': likes,
            'createTime': datetime.datetime.now(),
            'day': datetime.datetime.now().strftime('%Y-%m-%d'),
            "publishDate": publishDate,
            "publishDateDay": publishDateDay,
        }
        gMongoDb.get_collection('youtube_detail_info').insert_one(item)


def fetch_and_save_comments_info():
    gMongoClient = pymongo.MongoClient()
    gMongoDb = gMongoClient['crawlers']
    docs = gMongoDb.get_collection('youtube_detail_info').find({"commentsCount": {"$exists": False}})
    for doc in docs:
        url = f'https://www.youtube.com/watch?v={doc["videoId"]}'

        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'x-client-data': 'CIq2yQEIpbbJAQipncoBCLXsygEIk6HLAQia/swBCIagzQEIj+HNAQiE4s0BCN/rzQEI5uzNAQjB7s0BCIrvzQEIg/DNAQiG8M0BCL7xzQEIjPLNARj2yc0BGKfqzQEY+fLNAQ==',
            'sec-fetch-site': 'same-origin', 'sec-fetch-mode': 'navigate', 'sec-fetch-user': '?1',
            'Cookie': f"{cookie}",
            'sec-fetch-dest': 'document', 'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
        resp = requests.get(url=url, headers=headers)

        response = scrapy.Selector(text=resp.text)
        token = re.findall(r'"continuationCommand":{"token":"(.*?)"', resp.text)[0]

        apiKey = re.findall(r'"innertubeApiKey":"(.*?)"', resp.text)[0]

        url = f'https://www.youtube.com/youtubei/v1/next?key={apiKey}&prettylogging.info=false'

        payload = {
            "context": {"client": {"deviceMake": "Apple", "deviceModel": "", "visitorData": "", "clientName": "WEB",
                                   "clientVersion": "2.20240123.01.00", "configInfo": {"appInstallData": ""},
                                   "mainAppWebInfo": {"graftUrl": ""}}, "user": {"lockedSafetyMode": False},
                        "request": {"useSsl": True, "internalExperimentFlags": [], "consistencyTokenJars": []},
                        "clickTracking": {"clickTrackingParams": ""}, "adSignalsInfo": {"params": [], "bid": ""}},
            "continuation": f"{token}"}
        videoResp = requests.post(url=url, headers=headers, json=payload)
        videoRespJson = json.loads(videoResp.text)
        try:
            commentsCount = re.findall(r'"commentsCount":\{"runs":\[\{"text":"(.*?)"\}\]\}', videoResp.text)[0]
        except Exception as e:
            logging.info(e)
            commentsCount = 0

        gMongoDb.get_collection('youtube_detail_info').update_one({'_id': doc['_id']},
                                                                  {'$set': {'commentsCount': commentsCount}})


def get_video_list(token, channelTitle, channelId, canonicalBaseUrl, subscriberCount, videosCount, gMongoDb):
    videlListUrl = 'https://www.youtube.com/youtubei/v1/browse?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8&prettylogging.info=false'
    payload = {"context": {"client": {"deviceMake": "Apple", "deviceModel": "", "visitorData": "", "clientName": "WEB",
                                      "clientVersion": "2.20240123.01.00", "configInfo": {"appInstallData": ""},
                                      "mainAppWebInfo": {"graftUrl": ""}}, "user": {"lockedSafetyMode": False},
                           "request": {"useSsl": True, "internalExperimentFlags": [], "consistencyTokenJars": []},
                           "clickTracking": {"clickTrackingParams": ""}, "adSignalsInfo": {"params": [], "bid": ""}},
               "continuation": f"{token}"}

    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'x-client-data': 'CIq2yQEIpbbJAQipncoBCLXsygEIk6HLAQia/swBCIagzQEIj+HNAQiE4s0BCN/rzQEI5uzNAQjB7s0BCIrvzQEIg/DNAQiG8M0BCL7xzQEIjPLNARj2yc0BGKfqzQEY+fLNAQ==',
        'sec-fetch-site': 'same-origin', 'sec-fetch-mode': 'navigate', 'sec-fetch-user': '?1',
        'Cookie': f"{cookie}",
        'sec-fetch-dest': 'document', 'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    videoResp = requests.post(url=videlListUrl, headers=headers, json=payload, )
    videoRespJson = json.loads(videoResp.text)
    logging.info(videoResp.text)
    # .onResponseReceivedActions[0].appendContinuationItemsAction.continuationItems
    videoList = videoRespJson['onResponseReceivedActions'][0]['appendContinuationItemsAction']['continuationItems']
    for eVideo in videoList[:-1]:
        videoId = eVideo['richItemRenderer']['content']['videoRenderer']['videoId']
        title = eVideo['richItemRenderer']['content']['videoRenderer']['title']['runs'][0]['text']
        # richItemRenderer.content.videoRenderer.shortViewCountText.simpleText
        shortViewCountText = eVideo['richItemRenderer']['content']['videoRenderer']['shortViewCountText']['simpleText']
        item = {
            'videoId': videoId,
            'title': title,
            'shortViewCountText': shortViewCountText,
            'channelTitle': channelTitle,
            'channelId': channelId,
            'canonicalBaseUrl': canonicalBaseUrl,
            'subscriberCount': subscriberCount,
            'videosCount': videosCount,
        }
        logging.info(item)
        try:
            gMongoDb['youtube'].insert_one(item)
        except DuplicateKeyError as e:
            logging.info("重复数据")
    try:
        continuationCommand = videoList[-1]['continuationItemRenderer']['continuationEndpoint']['continuationCommand']
        token = continuationCommand['token']
        return get_video_list(token)
    except Exception as e:
        logging.info(e)
        logging.info('没有下一页了')


def fetch_and_save_list_info():
    gMongoClient = pymongo.MongoClient()
    gMongoDb = gMongoClient['crawlers']
    url = 'https://www.youtube.com/@ganfutong/videos'

    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'x-client-data': 'CIq2yQEIpbbJAQipncoBCLXsygEIk6HLAQia/swBCIagzQEIj+HNAQiE4s0BCN/rzQEI5uzNAQjB7s0BCIrvzQEIg/DNAQiG8M0BCL7xzQEIjPLNARj2yc0BGKfqzQEY+fLNAQ==',
        'sec-fetch-site': 'same-origin', 'sec-fetch-mode': 'navigate', 'sec-fetch-user': '?1',
        'Cookie': f"{cookie}",
        'sec-fetch-dest': 'document', 'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    resp = requests.get(url=url, headers=headers,
                        )

    response = scrapy.Selector(text=resp.text)
    token = re.findall(r'"continuationCommand":{"token":"(.*?)"', resp.text)[0]
    context = response.xpath("//script[contains(string(),'var ytInitialData')]/text()").extract_first()
    contextJson = json.loads(context.replace('var ytInitialData = ', '')[:-1])

    subscriberCount = contextJson['header']['c4TabbedHeaderRenderer']['subscriberCountText']['simpleText']
    videosCountTexts = contextJson['header']['c4TabbedHeaderRenderer']['videosCountText']['runs']
    channelTitle = contextJson['header']['c4TabbedHeaderRenderer']['title']
    channelId = contextJson['header']['c4TabbedHeaderRenderer']['channelId']
    canonicalBaseUrl = contextJson['header']['c4TabbedHeaderRenderer']['navigationEndpoint']['browseEndpoint'][
        'canonicalBaseUrl']
    videosCount = ''
    for i in videosCountTexts:
        videosCount += i['text']

    token = token
    logging.info(token)
    get_video_list(token, channelTitle, channelId, canonicalBaseUrl, subscriberCount, videosCount, gMongoDb)


def fetch_and_save_account_info():
    gMongoClient = pymongo.MongoClient()
    gMongoDb = gMongoClient['crawlers']
    url = 'https://www.youtube.com/@ganfutong'

    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'x-client-data': 'CIq2yQEIpbbJAQipncoBCLXsygEIk6HLAQia/swBCIagzQEIj+HNAQiE4s0BCN/rzQEI5uzNAQjB7s0BCIrvzQEIg/DNAQiG8M0BCL7xzQEIjPLNARj2yc0BGKfqzQEY+fLNAQ==',
        'Cookie': f"{cookie}",
        'sec-fetch-site': 'same-origin', 'sec-fetch-mode': 'navigate', 'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document', 'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    resp = requests.get(url=url, headers=headers)

    response = scrapy.Selector(text=resp.text)
    token = re.findall(r'"continuationCommand":{"token":"(.*?)"', resp.text)[0]
    context = response.xpath("//script[contains(string(),'var ytInitialData')]/text()").extract_first()
    contextJson = json.loads(context.replace('var ytInitialData = ', '')[:-1])

    # 订阅数.header.c4TabbedHeaderRenderer.subscriberCountText
    subscriberCount = contextJson['header']['c4TabbedHeaderRenderer']['subscriberCountText']['simpleText']
    # 视频数 .header.c4TabbedHeaderRenderer.videosCountText
    videosCountTexts = contextJson['header']['c4TabbedHeaderRenderer']['videosCountText']['runs']
    channelTitle = contextJson['header']['c4TabbedHeaderRenderer']['title']
    channelId = contextJson['header']['c4TabbedHeaderRenderer']['channelId']
    apiKey = re.findall(r'"innertubeApiKey":"(.*?)"', resp.text)[0]

    canonicalBaseUrl = contextJson['header']['c4TabbedHeaderRenderer']['navigationEndpoint']['browseEndpoint'][
        'canonicalBaseUrl']
    videosCount = ''
    for i in videosCountTexts:
        videosCount += i['text']
    logging.info(json.dumps(contextJson))
    gMongoDb.get_collection('youtube_account_info').insert_one(item := {
        'channelTitle': channelTitle,
        'channelId': channelId,
        'canonicalBaseUrl': canonicalBaseUrl,
        'subscriberCount': subscriberCount,
        'videosCount': videosCount,
        'apiKey': apiKey,
        "createTime": datetime.datetime.now(),
    })


if __name__ == '__main__':
    cookie = ''
    fetch_and_save_comments_info()
