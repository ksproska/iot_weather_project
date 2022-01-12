import { Link } from "react-router-dom";

import Button from "@mui/material/Button";
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import CardHeader from "@mui/material/CardHeader";
import Typography from "@mui/material/Typography";

import styles from "../../../styles/Main/Home/roomCard.module.css";

// TODO: przyjmować roomId, temp, hum, press jako propsy
function RoomCard() {
    return (
        <Card className={styles.room_card_container} elevation={5}>
            <CardHeader title="Living room" />
            <CardContent>
                <Typography>
                    Temperature: 23.5°C
                </Typography>
                <Typography>
                    Humidity: 55%
                </Typography>
                <Typography>
                    Pressure: 1004 hPa
                </Typography>
                <Typography>
                    Thermostat: ON
                </Typography>
                <Typography>
                    Dryer: OFF
                </Typography>
            </CardContent>
            <CardActions>
                <Link to="/room/1">
                    <Button>
                        Check details
                    </Button>
                </Link>
            </CardActions>
        </Card>
    );
}

export default RoomCard;