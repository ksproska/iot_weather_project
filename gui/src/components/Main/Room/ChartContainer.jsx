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

function ChartContainer({ roomName, data }) {

    const [isTempHidden, setIsTempHidden] = useState(false);
    const [isHumHidden, setIsHumHidden] = useState(true);
    const [isPressHidden, setIsPressHidden] = useState(true);

    const [isThermoShown, setIsThermoShown] = useState(false);
    const [isDryerShown, setIsDryerShown] = useState(false);

    const [timeRange, setTimeRange] = useState("day");

    const buttonDayClass = styles.chart_button + " " + (timeRange === "day" ? styles.chart_button_selected : styles.chart_button_dimmed);
    const buttonMonthClass = styles.chart_button + " " + (timeRange === "month" ? styles.chart_button_selected : styles.chart_button_dimmed);
    const buttonYearClass = styles.chart_button + " " + (timeRange === "year" ? styles.chart_button_selected : styles.chart_button_dimmed);

    const buttonContainerDay = timeRange == "day" ? styles.chart_button_container_selected : styles.chart_button_container;
    const buttonContainerMonth = timeRange == "month" ? styles.chart_button_container_selected : styles.chart_button_container;
    const buttonContainerYear = timeRange == "year" ? styles.chart_button_container_selected : styles.chart_button_container;

    const switchTemp = () => {
        setIsTempHidden((prev) => !prev);
    };

    const switchHumidity = () => {
        setIsHumHidden((prev) => !prev);
    };

    const switchPressure = () => {
        setIsPressHidden((prev) => !prev);
    };

    const switchThermo = () => {
        setIsThermoShown(prev => !prev);
    }

    const switchDryer = () => {
        setIsDryerShown(prev => !prev);
    }

    const switchDay = () => {
        setTimeRange("day");
    };

    const switchMonth = () => {
        setTimeRange("month");
    };

    const switchYear = () => {
        setTimeRange("year");
    };

    return (
        <Grid container className={styles.chart_grid_container}>
            <Grid item xs={2} className={styles.chart_button_column}>
                <Stack spacing={1}>
                    <Box className={buttonContainerDay}>
                        <Button variant="outlined" className={buttonDayClass} onClick={switchDay}>
                            Today
                        </Button>
                    </Box>
                    <Box className={buttonContainerMonth}>
                        <Button variant="outlined" className={buttonMonthClass} onClick={switchMonth}>
                            This week
                        </Button>
                    </Box>
                    <Box className={buttonContainerYear}>
                        <Button variant="outlined" className={buttonYearClass} onClick={switchYear}>
                            This month
                        </Button>
                    </Box>
                </Stack>
            </Grid>
            <Grid item xs={8} className={styles.chart_container}>
                <Chart roomName={roomName} isTempHidden={isTempHidden} isHumHidden={isHumHidden} isPressHidden={isPressHidden}
                    isThermoShown={isThermoShown} isDryerShown={isDryerShown} roomData={data} timeRange={timeRange} />
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
                        <FormControlLabel control={<Checkbox onClick={switchThermo} />} label="Thermostat" />
                        <FormControlLabel control={<Checkbox onClick={switchDryer} />} label="Dryer" />
                    </FormGroup>
                </Stack>
            </Grid>
        </Grid >
    );
}

export default ChartContainer;