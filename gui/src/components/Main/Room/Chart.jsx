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

function Chart({ roomName, isTempHidden, isHumHidden, isPressHidden, isThermoShown, isDryerShown, roomData, timeRange, daySpread }) {

    let records = null;

    if (roomData !== null && roomData !== undefined) {
        records = roomData[timeRange];
    }

    const times = [];
    const temps = [];
    const humids = [];
    const pressures = [];
    const thermostats = [];
    const dryers = [];

    if (Array.isArray(records)) {
        if (timeRange === "day") {
            records.forEach((record, index) => index % daySpread === 0 ?
                times.push(`${('0' + record['hour']).slice(-2)}:${('0' + record['minute']).slice(-2)}`) : '');
        } else if (timeRange === "week") {
            records.forEach((record, index) => index % 6 === 0 ?
                times.push(`${('0' + record['hour']).slice(-2)}:00`) : '');
        } else {
            records.forEach(record => times.push(`${('0' + record['day']).slice(-2)}.${('0' + record['month']).slice(-2)}`));
        }
        records.forEach(record => temps.push(record['temperature']));
        records.forEach(record => humids.push(record['humidity']));
        records.forEach(record => pressures.push(record['pressure']));
        records.forEach(record => thermostats.push(record['thermostat_state']));
        records.forEach(record => dryers.push(record['dryer_state']));
    }

    const data = {
        labels: times,
        datasets: [
            {
                label: "Temperature",
                data: temps,
                yAxisID: 'y',
                borderColor: 'rgb(255, 99, 132)',
                backgroundColor: 'rgba(255, 99, 132, 0.5)',
                hidden: isTempHidden,
                pointBackgroundColor: function (context) {
                    let index = context.dataIndex;
                    let value = thermostats.length > 0 ? thermostats[index] : 0;
                    if (!isThermoShown) {
                        return 'rgb(255, 99, 132)';
                    } else {
                        return value === 0 ? 'white' : 'black';
                    }
                }
            },
            {
                label: "Humidity",
                data: humids,
                yAxisID: 'y1',
                borderColor: 'rgb(53, 162, 235)',
                backgroundColor: 'rgba(53, 162, 235, 0.5)',
                hidden: isHumHidden,
                pointBackgroundColor: function (context) {
                    let index = context.dataIndex;
                    let value = dryers.length > 0 ? dryers[index] : 0;
                    if (!isDryerShown) {
                        return 'rgb(53, 162, 235)';
                    } else {
                        return value === 0 ? 'black' : 'white';
                    }
                }
            },
            {
                label: "Pressure",
                data: pressures,
                yAxisID: 'y2',
                borderColor: 'rgb(70, 170, 10)',
                backgroundColor: 'rgba(70, 170, 10, 0.5)',
                hidden: isPressHidden
            },
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
                }//, ticks: {
                //     callback: function (val, index) {
                //         let returnVal = 0;
                //         if (timeRange === "week") {
                //             returnVal = index % 6 === 0 ? this.getLabelForValue(val) : '';
                //         } else {
                //             returnVal = this.getLabelForValue(val);
                //         }
                //         return returnVal;
                //     }
                // }
            },
            y: {
                type: 'linear',
                display: !isTempHidden,
                position: 'left',
                min: 15,
                max: 30,
                title: {
                    display: 'true',
                    text: 'Temperature [°C]'
                }
            },
            y1: {
                type: 'linear',
                display: !isHumHidden,
                position: 'left',
                min: 0,
                max: 1,
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