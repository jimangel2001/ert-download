import requests
import re
from bs4 import BeautifulSoup


def obtain_title(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    title = soup.find('title').text
    title = re.sub(":|/|\||\"", "-", title);
    return title

def obtain_player_url(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    player_iframe = soup.find('iframe')
    player_url = re.split('&', (player_iframe.attrs["src"]))[0]
    return player_url


def obtain_stream_url(url):
    html = requests.get(url).text
    stream_url = re.split("var HLSLink = '(.*)'", html)[1]
    if("dvrorigingr" not in stream_url):
        stream_url = re.sub("dvrorigin", "dvrorigingr", stream_url)
    stream_url = re.sub("/playlist.m3u8", "", stream_url)
    return stream_url


def obtain_chunklist(url):
    playlist_url = url + "/chunklist.m3u8"
    clean_chunklist = []
    chunklist = requests.get(playlist_url).text.split('\n')
    for chunk in chunklist:
        if ".ts" in chunk:
            clean_chunklist.append(chunk)
    return (clean_chunklist)


def obtain_data(url):
    title = obtain_title(url)
    player_url = obtain_player_url(url)
    stream_url = obtain_stream_url(player_url)
    return {"title": title, "stream_url": stream_url, "chunklist": obtain_chunklist(stream_url)}
