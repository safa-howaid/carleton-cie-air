
from dotenv import load_dotenv
from tqdm.auto import tqdm
from pinecone import Pinecone
import numpy as np
import os
import hashlib
import pandas

def create_paper_id(author, title):
  """Creates a hash from the author and title of a paper which serves as an id"""
  string = f"{author} - {title}"
  result = hashlib.md5(string.encode('utf-8'))
  return result.hexdigest()

# Load environment variables
load_dotenv()

# Read the paper data csv file as a pandas data frame
df = pandas.read_csv("paper_data.csv")
df['embedding'] = df.embedding.apply(eval).apply(np.array)
df = df.fillna('')
df["id"] = df.apply(lambda x: create_paper_id(x["author"], x["title"]), axis=1)

# Setup Pinecone client
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("semantic-search-openai")

# Insert paper data in batches of 32
batch_size = 32  
total_size = len(df['id'])
for i in tqdm(range(0, total_size, batch_size)):
  # set end position of batch
  i_end = min(i+batch_size, total_size)
  # get batch of IDs
  titles = df["title"][i: i+batch_size].tolist()
  abstracts = df["abstract"][i: i+batch_size].tolist()
  authors = df["author"][i: i+batch_size].tolist()
  dates = df["date"][i: i+batch_size].tolist()
  urls = df["url"][i: i+batch_size].tolist()
  ids = df["id"].astype(str)[i: i+batch_size].tolist()
  embeds = df["embedding"][i: i+batch_size].tolist()
  # prep metadata and upsert batch
  meta = [{"title": title, "abstract": abstract, "author": author, "date": date, "url": url} for (title, abstract, author, date, url) in zip(titles, abstracts, authors, dates, urls)]
  to_upsert = zip(ids, embeds, meta)
  # upsert to Pinecone
  index.upsert(vectors=list(to_upsert))