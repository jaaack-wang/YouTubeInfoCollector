from YouTube_Info_Collector import channel, comments


def get_links(url):
    channel.run(url)
    links = channel.get_links()
    return links


def get_comments(url):
    links = get_links(url)
    views = channel.get_views()
    for i in range(len(links)):
        try:
            if views[i] > 100000:
                comments.run(links[i])
        except:
            print("Something went wrong here...")
            continue


def main():
    urls = ["A list of links to YouTube Channels' VIDEOS webpage..."]
    c = 1
    for url in urls:
        print("\n" + "#" * 40)
        print(f'{"="*15} Starting #_{c} query {"="*15}')
        get_comments(url)
        print(f'{"="*15} #_{c} query complete{"="*15}')
    print(f'{"+"*15} Mission accomplished {"+"*15}')
    comments.quit_out()


if __name__ == '__main__':
    main()
