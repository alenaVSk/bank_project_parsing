# проект "bank_project_parsing"
Этот скрипт предназначен для парсинга содержимого веб-сайта и сохранения данных в формате JSON. 
Он извлекает заголовки, подзаголовки и контент из статей, а также сканирует и обрабатывает статьи, используя ссылки со страницы.
## Возможности
**Парсинг статей:**
- Извлекает заголовки (h3), подзаголовки (h4), абзацы (p) и списки (ul). 
- Обработка ссылок: Преобразует ссылки в формат Markdown.
- Очищает и структурирует текст для дальнейшей обработк
- Сохраняет собранную информацию в JSON-файл.

**Парсинг статей по ссылкам:**
- Сканирует главную страницу и находит все ссылки на статьи.
- Автоматически переходит по найденным ссылкам и извлекает содержимое каждой статьи.
- Сохраняет собранную информацию в JSON-файл.
  
## Установка
### 1. Клонируйте репозиторий:
```python
git clone https://github.com/alenaVSk/bank_project_parsing.git
cd bank_project_parsing 
```
### 2. Создайте и активируйте виртуальное окружение:
```python
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```
### 3. Установите зависимости:
```python
pip install -r requirements.txt
```
## Использование
### Настройте URL-адрес:
Откройте config.py и укажите URL главной страницы, которую нужно парсить. 
### Запустите скрипт:
```python
python parse_data.py
```
## Результат
После выполнения скрипта данные будут сохранены в файл all_articles.json  

Пример структуры данных в all_articles.json
```json
{
"page_title": "Часто задаваемые вопросы",
        "url": "url, на который перешли со страницы основного url (link_bank)",
        "content": [
{
    "title": "КРЕДИТЫ ФИЗИЧЕСКИМ ЛИЦАМ",
    "subtitle": "Возможно ли изменение процентной ставки .....",
    "content": "В соответствии со ...."
}
{
    "title": "На каких условиях будет храниться ....",
    "subtitle": null,
    "content": "Вклады, оформленные ....."
}
