import { Outlet, Link } from "react-router-dom";

import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Grid from "@mui/material/Grid";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";

import HomeIcon from '@mui/icons-material/Home';

import styles from "../../styles/Header/header.module.css";

// TODO: fetch'ować listę pomieszczeń [ 'id-room-1': {'name': 'Kitchen'}, 'id-room-2': {'name': 'Bathroom'}...]
function Header() {

    // living_room

    return (
        <Grid item xs={12}>
            <AppBar position="static">
                <Toolbar disableGutters className={styles.header_toolbar}>
                    <Box className={styles.header_button_box}>
                        <Link to="/">
                            <Button variant="outlined" className={styles.header_button}>
                                <HomeIcon className={styles.header_home_icon} />
                            </Button>
                        </Link>
                        <Button variant="outlined" className={styles.header_button}>
                            <Typography className={styles.header_button_text}>
                                Living Room
                            </Typography>
                        </Button>
                        <Button variant="outlined" className={styles.header_button}>
                            <Typography className={styles.header_button_text}>
                                Kitchen
                            </Typography>
                        </Button>
                        <Button variant="outlined" className={styles.header_button}>
                            <Typography className={styles.header_button_text}>
                                Bathroom
                            </Typography>
                        </Button>
                    </Box>
                </Toolbar>
            </AppBar>
        </Grid>
    );
}

export default Header;