/* eslint-disable jsx-a11y/anchor-is-valid */
/* eslint-disable react/jsx-no-target-blank */
import React from "react"
import logo from "../assets/logo.png"
import { useState } from "react";


export default function NavBar() {
    //useState hook to toggle the navbar on mobile
    const [navbar, setNavbar] = useState(false);

    return (
        <nav className="max-w-[720px] lg:max-w-[1236px] mx-auto font-serif text-[#284B63]">
            <div className="justify-between px-4 mx-auto lg:max-w-7xl lg:items-center lg:flex lg:px-8">
                <div >
                    <div className="flex items-center justify-between py-3 lg:py-5 lg:block">
                    <a
						href="https://carleton.ca"
						target="_blank"
						title="Carleton"
						className="flex h-[60px] w-[240px] hover:cursor-pointer lg:h-[80px] lg:min-h-[80px] lg:w-[320px] lg:min-w-[320px]  "
					>
						<img src={logo} className="h-full w-full" alt="" />
					</a>
                        <div className="lg:hidden">
                            <button
                                className="p-1 rounded-md outline-none"
                                onClick={() => setNavbar(!navbar)}
                            >
                                {navbar ? (
                                    <svg
                                        xmlns="http://www.w3.org/2000/svg"
                                        className="w-10 h-10"
                                        viewBox="0 0 20 20"
                                        fill="currentColor"
                                    >
                                        <path
                                            fillRule="evenodd"
                                            d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                                            clipRule="evenodd"
                                        />
                                    </svg>
                                ) : (
                                    <svg
                                        xmlns="http://www.w3.org/2000/svg"
                                        className="w-10 h-10"
                                        fill="none"
                                        viewBox="0 0 24 24"
                                        stroke="currentColor"
                                        strokeWidth={2}
                                    >
                                        <path
                                            strokeLinecap="round"
                                            strokeLinejoin="round"
                                            d="M4 6h16M4 12h16M4 18h16"
                                        />
                                    </svg>
                                )}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </nav>
    );
}