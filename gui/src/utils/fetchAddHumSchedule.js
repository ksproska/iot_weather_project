export default async function fetchAddHumSchedule(roomId, start, end, val) {

    let startTemp = new Date(start);
    let startLocal = startTemp.toLocaleString("pl").split(',')[1].trim();

    let endTemp = new Date(end);
    let endLocal = endTemp.toLocaleString("pl").split(',')[1].trim();

    console.log(start);
    console.log(end);
    console.log(val);

    console.log('here');

    return fetch(`/${roomId}/add_hum_schedule`, {
        body: JSON.stringify({ 'time_start': startLocal.slice(0, 5), 'time_end': endLocal.slice(0, 5), 'value': val / 100 }),
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json())
        .catch(err => console.error(err));
};