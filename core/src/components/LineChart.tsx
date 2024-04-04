import React, { Component } from 'react'
import { Chart as ChartJS, registerables } from 'chart.js';
import { Chart, Line  } from 'react-chartjs-2'
ChartJS.register(...registerables);

export default function LineChart(props: any) {


    return (
        <>
            <Line
                data={props.data}
                options={props.options}
            />
        </>
    )
};