"use client";
import Image from "next/image";
import React, { useEffect, useState } from "react";
import { Line } from "react-chartjs-2";
import { Client } from "@notionhq/client";


const notion = new Client({ auth: process.env.NOTION_TOKEN })

// Define type for response
type DataItem = {
  id: string;
  properties: {
    Name: {
      title: {
        plain_text: string;
      }[];
    };
  };
  // Add more properties as needed
};


export default function Home() {

  // THIS IS USED FOR THE NOTION CLIENT API


  // Initializing a client
  

  const [data, setData] = useState<DataItem[]>([]); 

  useEffect(() => {
    const fetchData = async () => {
      const notionDatabaseId = process.env.DATABASE_ID;

      if (notionDatabaseId) {
        try {
          const response = await notion.databases.query({
            database_id: notionDatabaseId,
          });

          setData(response.results as DataItem[]);
        } catch (error) {
          console.error('Error fetching data:', error);
        }
      }
    };

    fetchData();
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


  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <h1 className="text-6xl font-bold">Summer 2024 Internship Application Tracker</h1>
      <div className="flex flex-col items-center">
        <h2 className="text-4xl font-bold mt-8">Data</h2>
          {data.map(item => (
            <li key={item.id}>{item.properties.Name.title[0].plain_text}</li>
          ))}

        {/* Python Flask Data */}
        {/* {data.results == null ? <p>Loading...</p> : data.results} */}

        
      </div>
    </main>
  );
}
