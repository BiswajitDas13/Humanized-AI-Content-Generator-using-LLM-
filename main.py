import streamlit as st
import openai
import nltk
import random
import re
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize, sent_tokenize

# Initialize OpenAI API
openai.api_key = 'your openai key'

# Function to generate content using GPT-4
def generate_content(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant who is fond of writing humanized form of everything asked in a neat and correct format."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200,
        temperature=0.1
    )
    return response.choices[0].message['content'].strip()

# Function to replace words with synonyms with contextual awareness
def replace_with_synonyms(text):
    words = word_tokenize(text)
    new_words = []
    for word in words:
        synonyms = wordnet.synsets(word)
        if synonyms and random.random() < 0.3:  # 30% chance to replace with a synonym
            synonym = synonyms[0].lemmas()[0].name()
            new_words.append(synonym if synonym != word else word)
        else:
            new_words.append(word)
    return ' '.join(new_words)

# Function to introduce natural typos
def introduce_typos(text):
    words = text.split()
    for i in range(len(words)):
        if random.random() < 0.05:  # 5% chance to introduce a typo
            word = words[i]
            if len(word) > 3:  # Only introduce typos for words with more than 3 characters
                char_index = random.randint(1, len(word) - 2)
                typo = word[:char_index] + random.choice('abcdefghijklmnopqrstuvwxyz') + word[char_index + 1:]
                words[i] = typo
    return ' '.join(words)

# Function to vary sentence structure and length
def vary_sentence_structure(text):
    sentences = sent_tokenize(text)
    new_sentences = []
    for sentence in sentences:
        if random.random() < 0.3:  # 30% chance to alter sentence structure
            # Example transformation: splitting sentences
            parts = re.split(r'(\,|\;|\:|\-)', sentence)
            new_sentence = ' '.join(parts)
            new_sentences.append(new_sentence)
        else:
            new_sentences.append(sentence)
    return ' '.join(new_sentences)

# Function to add minor grammatical errors
def add_grammatical_errors(text):
    sentences = sent_tokenize(text)
    for i in range(len(sentences)):
        if random.random() < 0.2:  # 20% chance to add a grammatical error
            words = sentences[i].split()
            if len(words) > 4:
                # Example: wrong tense, incorrect article, etc.
                words[0] = words[0].lower() if words[0][0].isupper() else words[0].capitalize()
                sentences[i] = ' '.join(words)
    return ' '.join(sentences)

# Function to add personal touches and conversational tone
def add_personal_touches(text):
    additional_phrases = [
        "Personally, I believe",
        "In my experience",
        "I once thought that",
        "Interestingly,",
        "One time, I found myself thinking",
        "For instance,"
    ]
    sentences = sent_tokenize(text)
    enhanced_sentences = []
    for sentence in sentences:
        if random.random() < 0.4:  # 40% chance to add a personal touch
            sentence = random.choice(additional_phrases) + ", " + sentence
        enhanced_sentences.append(sentence)
    return ''.join(enhanced_sentences)

# Function to humanize content
def humanize_content(text):
    text = replace_with_synonyms(text)
    text = vary_sentence_structure(text)
    text = add_personal_touches(text)
    return text

# Streamlit App
def main():
    st.title("Humanized AI Content Generator")

    prompt = st.text_area("Enter your prompt:")

    if st.button("Generate"):
        if prompt:
            with st.spinner("Generating content..."):
                ai_generated_content = generate_content(prompt)
                humanized_content = humanize_content(ai_generated_content)
                st.subheader("Humanized Content")
                st.write(humanized_content)
        else:
            st.warning("Please enter a prompt.")

if __name__ == "__main__":
    main()
