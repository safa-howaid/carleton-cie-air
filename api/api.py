from openai import OpenAI
from flask import Flask, send_from_directory, request, jsonify, current_app, g as app_ctx
from flask_cors import cross_origin
from werkzeug.middleware.proxy_fix import ProxyFix
from dotenv import load_dotenv
from pinecone import Pinecone
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import time
import json

# Load environment variables to get OpenAI API Key
load_dotenv()


# Read the professors data json file as a dictionary
f = open('data/professor_data.json')
professor_data = json.load(f)
f.close()

# Initialize flask app
app = Flask(__name__, static_folder='../build', static_url_path='/')
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1)

# Initialize OpenAI client
openai_client = OpenAI()

# Initialize Pinecone client
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Global results variable
results = []

# Gets embeddings using OpenAi's "text-embedding-3-small" model
def get_embedding(text, model="text-embedding-3-small"):
   text = text.replace("\n", " ")
   return openai_client.embeddings.create(input = [text], model=model).data[0].embedding

# Generates professor knowledge summary based on relevant papers
def get_summary(query, professor, papers, model="gpt-3.5-turbo"):
    papers_str = ""
    for paper in papers:
        papers_str += f'Title: {paper["title"]}\n'
        if paper["abstract"]:
            papers_str += f'Abstract: {paper["abstract"]}\n'
        papers_str += "\n"
      
    user_prompt = "You're a system that helps researchers find professors to collaborate with. Your dataset contains the research papers of these professors. A researcher is interacting with the website, and gives you a topic, you look through the research papers and return a short paragraph (2-5 sentences) describing the professor's knowledge regarding the topic. Start your description with the professor's name. Do not describe or list the papers in your response, instead use the paper's content to determine the professor's knowledge.\n\n"
    user_prompt += f'Professor: {professor}\n'
    user_prompt += f'Topic: {query}\n'
    user_prompt += f'Relevant Papers: \n{papers_str}\n'

    response = openai_client.chat.completions.create(
      model=model,
      messages=[
        {"role": "user", "content": user_prompt},
      ]
    )
    return response.choices[0].message.content

# Gets summary for professor and updates results
def thread_function(query, professor, papers, index):
  global results
  summary = get_summary(query,professor,papers)
  results[index]["summary"] = summary

@app.before_request
def logging_before():
    # Store the start time for the request
    app_ctx.start_time = time.perf_counter()

@app.after_request
def logging_after(response):
    # Get total time in milliseconds
    total_time = time.perf_counter() - app_ctx.start_time
    time_in_ms = int(total_time * 1000)
    # Log the time taken for the endpoint 
    current_app.logger.info('%s ms %s %s %s', time_in_ms, request.method, request.path, dict(request.args))
    return response

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')
    
@app.route("/api/test")
@cross_origin()
def hello_world():
    return "Hello"

#localhost/search?query=searchValue
@app.route("/api/search/<search_term>")
@cross_origin()
def search(search_term):
    global results
    
    # Embed the search term
    search_term_vector = get_embedding(search_term)

    # Query pinecone for top 20 papers based on similarity score to the search term
    result = pc.Index("semantic-search-openai").query(vector=[search_term_vector], top_k=20, include_metadata=True)
    ranking = result["matches"]

    # Group papers by author name  
    top = {}
    for paper in ranking:
        author = paper['metadata']['author']
        if not author in top:
            top[author] = []
        work = {
          "title": paper['metadata']['title'],
          "abstract": paper['metadata']['abstract'],
          "url": paper['metadata']['url'],
        }
        top[author].append(work)

    # Sort the authors by most top ranked papers
    sorted_top = dict(sorted(top.items(), key=lambda item: len(item[1]),reverse=True))

    # Format JSON results
    results = []
    futures = []
    
    # Multithreading while making calls to generate summary
    with ThreadPoolExecutor(max_workers=10) as executor:
      for index, (professor, papers) in enumerate(sorted_top.items()):
          result = dict()
          result["name"] = professor
          result["title"] = professor_data[professor]["title"]
          result["department"] = professor_data[professor]["department"]
          result["url"] = professor_data[professor]["url"]
          result["papers"] = []
          for paper in papers:
              result["papers"].append({
                  "title": paper["title"],
                  "url": paper["url"]
              })
          results.append(result)
          futures.append(executor.submit(thread_function,search_term,professor,sorted_top[professor], index))

      for future in as_completed(futures):
        future.result()

    return jsonify(results)

if __name__ == '__main__':
    app.debug=True
    app.run()