"use client";

import React, { useEffect, useState } from "react";
import { fetchHeadlines, NewsArticle, analyzeSentiment, triggerRefresh } from "@/lib/apiClient";
import SentimentChart from "@/components/SentimentChart";
import { motion } from "framer-motion";
import { Loader2, TrendingUp, AlertTriangle, ExternalLink, RefreshCw, Globe } from "lucide-react";

type EnrichedArticle = NewsArticle & {
    sentiment?: {
        label: string;
        score: number;
    };
};

const LANGUAGES = [
    { code: "en", name: "English" },
    { code: "hi", name: "Hindi (हिंदी)" },
    { code: "bn", name: "Bengali (বাংলা)" },
    { code: "te", name: "Telugu (తెలుగు)" },
    { code: "mr", name: "Marathi (मराठी)" },
    { code: "ta", name: "Tamil (தமிழ்)" },
    { code: "ur", name: "Urdu (اردو)" },
    { code: "gu", name: "Gujarati (ગુજરાતી)" },
    { code: "kn", name: "Kannada (ಕನ್ನಡ)" },
    { code: "ml", name: "Malayalam (മലയാളം)" },
    { code: "or", name: "Odia (ଓଡ଼ିଆ)" },
    { code: "pa", name: "Punjabi (ਪੰਜਾਬੀ)" },
    { code: "as", name: "Assamese (অসমীয়া)" },
    { code: "mai", name: "Maithili (मैथिली)" },
    { code: "sat", name: "Santali (संताली)" },
    { code: "ks", name: "Kashmiri (कश्मीरी)" },
    { code: "ne", name: "Nepali (नेपाली)" },
    { code: "doi", name: "Dogri (डोगरी)" },
    { code: "gom", name: "Konkani (कोंकणी)" },
    { code: "sd", name: "Sindhi (सिंधी)" },
    { code: "mni", name: "Manipuri (মণিপুরী)" },
    { code: "sa", name: "Sanskrit (संस्कृत)" },
];

