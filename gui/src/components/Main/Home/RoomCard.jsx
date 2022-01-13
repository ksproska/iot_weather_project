import { Link } from "react-router-dom";

import Button from "@mui/material/Button";
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import CardHeader from "@mui/material/CardHeader";
import Typography from "@mui/material/Typography";

import styles from "../../../styles/Main/Home/roomCard.module.css";

// TODO: przyjmować roomId, temp, hum, press jako propsy
function RoomCard({ room }) {
    return (
        <Card className={styles.room_card_container} elevation={5}>
            <CardHeader title="Living room" />
            <CardContent>
                <Typography>
                    Temperature: {room['temperature']}
                </Typography>
                <Typography>
                    Humidity: {room['humidity']}
                </Typography>
                <Typography>
                    Pressure: {room['pressure']}
                </Typography>
                <Typography>
                    Thermostat: {room['thermostat_state']}
                </Typography>
                <Typography>
                    Dryer: {room['dryer_state']}
                </Typography>
            </CardContent>
            <CardActions>
                <Link to={"/room/" + room['room_identifier']}>
                    <Button>
                        Check details
                    </Button>
                </Link>
            </CardActions>
        </Card>
    );
}

export default RoomCard;