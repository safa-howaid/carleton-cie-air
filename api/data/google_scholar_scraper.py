# Fetches google scholar urls from a csv file, scrapes web data, and uploads it to Pinecone DB
 
from bs4 import BeautifulSoup
from openai import OpenAI
from dotenv import load_dotenv
from pinecone import Pinecone
from datetime import datetime
from fake_useragent import UserAgent
import pandas
import requests
import json 
import time
import hashlib
import os
import pandas
import random


def create_paper_id(author, title):
  """Creates a hash from the author and title of a paper which serves as an id"""
  string = f"{author} - {title}"
  result = hashlib.md5(string.encode('utf-8'))
  return result.hexdigest()

def get_embedding(text, model="text-embedding-3-small"):
   """Generates text embeddings using OpenAi's "text-embedding-3-small" model"""
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding

def get_wait_time():
  """Generates wait time to avoid ip blocking (1-2 mins)"""
  return random.randint(60, 180)

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI()

# Read the input url csv file as a pandas data frame
df = pandas.read_csv("webscraping_urls.csv")

# Initialize random User Agent generator
ua = UserAgent()

# HTML header for google scholar get request
headers = {
  "User-Agent": ua.random,
}
google_scholar_base = "https://scholar.google.com"

data = []

# Filter rows to just the ones that were not marked as scraped
filtered_df = df.loc[(df['is_scraped'] == 0) & (df["google_scholar_url"].notnull())]

# Iterate over each row in the urls csv file
for index, row in df.iterrows():
  faculty = row["name"]

  # If faculty member was already scraped, skip them
  if row['is_scraped'] == 1:
    continue

  print("Fetching papers for", faculty)
  URL = row["google_scholar_url"]
  
  if pandas.notnull(URL):
    # Ensure that papers are sorted by publishing year
    URL += "&pagesize=80&view_op=list_works&sortby=pubdate"
    headers["User-Agent"] = ua.random

    # Fetch and parse the faculty member's page
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    ip_blocked = len(soup(text=lambda t: "unusual traffic" in t.text)) > 0 or len(soup(text=lambda t: "That’s an error." in t.text)) > 0
    if ip_blocked:
      print("Google scholar blocked your ip.... exiting...")
      exit()

    # Get the hyperlinks for all the papers belonging to the faculty member
    papers = soup.find_all("a", class_="gsc_a_at")

    # Visit the page for each paper and scrape parts of it
    count = 0
    for paper in papers:
      paper_info = {}

      # Get the title of the paper
      title = paper.text.strip()
      paper_info["title"] = title

      # Get the url of the paper
      paper_URL = google_scholar_base + paper["href"]
      paper_info["url"] = paper_URL

      # Open the page and parse its content
      headers["User-Agent"] = ua.random
      paper_page = requests.get(paper_URL, headers=headers)
      soup = BeautifulSoup(paper_page.content, "html.parser")

      # If no data retrieved, the IP has been blocked. Break out of loop to reset manually
      ip_blocked = len(soup(text=lambda t: "unusual traffic" in t.text)) > 0 or len(soup(text=lambda t: "That's an error." in t.text)) > 0
      if ip_blocked:
        print("Google scholar blocked your ip.... exiting...")
        exit()

      # Get the abstract of the paper
      abstract_div = soup.find("div", class_="gsh_small")
      if abstract_div:
        abstract = abstract_div.text
        paper_info["abstract"] = abstract
      else:
        paper_info["abstract"] = ""

      # Get the date that the paper was published in
      fields = soup.find_all("div", class_="gsc_oci_field")
      if len(fields) >= 2 and fields[1] and fields[1].text == "Publication date":
        date = soup.find_all("div", class_="gsc_oci_value")[1].text
        paper_info["date"] = date
      else:
        paper_info["date"] = ""
      
      # Once we reach a paper that was not published within the last 10 years,
      # We can break out of the loop and move onto the next faculty member because
      # the papers are sorted by publishing year
      current_year = int(datetime.now().strftime('%Y'))
      if paper_info["date"]:
        published_year = int(paper_info["date"].split("/")[0])
        if published_year < (current_year - 10): 
          break

      paper_info["id"] = create_paper_id(faculty, paper_info["title"])
      paper_info["author"] = faculty
      paper_info["embedding_text"] = f'Title: {paper_info["title"]}; Abstract: {paper_info["abstract"]}'
      # Get text embedding from OpenAI
      paper_info["embedding"] = get_embedding(paper_info["embedding_text"], model='text-embedding-3-small')

      # Initialize Pinecone client
      pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
      pc_index = pc.Index("semantic-search-openai")
      # Insert paper into Pinecone
      pc_index.upsert(vectors=[
        {
          "id": paper_info["id"], 
          "values": paper_info["embedding"], 
          "metadata": {"title": paper_info["title"], "abstract": paper_info["abstract"], "author": paper_info["author"], "date": paper_info["date"], "url": paper_info["url"]}
        },
      ])
      
      # Append the paper to the list of papers
      count += 1
      data.append(paper_info)

      # Output and save the data in a json file
      with open("google_scholar_data.json", "w", encoding='utf8') as outfile: 
        json.dump(data, outfile, ensure_ascii=False, indent=4)

      # Pause to avoid IP blocking
      time.sleep(get_wait_time())

    # Attach the list of papers to the faculty member that wrote it
    print("Retrieved", count, "papers.")
    print("Completed", (index+1), "/", len(filtered_df.index), "faculty members.\n\n")

    # Modify webscraping csv to mark the faculty member as scraped
    df.at[index, "is_scraped"] = 1
    with open("webscraping_urls.csv", "w") as outfile: 
      df.to_csv(outfile, encoding='utf-8', index=False)

print("Webscraping google scholar completed.\n")
