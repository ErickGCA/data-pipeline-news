import json
import re
import os
import unicodedata

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(base_dir, "data")

def normalize_text(text):
    if not text:
        return ""
    text = text.lower()
    return ''.join(c for c in unicodedata.normalize('NFD', text)
                  if unicodedata.category(c) != 'Mn')

def is_alcohol_accident(text):
    text = text.lower()

    keywords = [
        r"acidente.*(álcool|alcool|bebida|embriagado|embriaguez)",
        r"embriagado|embriaguez",
        r"(dirigia|conduzia|ao volante).*(bêbado|bebado|alcoolizado|embriagado)",
        r"(motorista|condutor).*(bêbado|bebado|alcoolizado|embriagado)",
        r"sob (efeito|influência).*(álcool|alcool|bebida)",
        r"(teste|exame).*(alcoolemia|etilômetro|bafômetro)",
        r"lei seca.*(acidente|colisão|batida|capotamento|atropelamento)",
        r"(álcool|alcool|bebida).*(volante|direção)",
        r"(capotamento|colisão|batida|acidente).*(álcool|alcool|embriaguez)",
        r"(vítima|vitima|morto|ferido).*(motorista|condutor).*(bêbado|bebado|alcoolizado|embriagado)",
    ]
    
    norm_text = normalize_text(text)
    norm_keywords = [
        r"acidente.*(alcool|bebida|embriagado|embriaguez)",
        r"embriagado|embriaguez",
        r"(dirigia|conduzia|ao volante).*(bebado|alcoolizado|embriagado)",
        r"(motorista|condutor).*(bebado|alcoolizado|embriagado)",
        r"sob (efeito|influencia).*(alcool|bebida)",
        r"(teste|exame).*(alcoolemia|etilometro|bafometro)",
        r"lei seca.*(acidente|colisao|batida|capotamento|atropelamento)",
        r"(alcool|bebida).*(volante|direcao)",
        r"(capotamento|colisao|batida|acidente).*(alcool|embriaguez)",
        r"(vitima|morto|ferido).*(motorista|condutor).*(bebado|alcoolizado|embriagado)",
    ]
    
    return any(re.search(kw, text) for kw in keywords) or any(re.search(kw, norm_text) for kw in norm_keywords)

def calculate_relevance(text):
    text = text.lower()
    score = 0
    
    primary_patterns = [
        r"(dirigia|conduzia|ao volante).*(bêbado|bebado|alcoolizado|embriagado)",
        r"(motorista|condutor).*(bêbado|bebado|alcoolizado|embriagado)",
        r"sob (efeito|influência) de (álcool|alcool)",
        r"(teste|exame).*(alcoolemia|etilômetro|bafômetro).*(positivo|acima)",
        r"lei seca.*(infração|infracao|autuado|detido)"
    ]
    
    secondary_patterns = [
        r"(acidente|colisão|batida).*(álcool|alcool)",
        r"lei seca",
        r"(bafômetro|etilômetro)",
        r"(embriagado|embriaguez)",
        r"(vítima|vitima|morto|ferido).*(álcool|alcool)"
    ]
    
    tertiary_patterns = [
        r"acidente",
        r"álcool|alcool",
        r"colisão|batida",
        r"motorista|condutor"
    ]
    
    for pattern in primary_patterns:
        if re.search(pattern, text):
            score += 3
    
    for pattern in secondary_patterns:
        if re.search(pattern, text):
            score += 2
    
    for pattern in tertiary_patterns:
        if re.search(pattern, text):
            score += 1
    
    return score

def transform(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)

        filtered_news = []
        for article in raw_data:
            content = f"{article.get('title', '')} {article.get('description', '')} {article.get('content', '')}"
            
            if is_alcohol_accident(content):
                relevance_score = calculate_relevance(content)
                
                filtered_news.append({
                    "title": article.get("title"),
                    "description": article.get("description"),
                    "url": article.get("url"),
                    "publishedAt": article.get("publishedAt"),
                    "relevance_score": relevance_score,
                    "source": article.get("source", {}).get("name")
                })

        filtered_news.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(filtered_news, f, ensure_ascii=False, indent=4)

        print(f"{len(filtered_news)} notícias relevantes salvas em '{output_path}'")
        
        if filtered_news:
            print("\nNotícias mais relevantes:")
            for i, news in enumerate(filtered_news[:5], 1):
                print(f"{i}. [{news.get('relevance_score')}] {news.get('title')}")

if __name__ == "__main__":
    input_path = os.path.join(data_dir, "raw_news.json")
    output_path = os.path.join(data_dir, "filtered_news.json")
    
    try:
        transform(input_path, output_path)
    except Exception as e:
        print(f"Erro na transformação dos dados: {e}")