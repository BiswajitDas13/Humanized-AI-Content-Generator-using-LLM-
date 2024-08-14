import openai
import nltk
import random
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize, sent_tokenize
import streamlit as st

# Initialize OpenAI API
openai.api_key = 'your api key'

# Function to generate content using GPT-4
def generate_content(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",  # You can use "gpt-4-turbo" if you have access
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200,
        temperature=0.7
    )
    return response.choices[0].message['content'].strip()

# Function to replace words with synonyms
def replace_with_synonyms(text):
    words = word_tokenize(text)
    new_words = []
    for word in words:
        synonyms = wordnet.synsets(word)
        if synonyms:
            new_word = synonyms[0].lemmas()[0].name()
            if new_word != word:
                new_words.append(new_word)
            else:
                new_words.append(word)
        else:
            new_words.append(word)
    return ' '.join(new_words)

# Function to introduce typos
def introduce_typos(text):
    words = text.split()
    for i in range(len(words)):
        if random.random() < 0.05:  # 5% chance to introduce a typo
            word = words[i]
            if len(word) > 2:
                char_index = random.randint(0, len(word) - 1)
                typo = word[:char_index] + random.choice('abcdefghijklmnopqrstuvwxyz') + word[char_index + 1:]
                words[i] = typo
    return ' '.join(words)

# Function to vary sentence length
def vary_sentence_length(text):
    sentences = sent_tokenize(text)
    new_sentences = []
    for sentence in sentences:
        if random.random() < 0.2:  # 20% chance to modify sentence length
            new_sentences.append(sentence + ' ' + random.choice(['Moreover,', 'Additionally,', 'In conclusion,']))
        else:
            new_sentences.append(sentence)
    return ' '.join(new_sentences)

# Function to add personal touches
def add_personal_touches(text):
    additional_phrases = [
        "Let me share a little story with you,",
        "You know, one time I found myself thinking,",
        "Here's a thought from my own experience,",
        "It reminds me of when I once,",
        "From my own perspective,",
        "Here's an interesting fact from my life,",
        "Just the other day, I was thinking,"
    ]

    sentences = sent_tokenize(text)
    enhanced_sentences = []

    for sentence in sentences:
        if random.random() < 0.3:  # 30% chance to add a personal touch
            sentence = random.choice(additional_phrases) + " " + sentence
        enhanced_sentences.append(sentence)

    return ' '.join(enhanced_sentences)

# Function to humanize content
def humanize_content(text):
    text = replace_with_synonyms(text)
    text = introduce_typos(text)
    text = vary_sentence_length(text)
    text = add_personal_touches(text)
    return text

# Streamlit app
st.title("AI Content Humanizer")

prompt = st.text_input("Enter your prompt:")

if st.button("Generate Humanized Content"):
    if prompt:
        ai_generated_content = generate_content(prompt)
        humanized_content = humanize_content(ai_generated_content)
        st.subheader("Humanized Content:")
        st.write(humanized_content)
    else:
        st.error("Please enter a prompt.")
