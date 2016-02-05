#coding=utf-8

import requests
import cPickle
import hashlib
import time


def load_post_links():
    with open('../data/links.pickle', 'rb') as f:
        links = cPickle.load(f)

    return links


def crawl_all_posts():
    links = load_post_links()

    for each_link in links[:]:
        print each_link
        r = requests.get(each_link)

        file_name = hashlib.md5(each_link).hexdigest()
        with open('../data/posts/' + file_name + '.html', 'w') as f:
            f.write(r.text.encode('utf-8'))

        time.sleep(3)

    return


if __name__ == '__main__':
    crawl_all_posts()