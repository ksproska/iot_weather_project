export default async function fetchAddTempSchedule(roomId, start, end, val) {

    let startTemp = new Date(start);
    let startLocal = startTemp.toLocaleString("pl").split(',')[1].trim();

    let endTemp = new Date(end);
    let endLocal = endTemp.toLocaleString("pl").split(',')[1].trim();

    console.log(startLocal);
    console.log(endLocal);
    console.log(val);

    console.log('here');

    return fetch(`/${roomId}/add_temp_schedule`, {
        body: JSON.stringify({ 'time_start': startLocal.slice(0, 5), 'time_end': endLocal.slice(0, 5), 'value': val }),
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json())
        .catch(err => console.error(err));
};