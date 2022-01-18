import { Link } from "react-router-dom";

import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Grid from "@mui/material/Grid";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";

import HomeIcon from '@mui/icons-material/Home';

import styles from "../../styles/Header/header.module.css";

function Header({ rooms }) {

    return (
        <Grid item xs={12} className={styles.header_container}>
            <AppBar position="static">
                <Toolbar disableGutters className={styles.header_toolbar}>
                    <Box className={styles.header_button_box}>
                        <Link to="/">
                            <Button variant="outlined" className={styles.header_button}>
                                <HomeIcon className={styles.header_home_icon} />
                            </Button>
                        </Link>
                        {rooms != null ? rooms['rooms'].map((room) =>
                            <Link to={"/room/" + room['room_identifier']} key={room['room_identifier']}>
                                <Button variant="outlined" className={styles.header_button}>
                                    <Typography className={styles.header_button_text}>
                                        {room['display_name']}
                                    </Typography>
                                </Button>
                            </Link>
                        ) : null}
                    </Box>
                </Toolbar>
            </AppBar>
        </Grid>
    );
}

export default Header;