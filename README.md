# Languague_scraper
This is a practice of how to make a scraper, you'll learn to find elements in the html, and select the information that you want.

## Introduction

We will be using this page 'https://www.reverso.net/text_translation.aspx?lang=EN' 

We can read its robots.txt here: 'https://www.reverso.net/robots.txt'

On this page, we can find the conjugation of verbs in various languages. We will focus on English, Portuguese, French, Spanish, German and Italian.

## Libraries

- requests;
- bs4 (BeautifulSoup);
- pandas;
- http.client;
- logging;
- re;

## Objective

The aims of this is obtain each verb tense of 2000 links.
Each tense has sentences of first, second, third person singular and plural. There are six sentences in total.
You can run the program from the console and observe the link and number of the scraped verb.

# Quick Start 

We have some links in HOME_LANGUAGE_URL for some languages.
You only need to change the variable of the URL you want to scrape.
For example:

run(HOME_PORTUGUESE_URL)
