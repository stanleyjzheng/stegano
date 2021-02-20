// import logo from "./logo.svg";
import "./App.css";
import { useState } from "react";

function App() {
    const [file, setFile] = useState();

    const onChange = (e) => {
        setFile(e.target.files[0]);
    };

    const onSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append("file", file);
        const response = await fetch("/api/upload", {
            method: "POST",
            body: formData,
        });
        console.log(response);
    };

    return (
        <div className="App">
            <header className="App-header">
                <p>Upload Image!</p>
                <form onSubmit={onSubmit}>
                    <input required type="file" onChange={onChange} />
                    <button type="submit">Upload</button>
                </form>
                {/* <img src={image} /> */}

                {/* <img src={logo} className="App-logo" alt="logo" /> */}
                {/* <a
                    className="App-link"
                    href="https://reactjs.org"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    Learn React
                </a> */}
            </header>
        </div>
    );
}

export default App;
