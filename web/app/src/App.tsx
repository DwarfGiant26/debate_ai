import React, {useState} from 'react';
import './App.css';
import defaultProfile from './default-avatar.jpg'
import {Backend} from "./Backend"
import { useFilePicker } from 'use-file-picker';
import {FileContent} from "use-file-picker/types";
import {GetterT} from "./TypeHelper"

let backend: Backend = new Backend(" http://localhost:8000");

function App() {
    const [transcript, setTranscript] = useState("");
    return (
        <div className="App">
            <div className="column-container">
                <Debater isDebaterA={true}/>
                <DebatePlatform transcript={transcript} setTranscript={setTranscript}/>
                <Debater isDebaterA={false}/>
            </div>
        </div>
            );
}

function DebatePlatform({transcript, setTranscript}: {transcript: string, setTranscript: React.Dispatch<any>}) {
    return (
        <div className="debate-platform">
            <div className="upper-section">
                <Transcript content={transcript} lineSeparator={"---"}/>
            </div>
            <div className="lower-section">
                <StartDebateButton setTranscript={setTranscript}/>
            </div>
        </div>
    );
}

function Debater({isDebaterA}: {isDebaterA: boolean}) {
    return (
        <div className="debater">
            <div className="upper-section">
                <DebaterProfile/>
            </div>
            <div className="lower-section">
                <FilePicker isDebaterA={isDebaterA}/>
            </div>
        </div>
    );
}

function Transcript({content, lineSeparator}: { content: string, lineSeparator: string }) {
    let lines: string[] = content.split(lineSeparator);
    let isLeft: boolean = true;
    const rows = []

    for (let i = 0; i < lines.length; i++) {
        let temp: string[] = lines[i].split(":");
        let message: string = temp.slice(1, temp.length).join("");

        rows.push(
            <div className= {isLeft ? "message-left": "message-right"} key={i}>
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
        <div className={"profile-img"}>
            <img className="profile_img" src={defaultProfile} alt="profile image"></img>
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

function FilePicker({isDebaterA}: {isDebaterA: boolean}) {
    const { openFilePicker, filesContent, loading } = useFilePicker({
        accept: '.*',
    });

    if (loading) {
        return <div>Loading...</div>;
    }

    let getFileNames: GetterT<string[]> = () => filesContent.map((file, index) => (
            file.name
        ));
    function getFiles(): FileContent<any>[] {
        if (filesContent.length == 0){
            return [];
        }
        return filesContent;
    }

    return (
        <div className="file-picker">
            <button onClick={() => openFilePicker()}>Select files</button>
            <br />
            {getFileNames()}
            <StartIndexButton getFiles={getFiles} isDebaterA={isDebaterA}/>
        </div>
    );
}

function StartIndexButton({getFiles, isDebaterA}: {getFiles: GetterT<FileContent<string>[]>, isDebaterA: boolean}){
    function getFileContents(){
        let contents: string = "";
        getFiles().forEach((content) => {
            contents += content.content + "\n";
        });
        return contents;
    }
    return (
      <button onClick={() => backend.sendFiles(getFileContents(), isDebaterA)}>
          Start Index
      </button>
    );
}



export default App;
