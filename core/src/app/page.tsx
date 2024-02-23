"use client";
import Image from "next/image";
import React, { useEffect, useState } from "react";
import { Line } from "react-chartjs-2";



async function getPages(numPages = null) {
  const url = `https://api.notion.com/v1/databases/${process.env.DATABASE_ID}/query`;
  const getAll = numPages === null;
  const pageSize = getAll ? 100 : numPages;

  let payload = { "page_size": pageSize };

  // Request the first page
  try {
    let response = await fetch(url, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${process.env.NOTION_TOKEN}`,
        'Notion-Version': '2021-08-16',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });
  } catch (error) {
    console.error("Error fetching data from Notion:", error);
  }
  

  let data = await response.json();
  let workingData = data["results"][0]
  console.log("here is the data: " + JSON.stringify(workingData, null, 2));

  // Error handling
  if (!data.results) {
    console.log("Error: No 'results' key found in the response JSON.");
    console.log("Response JSON:", data);
    return [];
  }

  interface Payload {
    page_size: number;
    start_cursor?: string;
  }

  // If we want all pages, keep requesting until there are no more pages
  let results = data.results;
      while (data.has_more && getAll) {
          let payload: Payload = { "page_size": pageSize, "start_cursor": data.next_cursor };
          response = await fetch(url, {
              method: 'POST',
              headers: {
                  'Authorization': `Bearer ${process.env.NOTION_TOKEN}`,
                  'Notion-Version': '2021-08-16',
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify(payload)
          });
          data = await response.json();
          if (data.results) {
              results = [...results, ...data.results];
          }
      }

    return results
  }

  



export default function Home() {
  const [results, setResults] = useState([]);

  useEffect(() => {
    getPages().then(data => setResults(data));
  }, []);

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <h1 className="text-6xl font-bold">Welcome to my website</h1>
      <div className="flex flex-col items-center">
        {
          results.map((page) => {
            return (
              <div key={page["STATUS"]} className="flex flex-col items-center">
                <h2 className="text-2xl font-bold mt-8">{page['STATUS']}</h2>
              </div>
            )
          })
        }
        <h2 className="text-4xl font-bold mt-8">Hi, I'm John Doe</h2>
        <p className="text-2xl text-center mt-4">
          I'm a web developer and I love building websites and web applications.
        </p>
      </div>
    </main>
  );
}
