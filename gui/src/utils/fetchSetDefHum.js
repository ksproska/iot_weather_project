export default async function fetchSetHumTemp(roomId, defHum) {
    return fetch(`/${roomId}/set_def_hum`, {
        body: JSON.stringify({ 'def_humidity': defHum / 100 }),
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json())
        .catch(err => console.error(err));
};