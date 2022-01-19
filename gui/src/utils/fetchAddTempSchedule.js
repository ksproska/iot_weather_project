export default async function fetchAddTempSchedule(roomId, start, end, val) {

    let startTemp = new Date(start);
    let startLocal = startTemp.toLocaleString("pl").split(',')[1].trim();

    let endTemp = new Date(end);
    let endLocal = endTemp.toLocaleString("pl").split(',')[1].trim();

    return fetch(`/${roomId}/add_temp_schedule`, {
        body: JSON.stringify({ 'time_start': startLocal, 'time_end': endLocal, 'value': val }),
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json())
        .catch(err => console.error(err));
};