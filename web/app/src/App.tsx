import React, {useState} from 'react';
import './App.css';
import defaultProfile from './default-avatar.jpg'
import {Backend} from "./Backend"

let backend: Backend = new Backend(" http://localhost:8000");

function App() {
    const [transcript, setTranscript] = useState("");
    return (
        <div className="App">
            <div className="column-container">
                <DebaterProfile/>
                <Transcript content={transcript} lineSeparator={"---"} />
                <DebaterProfile/>
            </div>
            <StartDebateButton setTranscript={setTranscript}/>
        </div>
    );
}

function Transcript({content, lineSeparator}:{content: string, lineSeparator: string}) {
    let lines: string[] = content.split(lineSeparator);
    let isLeft: boolean = true;
    const rows = []

    for (let i = 0; i < lines.length; i++) {
        let temp: string[] = lines[i].split(":");
        let message: string = temp.slice(1, temp.length).join("");

        rows.push(
            <div className= {isLeft ? "message left": "message right"} key={i}>
                <p>{message}</p>
            </div>
        )
        isLeft = !isLeft
    }

    return (
        <div className="chat-container">
            {rows}
        </div>);
}

function DebaterProfile(){
    return (
        <div className={"Debater"}>
            <img src={defaultProfile} alt="profile image"></img>
        </div>
    );
}

function StartDebateButton({setTranscript}: {setTranscript: Function}){
    async function updateTranscript(){
        setTranscript(await backend.startDebate());
    }
    return (
        <button
            className={"start-debate-button"}
            key={0}
            title={"Start Debate"}
            onClick={() => updateTranscript()}>
            Start Debate
        </button>
    )
}



export default App;
