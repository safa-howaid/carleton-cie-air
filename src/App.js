import Navbar from "./components/Navbar"
import Hero from "./components/Hero"
import Cards from "./components/Cards"


import React, { useEffect } from 'react';

function App() {
	useEffect(() => {
		document.title = 'Carleton Interdisciplinary Ethical AI Research';
		document.body.style.backgroundColor = '#F0F9FF';
	  }, []);
	return (
		<>		
			<Navbar />
			<Hero />
			<Cards />
		</>
	)
}

export default App
