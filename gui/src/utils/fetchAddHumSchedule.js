export default async function fetchAddHumSchedule(roomId, start, end, val) {
    return fetch(`/${roomId}/add_hum_schedule`, {
        body: JSON.stringify({ 'time_start': start, 'time_end': end, 'value': val / 100 }),
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json())
        .catch(err => console.error(err));
};