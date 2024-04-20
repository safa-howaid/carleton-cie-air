# Backend Flask Server

## Setup
- Ensure that you have Python3 and pip installed
- Create python virtual environment: 
  - `python3 -m venv venv`
  - `source venv/bin/activate`
- To install required packages: `python3 -m pip install -r requirements.txt`
- Create a `.env` file and include the following environment variables:
  - `OPENAI_API_KEY`: API key from OpenAI used for text embedding and text generation
  - `PINECONE_API_KEY`: API key from the Pinecone vector database used for querying research papers

## Run Server Locally
To run server for development purposes: `flask run`

To run server with Gunicorn: `gunicorn --config gunicorn_config.py app:app`

## Data Collection
Data is collected by scraping the google scholar urls for each faculty member under `data/webscraping_urls.csv`.

To add data for a new faculty member:
- Add their name to `data/webscraping_urls.csv` along with the google scholar url
- Set their `is_scraped` column to `0` to mark this faculty member as not yet scraped.
- Run `python3 data/google_scholar_scraper.py` to scrape data from Google Scholar and insert it into a Pinecone Vector database to be included when search queries are received. 

NOTE: The webscraper script assumes that you already have a Pinecone DB index named `semantic-search-openai` with vector dimensions set to 1536.