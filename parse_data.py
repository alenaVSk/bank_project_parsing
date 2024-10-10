import requests
from bs4 import BeautifulSoup
import json
import re
from urllib.parse import urljoin
from config import link_bank


#функция очистки текста
def clean_text(text):
    text = re.sub(r'[\xa0\xad]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def parse_content(element):
    if element.name == 'p':
        content = ''
        for child in element.children:
            if child.name == 'a':
                href = child.get('href', '')
                text = clean_text(child.text)
                content += f'[{text}]({href})'
            else:
                content += child.string if child.string else ''
        return clean_text(content)
    elif element.name == 'ul':
        return parse_list(element)
    else:
        return clean_text(element.text)


#функция обрабатывает HTML-списки(элементы списка ('li'))
def parse_list(ul_element):
    return "\n".join("• " + parse_content(li) for li in ul_element.find_all('li'))


#функция парсинга страницы
def parse_article(url):
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        article_body = soup.find('section', class_='article__body')

        if not article_body:
            print("Не удалось найти секцию статьи.")
            return []

        article_content = []
        current_title = None
        current_subtitle = None
        current_content = []

        for element in article_body.children:
            if element.name == 'h3':
                if current_title:
                    article_content.append({
                        "title": current_title,
                        "subtitle": current_subtitle,
                        "content": ' '.join(current_content)
                    })
                current_title = clean_text(element.text)
                current_subtitle = None
                current_content = []
            elif element.name == 'h4':
                if current_subtitle:
                    article_content.append({
                        "title": current_title,
                        "subtitle": current_subtitle,
                        "content": ' '.join(current_content)
                    })
                current_subtitle = clean_text(element.text)
                current_content = []
            elif element.name in ['p', 'ul']:
                current_content.append(parse_content(element))

        # Добавляем последний раздел
        if current_title:
            article_content.append({
                "title": current_title,
                "subtitle": current_subtitle,
                "content": ' '.join(current_content)
            })

        return article_content
    except requests.RequestException as e:
        print(f"Произошла ошибка при запросе URL: {e}")
        return []


#парсит главную страницу со списком ссылок
def parse_main_page(url):
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        links = soup.find_all('a', class_='page_menu')
        
        result = []
        for link in links:
            href = link.get('href')
            if href:
                full_url = urljoin(url, href)
                title = clean_text(link.text)
                article_data = parse_article(full_url)
                if article_data:
                    result.append({
                        "page_title": title,
                        "url": full_url,
                        "content": article_data
                    })
                else:
                    print(f"Не удалось получить данные для страницы: {full_url}")

        return result
    except requests.RequestException as e:
        print(f"Произошла ошибка при запросе главной страницы {url}: {e}")
        return []


#функция сохраняет данные в JSON-файл
def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":

    main_url = "dddddd"

    all_data = parse_main_page(main_url)
    save_to_json(all_data, 'all_articles.json')
    print(f"Данные всех статей сохранены в файл all_articles.json. Количество обработанных страниц: {len(all_data)}")
