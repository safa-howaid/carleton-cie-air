# Build step #1: build the React front end
FROM    node:16-alpine as build-step
WORKDIR /app
ENV     PATH /app/node_modules/.bin:$PATH

# Copy local code to the container image
COPY ./tailwind.config.js ./package.json ./package-lock.json ./
COPY ./src ./src
COPY ./public ./public

# Install modules
RUN npm install

# Create build directory
RUN npm run build 

# Build step #2: build the backend server with the client as static files
FROM    python:3.9
WORKDIR /app

# Copy local code to the container image.
COPY  --from=build-step /app/build ./build
RUN   mkdir ./api
COPY  api/requirements.txt api/api.py api/.flaskenv api/.env api/gunicorn_config.py ./api/
COPY  api/data/professor_data.json	./api/data/professor_data.json
RUN	  pip install -r ./api/requirements.txt --no-cache-dir
ENV   FLASK_ENV production

EXPOSE  3000
WORKDIR /app/api
CMD		  ["gunicorn","--config","gunicorn_config.py","api:app"]