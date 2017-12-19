from logic import *
from tqdm import tqdm
from multiprocessing import Pool


def main():
    print('Starting')
    url = 'https://coinmarketcap.com/all/views/all/'
    driver = open_links(url)
    links = find_all_links(driver)
    pool = Pool(5)
    links_list = []
    [links_list.append(i) for i in links.values()]

    pool.map(get_data, tqdm(links_list))


if __name__ == '__main__':
    main()
