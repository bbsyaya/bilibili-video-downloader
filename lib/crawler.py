# coding: utf8

import os
import re
import time
import pycurl
import json
from StringIO import StringIO
import xml.etree.cElementTree as ET

# 伪装成iPad客户端
user_agent = 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10' \
             ' (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10'

# 伪造来源地址
refer_path = "http://www.bilibili.com"

# 匹配地址
_VALID_URL = r'https?://www\.bilibili\.(?:tv|com)/video/av(?P<id>\d+)(?:/index_(?P<page_num>\d+).html)?'

# 缓冲时间 (单位: 秒)
_TIME_DELTA = 10


def get_dlinks(source_url):
    """
    根据网页url图片的下载链接
    :param source_url: 原地址
    :return 返回图片的真实下载链接
    """
    # 负责拿到总页数
    result = []
    mobj = re.match(_VALID_URL, source_url)
    video_id = mobj.group('id')
    page_num = mobj.group('page_num') or '1'

    _json_url = 'http://api.bilibili.com/view?type=json&appkey=8e9fc618fbd41e28&id=%s&page=%s' % (video_id, page_num)
    curl = pycurl.Curl()
    curl.setopt(pycurl.USERAGENT, user_agent)
    curl.setopt(pycurl.REFERER, refer_path)

    # 获取str类型的数据
    buffers = StringIO()
    target_url = _json_url
    curl.setopt(pycurl.URL, target_url)
    curl.setopt(pycurl.WRITEDATA, buffers)
    curl.perform()
    body = buffers.getvalue()
    buffers.close()
    view_data = json.loads(body)
    total_pages = view_data['pages'] or 0
    # print total_pages
    for i in xrange(0, total_pages):
        _json_url = 'http://api.bilibili.com/view?type=json&appkey=8e9fc618fbd41e28&id=%s&page=%s' % (video_id, i + 1)
        buffers = StringIO()
        target_url = _json_url
        curl.setopt(pycurl.URL, target_url)
        curl.setopt(pycurl.WRITEDATA, buffers)
        curl.perform()
        body = buffers.getvalue()
        buffers.close()
        view_data = json.loads(body)
        cid = view_data['cid']
        title = view_data['title']
        # print title, cid, i+1
        _xml_url = 'http://interface.bilibili.com/v_cdn_play?appkey=8e9fc618fbd41e28&cid=%s' % cid
        target_url = _xml_url
        buffers = StringIO()
        curl.setopt(pycurl.URL, target_url)
        curl.setopt(pycurl.WRITEDATA, buffers)
        curl.perform()

        body = buffers.getvalue()
        buffers.close()

        doc = ET.fromstring(body)
        entries = []

        for durl in doc.findall('./durl'):
            # size = durl.find('./size').text
            # formats = [
            #     durl.find('./url').text
            #     # 'url': durl.find('./url').text,
            #     # 'filesize': size,
            #     # 'ext': 'flv',
            # ]
            formats = durl.find('./url').text

            # backup_urls = durl.find('./backup_url')
            # if backup_urls:
            #     for backup_url in backup_urls.findall('./url'):
            #         formats.append({'url': backup_url.text})
            # formats.reverse()

            entries.append({
                # 'id': '%s_part%s' % (cid, durl.find('./order').text),
                'title': title + str(i + 1),
                # 'duration': durl.find('./length').text,
                'formats': formats,
            })

        info = {
            # 'id': cid,
            'title': title + str(i + 1),
            # 'description': view_data.get('description'),
            # 'thumbnail': view_data.get('pic'),
            # 'uploader': view_data.get('author'),
            # 'timestamp': view_data.get('created'),
            # 'view_count': view_data.get('play'),
            # 'duration': doc.find('./timelength').text
        }

        if len(entries) == 1:
            entries[0].update(info)
            result.append(tuple(entries[0].values()))
        else:
            info.update({
                '_type': 'multi_video',
                # 'id': video_id,
                'entries': entries,
            })

            result.append(tuple(info.values()))
        time.sleep(_TIME_DELTA)
        if i == 10:
            break
    curl.close()

    return result


def save_to_file(d_links, file_name):
    """
    将图片链接存入文件
    :param d_links: 图片真实下载链接
    :param :file_name: 文件名
    :return
    """
    try:
        if not d_links:
            return
        base_dir = 'out/'
        if not os.path.exists(base_dir):
            os.mkdir(base_dir)
        file_object = open(base_dir + file_name, 'a')

        for item in d_links:
            file_object.write('\t'.join(item).encode('utf8'))
            file_object.write('\n')
        file_object.close()
    except IOError:
        print 'file not exist!'
        exit()


