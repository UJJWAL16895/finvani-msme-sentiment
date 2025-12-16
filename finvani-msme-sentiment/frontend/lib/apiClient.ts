export type SentimentResponse = {
    label: "POSITIVE" | "NEGATIVE" | "NEUTRAL" | "UNKNOWN";
    score: number;
};

export type NewsArticle = {
    title: string;
    link: string;
    published_date: string;
    source: string;
    summary?: string;
};

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function analyzeSentiment(text: string): Promise<SentimentResponse> {
    try {
        const response = await fetch(`${API_BASE_URL}/analyze/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ text }),
        });

        if (!response.ok) {
            throw new Error(`API error: ${response.status} ${response.statusText}`);
        }

        const data: SentimentResponse = await response.json();
        return data;
    } catch (error) {
        console.error("Failed to analyze sentiment:", error);
        throw error;
    }
}

export async function fetchHeadlines(lang: string = "en", randomize: boolean = false): Promise<NewsArticle[]> {
    const url = `${API_BASE_URL}/news/latest?lang=${lang}&randomize=${randomize}`;
    try {
        const response = await fetch(url, { cache: 'no-store' });
        if (!response.ok) {
            throw new Error("Failed to fetch news");
        }
        const data = await response.json();
        // Ensure data is array
        if (Array.isArray(data)) {
            return data;
        } else {
            console.error("News data is not an array:", data);
            return [];
        }
    } catch (error) {
        console.error("Error fetching headlines:", error);
        return [];
    }
}

export async function triggerRefresh(): Promise<void> {
    const url = `${API_BASE_URL}/news/refresh`;
    try {
        await fetch(url, { method: "POST" });
    } catch (error) {
        console.error("Error triggering refresh:", error);
    }
}

export async function checkBackendHealth(): Promise<boolean> {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        return response.ok;
    } catch (error) {
        return false;
    }
}
