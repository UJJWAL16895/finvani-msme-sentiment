"use client";

import Link from "next/link";
import { ArrowRight, BarChart2, Zap, Globe, ShieldCheck } from "lucide-react";
import { motion } from "framer-motion";

export default function Home() {
    return (
        <div className="min-h-screen bg-slate-950 text-white overflow-hidden">
            {/* Background Gradients */}
            <div className="absolute top-0 left-0 w-full h-[500px] bg-gradient-to-b from-slate-900 to-transparent -z-10"></div>
            <div className="absolute top-[-100px] left-[-100px] w-[500px] h-[500px] bg-cyan-500/10 rounded-full blur-[100px] pointer-events-none"></div>
            <div className="absolute  bottom-[-100px] right-[-100px] w-[500px] h-[500px] bg-blue-600/10 rounded-full blur-[100px] pointer-events-none"></div>

            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16">

                {/* Hero Section */}
                <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8 }}
                    className="text-center mb-24"
                >
                    <span className="inline-block py-1 px-3 rounded-full bg-slate-800/50 border border-slate-700 text-cyan-400 text-sm font-medium mb-6 backdrop-blur-sm">
                        v1.0 Public Beta
                    </span>
                    <h1 className="text-6xl md:text-7xl font-extrabold tracking-tight mb-8">
                        <span className="block text-white">Sentiment Intelligence for</span>
                        <span className="bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-600 bg-clip-text text-transparent">
                            Modern Finance
                        </span>
                    </h1>
                    <p className="mt-4 max-w-2xl mx-auto text-xl text-slate-400">
                        Advanced NLP models decoding MSME market trends from thousands of diverse data sources in real-time.
                    </p>

                    <div className="mt-10 flex justify-center gap-4">
                        <Link
                            href="/headlines"
                            className="px-8 py-4 bg-blue-600 hover:bg-blue-500 text-white rounded-lg font-semibold flex items-center transition-all shadow-[0_0_20px_-5px_#2563EB] hover:shadow-[0_0_30px_-5px_#2563EB]"
                        >
                            <Zap className="mr-2 h-5 w-5" />
                            Live Dashboard
                        </Link>
                        <Link
                            href="/tester"
                            className="px-8 py-4 bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-200 rounded-lg font-semibold flex items-center transition-all"
                        >
                            Try Model
                            <ArrowRight className="ml-2 h-5 w-5" />
                        </Link>
                    </div>
                </motion.div>

                {/* Feature Showcase */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                    {[
                        {
                            icon: <Globe className="h-8 w-8 text-cyan-400" />,
                            title: "Global Ingestion",
                            desc: "Parses Google News RSS feeds across multiple regions and vernaculars."
                        },
                        {
                            icon: <BarChart2 className="h-8 w-8 text-purple-400" />,
                            title: "Real-time Analytics",
                            desc: "Live sentiment scoring (POS/NEG/NEU) using fine-tuned DistilBERT."
                        },
                        {
                            icon: <ShieldCheck className="h-8 w-8 text-emerald-400" />,
                            title: "Enterprise Grade",
                            desc: "Built on FastAPI and Next.js, dockerized for scalable deployment."
                        }
                    ].map((feature, idx) => (
                        <motion.div
                            key={idx}
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            transition={{ delay: idx * 0.2 }}
                            viewport={{ once: true }}
                            className="p-8 bg-slate-900/50 backdrop-blur-lg border border-slate-800 rounded-2xl hover:border-slate-700 transition-colors"
                        >
                            <div className="mb-6 p-4 bg-slate-950 rounded-xl inline-block border border-slate-800">
                                {feature.icon}
                            </div>
                            <h3 className="text-xl font-bold text-white mb-3">{feature.title}</h3>
                            <p className="text-slate-400 leading-relaxed">
                                {feature.desc}
                            </p>
                        </motion.div>
                    ))}
                </div>

            </div>
        </div>
    );
}
