from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, time
import pandas as pd
from threading import Thread
import requests
import re
from random import random


# choose a driver
wd = webdriver.Chrome()
# specify the the wait time for a new page to be fully loaded
wait_time_for_loading = 1
ytv_list = []
links_titles = []


def crawl_page(url):
    wd.get(url)


def find_class_name(cname, plural=False):
    if plural is False:
        return wd.find_element_by_class_name(cname)
    else:
        return wd.find_elements_by_class_name(cname)


def get_text_by_class_name(cname, plural=False):
    if plural is False:
        return find_class_name(cname).text
    else:
        texts = [t.text for t in find_class_name(cname, True)]
        return texts


def get_tar_txt(regex, src_txt):
    text = re.findall(rf'{regex}', src_txt)
    if len(text) != 0:
        text = text[0] if len(text) == 1 or text[0] != text[-1] else text[1]
    else:
        text = ""
    return text


def get_digits(strg):
    num = ''.join(s for s in strg if s.isdigit())
    if len(num) != 0:
        return float(num)
    else:
        return 0


def multi_tasking(func, a_list, length, speed):
    threads = []
    for i in range(0, length, speed):
        t = Thread(target=func, args=(a_list[i:i+speed if length - speed else length],))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()


def channel_info():
    sleep(wait_time_for_loading)
    channel_name = get_text_by_class_name('style-scope ytd-channel-name')
    sub_num = wd.find_element_by_xpath('//*[@id="subscriber-count"]').text
    return channel_name, sub_num


def scroll_down(scrolling_limit=50):
    videos = find_class_name('style-scope ytd-grid-video-renderer', True)
    counter = 0
    while True:
        wd.find_element_by_tag_name('body').send_keys(Keys.END)
        sleep(wait_time_for_loading)
        videos_new = find_class_name('style-scope ytd-grid-video-renderer', True)
        counter += 1
        if len(videos) != len(videos_new) and counter != scrolling_limit:
            videos = videos_new
            print("Scrolling..." if random() > 0.5 else "..........")
        else:
            break


def get_links_titles(videos_):
    for video in videos_:
        v_info = video.find_element_by_xpath('.//*[@id="video-title"]')
        link = v_info.get_attribute('href')
        title = v_info.text
        links_titles.append([link, title])
    print("Processing..." if random() > 0.5 else "..........")


def get_videos_info(links_titles_):
    for link_title in links_titles_:
        link = link_title[0]
        title = link_title[1]
        r = requests.get(link)
        when = get_tar_txt('[A-Z][a-z]{2} \d{1,}, [\d]{4}', r.text)
        views = get_digits(get_tar_txt('(?<="viewCount":{"simpleText":")[\d,]+(?= views)', r.text))
        likes = get_digits(get_tar_txt('[\d,]+(?= likes)', r.text))
        dislikes = get_digits(get_tar_txt('[\d,]+(?= dislikes)', r.text))
        ratio = "" if dislikes == 0 else likes / dislikes
        ytv_list.append([title, when, views, likes, dislikes, (likes - dislikes), ratio, link])
    print("Processing..." if random() > 0.5 else "..........")


def get_links():
    links = [l[-1] for l in ytv_list[1:]]
    return links


def get_views():
    views = [v[2] for v in ytv_list[1:]]
    return views


def run(url_):
    global links_titles, ytv_list
    start = time()
    links_titles = []
    ytv_list = [['Title', 'Posted on', 'Views', 'Likes', 'Dislikes', 'Difference(L-D)', 'Ratio(L/D)', 'Link']]
    crawl_page(url_)
    ch_info = channel_info()
    filename = f'{ch_info[0]}({ch_info[1]}).xlsx'
    scroll_down(1)
    videos = find_class_name('style-scope ytd-grid-video-renderer', True)
    multi_tasking(get_links_titles, videos, len(videos), 100)
    print('Creating file....')
    multi_tasking(get_videos_info, links_titles, len(links_titles), 20)
    pd.DataFrame(ytv_list).to_excel(filename)
    print(f'File {filename} created!')
    end = time()
    print("Total time taken: " + str((end-start)))


def quit_out():
    wd.quit()


def main():
    urls = ["A list of links to YouTube Channels' VIDEOS webpage..."]
    for url in urls:
        try:
            run(url)
        except:
            continue
    quit_out()


if __name__ == '__main__':
    main()

