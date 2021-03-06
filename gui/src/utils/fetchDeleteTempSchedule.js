export default async function fetchDeleteTempSchedule(roomId, start, end, val) {
    return fetch(`/${roomId}/delete_temp_schedule`, {
        body: JSON.stringify({ 'time_start': start, 'time_end': end, 'value': val }),
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json())
        .catch(err => console.error(err));
};