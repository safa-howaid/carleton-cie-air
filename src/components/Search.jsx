import React from "react"

const Search = (props) => {
  // Handle pressing enter when in the search bar
  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      props.onSearch(event.target.value)
    }
  }

  // Handle clicking the search icon
  const handleClick = () => {
      var query = document.getElementById('query_input').value
      props.onSearch(query)
  }


	return (  
		<>
			<div className="py-2 mb-4">
				<h2 className="text-center text-3xl text-[#353535] font-semibold">
					Meet our
					<span className="text-[#3C6E71] font-bold "> Researchers</span>
				</h2>
			</div>
			<div className="mx-auto flex max-w-[720px] justify-center text-[#353535] lg:max-w-[1236px] ">
				<div className="flex items-center justify-center gap-x-6 ">
					<div>
						<div className="relative bg-transparent text-lg  w-[350px] sm:w-[500px] ">
							<div className="flex items-center border-b-2 text-[#353535] border-[#3C6E71] py-2">
								<input
                  id="query_input"
									className="mr-3 w-[450px] border-none font-semibold placeholder-[rgba(53,53,53,0.6)] bg-transparent px-2 leading-tight focus:outline-none"
									type="text"
									onKeyUp={handleKeyPress}
									placeholder="Machine Learning, Robotics etc.."
								/>
								<button className="absolute right-0 top-0 mt-[7px] mr-3" onClick={handleClick}>
									<svg
										className="h-6 w-6 fill-[#3C6E71]"
										xmlns="http://www.w3.org/2000/svg"
										version="1.1"
										id="Capa_1"
										x="0px"
										y="0px"
										viewBox="0 0 56.966 56.966"
										width="512px"
										height="512px"
									>
										<path d="M55.146,51.887L41.588,37.786c3.486-4.144,5.396-9.358,5.396-14.786c0-12.682-10.318-23-23-23s-23,10.318-23,23  s10.318,23,23,23c4.761,0,9.298-1.436,13.177-4.162l13.661,14.208c0.571,0.593,1.339,0.92,2.162,0.92  c0.779,0,1.518-0.297,2.079-0.837C56.255,54.982,56.293,53.08,55.146,51.887z M23.984,6c9.374,0,17,7.626,17,17s-7.626,17-17,17  s-17-7.626-17-17S14.61,6,23.984,6z" />
									</svg>
								</button>
							</div>
						</div>
					</div>
				</div>
			</div>
		</>
	)
}

export default Search
