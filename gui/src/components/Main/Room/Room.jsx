import { useEffect, useState } from "react";

import Grid from "@mui/material/Grid";

import ChartContainer from "./ChartContainer";
import CurrentRoomInfo from "./CurrentRoomInfo";
import HumidityAims from "./HumidityAims";
import TempAims from "./TempAims";

import fetchRoomAims from "../../../utils/fetchRoomAims";
import fetchRoomCurrent from "../../../utils/fetchRoomCurrent";
import fetchRoomData from "../../../utils/fetchRoomData";

import styles from "../../../styles/Main/Room/room.module.css";

function Room({ room }) {

    const [roomData, setRoomData] = useState(null);
    const [roomCurrent, setRoomCurrent] = useState(null);

    const [defTemp, setDefTemp] = useState(null);
    const [defHum, setDefHum] = useState(null);
    const [tempPrefs, setTempPrefs] = useState([]);
    const [humPrefs, setHumPrefs] = useState([]);

    console.log(roomData);

    useEffect(() => {

        let isSubscribed = true;

        if (room != null) {
            fetchRoomData(room['room_identifier']).then(isSubscribed ? (res) => setRoomData(res) : null)
                .catch(err => console.error(err));

            if (isSubscribed) {
                fetchRoomCurrent(room['room_identifier']).then(isSubscribed ? ((res) => {
                    let obj = {
                        "room_identifier": room['room_identifier'],
                        "display_name": room['display_name'],
                        "temperature": res['temperature'],
                        "humidity": res['humidity'],
                        "pressure": res['pressure'],
                        "thermostat_state": res['thermostat_state'],
                        "dryer_state": res['dryer_state']
                    };
                    setRoomCurrent(obj);
                }) : null).catch(err => console.error(err));
            }

            if (isSubscribed) {
                fetchRoomAims(room['room_identifier']).then(isSubscribed ? ((res) => {
                    setDefTemp(res['def_temp']);
                    setDefHum(res['def_hum']);
                    setTempPrefs(res['temp_prefs']);
                    setHumPrefs(res['hum_prefs']);
                }) : null).catch(err => console.error(err));
            }
        }

        return () => (isSubscribed = false);
    }, [room]);

    return (
        <Grid item container className={styles.room_main_box} columnSpacing={2}>
            <Grid item xs={12} xl={10}>
                {roomCurrent != null ? <ChartContainer roomName={roomCurrent['display_name']} data={roomData} /> : <div>LOADING</div>}
            </Grid>
            <Grid item xs={4} xl={2}>
                {roomCurrent != null ? <CurrentRoomInfo roomInfo={roomCurrent} /> : <div>LOADING</div>}
            </Grid>
            <Grid item xs={4} xl={6}>
                {defTemp != null ? <TempAims roomId={room['room_identifier']} defTemp={defTemp}
                    tempPrefs={tempPrefs} setDefTemp={setDefTemp} setTempPrefs={setTempPrefs} /> : <div>LOADING</div>}
            </Grid>
            <Grid item xs={4} xl={6}>
                {defHum != null ? <HumidityAims roomId={room['room_identifier']} defHum={defHum}
                    humPrefs={humPrefs} setDefHum={setDefHum} setHumPrefs={setHumPrefs} /> : <div>LOADING</div>}
            </Grid>
        </Grid >
    );
}

export default Room;