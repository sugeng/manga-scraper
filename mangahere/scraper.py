import re
import requests
from bs4 import BeautifulSoup
from libs.filename import safe
from libs.path import folder
from libs.download import download


class Scraper:
    soupify = None
    base_url = "http://www.mangahere.co/manga/"

    def __init__(self, manga_name):
        url = self.base_url + manga_name
        self.soupify = self.fetch(url)

    def chapter_lists(self):
        chapters = self.sorted_chapter();

        chapter_total = len(chapters)
        print(f"Total Chapters: {chapter_total}")
        for chapter_index, chapter in enumerate(chapters, start=1):
            print(f"Chapter {chapter_index}, Name : {chapter[0]}")

        choice = input("Download Chapter : ")

        print(f"Will download Chapter {chapters[int(choice) - 1][1]}")

    def sorted_chapter(self):
        chapters = []
        for name, url in sorted(self.lists()):
            chapters.append([name, url])

        return chapters

    def lists(self):
        section = self.soupify.find('div', {"class": "detail_list"})

        if section is not None:
            for chapter in section.find(self.get_lists).find_all('li'):
                chapter_url = chapter.find('a')['href']
                chapter_name = self.chapter_name(chapter)
                yield chapter_name, chapter_url

    def download(self):
        title = self.get_title()
        title = safe(title)

        for name, url in sorted(self.lists()):
            path = folder(f"{title}/{name}")
            download(self.pages(path, url))

        print("Downloading done...")

    def pages(self, path, url):
        soupify = self.fetch(url)

        select_lists = soupify.find('select', {'class': "wid60"})

        images = []
        for select in select_lists.find_all('option'):
            print(f"Building image link.. {select['value']}")
            url, name = self.image(select['value'])
            destination = path.joinpath(name)

            images.append([destination, url])

        return images

    def image(self, url):
        soupyfy = self.fetch(url)
        manga = soupyfy.find('section', {"id": "viewer"}).find('img', {"id": "image"})

        manga_link = manga['src']

        manga_extension = re.search(r'\.(\w+)\?', manga_link)
        image_name = re.sub(r'(\d*\.?\d+?)', lambda m: m.group(1).zfill(3),
                            manga['alt']) + '.' + manga_extension.group(1)

        image_name = safe(image_name)

        return manga_link, image_name

    def get_title(self):
        title = self.soupify.find('h1', {"class": "title"}).text
        return title.title()

    @staticmethod
    def fetch(url):
        page = requests.get(url)
        return BeautifulSoup(page.content, 'lxml')

    @staticmethod
    def chapter_name(chapter):
        chapter_name = chapter.find('span', {"class": "mr6"}).next_sibling
        chapter_name_from_url = chapter.find('a').text.strip()
        chapter_name_from_url = re.sub(r'\s(\d{1,3})', lambda m: ' ' + m.group(1).zfill(3), chapter_name_from_url)

        if chapter_name is not None:
            chapter_name_from_url = chapter_name_from_url + " " + chapter_name

        return safe(chapter_name_from_url)

    @staticmethod
    def get_lists(tag):
        return tag.name == "ul" and not tag.has_attr('class')
