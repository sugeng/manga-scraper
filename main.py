from mangahere.scraper import Scraper
import argparse

parser = argparse.ArgumentParser(description='Manga Scraper & Downloader')
parser.add_argument('-p', '--provider', choices=['mangahere', 'spectrum'], default='mangahere', help='Manga Site '
                                                                                                    'Provider, '
                                                                                                    'ex: mangahere')
parser.add_argument('-n', '--name', help='Manga name, used by mangahere provider')
parser.add_argument('-u', '--url', help='Manga url path, used by spectrumnexus')

args = parser.parse_args()


# parser = argparse.ArgumentParser()
# parser.add_argument("url")
# args = parser.parse_args()
#
# mangahere = Scraper(args.url)
#
#
# def chapter_choices():
#     chapters = mangahere.sorted_chapter()
#     total_chapter = len(chapters)
#
#     for chapter_index, chapter in enumerate(chapters, start=1):
#         print(f"Chapter : {chapter_index}, Name {chapter[0]}")
#
#     choice = input(f"Total Chapter {total_chapter} -- Chapter yang Akan didownload : ")
#     choice_clean = int(choice) - 1
#
#     if valid_choice(choice_clean, total_chapter) is not True:
#         print("Chapter not found..!")
#         exit()
#
#     print(chapters[choice_clean][1])
#
#
# def valid_choice(choice, total_chapter):
#     if choice > total_chapter:
#         return False
#
#     return True
#
# chapter_choices()