import React from 'react';
import './App.css';
import defaultProfile from './default-avatar.jpg'
import {Backend} from "./Backend"

let backend: Backend = new Backend("localhost:8080");

function App() {
    let transcript = "test transcript \n hello \n what";
    return (
        <div className="App">
            <div className="column-container">
                <DebaterProfile/>
                <Transcript content={transcript} lineSeparator={"\n"} />
                <DebaterProfile/>
            </div>
            <StartDebateButton/>
        </div>
    );
}

function Transcript({content, lineSeparator}:{content: string, lineSeparator: string}) {
    let lines: string[] = content.split(lineSeparator);
    let isLeft: boolean = true;
    const rows = []

    for (let i = 0; i < lines.length; i++) {
        rows.push(
            <div className= {isLeft ? "message left": "message right"} key={i}>
                <p>{lines[i]}</p>
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

function StartDebateButton(){
    return (
        <button
            className={"start-debate-button"}
            key={0}
            title={"Start Debate"}
            onSubmit={backend.startDebate}>
            Start Debate
        </button>
    )
}



export default App;
