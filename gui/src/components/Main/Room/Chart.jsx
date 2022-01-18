import { Line } from "react-chartjs-2";
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

function Chart({ roomName, isTempHidden, isHumHidden, isPressHidden }) {

    const data = {
        labels: ['21:00', '21:15', '21:30', '21:45', '22:00'],
        datasets: [
            {
                label: "Temperature",
                data: [20.5, 21.5, 21.0, 21.0, 22.0],
                yAxisID: 'y',
                borderColor: 'rgb(255, 99, 132)',
                backgroundColor: 'rgba(255, 99, 132, 0.5)',
                hidden: isTempHidden
            },
            {
                label: "Humidity",
                data: [0.6, 0.63, 0.55, 0.58, 0.6],
                yAxisID: 'y1',
                borderColor: 'rgb(53, 162, 235)',
                backgroundColor: 'rgba(53, 162, 235, 0.5)',
                hidden: isHumHidden
            },
            {
                label: "Pressure",
                data: [1020, 1015, 1018, 1020, 1021],
                yAxisID: 'y2',
                borderColor: 'rgb(235, 255, 51)',
                backgroundColor: 'rgba(235, 255, 51, 0.5)',
                hidden: isPressHidden
            }
        ]
    };

    const options = {
        responsive: true,
        interaction: {
            mode: 'index',
            intersect: false,
        },
        stacked: false,
        plugins: {
            title: {
                display: true,
                text: roomName
            },
            legend: {
                onClick: null
            }
        },
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Time'
                }
            },
            y: {
                type: 'linear',
                display: !isTempHidden,
                position: 'left',
                title: {
                    display: 'true',
                    text: 'Temperature [°C]'
                }
            },
            y1: {
                type: 'linear',
                display: !isHumHidden,
                position: 'left',
                title: {
                    display: 'true',
                    text: 'Humidity [%]'
                },
                grid: {
                    drawOnChartArea: false,
                },
            },
            y2: {
                type: 'linear',
                display: !isPressHidden,
                position: 'right',
                title: {
                    display: 'true',
                    text: 'Pressure [hPa]'
                },
                grid: {
                    drawOnChartArea: false,
                },
            }
        }
    };

    return (
        <Line options={options} data={data} />
    );
}

export default Chart;