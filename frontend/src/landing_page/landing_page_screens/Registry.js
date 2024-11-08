// // // import React, { useState } from "react";
// // // import LPProductValueAdd from "./Home/LPProductValueAdd";
// // // import LPHighLevel from "./Home/LPHighLevel";


// // // function Registry() {
// // //   return (
// // //       <div className="mx-5 lg:mx-2 mt-24">
// // //       <div className="text-3xl sm:text-4xl lg:text-5xl my-15 text-center font-medium lg:font-bold text-white">
// // //         Closed Sourced Agents
// // //       </div>
// // //       <div class="p-10 grid grid-cols-1 sm:grid-cols-1 md:grid-cols-3 lg:grid-cols-3 xl:grid-cols-3 gap-5 gap-y-0">
// // //         <LPHighLevel
// // //           image="/landing_page_assets/privatewhite.png"
// // //           title="Upreach"
// // //           description="Email Marketing Agent"
// // //         />
// // //         <LPHighLevel
// // //           image="/landing_page_assets/accuratewhite.png"
// // //           title="Private Chatbot"
// // //           description="Financial Analyst Agent"
// // //         />
// // //         <LPHighLevel
// // //           image="/landing_page_assets/accuratewhite.png"
// // //           title="Anote"
// // //           description="Data Labeler Agent"
// // //         />
// // //         </div>
// // //         <div class="px-10 py-0 grid grid-cols-1 sm:grid-cols-1 md:grid-cols-3 lg:grid-cols-3 xl:grid-cols-3 gap-5 gap-y-0">
// // //         <LPHighLevel
// // //           image="/landing_page_assets/citationswhite.png"
// // //           title="AI-RFP"
// // //           description="Grant Writer Agent"
// // //         />
// // //         <LPHighLevel
// // //           image="/landing_page_assets/citationswhite.png"
// // //           title="Autocode"
// // //           description="Software Engineer Agent"
// // //         />
// // //         <LPHighLevel
// // //           image="/landing_page_assets/citationswhite.png"
// // //           title="Applico"
// // //           description="Job Seeker Agent"
// // //         />
// // //         </div>
// // //       </div>
// // //   );
// // // }

// // // export default Registry;

// // import React from "react";
// // import LPHighLevel from "./Home/LPHighLevel";

// // function Registry() {
// //   return (
// //     <div className="mx-5 lg:mx-24 mt-24">
// //       <div className="text-3xl sm:text-4xl lg:text-5xl my-10 text-center font-medium lg:font-bold text-white">
// //         Closed Source Agents
// //       </div>

// //       <div className="grid grid-cols-1 sm:grid-cols-1 md:grid-cols-3 lg:grid-cols-3 xl:grid-cols-3 gap-8 px-8">
// //         <AgentCard
// //           image="/landing_page_assets/privatewhite.png"
// //           title="Upreach"
// //           description="Email Marketing Agent"
// //           moreInfoLink="#"
// //           websiteLink="https://agentwebsite.com/upreach"
// //         />
// //         <AgentCard
// //           image="/landing_page_assets/accuratewhite.png"
// //           title="Private Chatbot"
// //           description="Financial Analyst Agent"
// //           moreInfoLink="#"
// //           websiteLink="https://agentwebsite.com/privatechatbot"
// //         />
// //         <AgentCard
// //           image="/landing_page_assets/accuratewhite.png"
// //           title="Anote"
// //           description="Data Labeler Agent"
// //           moreInfoLink="#"
// //           websiteLink="https://agentwebsite.com/anote"
// //         />
// //         <AgentCard
// //           image="/landing_page_assets/citationswhite.png"
// //           title="AI-RFP"
// //           description="Grant Writer Agent"
// //           moreInfoLink="#"
// //           websiteLink="https://agentwebsite.com/ai-rfp"
// //         />
// //         <AgentCard
// //           image="/landing_page_assets/citationswhite.png"
// //           title="Autocode"
// //           description="Software Engineer Agent"
// //           moreInfoLink="#"
// //           websiteLink="https://agentwebsite.com/autocode"
// //         />
// //         <AgentCard
// //           image="/landing_page_assets/citationswhite.png"
// //           title="Applico"
// //           description="Job Seeker Agent"
// //           moreInfoLink="#"
// //           websiteLink="https://agentwebsite.com/applico"
// //         />
// //       </div>
// //     </div>
// //   );
// // }

