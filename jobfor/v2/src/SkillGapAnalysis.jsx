
const NEO = { boxShadow: "4px 4px 0px 0px #000000" };
const NEO_SM = { boxShadow: "2px 2px 0px 0px #000000" };
const B = "border-2 border-black";

const SKILLS_HAVE = [
  { label: "React.js & Hooks", pct: 95 },
  { label: "TypeScript", pct: 88 },
  { label: "Tailwind CSS", pct: 100 },
  { label: "State Management (Redux)", pct: 75 },
];

const SKILLS_IMPROVE = [
  { label: "Unit Testing (Jest/RTL)", pct: 55 },
  { label: "CI/CD Pipelines", pct: 40 },
];

const SKILLS_MISSING = [
  {
    title: "Micro-frontends",
    badge: "CRITICAL",
    badgeBg: "bg-red-100",
    badgeText: "text-red-600",
    desc: "Required for large scale architecture.",
    time: "12 hours",
  },
  {
    title: "Web Performance",
    badge: "REQUIRED",
    badgeBg: "bg-red-100",
    badgeText: "text-red-600",
    desc: "Core Web Vitals & Optimization strategies.",
    time: "8 hours",
  },
];

const LEARNING_PATH = [
  {
    step: "01",
    bg: "bg-[#1A4D2E]",
    text: "text-white",
    week: "WEEK 1: ADVANCED PATTERNS",
    desc: "Deep dive into Micro-frontends and Module Federation.",
  },
  {
    step: "02",
    bg: "bg-[#D8B4FE]",
    text: "text-black",
    week: "WEEK 2: TESTING STRATEGIES",
    desc: "Mastering React Testing Library and End-to-End testing with Playwright.",
  },
  {
    step: "03",
    bg: "bg-[#FACC15]",
    text: "text-black",
    week: "WEEK 3: PERFORMANCE OPS",
    desc: "Code splitting, image optimization, and caching strategies.",
  },
];

const NAV_LINKS = ["Dashboard", "Skill Gap", "Job Board", "Messages"];

