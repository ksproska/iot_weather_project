export default async function fetchRoomCurrent(roomId) {
    fetch(`/${roomId}/current`, {
        method: "GET",
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json())
        .catch(err => {
            console.error(err);
        });
};