// // function AgentCard({ image, title, description, moreInfoLink, websiteLink }) {
// //   return (
// //     <div className="bg-[#1a1a1a] rounded-lg shadow-lg p-6 flex flex-col items-center text-center text-white">
// //       <img src={image} alt={title} className="w-16 h-16 mb-4" />
// //       <h3 className="text-xl font-semibold mb-2">{title}</h3>
// //       <p className="text-md mb-4">{description}</p>
// //       <div className="flex gap-4">
// //         <a
// //           href={moreInfoLink}
// //           className="bg-gradient-to-r from-[#EDDC8F] to-[#F1CA57] text-black px-4 py-2 rounded-md font-semibold"
// //         >
// //           More Info
// //         </a>
// //         <a
// //           href={websiteLink}
// //           target="_blank"
// //           rel="noopener noreferrer"
// //           className="bg-[#F1CA57] text-black px-4 py-2 rounded-md font-semibold"
// //         >
// //           Visit Website
// //         </a>
// //       </div>
// //     </div>
// //   );
// // }

// // export default Registry;

// import React, { useState } from "react";
// import LPHighLevel from "./Home/LPHighLevel";

// function Registry() {
//   const [isModalOpen, setIsModalOpen] = useState(false);
//   const [selectedAgent, setSelectedAgent] = useState(null);

//   const agents = [
//     {
//       image: "/landing_page_assets/privatewhite.png",
//       title: "Upreach",
//       description: "Email Marketing Agent",
//       websiteLink: "https://agentwebsite.com/upreach",
//       details:
//         "Upreach is an advanced email marketing agent designed to streamline outreach and optimize email campaigns with AI-driven insights.",
//     },
//     {
//       image: "/landing_page_assets/accuratewhite.png",
//       title: "Private Chatbot",
//       description: "Financial Analyst Agent",
//       websiteLink: "https://agentwebsite.com/privatechatbot",
//       details:
//         "Private Chatbot is a financial analyst agent that provides real-time insights and data-driven analysis for your financial documents.",
//     },
//     {
//       image: "/landing_page_assets/accuratewhite.png",
//       title: "Anote",
//       description: "Data Labeler Agent",
//       websiteLink: "https://agentwebsite.com/anote",
//       details:
//         "Anote is a powerful data labeling agent that enables efficient and accurate data annotation for machine learning workflows.",
//     },
//     {
//       image: "/landing_page_assets/citationswhite.png",
//       title: "AI-RFP",
//       description: "Grant Writer Agent",
//       websiteLink: "https://agentwebsite.com/ai-rfp",
//       details:
//         "AI-RFP assists with grant writing, helping you draft, review, and submit high-quality grant proposals efficiently.",
//     },
//     {
//       image: "/landing_page_assets/citationswhite.png",
//       title: "Autocode",
//       description: "Software Engineer Agent",
//       websiteLink: "https://agentwebsite.com/autocode",
//       details:
//         "Autocode is a software engineer agent that automates coding tasks, improves code quality, and assists with code reviews.",
//     },
//     {
//       image: "/landing_page_assets/citationswhite.png",
//       title: "Applico",
//       description: "Job Seeker Agent",
//       websiteLink: "https://agentwebsite.com/applico",
//       details:
//         "Applico is a job-seeker agent that helps you find job opportunities, prepare applications, and streamline the job search process.",
//     },
//   ];

//   const openModal = (agent) => {
//     setSelectedAgent(agent);
//     setIsModalOpen(true);
//   };

//   const closeModal = () => {
//     setSelectedAgent(null);
//     setIsModalOpen(false);
//   };

//   return (
//     <div className="mx-5 lg:mx-24 mt-24">
//       <div className="text-3xl sm:text-4xl lg:text-5xl my-10 text-center font-medium lg:font-bold text-white">
//         Closed Source Agents
//       </div>

//       <div className="grid grid-cols-1 sm:grid-cols-1 md:grid-cols-3 lg:grid-cols-3 xl:grid-cols-3 gap-8 px-8">
//         {agents.map((agent, index) => (
//           <div
//             key={index}
//             className="bg-[#1a1a1a] rounded-lg shadow-lg p-6 flex flex-col items-center text-center text-white transition-transform transform hover:scale-105 cursor-pointer"
//             onClick={() => openModal(agent)}
//           >
//             <img src={agent.image} alt={agent.title} className="w-16 h-16 mb-4" />
//             <h3 className="text-xl font-semibold mb-2">{agent.title}</h3>
//             <p className="text-md mb-4">{agent.description}</p>
//             <button
//               className="bg-gradient-to-r from-[#EDDC8F] to-[#F1CA57] text-black px-4 py-2 rounded-md font-semibold"
//             >
//               More Info
//             </button>
//           </div>
//         ))}
//       </div>

