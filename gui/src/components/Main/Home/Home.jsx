import Grid from "@mui/material/Grid";

import RoomCard from "./RoomCard";

import styles from "../../../styles/Main/Home/home.module.css";

import fetchRoomnames from "../../../utils/fetchRoomnames";

function Home({ rooms }) {

    let roomData = [];

    if (rooms != null) {
        rooms['rooms'].map((room) => {
            fetchRoomnames(room['room_identifier']).then(res => {
                console.log(res);
                roomData.push({
                    "room_identifier": room['room_identifier'],
                    "display_name": room['display_name'],
                    "temperature": res['temperature'],
                    "humidity": res['humidity'],
                    "pressure": res['pressure'],
                    "thermostat_state": res['thermostat_state'],
                    "dryer_state": res['dryer_state']
                });
            }).catch(err => console.error(err));
        });
    }

    return (
        <>
            {rooms == null ? <div>ERR</div> :
                <Grid container className={styles.home_container}>
                    <Grid item xs={2} />
                    <Grid container item xs={8} className={styles.room_cards_container}>
                        {roomData.map(room =>
                        (<Grid item>
                            <RoomCard room={room} />
                        </Grid>))
                        }
                    </Grid>
                    <Grid item xs={2} />
                </Grid>
            }
        </>
    );
}

export default Home;