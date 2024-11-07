import React, { useState, useEffect, Suspense, lazy } from "react";

function LPHeader(props) {
  const [text, setText] = useState("Chat With Your");
  const [animation, setAnimation] = useState("slideIn");
  const urlObject = new URL(window.location.origin);
  var hostname = urlObject.hostname;
  if (hostname.startsWith("www.")) {
    hostname = hostname.substring(4);
  }
  urlObject.hostname = `dashboard.${hostname}`;

  var startPath = urlObject.toString();
  return (

    <section className="mt-24 pt-10 lg:mb-60">
      <div className="container mx-auto flex px-5 lg:flex-row flex-col items-center lg:items-start">
        <div className="lg:flex-grow lg:w-2/3 pt-12 lg:pr-24 md:pr-16 flex flex-col lg:items-start lg:text-left lg:mb-0 items-center text-center">
          {!props.open && (
            <h1
              className={`LP-header-h1 ${animation} text-4xl font-['Helvetica_Neue'] sm:text-4xl lg:text-6xl mb-4 font-semibold lg:font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-[#40C6FF] to-[#28B2FB]`}
            >
              {text}
            </h1>
          )}
          <h1 className={`text-3xl ${animation} sm:text-4xl lg:text-6xl mb-4 font-medium lg:font-bold font-['Helvetica_Neue']`}>
            Private Documents
          </h1>
          <h2 className="text-xl mb-5">Revealing insights, keeping data confidential</h2>
          <br class="inline-block"></br>
          <div className="flex flex-col sm:flex-row justify-center">
        <button
          className="btn-yellow mb-4 sm:mb-0 sm:mr-4 w-full sm:w-auto flex justify-center items-center"
          onClick={() => {
            window.location.assign(startPath);
          }}
        >
          Get Started
        </button>
        <button
          className="btn-black w-full sm:w-auto flex justify-center items-center"
          onClick={() => {
            window.location.assign("https://calendly.com/natanvidra/anote");
            // window.open(window.location["origin"] + "/aiday", "_blank");
          }}
        >
          Schedule Demo
        </button>
      </div>
        </div>
        <div className="flex-auto w-5/6 lg:w-1/3">
          <div className="md:w-full md:h-1/2 my-10">
          <img
            src="/landing_page_assets/home.png"
            loading="lazy"
          />
          </div>
        </div>
      </div>
    </section>
  );
}

export default LPHeader;
