"use client";

import React, { useState } from "react";
import { analyzeSentiment, SentimentResponse } from "@/lib/apiClient";
import { Loader2 } from "lucide-react";

export default function TesterPage() {
    const [inputText, setInputText] = useState("");
    const [result, setResult] = useState<SentimentResponse | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleAnalyze = async () => {
        if (!inputText.trim()) return;

        setLoading(true);
        setError(null);
        setResult(null);

        try {
            const data = await analyzeSentiment(inputText);
            setResult(data);
        } catch (err) {
            setError("Failed to connect to the backend. Is it running?");
        } finally {
            setLoading(false);
        }
    };

    const getLabelColor = (label: string) => {
        switch (label) {
            case "POSITIVE":
                return "text-green-600 bg-green-50 border-green-200";
            case "NEGATIVE":
                return "text-red-600 bg-red-50 border-red-200";
            default:
                return "text-gray-600 bg-gray-50 border-gray-200";
        }
    };

    return (
        <div className="min-h-screen bg-gray-50 flex flex-col items-center py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-2xl w-full space-y-8">
                <div className="text-center">
                    <h1 className="text-3xl font-extrabold text-gray-900 sm:text-4xl">
                        Sentiment Analyzer Tester
                    </h1>
                    <p className="mt-4 text-lg text-gray-500">
                        Paste a financial headline below to verify the model's prediction.
                    </p>
                </div>

                <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
                    <div className="space-y-6">
                        <div>
                            <label
                                htmlFor="headline"
                                className="block text-sm font-medium text-gray-700"
                            >
                                Headline Text
                            </label>
                            <div className="mt-1">
                                <textarea
                                    id="headline"
                                    name="headline"
                                    rows={4}
                                    className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                                    placeholder="e.g. RBI hikes repo rate, impacting MSME loans..."
                                    value={inputText}
                                    onChange={(e) => setInputText(e.target.value)}
                                />
                            </div>
                        </div>

                        <div>
                            <button
                                onClick={handleAnalyze}
                                disabled={loading || !inputText.trim()}
                                className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                {loading ? (
                                    <>
                                        <Loader2 className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" />
                                        Analyzing...
                                    </>
                                ) : (
                                    "Analyze Sentiment"
                                )}
                            </button>
                        </div>

                        {error && (
                            <div className="rounded-md bg-red-50 p-4">
                                <div className="flex">
                                    <div className="ml-3">
                                        <h3 className="text-sm font-medium text-red-800">Error</h3>
                                        <div className="mt-2 text-sm text-red-700">
                                            <p>{error}</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        )}

                        {result && (
                            <div className={`rounded-md border p-6 ${getLabelColor(result.label)}`}>
                                <div className="flex flex-col items-center">
                                    <span className="text-sm font-medium uppercase tracking-wider opacity-80">
                                        Prediction
                                    </span>
                                    <h2 className="mt-2 text-4xl font-bold tracking-tight">
                                        {result.label}
                                    </h2>
                                    <p className="mt-2 text-lg font-medium opacity-90">
                                        Confidence: {(result.score * 100).toFixed(2)}%
                                    </p>
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}
