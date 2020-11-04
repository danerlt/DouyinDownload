#!/usr/bin/env python  
# -*- coding:utf-8 -*-
import json
import logging
import os
import re

import requests
from flask import request, jsonify

from common import app

headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
}

logger = logging.getLogger(__name__)


def get_redirect_url(url):
    """链接获取重定向URL

    """
    try:
        res = requests.get(url=url, headers=headers)
        long_url = res.url
        return long_url
    except Exception as e:
        msg = f"获取重定向URL失败,url: {url}, error:%s " % str(e)
        logger.error(msg)
        raise Exception(msg)


def get_video_url(long_url, ratio="1080p"):
    """抖音长链接获取无水印视频链接

    :param long_url: 长链接 s.g: 'https://www.iesdouyin.com/share/video/6890908972346395918/?region=CN&mid=6890909915394984712&u_code=103219k33&titleType=title&did=3773171932861495&iid=34815435868088&utm_source=copy_link&utm_campaign=client_share&utm_medium=android&app=aweme'
    :param ratio 视频分辨率 默认 1080p
    :return: 无水印视频链接
    :rtype:
    """
    re_video_id = r"video/(\d+)/"
    search_obj = re.search(re_video_id, long_url)
    if search_obj:
        video_id = search_obj.group(1)
        # API 接口: "https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=6890908972346395918"
        api = f"https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={video_id}"
        res = requests.get(api, headers=headers).json()
        item_list = res["item_list"]
        for item in item_list:
            video = item["video"]
            play_addr = video["play_addr"]
            uri = play_addr["uri"]
            video_url = f"https://aweme.snssdk.com/aweme/v1/play/?video_id={uri}&ratio={ratio}&line=0"
            real_video_url = get_redirect_url(video_url)
            return real_video_url
    else:
        raise Exception(f"提取视频ID失败, url: {long_url}")


@app.route("/convert", methods=["POST"])
def convert():
    try:
        data = json.loads(request.data.decode())
        text = data.get("text")
        if not text:
            raise Exception("text不能空")
        logger.info(f"convert text: {text}")
        s = re.search(r"(http.*/)", text)
        if s is None:
            raise Exception("从text中提取短链接失败")
        else:
            short_url = s.group(1)
            rediect_url = get_redirect_url(short_url)
            video_url = get_video_url(rediect_url)
            return jsonify(status="ok", msg="ok", data=video_url)
    except Exception as e:
        logger.error("convert error: %s" % str(e))
        return jsonify(status="error", msg=str(e))


@app.route('/', methods=["GET"])
def index():
    from flask import Response
    root_dir = os.path.dirname(os.path.abspath(__file__))
    index_path = os.path.join(root_dir, "templates", "index.html")
    print(index_path)
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()
        return Response(content, mimetype="text/html")
