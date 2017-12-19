from selenium import webdriver
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
from multiprocessing import Pool


def open_links(url):
    driver = webdriver.PhantomJS()
    driver.set_window_size(1120, 550)
    driver.get(url)

    return driver


def get_links(links, i):
    links[i.text] = i.get_attribute("href") + 'historical-data/?start=20130428&end=20171219'
    return links


def find_all_links(driver):
    all_links = driver.find_elements_by_class_name('currency-name-container')
    links = {}
    [get_links(links, i) for i in all_links]

    return links


def get_values_min(i, curr):
    i = i.text.strip().split(' ')
    mini = i[2].split('\n')

    curr['{} {} {}'.format(i[0], i[1], mini[0])] = mini[4]

    return curr


def get_values_max(i, curr):
    i = i.text.strip().split(' ')
    maxi = i[2].split('\n')

    curr['{} {} {}'.format(i[0], i[1], maxi[0])] = maxi[5]

    return curr


def save_file(name, min_val, max_val):
    with open('curr.txt', 'a') as f:
        f.write('{}, min = {}, max = {} \n'.format(name, min_val, max_val))


def get_data(link):
    url = link
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'lxml')
    all_time = soup.find('table', {'class': 'table'})
    data = all_time.find_all('tr', {'class': 'text-right'})
    curr_min = {}
    curr_max = {}
    [get_values_min(i, curr_min) for i in data]
    [get_values_max(i, curr_max) for i in data]
    min_val = '{} - {}'.format(min(curr_min, key=curr_min.get), curr_min['{}'.format(min(curr_min, key=curr_min.get))])
    max_val = '{} - {}'.format(max(curr_max, key=curr_max.get), curr_max['{}'.format(max(curr_max, key=curr_max.get))])
    name = soup.find('title')
    name = name.text.split(' ')[0]
    save_file(name, min_val, max_val)

    # print(link)


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
