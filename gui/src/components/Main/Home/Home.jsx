import { useEffect, useState } from "react";

import Container from "@mui/material/Container";
import Grid from "@mui/material/Grid";

import RoomCard from "./RoomCard";

import styles from "../../../styles/Main/Home/home.module.css";

import fetchRoomCurrent from "../../../utils/fetchRoomCurrent";

function Home({ rooms }) {

    const [roomsCurrent, setRoomsCurrent] = useState([]);

    console.log(rooms);

    useEffect(() => {
        let roomData = [];

        async function fetchCurrent() {
            await Promise.all(rooms['rooms'].map(async (room) => {
                let result = await fetchRoomCurrent(room['room_identifier']);
                if (result !== undefined) {
                    roomData.push({
                        "room_identifier": room["room_identifier"],
                        "display_name": room["display_name"],
                        "temperature": result["temperature"],
                        "humidity": result["humidity"],
                        "pressure": result["pressure"],
                        "thermostat_state": result["thermostat_state"],
                        "dryer_state": result["dryer_state"]
                    });
                }
            })).then(() => setRoomsCurrent(roomData));
        }

        if (rooms != null) {
            fetchCurrent();
        }

    }, [rooms]);


    return (
        <>
            {rooms === null ? <Container>Loading...</Container> :
                <Grid container className={styles.home_container}>
                    <Grid item xs={2} />
                    <Grid container item xs={8} className={styles.room_cards_container}>
                        {roomsCurrent !== null ? roomsCurrent.map(room =>
                            <Grid item key={room['room_identifier']}>
                                <RoomCard room={room} />
                            </Grid>
                        ) : null}
                    </Grid>
                    <Grid item xs={2} />
                </Grid>
            }
        </>
    );
}

export default Home;