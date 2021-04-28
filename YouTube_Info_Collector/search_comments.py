from YouTube_Info_Collector import search, comments


def get_links(query):
    links_titles = search.run(query)[0]
    search.quit_out()
    links = [lt[0] for lt in links_titles]
    return links


def get_comments(query):
    links = get_links(query)
    try:
        for link in links:
            try:
                comments.run(link)
            except:
                continue
    except:
        print("Something went wrong here....")



def main():
    queries = ['A list of queries...']
    c = 1
    for query in queries:
        print("\n" + "#" * 40)
        print(f'{"="*15} Starting #_{c} query {"="*15}')
        get_comments(query)
        print(f'{"="*15} #_{c} query complete{"="*15}')
    print(f'{"+"*15} Mission accomplished {"+"*15}')
    comments.quit_out()

if __name__ == '__main__':
    main()