export default function SkillGapAnalysis() {
  return (
    <div className="bg-gray-50 text-black min-h-screen" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>
      <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Syne:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
      <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=swap" rel="stylesheet" />

      {/* MAIN */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">

        {/* Hero row */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-12">
          <div className={`lg:col-span-2 bg-white ${B} p-8`} style={NEO}>
            <p className="text-sm font-bold text-[#1A4D2E] mb-2 uppercase tracking-wider">Target Position</p>
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
              <h1 className="text-3xl md:text-4xl font-extrabold uppercase" style={{ fontFamily: "'Syne', sans-serif" }}>
                Senior Frontend Developer
              </h1>
              <button className={`bg-white ${B} px-4 py-2 flex items-center gap-2 font-bold`} style={NEO_SM}>
                Change Role <span className="material-symbols-outlined">edit</span>
              </button>
            </div>
          </div>

          <div className={`bg-[#D8B4FE] ${B} p-8 flex flex-col justify-center`} style={NEO}>
            <div className="flex justify-between items-end mb-4">
              <h2 className="text-2xl font-extrabold uppercase" style={{ fontFamily: "'Syne', sans-serif" }}>Overall Readiness</h2>
              <span className="text-4xl font-black">72%</span>
            </div>
            <div className={`w-full h-8 bg-white ${B} overflow-hidden`}>
              <div className="h-full bg-[#1A4D2E]" style={{ width: "72%" }}></div>
            </div>
          </div>
        </div>

        {/* Skills Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-12">

          {/* Skills You Have */}
          <div className="space-y-6">
            <div className="flex items-center gap-3">
              <div className={`w-10 h-10 bg-[#1A4D2E] text-white ${B} flex items-center justify-center`}>
                <span className="material-symbols-outlined">check_circle</span>
              </div>
              <h2 className="text-xl font-extrabold uppercase" style={{ fontFamily: "'Syne', sans-serif" }}>Skills You Have</h2>
            </div>
            <div className={`bg-white ${B} p-6 space-y-6`} style={NEO}>
              {SKILLS_HAVE.map(({ label, pct }) => (
                <div key={label}>
                  <div className="flex justify-between mb-2">
                    <span className="font-bold">{label}</span>
                    <span className="font-bold">{pct}%</span>
                  </div>
                  <div className={`w-full h-4 bg-gray-100 ${B} overflow-hidden`}>
                    <div className="h-full bg-[#1A4D2E]" style={{ width: `${pct}%` }}></div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Skills to Improve */}
          <div className="space-y-6">
            <div className="flex items-center gap-3">
              <div className={`w-10 h-10 bg-[#FACC15] text-black ${B} flex items-center justify-center`}>
                <span className="material-symbols-outlined">trending_up</span>
              </div>
              <h2 className="text-xl font-extrabold uppercase" style={{ fontFamily: "'Syne', sans-serif" }}>Skills to Improve</h2>
            </div>
            <div className="space-y-4">
              {SKILLS_IMPROVE.map(({ label, pct }) => (
                <div key={label} className={`bg-white ${B} p-6`} style={NEO}>
                  <div className="flex justify-between mb-4">
                    <span className="font-bold">{label}</span>
                    <span className="font-bold text-[#FACC15]">{pct}%</span>
                  </div>
                  <div className={`w-full h-4 bg-gray-100 ${B} overflow-hidden mb-4`}>
                    <div className="h-full bg-[#D8B4FE]" style={{ width: `${pct}%` }}></div>
                  </div>
                  <button className={`w-full bg-[#D8B4FE] ${B} py-2 font-bold`} style={NEO_SM}>
                    Learn More
                  </button>
                </div>
              ))}
            </div>
          </div>

          {/* Missing Critical Skills */}
          <div className="space-y-6">
            <div className="flex items-center gap-3">
              <div className={`w-10 h-10 bg-red-500 text-white ${B} flex items-center justify-center`}>
                <span className="material-symbols-outlined">warning</span>
              </div>
              <h2 className="text-xl font-extrabold uppercase" style={{ fontFamily: "'Syne', sans-serif" }}>Missing Critical Skills</h2>
            </div>
            <div className="space-y-4">
              {SKILLS_MISSING.map(({ title, badge, badgeBg, badgeText, desc, time }) => (
                <div key={title} className={`bg-white ${B} p-6`} style={NEO}>
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="text-lg font-extrabold uppercase" style={{ fontFamily: "'Syne', sans-serif" }}>{title}</h3>
                    <span className={`${badgeBg} ${badgeText} text-xs px-2 py-1 ${B} font-bold italic`}>{badge}</span>
                  </div>
                  <p className="text-sm text-gray-600 mb-4">{desc}</p>
                  <div className="flex items-center gap-2 mb-4 text-sm font-bold">
                    <span className="material-symbols-outlined text-sm">schedule</span> Est. {time}
                  </div>
                  <button className={`w-full bg-[#1A4D2E] text-white ${B} py-2 font-bold`} style={NEO_SM}>
                    Start Learning
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Learning Path Timeline */}
        <section className={`bg-white ${B} p-8`} style={NEO}>
          <h2 className="text-3xl font-extrabold uppercase mb-8" style={{ fontFamily: "'Syne', sans-serif" }}>
            Personalized Learning Path
          </h2>

          {/* Timeline */}
          <div className="relative space-y-8 before:absolute before:inset-0 before:ml-5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-black">
            {LEARNING_PATH.map(({ step, bg, text, week, desc }, i) => (
              <div
                key={step}
                className={`relative flex items-center justify-between md:justify-normal gap-4 ${i % 2 === 0 ? "md:flex-row-reverse" : ""} group`}
              >
                <div
                  className={`flex items-center justify-center w-10 h-10 ${B} ${bg} ${text} shrink-0 md:order-1 ${i % 2 === 0 ? "md:-translate-x-1/2" : "md:translate-x-1/2"}`}
                >
                  <span className="font-bold">{step}</span>
                </div>
                <div
                  className={`w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] bg-white ${B} p-6`}
                  style={NEO_SM}
                >
                  <time className="font-extrabold text-[#1A4D2E] text-sm block mb-2 uppercase" style={{ fontFamily: "'Syne', sans-serif" }}>
                    {week}
                  </time>
                  <p className="text-gray-600 mb-4">{desc}</p>
                  <a href="#" className="text-black font-bold flex items-center gap-1 hover:underline decoration-2 decoration-[#D8B4FE]">
                    View Resources <span className="material-symbols-outlined text-sm">open_in_new</span>
                  </a>
                </div>
              </div>
            ))}
          </div>
        </section>
      </main>

    </div>
  );
}
