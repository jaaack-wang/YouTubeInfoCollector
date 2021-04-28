from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, time, asctime
from random import random
import pandas as pd
from threading import Thread


# choose a driver
wd = webdriver.Chrome()
# specify the the wait time for a new page to be fully loaded
wait_time_for_loading = 6
coms_info = []


def crawl_page(url):
    wd.get(url)


def find_xpath(xpath, plural=False):
    if plural is False:
        return wd.find_element_by_xpath(xpath)
    else:
        return wd.find_elements_by_xpath(xpath)


def get_text_by_xpath(xpath, plural=False):
    if plural is False:
        return find_xpath(xpath).text
    else:
        texts = [t.text for t in find_xpath(xpath, True)]
        return texts


def get_num_comments():
    num_coms = get_text_by_xpath('//*[@id="count"]/yt-formatted-string').split(' ')[0]
    num_coms = ''.join(n for n in num_coms if n.isdigit())
    return float(num_coms)


def metadata(url):
    sleep(wait_time_for_loading)  # To allow the webpage to load
    # To scroll to a position where comments get loading
    wd.execute_script('window.scrollTo(0,400);')
    sleep(wait_time_for_loading)  # Making sure the first page of comments has been fully loaded
    title = get_text_by_xpath('//*[@id="container"]/h1/yt-formatted-string')
    when = get_text_by_xpath('//*[@id="date"]/yt-formatted-string')
    filename = f'{title}({when})'
    views = get_text_by_xpath('//*[@id="count"]/yt-view-count-renderer/span[1]').split(' ')[0]
    emos = wd.find_elements_by_tag_name('ytd-toggle-button-renderer')
    likes = emos[0].text
    dislikes = emos[1].text
    youtuber = get_text_by_xpath('//*[@id="text"]/a')
    num_subs = get_text_by_xpath('//*[@id="owner-sub-count"]').split(' ')[0]
    num_coms = get_num_comments()
    meta_data = [filename, [['VIEWS', 'LIKES', 'DISLIKES', 'LINK'],
                 [views, likes, dislikes, url],
                 ['#_COMMENTS', 'POSTED BY', 'SUBSCRIBERS','TIME CREATED'],
                 [num_coms, youtuber, num_subs, asctime()], ['', '', '', '']]]
    return meta_data


def scroll_down(scrolling_limit=50):
    coms = find_xpath('//*[@id="contents"]/ytd-comment-thread-renderer', True)
    # set a counter to avoid long time crawling
    counter = 0
    while True:
        wd.find_element_by_tag_name('body').send_keys(Keys.END)  # Scroll down to the bottom
        sleep(wait_time_for_loading)
        coms_new = find_xpath('//*[@id="contents"]/ytd-comment-thread-renderer', True)
        counter += 1
        if len(coms) != len(coms_new) and counter != scrolling_limit:
            coms = coms_new
            print("Scrolling..." if random() > 0.5 else "..........")
        else:
            break


def get_comments_info(coms):
    for com in coms:
        author = com.find_element_by_xpath('.//*[@id="author-text"]/span').text
        time = com.find_element_by_xpath('.//*[@id="header-author"]/yt-formatted-string/a').text
        text = com.find_element_by_xpath('.//*[@id="content"]').text
        upvotes = com.find_element_by_xpath('.//*[@id="vote-count-middle"]').text
        if len(upvotes) > 0:
            if upvotes.endswith(('k', 'K')):
                upvotes = float(upvotes[:-1]) * 1000
            else:
                upvotes = float(upvotes)
        else:
            upvotes = 0
        coms_info.append([author, time, upvotes, text])
    print("Processing..." if random() > 0.5 else "..........")
    return coms_info


def multi_tasking(func, a_list, length, speed):
    threads = []
    for i in range(0, length, speed):
        t = Thread(target=func, args=(a_list[i:i+speed if length - speed else length],))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()


def run(url_):
    global coms_info
    start = time()
    # Make coms_info defined here so that when multiple links provided,
    # there will be a new set of coms_info for each loop
    coms_info = [['USERNAME', 'POSTED ON', 'UPVOTES', 'COMMENTS']]
    # Directed to the youtube video of interest
    wd.get(url_)
    try:
        meta_data = metadata(url_)
        num_coms = get_num_comments()
        if num_coms > 250:
            # Scrolling down the webpage to load more comments
            # Users can set the times of scrolling by entering an integer
            # The default is 50. If users enter 0, the program will scroll down all the comments until it stops
            scroll_down(2)
            coms = find_xpath('//*[@id="contents"]/ytd-comment-thread-renderer', True)
            multi_tasking(get_comments_info, coms, len(coms), 50)
            print('Creating file....')
            filename = f'{meta_data[0]}.xlsx'
            pd.DataFrame(meta_data[1] + coms_info).to_excel(filename)
            print(f"File {filename} Created!")
            end = time()
            print("Total time taken: " + str((end - start)))
        else:
            print('Less than 250 comments!! Comments not extracted.')
    except:
        print("Something went wrong here....")


def quit_out():
    wd.quit()


def main():
    urls = ['A list of links to YouTube videos']
    for url in urls:
        try:
            run(url)
        except:
            continue
    quit_out()


if __name__ == '__main__':
    main()
