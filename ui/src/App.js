import "./App.css";
import { useState } from "react";
import { Button } from "@material-ui/core";
import IconButton from "@material-ui/core/IconButton";
import PhotoCamera from "@material-ui/icons/PhotoCamera";
import { makeStyles } from "@material-ui/core/styles";
import Typography from "@material-ui/core/Typography";
import MenuItem from "@material-ui/core/MenuItem";
import Select from "@material-ui/core/Select";
import InputLabel from "@material-ui/core/InputLabel";

const useStyles = makeStyles((theme) => ({
    root: {
        "& > *": {
            margin: theme.spacing(1),
        },
    },
    input: {
        display: "none",
    },
}));

function App() {
    const classes = useStyles();
    const [file, setFile] = useState();
    const [image, setImage] = useState(""); // image src

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
        setImage(await response.text());
        // setImage();
        // const {message, imageSrc] } await response.json();
        // console.log(message, imageSrc);
        // setImage(imageSrc);
    };

    return (
        <div className="App container">
            <br />
            <br />
            <br />
            <Typography
                variant="h2"
                color="secondary"
                component="h2"
                gutterBottom
            >
                Stegano
            </Typography>
            <Typography variant="h5" component="h2" gutterBottom>
                End-to-end steganography and steganlysis with Deep Convolutional
                Neural Networks
            </Typography>
            <Typography variant="h6" component="h2" gutterBottom>
                For best results, use a high resolution (at least 512x512)
                image.
            </Typography>
            <form className={classes.root} onSubmit={onSubmit}>
                {/* <input
                    accept="image/*"
                    className={classes.input}
                    id="contained-button-file"
                    multiple
                    type="file"
                /> */}
                <InputLabel id="demo-customized-select-label">Age</InputLabel>
                <Select
                    labelId="demo-customized-select-label"
                    id="demo-customized-select"
                    value="Age"
                    //   onChange={handleChange}
                    //   input={<BootstrapInput />}
                >
                    <MenuItem value="">
                        <em>None</em>
                    </MenuItem>
                    <MenuItem value={10}>Ten</MenuItem>
                    <MenuItem value={20}>Twenty</MenuItem>
                    <MenuItem value={30}>Thirty</MenuItem>
                </Select>
                {/* <Select
                    labelId="demo-simple-select-label"
                    id="demo-simple-select"
                    value="What would you like to do?"
                    //   onChange={handleChange}
                >
                    <MenuItem>Encode Image</MenuItem>
                    <MenuItem>Decode Image</MenuItem>
                    <MenuItem>Run Model On Image</MenuItem>
                </Select> */}
                <Button
                    type="submit"
                    variant="contained"
                    color="secondary"
                    className={classes.submit}
                    onClick={onSubmit}
                >
                    Upload
                </Button>
                <input
                    accept="image/*"
                    className={classes.input}
                    id="icon-button-file"
                    type="file"
                    onChange={onChange}
                />
                <label htmlFor="icon-button-file">
                    <IconButton
                        color="secondary"
                        aria-label="upload picture"
                        component="span"
                    >
                        <PhotoCamera />
                    </IconButton>
                </label>
            </form>
            <br />
            {image ? <img src={image} alt="stego" /> : null}
        </div>
    );
}

export default App;
