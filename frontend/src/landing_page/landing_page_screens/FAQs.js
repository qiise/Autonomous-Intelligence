import SideNavBar from "../landing_page_components/SideNavBar";

function FAQs() {
  const entries = [
    "What is Panacea?",
    "What problem are you solving?",
    "How does Panacea work?",
    "How is it Private?",
    "What tasks does Panacea support?",
    "How do you mitigate hallucinations?",
  ];
  const title = "FAQs";

  return (
    <div className="bg-[#141414]">
      <SideNavBar title={title} entries={entries} />
      <div className="w-4/5 mx-auto md:w-7/12 md:ml-20 lg:ml-36 pt-12 lg:pt-20">
        <div className="pt-14">
          <h2 className="text-2xl lg:text-4xl font-['Helvetica_Neue'] font-semibold lg:font-bold text-white">
            Frequently Asked Questions
          </h2>

          {/* What is Panacea? */}
          <h2
            className="bg-gradient-to-r from-[#EDDC8F] to-[#F1CA57] bg-clip-text text-transparent text-2xl lg:text-2xl mb-4 font-['Helvetica_Neue'] Applications-Header"
            id="WhatisPanacea"
          >
            What is Panacea?
          </h2>
          <p className="text-white font-['Helvetica_Neue'] text-xl leading-relaxed mb-6">
            Panacea is a platform for building autonomous agentic systems. Use Panacea to:
            <br /><br />
            <span className="font-bold">Build Agents with memory, knowledge, tools, and reasoning:</span> Panacea manages the agent’s state, memory, and knowledge.
            <br /><br />
            <span className="font-bold">Chat with your Agents using a beautiful Agent UI:</span> Panacea enables local agent execution and session management.
            <br /><br />
            <span className="font-bold">Coordinate teams of Agents:</span> Panacea supports task transfer and orchestrates agent collaboration.
            <br /><br />
            <span className="font-bold">Monitor and optimize Agents:</span> Track key metrics and logs to continuously improve your agents.
            <br /><br />
            <span className="font-bold">Build Agentic systems with integrated infrastructure:</span> Panacea provides both local and cloud support for APIs, databases, and vector databases.
          </p>

          <hr className="h-px my-10 bg-gradient-to-r from-[#EDDC8F] to-[#F1CA57] border-0 mx-auto" />

          {/* What problem are you solving? */}
          <h2
            className="bg-gradient-to-r from-[#EDDC8F] to-[#F1CA57] bg-clip-text text-transparent text-2xl lg:text-2xl mb-4 font-['Helvetica_Neue'] Applications-Header"
            id="Whatproblemareyousolving"
          >
            What problem are you solving?
          </h2>
          <p className="text-white font-['Helvetica_Neue'] text-xl leading-relaxed mb-6">
            Organizations need scalable, secure, and autonomous systems to handle complex workflows and data management. Traditional AI systems struggle to coordinate multiple tasks autonomously, limiting their potential. Panacea solves this by enabling robust autonomous agents that can operate independently, collaborate, and manage private data securely within a controlled environment.
          </p>

          <hr className="h-px my-10 bg-gradient-to-r from-[#EDDC8F] to-[#F1CA57] border-0 mx-auto" />

          {/* How does Panacea work? */}
          <h2
            className="bg-gradient-to-r from-[#EDDC8F] to-[#F1CA57] bg-clip-text text-transparent text-2xl lg:text-2xl mb-4 font-['Helvetica_Neue'] Applications-Header"
            id="HowdoesPanaceawork"
          >
            How does Panacea work?
          </h2>
          <p className="text-white font-['Helvetica_Neue'] text-xl leading-relaxed mb-6">
            Panacea creates autonomous agents with defined roles in a multi-agent environment. Key terms:
            <br /><br />
            <span className="font-bold">interface:</span> A human query interface for task assignments.
            <br />
            <span className="font-bold">node:</span> An individual agent, part of a multi-agent system.
            <br />
            <span className="font-bold">edges:</span> Communication links between agents.
            <br />
            <span className="font-bold">environment:</span> The workspace with task requirements for agents.
            <br />
            <span className="font-bold">orchestrator:</span> Manages tasks and communication across agents.
          </p>

          <hr className="h-px my-10 bg-gradient-to-r from-[#EDDC8F] to-[#F1CA57] border-0 mx-auto" />

          {/* How is it Private? */}
          <h2
            className="bg-gradient-to-r from-[#EDDC8F] to-[#F1CA57] bg-clip-text text-transparent text-2xl lg:text-2xl mb-4 font-['Helvetica_Neue'] Applications-Header"
            id="HowisitPrivate"
          >
            How is it Private?
          </h2>
          <p className="text-white font-['Helvetica_Neue'] text-xl leading-relaxed mb-6">
            Panacea prioritizes data privacy by operating entirely on-premises or within your organization’s private cloud. Agents can process sensitive data locally without exposing it to external servers. Panacea supports private databases and local models, ensuring data remains within your secure environment, complying with industry-grade security standards.
          </p>

          <hr className="h-px my-10 bg-gradient-to-r from-[#EDDC8F] to-[#F1CA57] border-0 mx-auto" />

          {/* What tasks does Panacea support? */}
          <h2
            className="bg-gradient-to-r from-[#EDDC8F] to-[#F1CA57] bg-clip-text text-transparent text-2xl lg:text-2xl mb-4 font-['Helvetica_Neue'] Applications-Header"
            id="WhattasksdoesPanaceasupport"
          >
            What tasks does Panacea support?
          </h2>
          <p className="text-white font-['Helvetica_Neue'] text-xl leading-relaxed mb-6">
            Panacea supports a range of tasks through autonomous agents, including:
            <br /><br />
            <span className="font-bold">Document Management:</span> Upload, process, and query documents locally or via APIs like EDGAR.
            <br /><br />
            <span className="font-bold">Data Processing:</span> Handle complex workflows in finance, healthcare, and more by securely analyzing data.
          </p>

          <hr className="h-px my-10 bg-gradient-to-r from-[#EDDC8F] to-[#F1CA57] border-0 mx-auto" />

          {/* How do you mitigate hallucinations? */}
          <h2
            className="bg-gradient-to-r from-[#EDDC8F] to-[#F1CA57] bg-clip-text text-transparent text-2xl lg:text-2xl mb-4 font-['Helvetica_Neue'] Applications-Header"
            id="Howdoyoumitigatehallucinations"
          >
            How do you mitigate hallucinations?
          </h2>
          <p className="text-white font-['Helvetica_Neue'] text-xl leading-relaxed mb-6">
            To reduce inaccuracies, Panacea employs advanced techniques like Retrieval-Augmented Generation (RAG) and domain-specific fine-tuning. Agents retrieve relevant information from trusted data sources, minimizing reliance on model-generated content alone. Panacea’s fine-tuning improves the reliability of agents, providing citations and evidence to support generated answers, ensuring transparency and accuracy.
          </p>

        </div>
      </div>
    </div>
  );
}

export default FAQs;
