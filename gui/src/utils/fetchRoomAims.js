export default async function fetchRoomAims(roomId) {
    fetch(`/${roomId}/aims`, {
        method: "GET",
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json())
        .catch(err => console.error(err));
};