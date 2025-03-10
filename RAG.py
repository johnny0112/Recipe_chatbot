import pandas as pd
import os
from openai_api import get_client, get_response, get_embedding
import json
import numpy as np

openai_client = get_client()


def load_data():
    df = pd.read_csv("data.csv")
    df = df.drop(columns=['author_note'], axis=1)
    return df

def chunk_text(text, chunk_size=2):
    chunks=[]
    steps = text.split(". ")
    for i in range(0, len(steps), chunk_size):
        chunk = ".".join(steps[i:i + chunk_size])
        chunks.append(chunk)
    return chunks


df = load_data()

def load_embedding_list():
    try:
        with open("data.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        for item in data:
            item["name"] = np.array(item["name"])
            item["ingredients"] = np.array(item["ingredients"])
            item["steps"] = [np.array(chunk) for chunk in item["steps"]]
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def cosine_similarity(u, v):
    u = np.array(u)
    v = np.array(v)
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))


def search_similarity(prompt):
    embedding_list = load_embedding_list()
        
    prompt_embedding = get_embedding(openai_client, prompt)

    similarities = []
    for recipe in embedding_list:
        name_similarity = cosine_similarity(prompt_embedding, recipe['name'])
        ingredients_similarity = cosine_similarity(prompt_embedding, recipe['ingredients'])
        step_similarities = [cosine_similarity(prompt_embedding, chunk_emb) for chunk_emb in recipe['steps']]
        steps_similarity = np.mean(step_similarities)
        average_similarity = np.mean([name_similarity, ingredients_similarity, steps_similarity])
        similarities.append((recipe['index'], name_similarity))

    most_similar_recipe = sorted(similarities, key=lambda x: x[1], reverse=True)[0]
    similar_recipe_index, highest_similarity = most_similar_recipe
    return most_similar_recipe


def RAG_based_response(most_similar_recipe,query):
    similarity_threshold = 0.4
    similar_recipe_index, highest_similarity = most_similar_recipe
    similar_recipe = df.iloc[similar_recipe_index]
    
    if highest_similarity < similarity_threshold:
        prompt = f"""
        Nejbližší recept v mé kuchařce je {similar_recipe['name']} s podobností {highest_similarity:.2f}, což je pod prahem {similarity_threshold}.
        
        Odpověz prosím věcně a přesně na dotaz: {query} 
        Pokud dotaz souvisí s vařením, zdvořile odpověz a uveď, že tento recept mi zatím v mé kuchařce chybí, ale rád vám nabídnu svoji verzi receptu.
        Pokud dotaz nesouvisí s vařením, zdvořile odmítni odpovědět.
        """
    else:
        step_chunks = chunk_text(similar_recipe['steps'])
        prompt = f"""
        Ve své kuchařce mám recept na {similar_recipe['name']} (podobnost: {highest_similarity:.2f}).

        Ingredience: {similar_recipe['ingredients']}
    
        Postup vaření:
        """
        for i, chunk in enumerate(step_chunks):
            prompt += f"\nKrok {i + 1}: {chunk}"
    
        prompt += f"""

        Začni odpověď slovy "Ve své kuchařce mám recept na {similar_recipe['name']}."
        Poté napiš podrobný návod na vaření tohoto jídla.
        U ingrediencí uveď jen výčet tak, jak máš zadaný, a ne žádné číselné hodnoty.
        Postup popiš přesně podle daných kroků, nerozšiřuj ho.
        """
    
    return prompt
