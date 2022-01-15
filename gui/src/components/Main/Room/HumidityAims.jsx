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
import Typography from "@mui/material/Typography";

import styles from "../../../styles/Main/Room/humidityAims.module.css";

function HumidityAims() {
    return (
        <Box className={styles.humidity_aims_container}>
            <Grid container columnSpacing={1}>
                <Grid item xs={10}>
                    <Typography variant="h6">
                        DEFAULT HUMIDITY: 55%
                    </Typography>
                    <TableContainer component={Paper} elevation={3}>
                        <Table>
                            <TableHead>
                                <TableRow>
                                    <TableCell className={styles.table_head_cell}>Start time</TableCell>
                                    <TableCell className={styles.table_head_cell}>End time</TableCell>
                                    <TableCell className={styles.table_head_cell}>Aim humidity</TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                <TableRow>
                                    <TableCell>12:00</TableCell>
                                    <TableCell>15:00</TableCell>
                                    <TableCell>60%</TableCell>
                                </TableRow>
                                <TableRow>
                                    <TableCell>22:00</TableCell>
                                    <TableCell>04:00</TableCell>
                                    <TableCell>40%</TableCell>
                                </TableRow>
                            </TableBody>
                        </Table>
                    </TableContainer>
                </Grid>
                <Grid item xs={2} display='flex' sx={{ flexDirection: 'column', justifyContent: 'space-between' }}>
                    <Button variant="contained" className={`${styles.humidity_aims_button} ${styles.humidity_aims_edit_button}`}>
                        EDIT
                    </Button>
                    <Button variant="contained" className={`${styles.humidity_aims_button} ${styles.humidity_aims_add_button}`}>
                        NEW
                    </Button>
                </Grid>
            </Grid>
        </Box>
    );
}

export default HumidityAims;