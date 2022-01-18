import { useEffect, useState } from "react";

import { BrowserRouter, Routes, Route } from "react-router-dom";

import Grid from "@mui/material/Grid";

import Header from "./components/Header/Header";
import Home from "./components/Main/Home/Home";
import Room from "./components/Main/Room/Room";
import WrongPage from "./components/Main/WrongPage";

import fetchRoomnames from "./utils/fetchRoomnames";

function App() {

    const [rooms, setRooms] = useState(null);
    const [isLoaded, setIsLoaded] = useState(false);

    useEffect(() => {
        fetchRoomnames().then(result => {
            setRooms(result);
            setIsLoaded(true);
        }).catch((err) => {
            console.error(err);
            setRooms(null);
            setIsLoaded(true);
        });
    }, []);

    return (
        <div className="App" style={{ height: '100%' }}>
            <Grid container sx={{ height: '100%' }}>
                <BrowserRouter>
                    <Header rooms={rooms} />
                    <Routes>
                        <Route path="/" element={<Home rooms={rooms} />} />
                        {rooms != null ? rooms['rooms'].map((room) =>
                            <Route path={"/room/" + room['room_identifier']} element={<Room room={room} />}
                                key={room['room_identifier']} />) : null}
                        <Route path="*" element={<WrongPage />} />
                    </Routes>
                </BrowserRouter>
            </Grid>
        </div>
    );
}

export default App;