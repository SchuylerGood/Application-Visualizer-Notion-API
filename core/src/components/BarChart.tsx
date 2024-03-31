import React, { Component } from 'react'
import { Chart as ChartJS, registerables } from 'chart.js';
import { Chart, Bar } from 'react-chartjs-2'
ChartJS.register(...registerables);

export default function BarChart(props: any) {    
    return(
        <div className='w-[900px]'>
            <Bar
                data={{
                    labels: props.labels,
                    datasets: [{
                        label:"# of Positions",
                        data: props.values,
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
                            labels: props.labels,
                            ticks: {
                                font: {
                                    size: 18
                                }
                            }
                        },
                        y: {
                            beginAtZero: true // Optionally configure the y-axis scale
                        },
                    }
                }}
            />
        </div>
    )
}

