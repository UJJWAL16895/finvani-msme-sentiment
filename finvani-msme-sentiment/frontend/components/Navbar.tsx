"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { checkBackendHealth } from "@/lib/apiClient";

function StatusIndicator() {
    const [isOnline, setIsOnline] = useState<boolean | null>(null);

    useEffect(() => {
        const check = async () => {
            const status = await checkBackendHealth();
            setIsOnline(status);
        };

        // Check immediately
        check();

        // Check every 30 seconds
        const interval = setInterval(check, 30000);
        return () => clearInterval(interval);
    }, []);

    if (isOnline === null) return null; // Loading

    return (
        <div className={`flex items-center px-2 py-1 rounded-full text-xs font-medium border ${isOnline
            ? "bg-green-900/30 border-green-500/50 text-green-400"
            : "bg-red-900/30 border-red-500/50 text-red-400"
            }`}>
            <span className={`w-2 h-2 rounded-full mr-2 ${isOnline ? "bg-green-500" : "bg-red-500 animate-pulse"}`}></span>
            {isOnline ? "System Online" : "Backend Offline"}
        </div>
    );
}

export default function Navbar() {
    return (
        <nav className="bg-slate-900 border-b border-slate-800">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between h-16">
                    <div className="flex items-center">
                        <Link href="/" className="flex-shrink-0">
                            <span className="text-xl font-bold bg-gradient-to-r from-blue-400 to-cyan-300 bg-clip-text text-transparent">
                                FinVani AI
                            </span>
                        </Link>

                        {/* Backend Status Indicator */}
                        <div className="ml-4 flex items-center space-x-2">
                            <StatusIndicator />
                        </div>

                        <div className="hidden md:block">
                            <div className="ml-10 flex items-baseline space-x-4">
                                <Link
                                    href="/"
                                    className="text-gray-300 hover:bg-slate-800 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors"
                                >
                                    Dashboard
                                </Link>
                                <Link
                                    href="/headlines"
                                    className="text-gray-300 hover:bg-slate-800 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors"
                                >
                                    Live Feed
                                </Link>
                                <Link
                                    href="/tester"
                                    className="text-gray-300 hover:bg-slate-800 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors"
                                >
                                    Sentiment Tester
                                </Link>
                            </div>
                        </div>
                    </div>

                    {/* Mobile menu button (simple implementation) */}
                    <div className="-mr-2 flex md:hidden">
                        <div className="text-gray-400 hover:text-white p-2">
                            {/* Mobile menu icon placeholder */}
                            <span className="sr-only">Open main menu</span>
                            <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16" />
                            </svg>
                        </div>
                    </div>
                </div>
            </div>
        </nav>
    );
}
