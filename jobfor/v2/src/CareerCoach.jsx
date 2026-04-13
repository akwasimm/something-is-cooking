import { useState, useRef, useEffect } from "react";

const NEO = { boxShadow: "4px 4px 0px 0px #000000" };
const NEO_SM = { boxShadow: "2px 2px 0px 0px #000000" };
const NEO_LAV = { boxShadow: "6px 6px 0px 0px #D8B4FE" };
const NEO_GRN = { boxShadow: "6px 6px 0px 0px #1A4D2E" };

const CHAT_HISTORY = [
  { label: "Resume Roast - Tech Lead", time: "2 hours ago", active: true },
  { label: "Salary Negotiation Strategy", time: "Yesterday", active: false },
  { label: "Interview Prep: Amazon", time: "3 days ago", active: false },
];

const SAVED_TIPS = [
  'Use "Situation, Task, Action, Result" for STAR questions.',
  "Always follow up within 24 hours of an interview.",
];

const QUICK_PROMPTS = [
  "[Review Resume]",
  "[Practice Interview]",
  "[Cover Letter]",
  "[Explain Salary Gap]",
];

const INITIAL_MESSAGES = [
  {
    role: "assistant",
    content: null,
    welcome: true,
  },
  {
    role: "user",
    content:
      "I have a Senior Product Designer interview tomorrow at a fintech startup. Can we practice some specific questions?",
  },
  {
    role: "assistant",
    content:
      "Excellent! For a Fintech startup, they'll likely focus on complex data visualization and trust-building. Let's start with this one:\n\n\"Tell me about a time you had to balance strict regulatory requirements with a seamless user experience. How did you handle the trade-offs?\"",
    highlight:
      '"Tell me about a time you had to balance strict regulatory requirements with a seamless user experience. How did you handle the trade-offs?"',
  },
];

const SYSTEM_PROMPT = `You are an expert AI Career Coach for JobFor, a modern job platform. Your name is JobFor Coach.

You help users with:
- Resume review and optimization (bullet point impact, ATS optimization)
- Interview preparation (STAR method, behavioral questions, technical interviews)
- Salary negotiation (data-backed scripts, counteroffer strategies)
- Cover letter writing
- Career pivots and job search strategy

Keep responses concise, practical, and actionable. Use a direct, encouraging tone. When practicing interview questions, provide the question first and then offer feedback after the user responds.

Format your responses clearly. When you ask an interview question, wrap it in quotes and make it stand out. When giving tips, use numbered lists or bullet points.`;

