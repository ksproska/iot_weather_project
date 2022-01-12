import Grid from "@mui/material/Grid";

import RoomCard from "./RoomCard";

import styles from "../../../styles/Main/Home/home.module.css";

// TODO: fetchować pomieszczenia ze wszystkim ['id-room-1': {'name': 'Kitchen', 'temp': '22.0'...}, ...]
function Home() {
    return (
        <Grid container className={styles.home_container}>
            <Grid item xs={2} />
            <Grid container item xs={8} className={styles.room_cards_container}>
                <Grid item>
                    <RoomCard />
                </Grid>
                <Grid item>
                    <RoomCard />
                </Grid>
                <Grid item>
                    <RoomCard />
                </Grid>
            </Grid>
            <Grid item xs={2} />
        </Grid>
    );
}

export default Home;