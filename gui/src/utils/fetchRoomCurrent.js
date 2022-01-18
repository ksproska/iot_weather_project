export default async function fetchRoomCurrent(roomId) {
    return fetch(`/${roomId}/current`, {
        method: "GET",
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json())
        .catch(err => {
            console.error(err);
        });
};