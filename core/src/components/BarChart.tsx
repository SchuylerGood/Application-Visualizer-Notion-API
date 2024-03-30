import React, { Component } from 'react'
import { Chart as ChartJS, registerables } from 'chart.js';
import { Chart, Bar } from 'react-chartjs-2'
ChartJS.register(...registerables);

export default function BarChart(props: any) {
    let numbers: {[key: string] : number} = {};

    if (props.data) {
        for (let i = 0; i < props.data.length; i++) {
            let statuses = props.data[i].status;
            statuses.forEach((status: string) => {
                if (!numbers.hasOwnProperty(status)) {
                    numbers[status] = 1;
                } else {
                    numbers[status] += 1;
                }
            })
        }
    }

    let labels = Object.keys(numbers);
    let values = Object.values(numbers);

    return(
        <>
            <Bar
                data={{
                    labels: labels,
                    datasets: [{
                        label:"# of Positions",
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
                options={{
                    scales: {
                        x: {
                            type: 'category', // Specify the scale type as 'category' for the x-axis
                            labels: labels,
                            ticks: {
                                font: {
                                    size: 24
                                }
                            }
                        },
                        y: {
                            beginAtZero: true // Optionally configure the y-axis scale
                        },
                    }
                }}
            />

        </>
    )
}

