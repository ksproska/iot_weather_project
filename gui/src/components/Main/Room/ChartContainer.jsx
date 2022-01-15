import { useState } from "react";

import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Checkbox from '@mui/material/Checkbox';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Grid from "@mui/material/Grid";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";

import Chart from "./Chart";

import styles from "../../../styles/Main/Room/chartContainer.module.css";

function ChartContainer({ roomName }) {

    const [isTempHidden, setIsTempHidden] = useState(false);
    const [isHumHidden, setIsHumHidden] = useState(true);
    const [isPressHidden, setIsPressHidden] = useState(true);

    const switchTemp = () => {
        setIsTempHidden((prev) => !prev);
    };

    const switchHumidity = () => {
        setIsHumHidden((prev) => !prev);
    };

    const switchPressure = () => {
        setIsPressHidden((prev) => !prev);
    };

    return (
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
                <Chart roomName={roomName} isTempHidden={isTempHidden} isHumHidden={isHumHidden} isPressHidden={isPressHidden} />
            </Grid>
            <Grid item xs={2} className={styles.chart_checkboxes_column}>
                <Stack>
                    <Typography variant="h6">
                        Sensors
                    </Typography>
                    <FormGroup>
                        <FormControlLabel control={<Checkbox defaultChecked onClick={switchTemp} />} label="Temperature" />
                        <FormControlLabel control={<Checkbox onClick={switchHumidity} />} label="Humidity" />
                        <FormControlLabel control={<Checkbox onClick={switchPressure} />} label="Pressure" />
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
    );
}

export default ChartContainer;