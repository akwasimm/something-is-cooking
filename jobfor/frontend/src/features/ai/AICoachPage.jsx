import { useState, useEffect, useRef } from 'react';
import { useAuth } from '../../context/AuthContext';
import { streamAiChat } from '../../api';
import styles from './AICoachPage.module.css';

const TIPS = [
    { icon: 'lightbulb', tip: 'Add in-demand skills from job descriptions to boost your profile match score.', category: 'Profile Boost' },
    { icon: 'trending_up', tip: 'Apply to companies with 15–50 employees — acceptance rates are 3× higher for mid-level roles.', category: 'Strategy' },
    { icon: 'schedule', tip: 'Best time to apply is Tuesday–Thursday 9AM–11AM for faster responses.', category: 'Timing' },
];

const QUICK_ACTIONS = [
    { icon: 'description', label: 'Review Resume',     prompt: 'Can you review my resume and give me specific improvement tips?' },
    { icon: 'mic',         label: 'Mock Interview',    prompt: 'Let\'s do a mock interview for a senior software engineer role.' },
    { icon: 'edit_note',   label: 'Cover Letter',      prompt: 'Help me write a compelling cover letter for a technology company.' },
    { icon: 'payments',    label: 'Salary Negotiation', prompt: 'Give me tips on how to negotiate my salary effectively in a job offer.' },
];

export default function AICoachPage() {
    const { user } = useAuth();
    const firstName = user?.profile?.firstName || user?.email?.split('@')[0] || 'there';
    const [messages, setMessages] = useState([
        {
            from: 'ai',
            text: `Hi ${firstName}! 👋 I'm your AI Career Coach. I can help you with interview prep, resume feedback, salary negotiation, and job search strategy.\n\nWhat would you like to work on today?`,
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        },
    ]);
    const [input, setInput] = useState('');
    const [sending, setSending] = useState(false);
    const endRef = useRef(null);

    useEffect(() => { endRef.current?.scrollIntoView({ behavior: 'smooth' }); }, [messages]);

    const sendMessage = async (overrideText) => {
        const text = (overrideText ?? input).trim();
        if (!text || sending) return;
        const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        setMessages(prev => [...prev, { from: 'user', text, time }]);
        if (!overrideText) setInput('');
        setSending(true);

        const aiMsgId = Date.now();
        setMessages(prev => [...prev, { id: aiMsgId, from: 'ai', text: '', time }]);

        try {
            await streamAiChat(text, null, (token) => {
                setMessages(prev =>
                    prev.map(m => m.id === aiMsgId ? { ...m, text: m.text + token } : m)
                );
            });
        } catch {
            setMessages(prev =>
                prev.map(m =>
                    m.id === aiMsgId
                        ? { ...m, text: "I'm having trouble connecting right now. Please ensure the backend is running and your OpenAI key is configured in `.env`." }
                        : m
                )
            );
        } finally {
            setSending(false);
        }
    };

    return (
        <div className={styles.page}>
            {/* ── Insight Cards ──────────────────────────────── */}
            <div className={styles.tipsGrid}>
                {TIPS.map((t, i) => (
                    <div key={i} className={styles.tipCard}>
                        <span className={`material-symbols-outlined ${styles.tipIcon}`}>{t.icon}</span>
                        <div>
                            <span className={styles.tipCategory}>{t.category}</span>
                            <p>{t.tip}</p>
                        </div>
                    </div>
                ))}
            </div>

            {/* ── Chat Section ──────────────────────────────── */}
            <section className={styles.chatSection}>
                {/* Header */}
                <div className={styles.chatHeader}>
                    <div className={styles.aiAvatar}>
                        <span className="material-symbols-outlined">smart_toy</span>
                    </div>
                    <div>
                        <h2>JobFor AI Coach</h2>
                        <span className={styles.onlineBadge}>
                            <span />
                            Online · Powered by AI
                        </span>
                    </div>
                </div>

                {/* Messages */}
                <div className={styles.messages}>
                    {messages.map((m, i) => (
                        <div key={i} className={`${styles.message} ${m.from === 'user' ? styles.userMsg : styles.aiMsg}`}>
                            {m.from === 'ai' && (
                                <div className={styles.msgAvatar}>
                                    <span className="material-symbols-outlined">smart_toy</span>
                                </div>
                            )}
                            <div className={styles.msgBubble}>
                                {m.from === 'ai' && m.text === '' && sending ? (
                                    <div className={styles.typingDot}>
                                        <span /><span /><span />
                                    </div>
                                ) : (
                                    <p>{m.text}</p>
                                )}
                                <span className={styles.msgTime}>{m.time}</span>
                            </div>
                        </div>
                    ))}
                    <div ref={endRef} />
                </div>

                {/* Quick Action Buttons */}
                <div className={styles.quickActions}>
                    {QUICK_ACTIONS.map((qa, i) => (
                        <button
                            key={i}
                            className={styles.quickBtn}
                            onClick={() => sendMessage(qa.prompt)}
                            disabled={sending}
                        >
                            <span className="material-symbols-outlined">{qa.icon}</span>
                            {qa.label}
                        </button>
                    ))}
                </div>

                {/* Input */}
                <div className={styles.chatInput}>
                    <input
                        type="text"
                        placeholder="Ask your AI Coach anything…"
                        value={input}
                        onChange={e => setInput(e.target.value)}
                        onKeyDown={e => e.key === 'Enter' && sendMessage()}
                        disabled={sending}
                    />
                    <button className={styles.sendBtn} onClick={() => sendMessage()} disabled={sending}>
                        <span className="material-symbols-outlined">send</span>
                    </button>
                </div>
            </section>
        </div>
    );
}
