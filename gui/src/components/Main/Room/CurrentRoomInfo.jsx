import Box from "@mui/material/Box";
import Paper from "@mui/material/Paper";
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';

import styles from "../../../styles/Main/Room/currentRoomInfo.module.css";

function CurrentRoomInfo({ roomInfo }) {
    return (
        <Box className={styles.room_info_container}>
            <TableContainer component={Paper} elevation={3}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell className={styles.table_head_cell}>Sensor</TableCell>
                            <TableCell className={styles.table_head_cell}>State</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        <TableRow>
                            <TableCell>Temperature</TableCell>
                            <TableCell>{roomInfo['temperature']} °C</TableCell>
                        </TableRow>
                        <TableRow>
                            <TableCell>Humidity</TableCell>
                            <TableCell>{roomInfo['humidity']} %</TableCell>
                        </TableRow>
                        <TableRow>
                            <TableCell>Pressure</TableCell>
                            <TableCell>{roomInfo['pressure']} hPa</TableCell>
                        </TableRow>
                    </TableBody>
                </Table>
            </TableContainer>
            <Box sx={{ height: '20px' }} />
            <TableContainer component={Paper} elevation={3}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell className={styles.table_head_cell}>Device</TableCell>
                            <TableCell className={styles.table_head_cell}>State</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        <TableRow>
                            <TableCell>Thermostat</TableCell>
                            <TableCell>{roomInfo['thermostat_state'] ? 'ON' : 'OFF'}</TableCell>
                        </TableRow>
                        <TableRow>
                            <TableCell>Dryer</TableCell>
                            <TableCell>{roomInfo['dryer_state'] ? 'ON' : 'OFF'}</TableCell>
                        </TableRow>
                    </TableBody>
                </Table>
            </TableContainer>
        </Box>
    );
}

export default CurrentRoomInfo;