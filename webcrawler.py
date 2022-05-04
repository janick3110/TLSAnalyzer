import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urlparse
import os
import datetime

url = ''
file = ''
links = []
hosts = []
visited_links = []
current_directory = ''
levels = 0


def get_page_content(url):  # searches the html text for links
    content = get_html_text(url)
    # übergebe html an beautifulsoup parser
    soup = BeautifulSoup(content, "html.parser")

    for post in soup.findAll('a'):
        link = post.get('href')

        if link not in links:
            if link is not None:
                if len(link) > 0 and link[0] != '#':
                    links.append(link)

    get_all_hosts()


def get_html_text(url):  # gets the html text from the website
    time.sleep(5)
    return requests.get(url).text


def get_domain(url):  # puts the found links in correct format
    parsed_uri = urlparse(url)
    return '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)


def get_host(url):  # determines the host of a given link
    if "https://" in url:
        tmp = url.replace('https://', '')
    elif "http://" in url:
        print(url + " may has not TLS")
        tmp = url.replace('http://', '')
    else:
        return None

    subtree = tmp.find('/')
    host = ''
    for i in range(0, subtree):
        host += tmp[i]
    return host


def get_command(url):  # creates the command for the TLS analysis
    command = 'python -m sslyze ' + url
    return command


def create_filename(host, path):  # creates the file path for the output
    if 'www.' in host:
        tmp = host.replace('www.', '')
    else:
        tmp = host
    file = tmp.replace('.', '_')

    file = path + "_" + file + "_TLS_Scan.txt"
    return file


def get_all_hosts():  # gathers all different hosts
    for link in links:
        if get_host(link) not in hosts and get_host(link) is not None:
            hosts.append(get_host(link))


def get_date(format):  # gives the file the date when the process was started
    now = datetime.datetime.now()
    times = now.strftime(format)
    return times


def visit_all_pages():  # analyses subpages for new hosts
    for link in links:
        if link not in visited_links:
            visited_links.append(link)
            get_page_content(link)


def runWebcrawler():
    url = str(input("Input the URL of your staring page:\n"))
    path = get_date('%Y-%m-%d_%H-%M-%S')

    get_page_content(url)

    for i in range(0, levels):
        visit_all_pages()

    i = 0
    file = open(path + '_log.txt', 'w')

    for host in hosts:
        i += 1
        command = get_command(host) + " > " + create_filename(host, path)
        timestamp = get_date('%H:%M:%S')
        print('[' + timestamp + ']   ' + "Scanning: " + host)
        file.write('[' + timestamp + ']   ' + "Scanning: " + host + '\n')
        os.system(command)
        # create_filename(host)
        print("Scanned " + host + ". " + str(len(hosts) - i) + " remaining.")
    print('Scanning complete. ' + str(len(links)) + " links were found and " + str(i) + " hosts were checked for TLS.")
    file.write(
        'Scanning complete. ' + str(len(links)) + " links were found and " + str(i) + " hosts were checked for TLS.")
