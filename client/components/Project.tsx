"use client"
import { useState, useEffect } from "react";
import { getCsrfToken } from "./getCsrfToken";

function Project() {
    const [date, setDate] = useState("");
    const [shortTermPrediction, setShortTermPrediction] = useState("");
    const [longTermPrediction, setLongTermPrediction] = useState("");
    const [loading, setLoading] = useState(false);
    const [csrfToken, setCsrfToken] = useState("");

    useEffect(() => {
        const fetchToken = async () => {
            const token = await getCsrfToken();
            console.log("CSRF Token:", token); // Debugging line
            setCsrfToken(token);
        };
        fetchToken();
    }, []);


    const handleAction = async (action: "generate_data" | "see_graph") => {
        setLoading(true);
        try {
            const response = await fetch("http://127.0.0.1:8000/api/forecast/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken,
                },
                body: JSON.stringify({ date, action }),
                credentials: "include",
            });
            const data = await response.json();
            setShortTermPrediction(data.short_term_prediction || "");
            setLongTermPrediction(data.long_term_prediction || "");
        } catch (error) {
            console.error("Error:", error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="w-screen h-screen bg-red-500 z-50 relative text-white">
            <h1>Energy Forecast</h1>
            <input
                type="date"
                className="text-black"
                value={date}
                onChange={(e) => setDate(e.target.value)}
                required
            />
            <button className="text-white px-2 py-1.5 border" onClick={() => handleAction("generate_data")}>
                Generate Augmented Data
            </button>
            <button className="text-white px-2 py-1.5 border" onClick={() => handleAction("see_graph")}>See Graph</button>

            {loading && <p>Running scripts... Please wait.</p>}
            {shortTermPrediction && (
                <p>Short-Term Prediction: {shortTermPrediction}</p>
            )}
            {longTermPrediction && (
                <p>Long-Term Prediction: {longTermPrediction}</p>
            )}
        </div>
    );
}

export default Project;
