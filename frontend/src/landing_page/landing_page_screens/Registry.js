import React, { useState } from "react";
import LPProductValueAdd from "./Home/LPProductValueAdd";
import LPHighLevel from "./Home/LPHighLevel";


function Registry() {
  return (
      <div className="mx-5 lg:mx-2 mt-24">
      <div className="text-3xl sm:text-4xl lg:text-5xl my-15 text-center font-medium lg:font-bold text-white">
        Closed Sourced Agents
      </div>
      <div class="p-10 grid grid-cols-1 sm:grid-cols-1 md:grid-cols-3 lg:grid-cols-3 xl:grid-cols-3 gap-5 gap-y-0">
        <LPHighLevel
          image="/landing_page_assets/privatewhite.png"
          title="Upreach"
          description="Email Marketing Agent"
        />
        <LPHighLevel
          image="/landing_page_assets/accuratewhite.png"
          title="Private Chatbot"
          description="Financial Analyst Agent"
        />
        <LPHighLevel
          image="/landing_page_assets/accuratewhite.png"
          title="Anote"
          description="Data Labeler Agent"
        />
        </div>
        <div class="px-10 py-0 grid grid-cols-1 sm:grid-cols-1 md:grid-cols-3 lg:grid-cols-3 xl:grid-cols-3 gap-5 gap-y-0">
        <LPHighLevel
          image="/landing_page_assets/citationswhite.png"
          title="AI-RFP"
          description="Grant Writer Agent"
        />
        <LPHighLevel
          image="/landing_page_assets/citationswhite.png"
          title="Autocode"
          description="Software Engineer Agent"
        />
        <LPHighLevel
          image="/landing_page_assets/citationswhite.png"
          title="Applico"
          description="Job Seeker Agent"
        />
        </div>
      </div>
  );
}

export default Registry;
