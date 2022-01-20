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

import fetchAddTempSchedule from "../../../utils/fetchAddTempSchedule";
import fetchDeleteTempSchedule from "../../../utils/fetchDeleteTempSchedule";
import fetchSetDefTemp from "../../../utils/fetchSetDefTemp";

import styles from "../../../styles/Main/Room/tempAims.module.css";

function TempAims({ roomId, defTemp, tempPrefs, setDefTemp, setTempPrefs }) {

    const [startTime, setStartTime] = useState(new Date());
    const [endTime, setEndTime] = useState(new Date());
    const [tempAim, setTempAim] = useState(defTemp);
    const [defTempForm, setDefTempForm] = useState(defTemp);

    const [isAddShown, setIsAddShown] = useState(false);
    const [isEditShown, setIsEditShown] = useState(false);

    const handleRemovePref = (start, end, val) => {
        fetchDeleteTempSchedule(roomId, start, end, val).then(res => {
            setTempPrefs(res['temp_prefs']);
        }).catch(err => console.error(err));
    };

    const handleAddForm = () => {
        if (isAddShown) {
            fetchAddTempSchedule(roomId, startTime, endTime, tempAim).then(res => {
                setTempPrefs(res['temp_prefs']);
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
            fetchSetDefTemp(roomId, defTempForm).then(() => setDefTemp(defTempForm))
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
        <Box className={styles.temp_aims_container}>
            <Grid container columnSpacing={1}>
                <Grid item xs={10}>
                    <Grid container>
                        <Typography variant="h6" sx={{ display: 'inline', alignSelf: 'center' }}>
                            DEFAULT TEMPERATURE:
                        </Typography>
                        {isEditShown ? <TextField variant="filled" label="Default temp" value={defTempForm}
                            onChange={(event) => setDefTempForm(event.target.value)} type="number" />
                            : <Typography variant="h6" sx={{ display: 'inline' }}>{defTemp + "°C"}</Typography>}
                        {isEditShown ? <Button color="error" variant="contained" onClick={closeEditForm}>X</Button> : null}
                    </Grid>
                    <TableContainer component={Paper} elevation={3}>
                        <Table>
                            <TableHead>
                                <TableRow>
                                    <TableCell className={styles.table_head_cell}>Start time</TableCell>
                                    <TableCell className={styles.table_head_cell}>End time</TableCell>
                                    <TableCell className={styles.table_head_cell}>Aim temperature</TableCell>
                                    <TableCell className={styles.table_head_cell}></TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {Array.isArray(tempPrefs) ? tempPrefs.map(pref => <TableRow key={pref['time_start']}>
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
                                        <TextField label="Temperature" variant="filled" type="number" value={tempAim}
                                            onChange={(event) => setTempAim(event.target.value)} />
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
                    <Button variant="contained" className={`${styles.temp_aims_button} ${styles.temp_aims_edit_button}`} onClick={handleEditForm}>
                        EDIT
                    </Button>
                    <Button variant="contained" className={`${styles.temp_aims_button} ${styles.temp_aims_add_button}`} onClick={handleAddForm}>
                        NEW
                    </Button>
                </Grid>
            </Grid>
        </Box>
    );
}

export default TempAims;