export default function HeadlinesPage() {
    const [articles, setArticles] = useState<EnrichedArticle[]>([]);
    const [loading, setLoading] = useState(true);
    const [metrics, setMetrics] = useState({ pos: 0, neg: 0, neu: 0 });
    const [selectedLang, setSelectedLang] = useState("en");

    async function loadData(randomize: boolean = false) {
        setLoading(true);
        try {
            const data = await fetchHeadlines(selectedLang, randomize);

            // Analyze top 10 articles concurrently for sentiment
            // Note: Model is English-based, so results on non-English might be inaccurate without translation.
            // Displaying raw result for now as requested.
            const topBatch = data.slice(0, 10);
            const enriched = await Promise.all(
                data.map(async (art, idx) => {
                    if (idx < 10) {
                        try {
                            const res = await analyzeSentiment(art.title);
                            return { ...art, sentiment: res };
                        } catch {
                            return art;
                        }
                    }
                    return art;
                })
            );

            setArticles(enriched);

            let p = 0, n = 0, u = 0;
            enriched.forEach(a => {
                // Type guard or check existence
                const s = (a as EnrichedArticle).sentiment;
                if (s?.label === "POSITIVE") p++;
                else if (s?.label === "NEGATIVE") n++;
                else if (s?.label === "NEUTRAL") u++;
            });
            setMetrics({ pos: p, neg: n, neu: u });

        } catch (e) {
            console.error("Fetch error:", e);
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        loadData();
    }, [selectedLang]); // Reload when language changes

    const container = {
        hidden: { opacity: 0 },
        show: {
            opacity: 1,
            transition: {
                staggerChildren: 0.1
            }
        }
    };

    const item = {
        hidden: { opacity: 0, y: 20 },
        show: { opacity: 1, y: 0 }
    };

    async function handleRefresh() {
        setLoading(true);
        try {
            // Trigger backend ingestion
            await triggerRefresh();
            // Wait 2 seconds for backend to start processing
            await new Promise(r => setTimeout(r, 2000));
            // Then load data with randomization to show new results
            await loadData(true);
        } catch (e) {
            console.error(e);
            setLoading(false);
        }
    }

    // ... inside render ...

    return (
        <div className="min-h-screen bg-slate-950 text-white p-6 lg:p-12">
            <div className="max-w-7xl mx-auto space-y-12">
                {/* Header Section */}
                <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-8 border-b border-slate-800 pb-8">
                    <div>
                        <h1 className="text-4xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
                            Live Market Sentiment
                        </h1>
                        <p className="mt-2 text-slate-400">
                            Real-time analysis of financial headlines impacting the MSME sector.
                        </p>
                    </div>

                    <div className="flex flex-wrap gap-4 items-center">
                        {/* Language Selector */}
                        <div className="flex items-center gap-2 bg-slate-900 border border-slate-700 rounded-lg px-3 py-2">
                            <Globe className="h-4 w-4 text-slate-400" />
                            <select
                                value={selectedLang}
                                onChange={(e) => setSelectedLang(e.target.value)}
                                className="bg-transparent border-none text-sm focus:ring-0 text-white [&>option]:text-black"
                            >
                                {LANGUAGES.map(lang => (
                                    <option key={lang.code} value={lang.code}>{lang.name}</option>
                                ))}
                            </select>
                        </div>

                        <button
                            onClick={handleRefresh}
                            className="p-2 bg-slate-800 hover:bg-slate-700 rounded-lg transition-colors border border-slate-700 text-slate-300"
                            title="Force Refresh Data"
                        >
                            <RefreshCw className={`h-5 w-5 ${loading ? 'animate-spin' : ''}`} />
                        </button>

                        <div className="hidden md:flex gap-4">
                            <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl flex items-center gap-3">
                                <div className="p-2 bg-emerald-500/10 rounded-lg">
                                    <TrendingUp className="text-emerald-400 h-6 w-6" />
                                </div>
                                <div>
                                    <p className="text-xs text-slate-500 uppercase tracking-wider">Bullish Signal</p>
                                    <p className="font-bold text-lg text-emerald-400">
                                        {metrics.pos > metrics.neg ? 'Strong' : 'Moderate'}
                                    </p>
                                </div>
                            </div>
                            <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl flex items-center gap-3">
                                <div className="p-2 bg-rose-500/10 rounded-lg">
                                    <AlertTriangle className="text-rose-400 h-6 w-6" />
                                </div>
                                <div>
                                    <p className="text-xs text-slate-500 uppercase tracking-wider">Risk Level</p>
                                    <p className="font-bold text-lg text-rose-400">
                                        {metrics.neg > 2 ? 'High' : 'Low'}
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Charts Section */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                    <div className="md:col-span-1 bg-slate-900/50 backdrop-blur-md border border-slate-800 rounded-2xl p-6">
                        <h3 className="text-lg font-semibold mb-6">Sentiment Distribution</h3>
                        <SentimentChart
                            positive={metrics.pos}
                            neutral={metrics.neu}
                            negative={metrics.neg}
                        />
                    </div>
                    <div className="md:col-span-2 bg-slate-900/50 backdrop-blur-md border border-slate-800 rounded-2xl p-6 relative overflow-hidden flex flex-col justify-center">
                        <div className="absolute top-0 right-0 p-32 bg-blue-500/10 rounded-full blur-3xl -mr-16 -mt-16 pointer-events-none"></div>
                        <h3 className="text-lg font-semibold mb-6">Market Insights ({LANGUAGES.find(l => l.code === selectedLang)?.name})</h3>
                        <p className="text-slate-300 leading-relaxed text-lg">
                            {articles.length === 0 ? "No data found for this language. Run ingestion script." : (
                                <>
                                    The current market sentiment in <strong>{LANGUAGES.find(l => l.code === selectedLang)?.name}</strong> media indicates
                                    a {metrics.pos > metrics.neg ? "Positive" : "Mixed"} outlook.
                                    Tracking {metrics.pos} positive signals against {metrics.neg} risks.
                                </>
                            )}
                        </p>
                        <div className="mt-6 flex gap-3">
                            <span className="text-xs font-mono text-cyan-400 bg-cyan-900/30 px-2 py-1 rounded">
                                Total: {articles.length} headlines
                            </span>
                            <span className="text-xs font-mono text-emerald-400 bg-emerald-900/30 px-2 py-1 rounded">
                                Analyzed: {Math.min(articles.length, 10)}
                            </span>
                        </div>
                    </div>
                </div>

                {/* News Grid */}
                <div>
                    <div className="flex justify-between items-center mb-6">
                        <h2 className="text-2xl font-bold">Latest Headlines ({selectedLang.toUpperCase()})</h2>
                    </div>

                    {loading ? (
                        <div className="flex justify-center py-20">
                            <Loader2 className="h-10 w-10 animate-spin text-cyan-400" />
                        </div>
                    ) : (
                        <motion.div
                            variants={container}
                            initial="hidden"
                            animate="show"
                            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
                        >
                            {articles.map((article, idx) => (
                                <motion.div
                                    key={idx}
                                    variants={item}
                                    whileHover={{ scale: 1.02, translateY: -5 }}
                                    className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-lg hover:shadow-cyan-500/10 transition-all group flex flex-col h-full"
                                >
                                    <div className="flex justify-between items-start mb-4">
                                        <span className="text-xs font-mono text-slate-500 bg-slate-800 px-2 py-1 rounded">
                                            {article.source || "Google News"}
                                        </span>
                                        {article.sentiment && (
                                            <div className="flex items-center gap-2 bg-slate-950 px-2 py-1 rounded-full border border-slate-800">
                                                <div className={`h-2 w-2 rounded-full ${article.sentiment.label === 'POSITIVE' ? 'bg-emerald-500 shadow-[0_0_8px_#10B981]' :
                                                    article.sentiment.label === 'NEGATIVE' ? 'bg-rose-500 shadow-[0_0_8px_#F43F5E]' :
                                                        'bg-cyan-400 shadow-[0_0_8px_#22D3EE]'
                                                    }`}></div>
                                                <span className={`text-xs font-bold ${article.sentiment.label === 'POSITIVE' ? 'text-emerald-400' :
                                                    article.sentiment.label === 'NEGATIVE' ? 'text-rose-400' :
                                                        'text-cyan-400'
                                                    }`}>
                                                    {article.sentiment.label} ({Math.round(article.sentiment.score * 100)}%)
                                                </span>
                                            </div>
                                        )}
                                    </div>

                                    <h3 className="text-lg font-medium text-slate-200 mb-3 line-clamp-3 group-hover:text-cyan-300 transition-colors flex-grow">
                                        {article.title}
                                    </h3>

                                    <div className="flex justify-between items-end mt-4 pt-4 border-t border-slate-800/50">
                                        <span className="text-xs text-slate-600">{new Date(article.published_date || "").toLocaleDateString()}</span>
                                        <a
                                            href={article.link}
                                            target="_blank"
                                            rel="noreferrer"
                                            className="text-slate-400 hover:text-white transition-colors"
                                        >
                                            <ExternalLink className="h-4 w-4" />
                                        </a>
                                    </div>
                                </motion.div>
                            ))}
                        </motion.div>
                    )}
                </div>
            </div>
        </div>
    );
}
