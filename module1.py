import bs4
import requests


class WebScrap():

    def __init__(self):
        self.url = 'https://habr.com'
        self.dir = '/ru/all/'
        self.KEYWORDS = ['python', 'дизайн', 'фото', 'web']


    def get_html(self):
        response = requests.get(f'''{self.url+self.dir}''')
        return response.text


    def pars_html(self):
        post = {}
        posts = []
        soup = bs4.BeautifulSoup(self.get_html(), 'html.parser')
        for record in soup.find_all('article'):
            date = record.time['title']
            directory = record.find(class_="tm-article-snippet__title-link")['href']
            name = record.find(class_="tm-article-snippet__title-link").span.text
            post = {'date':date, 'name':name, 'url':self.url + directory}
            posts.append(post)
        return posts


    def _req(self,url):
        response = requests.get(url)
        return response


    def search_in_link(self):
        posts_list = self.pars_html()
        find_posts = []
        for post in posts_list:
            response = self._req(post['url'])
            soup = bs4.BeautifulSoup(response.text, 'html.parser')
            text = soup.find(xmlns="http://www.w3.org/1999/xhtml").text
            for key in self.KEYWORDS:
                if key in text:
                    find_posts.append(post)
                    break  #Добавим выход из цикла потому как в одном посте может найтись несколько слов из поиска
        return find_posts


def main():
    test = WebScrap()
    links = test.search_in_link()
    for link in links:
        print(f'''{link['date']} {link['name']} {link['url']}''')


if __name__ == "__main__":
    main()


