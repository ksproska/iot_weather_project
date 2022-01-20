import { useState } from "react";

import AdapterDateFns from "@mui/lab/AdapterDateFns";
import LocalizationProvider from "@mui/lab/LocalizationProvider";
import plLocale from "date-fns/locale/pl";

import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Grid from "@mui/material/Grid";
import Paper from "@mui/material/Paper";
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import TextField from "@mui/material/TextField";
import TimePicker from "@mui/lab/TimePicker";
import Typography from "@mui/material/Typography";

import fetchAddHumSchedule from "../../../utils/fetchAddHumSchedule";
import fetchDeleteHumSchedule from "../../../utils/fetchDeleteHumSchedule";
import fetchSetDefHum from "../../../utils/fetchSetDefHum";

import styles from "../../../styles/Main/Room/humidityAims.module.css";

function HumidityAims({ roomId, defHum, humPrefs, setDefHum, setHumPrefs }) {

    const [startTime, setStartTime] = useState(new Date());
    const [endTime, setEndTime] = useState(new Date());
    const [humAim, setHumAim] = useState(defHum * 100);
    const [defHumForm, setDefHumForm] = useState(defHum * 100);

    const [isAddShown, setIsAddShown] = useState(false);
    const [isEditShown, setIsEditShown] = useState(false);

    const handleRemovePref = (start, end, val) => {
        fetchDeleteHumSchedule(roomId, start, end, val).then(res => {
            setHumPrefs(res);
        }).catch(err => console.error(err));
    };

    const handleAddForm = () => {
        if (isAddShown) {
            fetchAddHumSchedule(roomId, startTime, endTime, humAim).then(res => {
                console.log(res);
                setHumPrefs(res);
            }).catch(err => console.error(err));
            setIsAddShown(false);
        } else {
            setIsAddShown(true);
        }
    };

    const closeAddForm = () => {
        setIsAddShown(false);
    };

    const handleEditForm = () => {
        if (isEditShown) {
            fetchSetDefHum(roomId, defHumForm).then(() => setDefHum(defHumForm / 100))
                .catch(err => console.error(err));
            setIsEditShown(false);
        } else {
            setIsEditShown(true);
        }
    };

    const closeEditForm = () => {
        setIsEditShown(false);
    };

    return (
        <Box className={styles.humidity_aims_container}>
            <Grid container columnSpacing={1}>
                <Grid item xs={10}>
                    <Grid container>
                        <Typography variant="h6" sx={{ display: 'inline', alignSelf: 'center' }}>
                            DEFAULT HUMIDITY:
                        </Typography>
                        {isEditShown ? <TextField variant="filled" label="Default humidity" value={defHumForm}
                            onChange={(event) => setDefHumForm(event.target.value)} type="number" />
                            : <Typography variant="h6" sx={{ display: 'inline' }}>{defHum * 100 + "%"}</Typography>}
                        {isEditShown ? <Button color="error" variant="contained" onClick={closeEditForm}>X</Button> : null}
                    </Grid>
                    <TableContainer component={Paper} elevation={3}>
                        <Table>
                            <TableHead>
                                <TableRow>
                                    <TableCell className={styles.table_head_cell}>Start time</TableCell>
                                    <TableCell className={styles.table_head_cell}>End time</TableCell>
                                    <TableCell className={styles.table_head_cell}>Aim humidity</TableCell>
                                    <TableCell className={styles.table_head_cell}></TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {Array.isArray(humPrefs) ? humPrefs.map(pref => <TableRow key={pref['time_start']}>
                                    <TableCell>{pref['time_start']}</TableCell>
                                    <TableCell>{pref['time_end']}</TableCell>
                                    <TableCell>{pref['value']}</TableCell>
                                    <TableCell>
                                        <Button color="error" variant="contained" onClick={() => handleRemovePref(pref['time_start'], pref['time_end'], pref['value'] * 100)}>
                                            X
                                        </Button>
                                    </TableCell>
                                </TableRow>) : null}
                                {isAddShown ? <TableRow>
                                    <LocalizationProvider dateAdapter={AdapterDateFns} locale={plLocale}>
                                        <TableCell>
                                            <TimePicker label="Start time" value={startTime} onChange={(val) => setStartTime(val)}
                                                renderInput={(params) => <TextField variant="filled" {...params} />} />
                                        </TableCell>
                                        <TableCell>
                                            <TimePicker label="End time" value={endTime} onChange={(val) => setEndTime(val)}
                                                renderInput={(params) => <TextField variant="filled" {...params} />} />
                                        </TableCell>
                                    </LocalizationProvider>
                                    <TableCell>
                                        <TextField label="Humidity" variant="filled" type="number" value={humAim}
                                            onChange={(event) => setHumAim(event.target.value)} />
                                    </TableCell>
                                    <TableCell>
                                        <Button color="error" onClick={closeAddForm} variant="contained">Cancel</Button>
                                    </TableCell>
                                </TableRow> : null}
                            </TableBody>
                        </Table>
                    </TableContainer>
                </Grid>
                <Grid item xs={2} display='flex' sx={{ flexDirection: 'column', justifyContent: 'space-between' }}>
                    <Button variant="contained" className={`${styles.humidity_aims_button} ${styles.humidity_aims_edit_button}`} onClick={handleEditForm}>
                        EDIT
                    </Button>
                    <Button variant="contained" className={`${styles.humidity_aims_button} ${styles.humidity_aims_add_button}`} onClick={handleAddForm}>
                        NEW
                    </Button>
                </Grid>
            </Grid>
        </Box>
    );
}

export default HumidityAims;