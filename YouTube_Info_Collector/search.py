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
wait_time_for_loading = 5
links_titles = []
ytv_info = []
yt_channel_v_links =[]


def crawl_page(url):
    wd.get(url)


def converter_to_url(query_):
    fma = 'https://www.youtube.com/results?search_query={}'
    return fma.format('+'.join(q for q in query_.split(' ')))


def get_tar_txt(regex, src_txt):
    text = re.findall(rf'{regex}', src_txt)
    if len(text) != 0:
        text = text[0]
        # text = text[0] if len(text) == 1 or text[0] != text[-1] else text[1]
    else:
        text = ""
    return text


def get_digits(strg):
    if len(strg) != 0:
        if strg.endswith(('K', 'k')):
            num = float(strg[:-1]) * 1000
        elif strg.endswith(('M', 'm')):
            num = float(strg[:-1]) * 1000000
        else:
            num = float(''.join(s for s in strg if s.isdigit()))
        return num
    else:
        return ''


def multi_tasking(func, a_list, length, speed):
    threads = []
    for i in range(0, length, speed):
        t = Thread(target=func, args=(a_list[i:i+speed if length - speed else length],))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()


def scroll_down(scrolling_limit=30):
    sleep(wait_time_for_loading)
    videos = wd.find_elements_by_xpath('//*[@id="video-title"]')
    # set a counter to avoid long time crawling
    counter = 0
    while True:
        wd.find_element_by_tag_name('body').send_keys(Keys.END)  # Scroll down to the bottom
        print("Scrolling..." if random() > 0.5 else "..........")
        sleep(wait_time_for_loading)
        videos_new = wd.find_elements_by_xpath('//*[@id="video-title"]')
        counter += 1
        if len(videos) != len(videos_new) and counter != scrolling_limit:
            videos = videos_new
        else:
            break


def get_links_titles(videos_):
    for video in videos_:
        try:
            link = video.get_attribute('href')
            if link is not None:
                title = video.text
                links_titles.append([link, title])
        except:
            continue
    print("Processing..." if random() > 0.5 else "..........")
    return links_titles


def get_videos_info(links_titles_):
    for link_title in links_titles_:
        link = link_title[0]
        title = link_title[1]
        r = requests.get(link)
        when = get_tar_txt('[A-Z][a-z]{2} \d{1,}, [\d]{4}', r.text)
        views = get_digits(get_tar_txt('(?<="viewCount":{"simpleText":")[\d,]+(?= views)', r.text))
        likes = get_digits(get_tar_txt('[\d,]+(?= likes)', r.text))
        dislikes = get_digits(get_tar_txt('[\d,]+(?= dislikes)', r.text))
        difference = likes - dislikes if dislikes != '' else likes
        ratio = "" if dislikes == '' else likes/dislikes
        youtuber = get_tar_txt('(?<=ChannelName\":\")[^"]+', r.text)
        num_sub = get_digits(get_tar_txt('[\d.]+[KkMM]?(?= subscribers)', r.text))
        home_videos_page = 'https://www.youtube.com' + \
                           get_tar_txt('(?<=url":")/channel/[^"]+', r.text) + '/videos'
        ytv_info.append([title, when, views, likes, dislikes, difference, ratio,
                         youtuber, home_videos_page, num_sub, link])
        yt_channel_v_links.append(home_videos_page)
    print("Processing..." if random() > 0.5 else "..........")


def run(query):
    global links_titles, ytv_info, yt_channel_v_links
    start = time()
    url = converter_to_url(query)
    links_titles = []
    yt_channel_v_links = []
    ytv_info = [['Title', 'Posted on', 'Views', 'Likes', 'Dislikes', 'Difference(L-D)', 'Ratio(L/D)',
                 'Posted by', 'HOME_VIDEOS_PAGE_LINK', 'Subscribers','Video Link']]
    crawl_page(url)
    scroll_down(2)
    videos = wd.find_elements_by_xpath('//*[@id="video-title"]')
    multi_tasking(get_links_titles, videos, len(videos), 100)
    print("Collecting videos info...")
    multi_tasking(get_videos_info, links_titles, len(links_titles), 20)
    print('Creating file....')
    pd.DataFrame(ytv_info).to_excel(f'{query}.xlsx')
    print(f'File {query}.xlsx created!')
    end = time()
    print("Total time taken: " + str((end-start)))
    return links_titles, set(yt_channel_v_links)


def quit_out():
    wd.quit()


def main():
    queries = ['A list of queries...']
    for query in queries:
        try:
            run(query)
        except:
            continue
    quit_out()


if __name__ == '__main__':
    main()

