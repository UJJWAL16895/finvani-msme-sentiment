"use client";

import React from "react";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from "recharts";

type Props = {
    positive: number;
    neutral: number;
    negative: number;
};

const COLORS = {
    POSITIVE: "#10B981", // Emerald-500
    NEUTRAL: "#22D3EE",  // Cyan-400
    NEGATIVE: "#F43F5E", // Rose-500
};

export default function SentimentChart({ positive, neutral, negative }: Props) {
    const data = [
        { name: "Positive", value: positive, color: COLORS.POSITIVE },
        { name: "Neutral", value: neutral, color: COLORS.NEUTRAL },
        { name: "Negative", value: negative, color: COLORS.NEGATIVE },
    ];

    // Filter out zero values to avoid ugly empty segments
    const activeData = data.filter((d) => d.value > 0);

    if (activeData.length === 0) {
        return (
            <div className="flex h-64 items-center justify-center text-slate-500">
                No data available
            </div>
        );
    }

    return (
        <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                    <Pie
                        data={activeData}
                        cx="50%"
                        cy="50%"
                        innerRadius={60}
                        outerRadius={80}
                        paddingAngle={5}
                        dataKey="value"
                        stroke="none"
                    >
                        {activeData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                    </Pie>
                    <Tooltip
                        contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', borderRadius: '8px', color: '#fff' }}
                        itemStyle={{ color: '#fff' }}
                    />
                </PieChart>
            </ResponsiveContainer>
            <div className="mt-4 flex justify-center gap-6">
                {data.map((item) => (
                    <div key={item.name} className="flex items-center gap-2">
                        <div
                            className="h-3 w-3 rounded-full"
                            style={{ backgroundColor: item.color }}
                        />
                        <span className="text-sm text-slate-400">
                            {item.name} ({item.value})
                        </span>
                    </div>
                ))}
            </div>
        </div>
    );
}
