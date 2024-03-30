import React, { Component } from 'react'
import { Chart as ChartJS, registerables } from 'chart.js';
import { Chart, Doughnut  } from 'react-chartjs-2'
ChartJS.register(...registerables);

export default function DoughnutChart(props: any) {
    let categoryCounts: { [key: string]: number } = {};

    if (props.data) {
        // Loop through the data and count occurrences of each category
        for (let i = 0; i < props.data.length; i++) {
            let catName = props.data[i].category;

            // for each category in catName add one to the count of each category
            catName.forEach((cat: string) => {
                if (!categoryCounts.hasOwnProperty(cat)) {
                    categoryCounts[cat] = 1;
                } else {
                    // If the category name already exists in the counts object, increment its count
                    categoryCounts[cat]++;
                }
            });
        }
    }

    // If you need labels and values separately, you can extract them from the categoryCounts object
    let labels = Object.keys(categoryCounts);
    let values = Object.values(categoryCounts);

    return(
        <>
            <Doughnut
                data={{
                    labels: labels,
                    datasets: [{
                        label: '# of Positions',
                        data: values,
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)',  // Red
                            'rgba(54, 162, 235, 0.2)',   // Blue
                            'rgba(255, 206, 86, 0.2)',   // Yellow
                            'rgba(75, 192, 192, 0.2)',   // Teal
                            'rgba(153, 102, 255, 0.2)',  // Purple
                            'rgba(255, 159, 64, 0.2)',   // Orange
                            'rgba(160, 82, 45, 0.2)',    // Brown
                            'rgba(46, 204, 113, 0.2)'    // Green
                        ],
                        borderColor: [
                            'rgba(255, 99, 132, 1)',    // Red
                            'rgba(54, 162, 235, 1)',     // Blue
                            'rgba(255, 206, 86, 1)',     // Yellow
                            'rgba(75, 192, 192, 1)',     // Teal
                            'rgba(153, 102, 255, 1)',    // Purple
                            'rgba(255, 159, 64, 1)',     // Orange
                            'rgba(160, 82, 45, 1)',      // Brown
                            'rgba(46, 204, 113, 1)'      // Green
                        ],
                        borderWidth: 2
                    }]
                }}
            />
        </>
    )
}