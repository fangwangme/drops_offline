#coding=utf-8

import html2text
import requests
import shutil
import glob
import sys
import re
import os
from lxml import html
import cPickle
import time

reload(sys)
sys.setdefaultencoding('utf-8')


def get_post_list():
    file_list = glob.glob('../data/posts/*.html')

    return file_list


def generate_all_post():
    file_list = get_post_list()

    post_infos = []

    md_path = '../data/markdown/'
    if not os.path.exists(md_path):
        os.makedirs(md_path)

    for each_file in file_list:
        with open(each_file) as f:
            content = f.read()

        file_name = each_file[each_file.rfind('/')+1:each_file.rfind('.')]
        each_post_infos = parse_post_info(content)
        post_infos.append((file_name, each_post_infos[0], each_post_infos[1],
                           each_post_infos[2]))
        temp_md_content = html2text.html2text(content.decode('utf-8'))
        del content

        start_pos = temp_md_content.find('乌云知识库') + len('乌云知识库') - 2
        end_pos = temp_md_content.find('[ __收藏 ]')
        temp_md_content = temp_md_content[start_pos:end_pos]
        md_content = fix_image_path(temp_md_content)

        with open(md_path + file_name + '.md', 'w') as f:
            f.write(md_content)

        time.sleep(5)

    with open('../data/post_info.pickle', 'wb') as f:
        cPickle.dump(post_infos, f)


def parse_post_info(content):
    """
    解析文章的基本信息:
    1. 标题
    2. 所属类别
    3. 发布时间
    :return:
    """

    title = 'NULL'
    catalog = 'NULL'
    post_time = 'NULL'

    try:
        ele = html.fromstring(content)
        title = ele.find_class('entry-title ng-binding')[0].text.encode('utf-8')
        meta_ele = ele.find_class('entry-meta')[0]
        post_time = meta_ele.xpath('time/@title')[0]

    except Exception, e:
        pass

    return str(title), str(catalog), str(post_time)


def fix_image_path(md_content):
    """
    1. 抓取文章中出现的图片,将其保存在本地
    2. 替换 markdown 中的图片路径
    :param md_content:
    :return new_md_content
    """

    img_pat = re.compile(r'!\[.*?\((.*?)\)', re.S)
    img_list = img_pat.findall(md_content)

    png_path = '../data/png/'
    if not os.path.exists(png_path):
        os.makedirs(png_path)

    for each_img_url in img_list:
        new_img_url = each_img_url.strip().replace('\n','').replace('\r','')
        png_file_name = new_img_url.split('/')[-1]
        r = requests.get(new_img_url, stream=True)

        with open(png_path + png_file_name, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

        md_content = md_content.replace(each_img_url, '../png/' + png_file_name)

    return md_content


if __name__ == '__main__':
    generate_all_post()
