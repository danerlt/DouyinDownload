#!/usr/bin/env python  
# -*- coding:utf-8 -*-
from douyin.controller import get_redirect_url, get_video_url


def test_get_long_url():
    url = "https://v.douyin.com/JmynAX6/"
    long_url = get_redirect_url(url)
    print(long_url)


def test_get_video_url():
    url = "https://v.douyin.com/JmynAX6/"
    long_url = get_redirect_url(url)
    video_url = get_video_url(long_url)
    print(video_url)


if __name__ == '__main__':
    # test_get_long_url()
    test_get_video_url()
