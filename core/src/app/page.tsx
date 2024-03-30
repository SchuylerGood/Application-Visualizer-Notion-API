"use client";
import Image from "next/image";
import React, { useEffect, useState } from "react";
import { Line } from "react-chartjs-2";
import { Client } from "@notionhq/client";

// Components
import BarChart from "@/components/BarChart";
import DoughnutChart from "@/components/DoughnutChart";

export default function Home() {
  const [data, setData] = useState(null);
  const [hasMore, setHasMore] = useState(false);
  const [nextCursor, setNextCursor] = useState(null);


  useEffect(() => {
    // Fetch data from the server when the component mounts
    fetch('http://localhost:3001/')
      .then(response => response.json())
      .then(data => {
        setData(data);
        // console.log(data[0]);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  }, []);



  // THIS IS USED FOR THE PYTHON FLASK SERVER
  // const [data, setData] = useState([]);

  // useEffect(() => {
  //   fetchData();
  // }, []);

  // const fetchData = async () => {
  //   try {
  //     const response = await fetch("http://127.0.0.1:5328");
  //     if (!response.ok) {
  //       throw new Error("Network response was not ok");
  //     }
  //     const jsonData = await response.json();
  //     setData(jsonData);
  //   } catch (error) {
  //     console.error("Error fetching data:", error);
  //   }
  // };
  const flaskData = (data: any) => {
    return(
      <>
        <div className="flex flex-col items-center">
          <h1>Python Flask Data</h1>
          {data.results == null ? <p>Loading...</p> : data.results}
        </div>
      </>
    )
  }


  return (
    <main className="flex flex-col items-center">
      <h1 className="text-6xl font-bold">Summer 2024 Internship Application Tracker</h1>
      
      <div className="w-full flex flex-row justify-center space-x-8">
        <div className="bg-gray-300 rounded-2xl p-8 w-auto h-[600px] m-8">
          <h1 className="text-4xl font-bold">Number of Applications</h1>
          <BarChart data={data}/>
        </div>
        
        <div className="bg-gray-300 rounded-2xl p-8 w-auto h-[600px] m-8">
          <h1 className="text-4xl font-bold">Position Types</h1>
          <DoughnutChart data={data}/>
        </div>
      </div>
{/*       

      <div className="bg-gray-200 rounded-2xl p-8 w-full h-[500px]">
        <h1 className="text-4xl font-bold">State Location</h1>
        <BarChart />
      </div>

      <div className="bg-gray-200 rounded-2xl p-8 w-full h-[500px]">
        <h1 className="text-4xl font-bold">Country Location</h1>
        <BarChart />
      </div> */}
      
      
    </main>
  );
}
