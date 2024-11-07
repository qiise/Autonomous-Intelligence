import React from "react";

import LPHighLevel from "./LPHighLevel";

function LPHighLevels() {
  return (
    <div className="mx-5 lg:mx-24 mb-10">
      <div className="text-3xl sm:text-4xl lg:text-5xl md:my-2 text-center font-semibold md:font-bold sm:mt-4 md:mt-4">
        How Panacea Works
      </div>
      <h2 className="text-center pt-3">
      Chat with your documents in a privacy preserving way, keeping your data secure.
      </h2>
      <div class="p-10 grid grid-cols-1 md:grid-cols-3 gap-5">
        <LPHighLevel
          image="/landing_page_assets/upload.png"
          title="Upload"
          description="Upload your private documents (PDF, CSV, DOCX, XLSX, HTML, TXT, PPTX supported)."
        />
        <LPHighLevel
          image="/landing_page_assets/chat.png"
          title="Chat"
          description="Ask questions on your documents with LLMs like Llama2, Mistral or fined tuned models."
        />
        <LPHighLevel
          image="/landing_page_assets/evaluate.png"
          title="Evaluate"
          description="Get citations for answers, and ensure the answer is correct to mitigate hallucinations."
        />
      </div>
    </div>
  );
}

export default LPHighLevels;