export default function CareerCoach() {
  const [messages, setMessages] = useState(INITIAL_MESSAGES);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);
  const textareaRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [input]);

  const sendMessage = async (text) => {
    const userText = (typeof text === 'string' ? text : input).trim();
    if (!userText || loading) return;
    setInput("");

    const userMsg = { role: "user", content: userText };
    const updatedMessages = [...messages, userMsg];
    setMessages(updatedMessages);
    setLoading(true);

    // Build API message history (exclude welcome/highlight special fields)
    const apiMessages = updatedMessages
      .filter((m) => m.content)
      .map((m) => ({
        role: m.role,
        content: m.role === "assistant" && m.highlight
          ? m.content.replace(`\n\n${m.highlight}`, `\n\n${m.highlight}`)
          : m.content,
      }));

    try {
      const res = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "claude-sonnet-4-20250514",
          max_tokens: 1000,
          system: SYSTEM_PROMPT,
          messages: apiMessages,
        }),
      });
      const data = await res.json();
      const reply = data.content?.map((b) => b.text || "").join("\n") || "Sorry, I couldn't process that. Please try again.";

      // Detect if reply contains a standalone interview question in quotes
      const quoteMatch = reply.match(/"([^"]{40,})"/);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: reply,
          highlight: quoteMatch ? quoteMatch[0] : null,
        },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Connection error. Please try again.", highlight: null },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKey = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div
      className="bg-[#F9FAFB] text-black flex flex-col overflow-hidden"
      style={{ fontFamily: "'Space Grotesk', sans-serif", height: "calc(100vh - 80px)" }}
    >
      <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Syne:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
      <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=swap" rel="stylesheet" />

      {/* BODY */}
      <div className="flex flex-1 overflow-hidden">

        {/* SIDEBAR */}
        <aside className="w-64 border-r-2 border-black bg-white flex-col shrink-0 overflow-y-auto hidden lg:flex">
          <div className="p-4">
            <button
              className="w-full bg-[#1A4D2E] text-white font-bold py-2 px-4 border-2 border-black transition-all hover:translate-x-[2px] hover:translate-y-[2px] flex items-center justify-center gap-2 mb-6"
              style={NEO_SM}
              onClick={() => setMessages(INITIAL_MESSAGES)}
            >
              <span className="material-symbols-outlined">add_comment</span>
              New Session
            </button>

            {/* Chat History */}
            <div className="mb-6">
              <h3 className="text-xs font-black uppercase tracking-widest text-gray-500 mb-3">Chat History</h3>
              <div className="space-y-2">
                {CHAT_HISTORY.map(({ label, time, active }) => (
                  <div
                    key={label}
                    className={`p-3 border-2 border-black cursor-pointer transition-colors ${active ? "bg-[#D8B4FE]/20" : "hover:bg-gray-50"}`}
                    style={active ? NEO_SM : {}}
                  >
                    <p className="font-bold text-sm truncate">{label}</p>
                    <p className="text-[10px] text-gray-500 font-bold uppercase mt-1">{time}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Saved Tips */}
            <div>
              <h3 className="text-xs font-black uppercase tracking-widest text-gray-500 mb-3">Saved Tips</h3>
              <div className="space-y-2">
                {SAVED_TIPS.map((tip) => (
                  <div key={tip} className="flex items-start gap-3 p-3 bg-[#FACC15]/10 border-2 border-dashed border-black">
                    <span className="material-symbols-outlined text-[#FACC15] shrink-0">lightbulb</span>
                    <p className="text-sm font-medium">{tip}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </aside>

        {/* CHAT MAIN */}
        <main className="flex-1 flex flex-col relative bg-gray-50/50 overflow-hidden">

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 md:p-8">
            <div className="max-w-4xl mx-auto space-y-6">
              {messages.map((msg, i) => (
                <ChatMessage key={i} msg={msg} />
              ))}

              {/* Loading bubble */}
              {loading && (
                <div className="flex items-start gap-3">
                  <div className="w-8 h-8 bg-[#D8B4FE] border-2 border-black flex items-center justify-center shrink-0" style={NEO_SM}>
                    <span className="text-lg">🤖</span>
                  </div>
                  <div className="bg-[#D8B4FE]/20 border-2 border-black p-4" style={NEO_SM}>
                    <div className="flex gap-2 items-center">
                      {[0, 1, 2].map((d) => (
                        <div
                          key={d}
                          className="w-2 h-2 bg-[#1A4D2E] rounded-full animate-bounce"
                          style={{ animationDelay: `${d * 0.15}s` }}
                        />
                      ))}
                    </div>
                  </div>
                </div>
              )}
              <div ref={bottomRef} />
            </div>
          </div>

          {/* Input area */}
          <div className="border-t-2 border-black bg-white p-4 shrink-0 z-10 relative">
            <div className="max-w-4xl mx-auto">
              {/* Quick prompts */}
              <div className="flex flex-wrap gap-3 mb-4">
                {QUICK_PROMPTS.map((p) => (
                  <button
                    key={p}
                    className="px-4 py-2 bg-white border-2 border-black font-bold text-xs uppercase tracking-wider transition-all hover:translate-x-[1px] hover:translate-y-[1px]"
                    style={NEO_SM}
                    onClick={() => sendMessage(p.replace(/[\[\]]/g, ""))}
                  >
                    {p}
                  </button>
                ))}
              </div>

              {/* Textarea + send */}
              <div className="relative flex items-end border-2 border-black bg-white" style={NEO}>
                <textarea
                  ref={textareaRef}
                  className="flex-1 p-4 pr-4 font-medium focus:ring-0 focus:outline-none resize-none bg-transparent min-h-[52px] max-h-48 overflow-y-auto"
                  placeholder="Type your question here..."
                  rows={1}
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={handleKey}
                />
                <div className="flex items-center gap-2 p-3 shrink-0">
                  <button className="p-2 hover:bg-gray-100 transition-colors rounded">
                    <span className="material-symbols-outlined text-[20px]">attach_file</span>
                  </button>
                  <button
                    className="bg-[#1A4D2E] text-white font-bold px-4 py-2 border-2 border-black transition-all hover:translate-x-[1px] hover:translate-y-[1px] disabled:opacity-50 disabled:cursor-not-allowed"
                    style={NEO_SM}
                    onClick={() => sendMessage(input)}
                    disabled={loading || !input.trim()}
                  >
                    SEND
                  </button>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}

function ChatMessage({ msg }) {
  const isUser = msg.role === "user";

  if (msg.welcome) {
    return (
      <div className="flex items-start gap-3">
        <div className="w-8 h-8 bg-[#D8B4FE] border-2 border-black flex items-center justify-center shrink-0" style={{ boxShadow: "2px 2px 0px 0px #000" }}>
          <span className="text-lg">🤖</span>
        </div>
        <div className="bg-[#D8B4FE]/20 border-2 border-black p-4 max-w-[85%]" style={{ boxShadow: "4px 4px 0px 0px #D8B4FE" }}>
          <h2 className="text-lg font-black mb-3 uppercase" style={{ fontFamily: "'Syne', sans-serif" }}>
            Welcome back, Jordan!
          </h2>
          <p className="font-medium text-sm mb-3">
            I'm your AI Career Coach. I'm ready to help you land that dream role. What should we focus on today?
          </p>
          <ul className="space-y-2">
            {[
              ["Resume Review", "I'll analyze your bullet points for impact."],
              ["Interview Prep", "Roleplay difficult behavioral questions."],
              ["Salary Negotiation", "Get data-backed scripts for your next offer."],
            ].map(([bold, rest]) => (
              <li key={bold} className="flex items-center gap-2">
                <span className="material-symbols-outlined text-[#1A4D2E] text-sm" style={{fontSize: "16px"}}>check_circle</span>
                <span className="text-sm"><span className="font-bold">{bold}:</span> {rest}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    );
  }

  if (isUser) {
    return (
      <div className="flex items-start gap-3 flex-row-reverse">
        <div className="w-8 h-8 bg-white border-2 border-black flex items-center justify-center shrink-0" style={{ boxShadow: "2px 2px 0px 0px #000" }}>
          <span className="text-lg">👤</span>
        </div>
        <div className="bg-white border-2 border-black p-4 max-w-[85%]" style={{ boxShadow: "4px 4px 0px 0px #1A4D2E" }}>
          <p className="font-bold text-sm whitespace-pre-wrap">{msg.content}</p>
        </div>
      </div>
    );
  }

  // Assistant message — render highlight block if present
  const { content, highlight } = msg;
  let before = content;
  let after = null;

  if (highlight && typeof content === "string") {
    const idx = content.indexOf(highlight);
    if (idx !== -1) {
      before = content.slice(0, idx).trim();
      after = content.slice(idx + highlight.length).trim();
    }
  }

  return (
    <div className="flex items-start gap-3">
      <div className="w-8 h-8 bg-[#D8B4FE] border-2 border-black flex items-center justify-center shrink-0" style={{ boxShadow: "2px 2px 0px 0px #000" }}>
        <span className="text-lg">🤖</span>
      </div>
      <div className="bg-[#D8B4FE]/20 border-2 border-black p-4 max-w-[85%]" style={{ boxShadow: "4px 4px 0px 0px #D8B4FE" }}>
        {before && <p className="font-medium text-sm mb-3 whitespace-pre-wrap">{before}</p>}
        {highlight && (
          <p className="font-black text-sm italic bg-white p-3 border-2 border-black mb-3">{highlight}</p>
        )}
        {after && <p className="font-medium text-sm whitespace-pre-wrap">{after}</p>}
        {!highlight && <p className="font-medium text-sm whitespace-pre-wrap">{content}</p>}
      </div>
    </div>
  );
}
