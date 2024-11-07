import React, { useState } from "react";
import LPProductValueAdd from "./Home/LPProductValueAdd";
import LPHighLevel from "./Home/LPHighLevel";


function FinanceGPT() {
  return (
    <div className="text-white max-w-screen">
    <div className="w-screen">
      <div className="w-full md:w-3/4 mx-auto my-10">
        <div className="flex flex-col-reverse md:flex-row items-center">
          <img
              src="/landing_page_assets/IsPrivate.png"
              className="w-11/12 md:w-3/5 rounded-xl"
          ></img>
          <div className="px-10 mb-5">
            <div className="text-2xl font-semibold py-5">
              How is it Private?
            </div>
            <div className="text-lg">
              Uploaded data is stored locally, on premise, for enterprise grade security. Connect to data
              within your local mysql database. LLMs like GPT4All and Llama2 run
              locally on your device. All queries stay on your computer, never
              leaving your private, secure data silo.
          </div>
        </div>
      </div>
      </div>

      <div className="">

      <div className="mx-5 lg:mx-2 mt-24">
      <div className="text-3xl sm:text-4xl lg:text-5xl my-15 text-center font-medium lg:font-bold">
        Private Chatbot Value Add
      </div>
      <div class="p-10 grid grid-cols-1 sm:grid-cols-1 md:grid-cols-3 lg:grid-cols-3 xl:grid-cols-3 gap-5">
        <LPHighLevel
          image="/landing_page_assets/privatewhite.png"
          title="Private"
          description="Data remains private, secure and on-premise, with the LLMs staying local to your silo"
        />
        <LPHighLevel
          image="/landing_page_assets/accuratewhite.png"
          title="Accurate"
          description="Choose your model type (Llama2, Mistral) or import your fine tuned model for enhanced accuracy"
        />
        <LPHighLevel
          image="/landing_page_assets/citationswhite.png"
          title="Citations"
          description="View accurate citations to see the page number and text where the model's answer came from"
        />
        </div>
      </div>
    </div>
    </div>
  </div>
  );
}

export default FinanceGPT;
