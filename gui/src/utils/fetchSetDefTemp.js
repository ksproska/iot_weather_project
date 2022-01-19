export default async function fetchSetDefTemp(roomId, defTemp) {
    return fetch(`/${roomId}/set_def_temp`, {
        body: JSON.stringify({ 'def_temperature': defTemp }),
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json())
        .catch(err => console.error(err));
};