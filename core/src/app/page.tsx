"use client";
import Image from "next/image";
import React, { useEffect, useState } from "react";
import { Line } from "react-chartjs-2";

export default function Home() {

  const [data, setData] = useState([]);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5328");
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const jsonData = await response.json();
      setData(jsonData);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  // console.log(data.results)

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <h1 className="text-6xl font-bold">Summer 2024 Internship Application Tracker</h1>
      <div className="flex flex-col items-center">
        <h2 className="text-4xl font-bold mt-8">Data</h2>
        
        {data.results == null ? <p>Loading...</p> : data.results}

        
      </div>
    </main>
  );
}
