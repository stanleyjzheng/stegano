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
import FormControl from "@material-ui/core/FormControl";
import { toast } from "react-toastify";

const useStyles = makeStyles((theme) => ({
    root: {
        "& > *": {
            margin: theme.spacing(1),
        },
    },
    input: {
        display: "none",
    },
    formControl: {
        margin: theme.spacing(1),
        minWidth: 220,
    },
    submit: {
        marginTop: 20,
    },
    photobutton: {
        marginTop: 10,
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
        console.log(option);
        if (file === undefined) {
            toast.error("Oop! Please Upload a File with the Camera Button!");
            setImage("");
            return;
        }
        const formData = new FormData();
        formData.append("file", file);
        if (option === "Encode Image") {
            const response = await fetch("/api/encode", {
                method: "POST",
                body: formData,
            });
            setImage(await response.text());
        } else if (option === "Decode Image") {
            const response = await fetch("/api/decode", {
                method: "POST",
                body: formData,
            });
            console.log(await response.text());
        } else {
            // Run Model On Image
            // TODO
            const response = await fetch("/api/predict", {
                method: "POST",
                body: formData,
            });
            console.log(await response.text());
        }
        // toast.info("Uploaded File Successfully!");
        // setImage();
        // const {message, imageSrc] } await response.json();
        // console.log(message, imageSrc);
        // setImage(imageSrc);
    };

    const [option, setOption] = useState("Encode Image");
    const [open, setOpen] = useState(false);

    const handleChange = (event) => {
        setOption(event.target.value);
    };

    const handleClose = () => {
        setOpen(false);
    };

    const handleOpen = () => {
        setOpen(true);
    };

    return (
        <div className="App">
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
                <br />

                <FormControl className={classes.formControl}>
                    <InputLabel id="demo-controlled-open-select-label">
                        What would you like to do?
                    </InputLabel>
                    <Select
                        labelId="demo-controlled-open-select-label"
                        id="demo-controlled-open-select"
                        open={open}
                        onClose={handleClose}
                        onOpen={handleOpen}
                        value={option}
                        onChange={handleChange}
                        defaultValue="Encoded Image"
                    >
                        <MenuItem value={"Encode Image"}>Encode Image</MenuItem>
                        <MenuItem value={"Decode Image"}>Decode Image</MenuItem>
                        <MenuItem value={"Run Model On Image"}>
                            Run Model On Image
                        </MenuItem>
                    </Select>
                </FormControl>

                {/* <FormControl className={classes.formControl}>
                    <InputLabel id="demo-controlled-open-select-label">
                        What would you like to do?
                    </InputLabel>

                    <Select
                        labelId="demo-controlled-open-select-label"
                        id="demo-controlled-open-select"
                        open={open}
                        onClose={handleClose}
                        onOpen={handleOpen}
                        value={age}
                        onChange={handleChange}
                    >
                        <MenuItem>Encode Image</MenuItem>
                        <MenuItem>Decode Image</MenuItem>
                        <MenuItem>Run Model On Image</MenuItem>
                    </Select>
                </FormControl> */}
                {/* <br /> */}
                {/* <Select
                    labelId="demo-simple-select-label"
                    id="demo-simple-select"
                    value="What would you like to do?"
                    //   onChange={handleChange}
                >
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
                        className={classes.photobutton}
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
