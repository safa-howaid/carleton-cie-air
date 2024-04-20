import React from "react"
import hero from "../assets/hero.jpg"

const Hero = () => {
	return (
		<>
			<main className="scroll-smooth text-[#284B63]">
				<section className="mx-auto w-full max-w-[720px] px-4 font-serif  lg:max-w-[1236px] ">
					<div className="container mx-auto flex flex-col-reverse items-center pt-10 lg:pb-10 lg:flex-row">
						<div className="mb-10 w-full  lg:mb-0 lg:w-1/2 lg:max-w-2xl">
							<img
								className="rounded-md object-cover object-center"
								alt="AI Research"
								src={hero}
							/>
						</div>
						<div className="flex flex-col items-center gap-10 text-center lg:w-1/2 lg:flex-grow lg:items-start lg:pl-20 lg:text-left">
							<h1 className="mb-4 text-xl font-semibold sm:text-4xl">
								Carleton AI Research
							</h1>
							<p className="mb-8 lg:text-xl text-[#353535] leading-relaxed">
								Carleton AI
								Research (CU-A) aims to connect
								AI researchers at Carleton with problem owners 
								for	sustainable development of Ethical AI. <br></br> <br></br>
                Check out our search engine specialized to find AI-related faculty members at Carleton University.
							</p>

						</div>
					</div>
				</section>
			</main>
		</>
	)
}

export default Hero
