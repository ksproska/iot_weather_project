import { useEffect } from "react";

import { BrowserRouter, Routes, Route } from "react-router-dom";

import Header from "./components/Header/Header";
import Home from "./components/Main/Home/Home";
import Room from "./components/Main/Room/Room";
import WrongPage from "./components/Main/WrongPage";

function App() {

    useEffect(() => {
        fetch("/roomnames", {
            method: "GET",
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(res => res.json()).then(result => {
            console.log(result);
        }).catch((err) => {
            console.error(err);
        });
    });

    return (
        <div className="App" style={{ height: '100%' }}>
            <BrowserRouter>
                <Header />
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/room/:roomId" element={<Room />} />
                    <Route path="*" element={<WrongPage />} />
                </Routes>
            </BrowserRouter>
        </div>
    );
}

export default App;