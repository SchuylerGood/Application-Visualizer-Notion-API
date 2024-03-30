import React, { Component } from 'react'

// Chart Imports
import { Chart } from 'chart.js';
import {SankeyController, Flow} from 'chartjs-chart-sankey';
Chart.register(SankeyController, Flow);

export default function SankeyChart() {

    const colors = {
        a: 'red',
        b: 'green',
        c: 'blue',
        d: 'gray'
    };
      
    const getColor = (key) => colors[key];

    const chart = new Chart(ctx, {
    type: 'sankey',
    data: {
        datasets: [{
        label: 'My sankey',
        data: [
            {from: 'a', to: 'b', flow: 10},
            {from: 'a', to: 'c', flow: 5},
            {from: 'b', to: 'c', flow: 10},
            {from: 'd', to: 'c', flow: 7}
        ],
        colorFrom: (c) => getColor(c.dataset.data[c.dataIndex].from),
        colorTo: (c) => getColor(c.dataset.data[c.dataIndex].to),
        colorMode: 'gradient', // or 'from' or 'to'
        /* optional labels */
        labels: {
            a: 'Label A',
            b: 'Label B',
            c: 'Label C',
            d: 'Label D'
        },
        /* optional priority */
        priority: {
            b: 1,
            d: 0
        },
        /* optional column overrides */
        column: {
            d: 1
        },
        size: 'max', // or 'min' if flow overlap is preferred
        }]
    },
    });


    return (
        <div>
            <h1>Sankey Chart</h1>
        </div>
    );
}