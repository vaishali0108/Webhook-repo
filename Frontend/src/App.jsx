// src/App.jsx
import { useState, useEffect } from "react";
import "./App.css";

function App() {
  const [events, setEvents] = useState([]);

  const fetchEvents = async () => {
    try {
      const res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/events`);
      const data = await res.json();
      setEvents(data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchEvents(); // First call immediately

    const interval = setInterval(() => {
      fetchEvents();
    }, 15000); // every 15 seconds

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 p-6 flex flex-col items-center">
      <h1 className="text-3xl font-bold mb-8 text-gray-800">GitHub Webhook Events</h1>

      <div className="w-full max-w-3xl space-y-4">
        {events.length === 0 && (
          <p className="text-center text-gray-500">No events yet. Waiting for GitHub actions...</p>
        )}

        {events.map((e, i) => (
          <div
            key={i}
            className="bg-white p-5 rounded-xl shadow-md border-l-4 border-blue-500 transition-transform transform hover:scale-105"
          >
            <p className="text-sm text-gray-700 font-medium">{e.message}</p>
            <p className="mt-2 text-xs text-gray-400">
              Saved at: {new Date(e.timestamp).toLocaleString()}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
