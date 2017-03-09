import re
import requests
from bs4 import BeautifulSoup

from libs.filename import safe
from libs.path import folder
from libs.download import download


class Scraper:
    soupify = None
    base_url = None

    def __init__(self, url):
        self.base_url = url
        self.soupify = self.fetch(url)

    def get(self):
        titles = self.soupify.find_all('div', {'class': 'viewerLabel'})
        title = titles[1].text

        for volume in self.get_volumes():
            path = folder(f"{title}/{volume}")
            volume_path = re.sub('\s', '+', volume.strip())
            images = []
            volume_page = self.base_url + "?ch=" + volume_path + "&page=1"
            self.soupify = self.fetch(volume_page)
            for chapter in self.get_chapter(volume_path):
                image_name = safe(chapter.split('/')[-1])
                destination = path.joinpath(image_name)
                images.append([destination, chapter])

            download(images)

    @staticmethod
    def get_image(page):
        image = page.find('img', {'id': 'mainimage'})

        if image is not None:
            return image['src']

        return None

    def get_volumes(self):
        volumes = self.soupify.find('select', {'class': 'selectchapter'})
        for volume in volumes.find_all('option'):
            yield volume['value']

    def get_chapter(self, volume):
        chapters = self.soupify.find('select', {'class': 'selectpage'})
        for chapter in chapters.find_all('option'):
            page_path = self.base_url + "?ch=" + volume + "&page=" + chapter['value']
            page = self.fetch(page_path)
            image_url = self.get_image(page)

            print(f"Generating Image Link... {page_path}")
            if image_url is not None:
                yield image_url

    @staticmethod
    def fetch(url):
        page = requests.get(url)
        return BeautifulSoup(page.content, 'lxml')