//       {isModalOpen && selectedAgent && (
//         <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-75 z-50">
//           <div className="bg-[#1a1a1a] w-11/12 md:w-2/3 lg:w-1/3 rounded-lg p-8 text-white relative">
//             <button
//               className="absolute top-2 right-2 text-2xl font-bold"
//               onClick={closeModal}
//             >
//               &times;
//             </button>
//             <img src={selectedAgent.image} alt={selectedAgent.title} className="w-20 h-20 mx-auto mb-4" />
//             <h2 className="text-2xl font-bold mb-4">{selectedAgent.title}</h2>
//             <p className="text-md mb-6">{selectedAgent.details}</p>
//             <a
//               href={selectedAgent.websiteLink}
//               target="_blank"
//               rel="noopener noreferrer"
//               className="inline-block bg-gradient-to-r from-[#EDDC8F] to-[#F1CA57] text-black px-4 py-2 rounded-md font-semibold"
//             >
//               Visit Website
//             </a>
//           </div>
//         </div>
//       )}
//     </div>
//   );
// }

// export default Registry;

import React, { useState } from "react";

function Registry() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedAgent, setSelectedAgent] = useState(null);

  const agents = [
    {
      image: "/landing_page_assets/privatewhite.png",
      title: "Upreach",
      description: "Email Marketing Agent",
      websiteLink: "https://agentwebsite.com/upreach",
      details:
        "Upreach is an advanced email marketing agent designed to streamline outreach and optimize email campaigns with AI-driven insights.",
      features: ["Automated Campaigns", "Personalized Outreach", "Data Analytics"],
      useCases: ["Lead Generation", "Customer Retention", "Campaign Performance Tracking"],
      capabilities: "Upreach can send automated, personalized emails, track user engagement, and analyze campaign results to optimize future strategies.",
    },
    {
      image: "/landing_page_assets/accuratewhite.png",
      title: "Private Chatbot",
      description: "Financial Analyst Agent",
      websiteLink: "https://agentwebsite.com/privatechatbot",
      details:
        "Private Chatbot provides real-time financial insights, powered by AI to help you make data-driven decisions.",
      features: ["Financial Data Analysis", "Real-Time Reporting", "Customizable Dashboards"],
      useCases: ["Portfolio Analysis", "Market Trend Monitoring", "Risk Assessment"],
      capabilities: "This agent can analyze financial reports, detect trends, and generate custom financial dashboards.",
    },
    {
      image: "/landing_page_assets/accuratewhite.png",
      title: "Anote",
      description: "Data Labeler Agent",
      websiteLink: "https://agentwebsite.com/anote",
      details:
        "Anote is a powerful data labeling agent that provides accurate and efficient annotation for machine learning datasets.",
      features: ["Automated Labeling", "Quality Control", "Dataset Export"],
      useCases: ["Image Annotation", "Text Labeling", "Entity Extraction"],
      capabilities: "Anote supports multiple annotation formats and can handle large datasets efficiently with quality assurance features.",
    },
    {
      image: "/landing_page_assets/citationswhite.png",
      title: "AI-RFP",
      description: "Grant Writer Agent",
      websiteLink: "https://agentwebsite.com/ai-rfp",
      details:
        "AI-RFP assists with grant writing, helping you draft, review, and submit high-quality grant proposals efficiently.",
      features: ["Automated Proposal Drafting", "Review Assistance", "Funding Source Analysis"],
      useCases: ["Grant Application Preparation", "Funding Opportunity Research", "Proposal Quality Enhancement"],
      capabilities: "AI-RFP streamlines the grant writing process by automating proposal drafts and assisting with funding source research.",
    },
    {
      image: "/landing_page_assets/citationswhite.png",
      title: "Autocode",
      description: "Software Engineer Agent",
      websiteLink: "https://agentwebsite.com/autocode",
      details:
        "Autocode is a software engineer agent that automates coding tasks, improves code quality, and assists with code reviews.",
      features: ["Code Generation", "Automated Code Reviews", "Error Detection"],
      useCases: ["Software Development Assistance", "Code Optimization", "Quality Assurance"],
      capabilities: "Autocode can generate and review code, detect potential errors, and provide recommendations for optimization.",
    },
    {
      image: "/landing_page_assets/citationswhite.png",
      title: "Applico",
      description: "Job Seeker Agent",
      websiteLink: "https://agentwebsite.com/applico",
      details:
        "Applico is a job-seeker agent that helps you find job opportunities, prepare applications, and streamline the job search process.",
      features: ["Job Search Optimization", "Application Tracking", "Resume and Cover Letter Assistance"],
      useCases: ["Job Opportunity Discovery", "Application Management", "Personalized Job Recommendations"],
      capabilities: "Applico aids in finding job listings, managing applications, and providing tailored job recommendations based on user profiles.",
    },
    {
      image: "/landing_page_assets/citationswhite.png",
      title: "MarketSense",
      description: "Market Research Agent",
      websiteLink: "https://agentwebsite.com/marketsense",
      details:
        "MarketSense is a market research agent that gathers, analyzes, and interprets market data to provide strategic insights.",
      features: ["Competitor Analysis", "Trend Monitoring", "Consumer Insights"],
      useCases: ["New Market Entry Analysis", "Product Development Insights", "Competitive Positioning"],
      capabilities: "MarketSense collects and analyzes data to provide actionable insights on market trends, customer preferences, and competitor strategies.",
    },
    {
      image: "/landing_page_assets/citationswhite.png",
      title: "Assistly",
      description: "Customer Support Agent",
      websiteLink: "https://agentwebsite.com/assistly",
      details:
        "Assistly is a customer support agent that provides automated responses, tracks inquiries, and enhances customer satisfaction.",
      features: ["Automated Responses", "Inquiry Tracking", "Personalized Support"],
      useCases: ["Customer Service Automation", "Complaint Resolution", "Support Ticket Management"],
      capabilities: "Assistly can handle customer inquiries, resolve complaints, and manage support tickets for streamlined customer service.",
    },
    {
      image: "/landing_page_assets/citationswhite.png",
      title: "TeamUp",
      description: "Project Manager Agent",
      websiteLink: "https://agentwebsite.com/teamup",
      details:
        "TeamUp is a project management agent that assists in task assignment, timeline tracking, and team coordination.",
      features: ["Task Assignment", "Progress Tracking", "Team Collaboration"],
      useCases: ["Project Planning", "Task Management", "Timeline Tracking"],
      capabilities: "TeamUp enables teams to stay on track by assigning tasks, monitoring project timelines, and enhancing team collaboration.",
    },
  ];

  const openModal = (agent) => {
    setSelectedAgent(agent);
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setSelectedAgent(null);
    setIsModalOpen(false);
  };

  return (
    <div className="mx-5 lg:mx-24 mt-24">
      <div className="text-3xl sm:text-4xl lg:text-5xl my-10 text-center font-medium lg:font-bold text-white">
        Closed Source Agents
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-1 md:grid-cols-3 lg:grid-cols-3 xl:grid-cols-3 gap-8 px-8">
        {agents.map((agent, index) => (
          <div
            key={index}
            className="bg-[#1a1a1a] rounded-lg shadow-lg p-6 flex flex-col items-center text-center text-white transition-transform transform hover:scale-105 cursor-pointer"
            onClick={() => openModal(agent)}
          >
            <img src={agent.image} alt={agent.title} className="w-16 h-16 mb-4" />
            <h3 className="text-xl font-semibold mb-2">{agent.title}</h3>
            <p className="text-md mb-4">{agent.description}</p>
            <button
              className="bg-gradient-to-r from-[#EDDC8F] to-[#F1CA57] text-black px-4 py-2 rounded-md font-semibold"
            >
              More Info
            </button>
          </div>
        ))}
      </div>

      {isModalOpen && selectedAgent && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-75 z-50">
          <div className="bg-[#1a1a1a] w-11/12 md:w-3/4 lg:w-1/2 rounded-lg p-8 text-white relative max-h-screen overflow-y-auto">
            <button
              className="absolute top-2 right-2 text-2xl font-bold"
              onClick={closeModal}
            >
              &times;
            </button>
            <h1 className="mx-auto mb-4 text-4xl font-bold "> {selectedAgent.title} </h1>
            <hr className="h-px mb-4 bg-white border-0 mx-auto" />
            <h2 className="text-2xl font-bold mb-4 bg-gradient-to-r from-[#EDDC8F] to-[#F1CA57] bg-clip-text text-transparent">About</h2>
            <p className="text-lg mb-6">{selectedAgent.details}</p>

            <div className="mb-6">
              <h3 className="text-2xl font-semibold mb-2 bg-gradient-to-r from-[#EDDC8F] to-[#F1CA57] bg-clip-text text-transparent">Features</h3>
              <ul className="list-disc list-inside text-md space-y-2">
                {selectedAgent.features.map((feature, index) => (
                  <li key={index}>{feature}</li>
                ))}
              </ul>
            </div>

            <div className="mb-6">
              <h3 className="text-2xl font-semibold mb-2 bg-gradient-to-r from-[#EDDC8F] to-[#F1CA57] bg-clip-text text-transparent">Use Cases</h3>
              <ul className="list-disc list-inside text-md space-y-2">
                {selectedAgent.useCases.map((useCase, index) => (
                  <li key={index}>{useCase}</li>
                ))}
              </ul>
            </div>

            <div className="mb-8">
              <h3 className="text-2xl font-semibold mb-2 bg-gradient-to-r from-[#EDDC8F] to-[#F1CA57] bg-clip-text text-transparent">Capabilities</h3>
              <p className="text-md leading-relaxed">{selectedAgent.capabilities}</p>
            </div>

            <a
              href={selectedAgent.websiteLink}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-block bg-gradient-to-r from-[#EDDC8F] to-[#F1CA57] text-black px-4 py-2 rounded-md font-semibold mt-4"
            >
              Visit Website
            </a>
          </div>
        </div>
      )}
    </div>
  );
}

export default Registry;
