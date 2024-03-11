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


  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <h1 className="text-6xl font-bold">Welcome to my website</h1>
      <div className="flex flex-col items-center">
        <h2 className="text-4xl font-bold mt-8">Hi, I'm John Doe</h2>
        <p className="text-2xl text-center mt-4">
          I'm a web developer and I love building websites and web applications.
        </p>
        {data.results}
      </div>
    </main>
  );
}
