import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import Box from '@mui/material/Box';
import Button from "@mui/material/Button";
import Checkbox from '@mui/material/Checkbox';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Grid from "@mui/material/Grid";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";

import Chart from "./Chart";
import RoomCard from "../Home/RoomCard";

import fetchRoomData from "../../../utils/fetchRoomData";

import styles from "../../../styles/Main/Room/room.module.css";

function Room({ rooms }) {

    const params = useParams();
    let roomId = params.roomId;

    console.log(roomId);

    const [roomObj, setRoomObj] = useState(null);
    const [timeInterval, setTimeInterval] = useState("day");

    if (rooms != null) {
        console.log(rooms);
    }

    useEffect(() => {
        fetchRoomData(roomId).then(res =>
            console.log(res)
        ).catch(err => console.error(err));
    }, [rooms, roomId]);

    return (
        <Box className={styles.room_main_box}>
            <Grid container className={styles.chart_grid_container}>
                <Grid item xs={2} className={styles.chart_button_column}>
                    <Stack spacing={1}>
                        <Box className={styles.chart_button_container_selected}>
                            <Button variant="outlined" className={styles.chart_button + " " + styles.chart_button_selected}>
                                Today
                            </Button>
                        </Box>
                        <Box className={styles.chart_button_container}>
                            <Button variant="outlined" className={styles.chart_button + " " + styles.chart_button_dimmed}>
                                This week
                            </Button>
                        </Box>
                        <Box className={styles.chart_button_container}>
                            <Button variant="outlined" className={styles.chart_button + " " + styles.chart_button_dimmed}>
                                This month
                            </Button>
                        </Box>
                    </Stack>
                </Grid>
                <Grid item xs={8} className={styles.chart_container}>
                    <Chart />
                </Grid>
                <Grid item xs={2} className={styles.chart_checkboxes_column}>
                    <Stack>
                        <Typography variant="h6">
                            Sensors
                        </Typography>
                        <FormGroup>
                            <FormControlLabel control={<Checkbox defaultChecked />} label="Temperature" />
                            <FormControlLabel control={<Checkbox />} label="Humidity" />
                            <FormControlLabel control={<Checkbox />} label="Pressure" />
                        </FormGroup>
                        <Typography variant="h6">
                            Devices
                        </Typography>
                        <FormGroup>
                            <FormControlLabel control={<Checkbox />} label="Thermostat" />
                            <FormControlLabel control={<Checkbox />} label="Dryer" />
                        </FormGroup>
                    </Stack>
                </Grid>
            </Grid >
        </Box >
    );
}

export default Room;