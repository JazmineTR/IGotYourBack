import requests
from bs4 import BeautifulSoup
from transformers import pipeline
import newspaper

def is_news_site(url):
    news_urls = ["cnn.com", "foxnews.com", "nytimes.com", "washingtonpost.com", "nbcnews.com", "apnews.com", "bbcnews.com", "aljazeera.com", "wsj.com"]
    for string in news_urls:
        if string in url:
            return True
    return False

def retrieve_article_content(url):
    article = newspaper.Article(url)
    article.download()
    article.parse()

    return article.text

def get_news_articles(tags):
    articles = []

    api_key = 'AIzaSyB1SL9kKEfkeDaOrrEsY_yDxw7qMJlHLJY'
    search_engine_id = 'f61a10c9a5466475f'
    num_results = 10

    search_url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q={tags}&num={num_results}"
    response = requests.get(search_url)
    print(response)
    search_results = response.json()
    print(search_results)


    # Process the search_results JSON and extract relevant information
    articles = search_results.get('items', [])
    filtered_articles = []
    for article in articles:
        title = article.get('title')
        url = article.get('link')
        print(url)
        metatags = article['pagemap'].get('metatags', [])
        publication_date = next((tag.get('pubdate') for tag in metatags if 'pubdate' in tag), None)
        if is_news_site(url):
            print(url)
            content = retrieve_article_content(url)
            filtered_articles.append({'title': title, 'url': url, 'publication_date': publication_date, 'content': content})

    for article in filtered_articles:
        print(f"Title: {article['title']}")
        print(f"URL: {article['url']}")
        print(f"Publication Date: {article['publication_date']}")
        print()
    return filtered_articles



def summarize_articles(articles):
    summarize = pipeline('summarization')
    for article in articles:
        content = article['content']
        print(content)
        summary = summarize(content, max_length= 3, min_length=0, do_sample=False)
        article['summary'] = summary[0]['summary_text']

    return articles


user_tags = 'politics'
articles = get_news_articles(user_tags)
articles = summarize_articles(articles)

for article in articles:
    print(article['content'])
    print("Title:", article['title'])
    print("Summary:", article['summary'])
    print()

