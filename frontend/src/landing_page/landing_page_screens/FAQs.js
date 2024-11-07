import SideNavBar from "../landing_page_components/SideNavBar";


function FAQs() {
  var entries = [
    "What is Private Chatbot?",
    "What problem are you solving?",
    "How does Private Chatbot work?",
    "How is it Private?",
    "What tasks do Private Chatbot support?",
    "How do you mitigate hallucinations?",
  ];
  var title = "FAQs";
  return (
    <div className="bg-[#141414]
 ">
      <SideNavBar title={title} entries={entries} />
      <div className="w-4/5 mx-auto md:w-7/12 md:ml-20 lg:ml-36 pt-12 lg:pt-20">
        <div className="pt-14">
          <h2 className="text-2xl lg:text-4xl font-['Helvetica_Neue'] font-semibold lg:font-bold text-white">
            Frequently Asked Questions
          </h2>
          <h2
            className="bg-clip-text text-transparent bg-gradient-to-r from-[#40C6FF] to-[#28B2FB] text-2xl lg:text-2xl mb-4 font-['Helvetica_Neue'] Applications-Header"
            id="WhatisPrivateChatbot"
          >
            What is Private Chatbot?
          </h2>
          <p className="text-white font-['Helvetica_Neue'] text-xl">
            Private Chatbot is an AI-powered chatbot that is able to answer questions from private documents with more accuracy than a generalized LLM. The Private Chatbot is an AI Assistant that is intended to help reduce the time and effort human analysts have to spend manually extracting information from unstructured documents.
          </p>
          <hr class="h-px my-10 bg-[#40C6FF] border-0 mx-auto"></hr>
          <h2
            className="bg-clip-text text-transparent bg-gradient-to-r from-[#40C6FF] to-[#28B2FB] text-2xl lg:text-2xl mb-4 font-['Helvetica_Neue'] Applications-Header"
            id="Whatproblemareyousolving"
          >
            What problem are you solving?
          </h2>
            <p className="text-white font-['Helvetica_Neue'] text-xl">
            Financial enterprises want to leverage Generative AI for analytics purposes, but have sensitive data that can not be shared off-premises to LLMs like ChatGPT. Financial Enterprises want to leverage LLMs and Generative AI for analytics, while keeping their data private and secure.
            </p>
        </div>
        <hr class="h-px my-10 bg-[#40C6FF] border-0 mx-auto"></hr>
        <h2
            className="bg-clip-text text-transparent bg-gradient-to-r from-[#40C6FF] to-[#28B2FB] text-2xl lg:text-2xl mb-4 font-['Helvetica_Neue'] Applications-Header"
            id="HowdoesPrivateChatbotwork"
          >
            How does Private Chatbot work?
          </h2>
        <p className="text-white font-['Helvetica_Neue'] text-xl">
            To use Private Chatbot, there are 3 main steps:
            <br></br>
            <br></br>
            <span className="font-bold">1. Upload:</span> Upload your documents (PDF, DOCX, PPTX, TXT, CSV, XLSX) to a local silo.
            <br></br>
            <span className="font-bold">2. Chat:</span> Ask questions on your documents. Get answers and converse with your data.
            <br></br>
            <span className="font-bold">3. Evaluate:</span> View relevant / accurate citations to ensure the models answers are correct.
        </p>
        <hr class="h-px my-10 bg-[#40C6FF] border-0 mx-auto"></hr>
        <h2
            className="bg-clip-text text-transparent bg-gradient-to-r from-[#40C6FF] to-[#28B2FB] text-2xl lg:text-2xl mb-4 font-['Helvetica_Neue'] Applications-Header"
            id="HowisitPrivate"
          >
            How is it Private?
          </h2>
        <p className="text-white font-['Helvetica_Neue'] text-xl">
        Uploaded data is stored locally, on premise, for enterprise grade security. Connect to data within your local mysql database. LLMs like GPT4All and Llama2 run locally on your device. All queries stay on your computer, never leaving your private, secure data silo.
        </p>
        <hr class="h-px my-10 bg-[#40C6FF] border-0 mx-auto"></hr>
        <h2
            className="bg-clip-text text-transparent bg-gradient-to-r from-[#40C6FF] to-[#28B2FB] text-2xl lg:text-2xl mb-4 font-['Helvetica_Neue'] Applications-Header"
            id="WhattasksdoPrivateChatbotsupport"
          >
            What tasks do Private Chatbot support?
          </h2>

        <p className="text-white font-['Helvetica_Neue'] text-xl">
            On Private Chatbot, you can either upload your own documents, or connect to financial documents within the EDGAR API.
            <br></br>
        <br></br>
        <span className="font-bold">Upload Documents:</span> User can upload documents such as PDFs, DOCXs, TXTs, PPTXs, etc. locally from their computer and query questions based off of it.
        <br></br>
        <br></br>
        <span className="font-bold">Query from EDGAR API:</span> With the SEC's EDGAR API, users can enter a company ticker and retrieve relevant financial documents, then query questions.
        </p>
        <hr class="h-px my-10 bg-[#40C6FF] border-0 mx-auto"></hr>
        <h2
            className="bg-clip-text text-transparent bg-gradient-to-r from-[#40C6FF] to-[#28B2FB] text-2xl lg:text-2xl mb-4 font-['Helvetica_Neue'] Applications-Header"
            id="Howdoyoumitigatehallucinations"
          >
            How do you mitigate hallucinations?
          </h2>
        <p className="text-white font-['Helvetica_Neue'] text-xl">
        To mitigate hallucinations, we employ novel research techniques in fine tuning and retrieval augmented generation to provide more accurate answers as well as robust citations.
        <br></br>
        <br></br>
        <span className="font-bold">Fine Tuning LLMs for Accurate Answers:</span> To mitigate hallucinations, we leverage parameter efficient fine tuning with techniques such as LORA and Q-LORA for private LLMs such as Llama2. We have benchmarked LLMs with evaluation metrics such as rouge-l, LLM eval, cosine similarity and bleu score, and have shown that fine tuning significantly enhances the accuracy of the answers for your specific dataset.
        <br></br>
        <br></br>
        <span className="font-bold">Enhanced Retrieval for Accurate Citations:</span> To mitigate hallucinations, you can view the text from the specific document and page number where the model's answer came from. To ensure our model finds the right chunk for the citation, we have done a lot of research on how LLMs use retrieval augmented generation, and have benchmarked a variety of retrieval techniques such as HyDE and FLARE.
        </p>
        <hr class="h-px my-10 bg-[#40C6FF] border-0 mx-auto"></hr>
        <br></br>
        <br></br>
      </div>
    </div>
  );
}

export default FAQs;
