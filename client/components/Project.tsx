"use client";

import { useState, useEffect } from "react";
import { getCsrfToken } from "./getCsrfToken";
import { Line } from "react-chartjs-2";
import {
    Chart as ChartJS,
    LineElement,
    PointElement,
    LinearScale,
    CategoryScale,
    Tooltip,
    Legend,
} from "chart.js";

// Register Chart.js components
ChartJS.register(LineElement, PointElement, LinearScale, CategoryScale, Tooltip, Legend);

interface ShortTermPrediction {
    date: string;
    price: number;
}

function Project() {
    const [date, setDate] = useState<string>("");
    const [shortTermPredictions, setShortTermPredictions] = useState<ShortTermPrediction[]>([]);
    const [longTermPrediction, setLongTermPrediction] = useState<string>("");
    const [loading, setLoading] = useState<boolean>(false);
    const [csrfToken, setCsrfToken] = useState<string>("");

    useEffect(() => {
        const fetchToken = async () => {
            const token = await getCsrfToken();
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
            if (action === "generate_data") {
                setShortTermPredictions(data.short_term_predictions || []);
                setLongTermPrediction(data.long_term_prediction || "");
            }
        } catch (error) {
            console.error("Error:", error);
        } finally {
            setLoading(false);
        }
    };
    const chartData = {
        labels: shortTermPredictions.map(prediction => prediction.date), // Dates returned from the backend
        datasets: [
            {
                label: "Short-Term Predictions",
                data: shortTermPredictions.map(prediction => prediction.price),
                borderColor: "rgba(75,192,192,1)",
                backgroundColor: "rgba(75,192,192,0.2)",
                fill: true,
                tension: 0.4,
            },
        ],
    };



    return (
        <div id="project" className="w-screen h-screen p-4 z-50 relative mt-40 text-white">
            <h1 className="text-4xl">Energy Forecast</h1>
            <div className="flex flex-col w-full h-[50vh] gap-2 justify-center items-center">
                <input
                    type="date"
                    className="text-black w-60 px-2 py-1.5 rounded-md"
                    value={date}
                    onChange={(e) => setDate(e.target.value)}
                    required
                />
                <button
                    className="text-white px-2 w-80 py-1.5 border rounded-md"
                    onClick={() => handleAction("generate_data")}
                >
                    Generate Augmented Data
                </button>

                {loading && <p>Running scripts... Please wait.</p>}
                {shortTermPredictions.length > 0 && (
                    <div>
                        <Line data={chartData} />
                    </div>
                )}
                {longTermPrediction && (
                    <p>Long-Term Prediction: {longTermPrediction}</p>
                )}
            </div>
        </div>
    );
}

export default Project;
