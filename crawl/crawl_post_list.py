#coding=utf-8

import requests
from lxml import html
import cPickle
import time

origin_url = 'http://drops.wooyun.org/'


def crawl_all_post_links():
    """
    抓取 wooyun drops 上面的所有文章链接
    :return: 
    """
    crawl_flag = True
    page_num = 1
    link_list = []
    while crawl_flag:
        crawl_url = origin_url + 'page/' + str(page_num)
        print crawl_url
        r = requests.get(crawl_url)
        content = r.text.encode('utf-8')

        if len(content) < 1000:
            crawl_flag = False

        each_page_links = parse_links(content)
        if not each_page_links:
            break
        else:
            link_list += each_page_links

        page_num += 1
        time.sleep(5)

    with open('../data/links.pickle', 'wb') as f:
        cPickle.dump(link_list, f)

    return


def parse_links(content):
    """
    利用 lxml 解析文章链接,返回该页面中所有文章的链接
    :parameter:content
    :return:link list
    """

    each_page_link = []
    try:
        ele = html.fromstring(content)
    except Exception, e:
        print 'parse links failed, error: %s' % str(e)
        return each_page_link

    try:
        link_ele_list = ele.find_class('entry-title')
        each_page_link = [str(each_ele.xpath('a/@href')[0]) for each_ele in link_ele_list]
    except Exception, e:
        print 'parse links failed, error : %s' % str(e)

    return each_page_link


if __name__ == '__main__':
    crawl_all_post_links()
