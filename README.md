# Carleton Interdisciplinary Ethical AI Research (CIE-AIR)
A website to search for and find researchers in your field of interest at Carleton University. 

This project is currently deployed to [https://iml.carleton.ca/CIE-AIR/](https://iml.carleton.ca/CIE-AIR/).

## Development Setup
The repository contains code for both the React frontend and the Flask backend server under `/api`

- To install the react dependencies, run `npm install` in the folder root.
- To start the react app in development mode, run `npm start` in the folder root. Then, open [http://localhost:3000](http://localhost:3000) to view it in your browser.
- To create the build directory, run `npm run build` in the folder root. 

Follow the instructions under `/api/README.md` for Flask setup.

## Packaging
- Build docker image: `docker build -f dockerfile -t carleton-cie-air .`
- Run docker image: `docker run --rm -p 3000:3000 carleton-cie-air`

Once the image is running, connect to [http://localhost:3000](http://localhost:3000)

The docker image is hosted on https://hub.docker.com/r/safahowaid/carleton-cie-air 
- The latest image can be pulled by running: `docker image pull safahowaid/carleton-cie-air:main`
- To run the pulled image: `docker run -d -p 3000:3000 safahowaid/carleton-cie-air:main`
