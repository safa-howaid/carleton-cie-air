/* eslint-disable no-unused-vars */
import React, { useState } from "react"
import Search from "./Search"

const Cards = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchData = async (searchValue) => {
    if (searchValue) {
      try {
        searchValue = searchValue.toLowerCase();
        setLoading(true)
        const response = await fetch(`/api/search/${searchValue}`, { headers: {'Content-Type': 'application/json'},})
        if (!response.ok) {
          throw new Error('Network response was not ok.');
        }
        const data = await response.json();
        setData(data);
        setLoading(false);
      } catch (error) {
        setError(error.message);
        setLoading(false);
      }
    }  
  };
	  
	return (
		<>
			<Search onSearch={fetchData} />
			<div className="container mx-auto  px-6 font-serif pb-20 text-[#284B63] lg:max-w-[1236px]">
				<section className="text-center text-[#284B63]">
					<div className="mt-12">
						{loading ? (
                    <div className="flex justify-center items-center" role="status">
                      <svg aria-hidden="true" className="w-8 h-8 text-gray-200 animate-spin dark:text-gray-600 fill-red-600" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>
                          <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/>
                      </svg>
                      <span className="sr-only">Loading...</span>
                    </div>
							) : (data.length > 0) ?
              ( 
                <div className="grid lg:grid-cols-2 lg:gap-12">
                  {data.map((item) => (
                    <div key={item.name} className="my-2 mx-auto lg:mb-0">
                      <div className="lg:block w-[700px] max-w-[80vw] lg:w-[600px] border-b-2 border-transparent hover:border-[#284B63] items-center flex p-6 h-full relative rounded-lg bg-white shadow-lg">
                        <div className="flex text-left flex-col gap-5 lg:gap-[12px] sm:pl-20 lg:p-6">
                          <a href={item.url} target="_blank" className="md:text-xl cursor-pointer font-bold hover:opacity-80" rel="noreferrer">{item.name}</a>
                          <p className="text-sm">{item.title}</p>
                          <p className="text-sm">{item.department}</p>
                          <hr className="h-px my-2 bg-[#284B63] border-[#284B63]"></hr>
                          <p className="text-sm">{item.summary}</p>
                          <p className="md:text-xl cursor-pointer font-bold" rel="noreferrer">Relevant Work:</p>
                          <ul className="list-disc space-y-1">
                            {item.papers.map((paper) => (
                              <li><a key={paper.title} href={paper.url} target="_blank" className="text-sm cursor-pointer hover:opacity-80" rel="noreferrer">{paper.title}</a></li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : error ?
              (
                <p className="text-sm">Error occurred while fetching results...</p>
              )  : (
                <div></div>
              )
            }
					</div>
				</section>
			</div>
		</>
	)
}

export default Cards
