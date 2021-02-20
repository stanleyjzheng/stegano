// import logo from "./logo.svg";
import "./App.css";
import { useForm } from "react-hook-form";

function App() {
    const { register, handleSubmit } = useForm();

    const onSubmit = async (data) => {
        const imageFile = data.image[0];
        const response = await fetch("/api/upload", {
            method: "POST",
            body: imageFile,
        });
        console.log(await response.text());
    };

    return (
        <div className="App">
            <header className="App-header">
                <p>Upload Image!</p>
                <form onSubmit={handleSubmit(onSubmit)}>
                    <input required ref={register} type="file" name="image" />
                    <button type="submit">Upload</button>
                </form>
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
