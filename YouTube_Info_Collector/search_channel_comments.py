from YouTube_Info_Collector import search, channel_comments
from time import sleep


def get_cnl_links(query):
    cnl_links= search.run(query)[1]
    search.quit_out()
    return cnl_links


def get_cnl_comments(link):
    channel_comments.get_comments(link)


def main():
    queries = ['A list of queries..']
    c = 1
    for query in queries:
        print("\n" + "#" * 60)
        print(f'{"="*15} Starting #_{c} query {"="*15}')
        links = get_cnl_links(query)
        print(f'{"="*15} #_{c} query complete and links of channels gotten {"="*15}')
        sleep(3)
        for link in links:
            get_cnl_comments(link)
        print(f'{"-" * 20} Comments from videos of targeted channel COLLECTED {"-" * 20}')
    print(f'{"="*15} Mission accomplished {"="*15}')


if __name__ == '__main__':
    main()
