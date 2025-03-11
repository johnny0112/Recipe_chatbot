import pandas as pd
import os
from openai_api import get_client, get_embedding
import json
import numpy as np
from RAG import chunk_text, load_data

#funkce na embedding původního csv souboru s recepty
def transform_data(df):
    openai_client = get_client()
    embedding_list = []
    
    for i in range(len(df)):
        name_embedding = get_embedding(openai_client, df.iloc[i]['name'])
        ingredients_embedding = get_embedding(openai_client, df.iloc[i]['ingredients'])
        step_chunks = chunk_text(df.iloc[i]['steps'])
        steps_embedding = []
        for chunk in step_chunks:
            steps_embedding.append(get_embedding(openai_client, chunk))
        embedding_list.append({
            "index": i,
            "name": name_embedding,
            "ingredients": ingredients_embedding,
            "steps": steps_embedding
        })
    return embedding_list
    
#načtení csv souboru, transformace do embeddingu a uložení ve formě JSON souboru
def main():
    df = load_data()
    embedding_list = transform_data(df)
    
    with open("data.json", "w", encoding="utf-8") as file:
        json.dump(embedding_list, file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main() 
