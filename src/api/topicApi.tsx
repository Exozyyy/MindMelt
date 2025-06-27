import { API_URL } from "../config";

export const postTopicData = async <T>(topic: string): Promise<T> => {
    const response = await fetch(`${API_URL}explain-topic`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ topic })
    });

    if (!response.ok) {
        throw new Error("Failed to fetch");
    }

    return (await response.json()) as T;
};