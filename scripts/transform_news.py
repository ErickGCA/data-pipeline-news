#Necessário adicionar mais palavras chaves para o proposito 

import json
import os
import re

def alcohol_accident(text):
    text = text.lower()
    keywords = [ 
        r"acidente.*(álcool|alcool)",
        r"embrigado",
        r"dirigia.*(bêbado|alcoolizado)",
        r"motorista.*(bêbado|alcoolizado)",
        r"sob efeito de álcool",
       # r"vale tudo", <- expressão de teste
    ]
    return any(re.search(kw, text) for kw in keywords)
def transform(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)

        filtered_news = []
        for article in raw_data:
            content = f"{article.get('title', '')} {article.get('description', '')}"
            if alcohol_accident(content):
                filtered_news.append({
                    "title": article.get("title"),
                    "description": article.get("description"),
                    "url": article.get("url"),
                    "publishedAt": article.get("publishedAt")
                })

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding = 'utf-8') as f:
            json.dump(filtered_news, f, ensure_ascii = False, indent = 4)

        print(f"{len(filtered_news)} notícias relevantes salvas em '{output_path}'")


if __name__ == "__main__":
    input_path = "../pipelines-news/data/raw_news.json"
    output_path = "../pipelines-news/data/filtered_news.json"
    transform(input_path, output_path)