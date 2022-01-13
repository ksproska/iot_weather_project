export default async function fetchRoomnames() {
    fetch("/roomnames", {
        method: "GET",
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json())
        .catch(err => {
            console.error(err);
        });
}