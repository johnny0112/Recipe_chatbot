# AI Chef - RAG-Based Cooking Assistant

AI Chef is a cooking assistant application that utilizes Retrieval-Augmented Generation (RAG) to provide structured and contextually relevant recipe recommendations. The system combines vector search and OpenAI's language model to deliver precise responses based on user queries.

## Features

- **RAG-Based Recipe Retrieval**: Identifies the most relevant recipe by searching a vector database of precomputed embeddings.
- **Structured Recipe Generation**: AI provides step-by-step cooking instructions based on retrieved recipes..
- **Interactive Query Handling**: Supports follow-up questions for deeper exploration of cooking techniques and ingredients.

## Project Structure

- **`main.py`**  
  Implements the Streamlit interface for user interaction.  
  Handles queries by retrieving relevant recipes and generating responses.  
  Calls `search_similarity()` and `RAG_based_response()` to process inputs.

- **`RAG.py`**  
  Implements the Retrieval-Augmented Generation (RAG) pipeline.  
  `search_similarity()` retrieves the most similar recipe by comparing vector embeddings based on cosine similarity.  
  `RAG_based_response()` constructs efficient prompts based on retrieved data.

- **`initialize_embeddings.py.py`**  
  Prepares recipe data for embedding generation.  
  Implements `chunk_text()` to segment recipe steps for better contextual representation.
  Loads precomputed embeddings from `data.json`.

- **`openai_api.py`**  
  Interfaces with the OpenAI API for text embedding and response generation.  
  `get_embedding()` generates vector representations of recipe components based on model text-embedding-3-small.  
  `get_response()` streams responses from the language model gpt-4o-2024-11-20.

  ![image](https://github.com/user-attachments/assets/d47a5af4-f57c-4d1d-9d4d-f939274dd6c1)

