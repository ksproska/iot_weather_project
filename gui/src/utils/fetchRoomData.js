export default async function fetchRoomData(roomId) {
    fetch(`/${roomId}/data`, {
        method: "GET",
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json())
        .catch(err => console.error(err));
};