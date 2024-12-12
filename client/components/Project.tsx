"use client";
import { useState, useEffect } from "react";
import { Line } from "react-chartjs-2";
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
} from "chart.js";
import { getCsrfToken } from "./getCsrfToken";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

interface Prediction {
    date: string;
    price: number;
}

const boxPlot = [
    {
        name: "",
        img: "/d.png"
    },
    {
        name: "",
        img: "/m.png"
    },
    {
        name: "",
        img: "/q.png"
    },
    {
        name: "",
        img: "/y.png"
    },
]

function Project() {
    const [date, setDate] = useState<string>("");
    const [shortTermPredictions, setShortTermPredictions] = useState<Prediction[]>([]);
    const [longTermPrediction, setLongTermPrediction] = useState<string>("");
    const [loading, setLoading] = useState<boolean>(false);
    const [csrfToken, setCsrfToken] = useState<string>("");
    const [updatedPredictions, setUpdatedPredictions] = useState<Prediction[]>([]);
    const [mappedDate, setMappedDate] = useState<string | null>();
    const [showModal, setShowModal] = useState<boolean>(false);
    const [modalIndex, setModalIndex] = useState<number | null>(null);
    const [modalValues, setModalValues] = useState({
        temperature: 25, // Ideal temperature
        humidity: 50, // Ideal humidity
        precipitation: 10, // Ideal precipitation amount
    });
    const [graph, setGraph] = useState<boolean>(false);

    useEffect(() => {
        const fetchToken = async () => {
            const token = await getCsrfToken();
            setCsrfToken(token);
        };
        fetchToken();
        fetchCurrentWeather();
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
                const predictions: Prediction[] = data.short_term_predictions || [];
                setShortTermPredictions(predictions);
                setLongTermPrediction(data.long_term_prediction || "");
                setUpdatedPredictions(predictions);
                setMappedDate(data.mapped_date);
            }
        } catch (error) {
            console.error("Error:", error);
        } finally {
            setLoading(false);
        }
    };

    const updateHoliday = (index: number) => {
        const updated = [...updatedPredictions];
        updated[index].price *= 1.2;
        setUpdatedPredictions(updated);
    };

    const openModal = (index: number) => {
        setModalIndex(index);
        setShowModal(true);
    };

    const handleModalChange = (field: string, value: number) => {
        setModalValues((prev) => ({ ...prev, [field]: value }));
    };

    const submitModal = () => {
        if (modalIndex !== null) {
            const updated = [...updatedPredictions];
            const { temperature, humidity, precipitation } = modalValues;

            // Adjust the price based on new values
            const adjustmentFactor =
                1 + (temperature - 25) * 0.01 - (humidity - 50) * 0.005 + (precipitation - 10) * 0.002;

            updated[modalIndex].price *= Math.max(0.5, Math.min(1.5, adjustmentFactor)); // Keep adjustments within a realistic range

            setUpdatedPredictions(updated);
        }
        setShowModal(false);
    };

    const chartData = {
        labels: updatedPredictions.map((prediction) => prediction.date),
        datasets: [
            {
                label: "Short-Term Predictions",
                data: updatedPredictions.map((prediction) => prediction.price),
                borderColor: "rgba(75,192,192,1)",
                backgroundColor: "rgba(75,192,192,0.2)",
                fill: true,
                tension: 0.4,
            },
        ],
    };

    const today = new Date().toISOString().split("T")[0];

    const fetchCurrentWeather = async () => {
        try {
            const response = await fetch(
                "http://api.weatherapi.com/v1/current.json?key=e80c903f3a1d42e280b125702233110&q=france&aqi=no"
            );
            const data = await response.json();
            return {
                temperature: data.current.temp_c,
                humidity: data.current.humidity,
                precipitation: data.current.precip_mm,
            };
        } catch (error) {
            console.error("Error fetching weather data:", error);
            return null;
        }
    };

    const handleCurrentWeather = async (index: number) => {
        const weatherData = await fetchCurrentWeather();
        if (weatherData) {
            const updated = [...updatedPredictions];
            const { temperature, humidity, precipitation } = weatherData;

            // Adjust the price using the fetched weather data
            const adjustmentFactor =
                1 + (temperature - 25) * 0.01 - (humidity - 50) * 0.005 + (precipitation - 10) * 0.002;
            updated[index].price *= Math.max(0.5, Math.min(1.5, adjustmentFactor)); // Keep adjustments realistic

            setUpdatedPredictions(updated);
        }
    };


    return (
        <div id="project" className="w-screen h-screen p-4 z-50 relative mt-40 text-white">
            <h1 className="text-4xl">Energy Forecast</h1>
            <div className="flex flex-col w-full min-h-[50vh] h-max gap-2 justify-center items-center">
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
                    Submit
                </button>

                {loading && <p>Running scripts... Please wait.</p>}

                {
                    shortTermPredictions.length > 0 &&
                    <>
                        <div>
                            <h1>Electric Power Consumption overtime:</h1>
                            <div className="w-[80vw]  h-max">

                                <img src="/ea.png" alt="Electric Power Consumption overtime" />

                            </div>
                        </div>
                        <div>
                            <h1>Box Plot:</h1>
                            <div className="w-[80vw] mx-auto grid  grid-cols-2 gap-2 h-max">
                                {boxPlot.map((item, i) => (
                                    <div key={i} >
                                        <p>{item.name}</p>
                                        <img src={item.img} alt={item.name} />
                                    </div>
                                ))}
                            </div>
                        </div>
                    </>
                }

                {shortTermPredictions.length > 0 && (
                    <div>
                        <div className="bg-white p-4">
                            <Line data={chartData} />
                        </div>
                        <div className="mt-4">
                            {updatedPredictions.map((prediction, index) => (
                                <div key={index} className="flex items-center gap-4 mb-2">
                                    <p>{prediction.date}</p>
                                    <button
                                        className="bg-blue-500 px-2 py-1 text-white rounded-md"
                                        onClick={() => updateHoliday(index)}
                                    >
                                        Mark as Holiday
                                    </button>
                                    {
                                        prediction.date === today
                                            ?
                                            <button
                                                className="bg-red-400 px-2 py-1 text-white rounded-md"
                                                onClick={() => handleCurrentWeather(index)}
                                            >
                                                Apply Current Weather Condition
                                            </button>
                                            :
                                            <button
                                                className="bg-green-500 px-2 py-1 text-white rounded-md"
                                                onClick={() => openModal(index)}
                                            >
                                                Improve Weather Condition
                                            </button>
                                    }
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {longTermPrediction && (
                    <p>Long-Term Prediction: {longTermPrediction}</p>
                )}

                {(shortTermPredictions.length > 0 && mappedDate) && (
                    <p>Short-Term Prediction: {shortTermPredictions[0].price}</p>
                )}

                {
                    shortTermPredictions.length > 0 &&
                    <>
                        <div>
                            <h1>7-Fold time series split on Test data</h1>
                            <div className="w-[80vw]  h-max">

                                <img src="/7f.png" alt="7-Fold" />

                            </div>
                        </div>
                    </>
                }
            </div>

            {/* Modal */}
            {showModal && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center text-black">
                    <div className="bg-white p-4 rounded-md w-96">
                        <h2 className="text-xl font-bold mb-4">Adjust Weather Conditions</h2>
                        <div className="flex flex-col gap-2">
                            <label>
                                Temperature:
                                <input
                                    type="number"
                                    value={modalValues.temperature}
                                    onChange={(e) =>
                                        handleModalChange("temperature", parseFloat(e.target.value))
                                    }
                                    className="text-black w-full px-2 py-1 rounded-md"
                                />
                            </label>
                            <label>
                                Humidity:
                                <input
                                    type="number"
                                    value={modalValues.humidity}
                                    onChange={(e) =>
                                        handleModalChange("humidity", parseFloat(e.target.value))
                                    }
                                    className="text-black w-full px-2 py-1 rounded-md"
                                />
                            </label>
                            <label>
                                Precipitation Amount:
                                <input
                                    type="number"
                                    value={modalValues.precipitation}
                                    onChange={(e) =>
                                        handleModalChange("precipitation", parseFloat(e.target.value))
                                    }
                                    className="text-black w-full px-2 py-1 rounded-md"
                                />
                            </label>
                        </div>
                        <div className="flex justify-end mt-4 gap-2">
                            <button
                                className="bg-gray-500 px-4 py-2 text-white rounded-md"
                                onClick={() => setShowModal(false)}
                            >
                                Cancel
                            </button>
                            <button
                                className="bg-green-500 px-4 py-2 text-white rounded-md"
                                onClick={() => submitModal()}
                            >
                                Submit
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default Project;
