import { useEffect, useState } from "react";

import Grid from "@mui/material/Grid";

import ChartContainer from "./ChartContainer";
import CurrentRoomInfo from "./CurrentRoomInfo";
import HumidityAims from "./HumidityAims";
import TempAims from "./TempAims";

import fetchRoomCurrent from "../../../utils/fetchRoomCurrent";
import fetchRoomData from "../../../utils/fetchRoomData";

import styles from "../../../styles/Main/Room/room.module.css";

// TODO: usuwanko aimów
// TODO: jak ma wyglądać edit i add nowych aimów
// TODO: ogólnie wygląd (szczególnie kolorki i jakieś rameczki, co do responsywności to chyba za dużo zabawy jak na oddanie Nowakowi)
// TODO: reload'ować dokument czy nie :thinking:
// TODO: humidity castować mam ja na procenty, czy mam dostawać
// TODO: potrzebuję danych przykładowych dla testowanka

// TODO: CONFIRMED - Devices przy włączeniu mają nakładać punkty na ten wykres liniowy (jakiś szary-OFF i normalny-ON)

function Room({ room, timestamp }) {

    const [roomData, setRoomData] = useState(null);
    const [roomCurrent, setRoomCurrent] = useState(null);

    useEffect(() => {

        if (room != null) {
            fetchRoomData(room['room_identifier']).then((res) => setRoomData(res))
                .catch(err => console.error(err));

            fetchRoomCurrent(room['room_identifier']).then((res) => {
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
            }).catch(err => console.error(err));
        }

    }, [room]);

    return (
        <Grid item container className={styles.room_main_box} columnSpacing={2}>
            <Grid item xs={12} xl={10}>
                {roomCurrent != null ? <ChartContainer roomName={roomCurrent['display_name']} /> : <div>LOADING</div>}
            </Grid>
            <Grid item xs={4} xl={2}>
                {roomCurrent != null ? <CurrentRoomInfo roomInfo={roomCurrent} /> : <div>LOADING</div>}
            </Grid>
            <Grid item xs={4} xl={6}>
                <TempAims />
            </Grid>
            <Grid item xs={4} xl={6}>
                <HumidityAims />
            </Grid>
        </Grid >
    );
}

export default Room;