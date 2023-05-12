const express = require('express'); //Import the express dependency
const multer = require('multer');
const path = require('path');
const fs = require('fs');

const app = express();              //Instantiate an express app, the main work horse of this server
const port = 5000;                  //Save the port number where your server will be listening

//Idiomatic expression in express to route and respond to a client request
app.get('/', (req, res) => {        //get requests to the root ("/") will route here
    res.sendFile('index.html', {root: __dirname});      //server responds by sending the index.html file to the client's browser
                                                        //the .sendFile method needs the absolute path to the file, see: https://expressjs.com/en/4x/api.html#res.sendFile 
});

// Configure multer storage
const storage = multer.diskStorage({
    destination: './uploads/',
    filename: function (req, file, cb) {
      cb(null, file.fieldname + '-' + Date.now() + path.extname(file.originalname));
    }
  });
  
// Initialize multer upload
const upload = multer({
    storage: storage,
    limits: { files: 5 } // Limiting to a maximum of 5 files
  }).array('images', 5);
  

// Serve static the image uploads
app.use(express.static('uploads'));

// Serve static files
app.use(express.static('public'));

// Handle POST request to /upload
app.post('/upload', upload, (req, res) => {
    if (!req.files || req.files.length === 0) {
      res.status(400).send('No files uploaded.');
    } else {
      const filesToDelete = [];
      req.files.forEach((file) => {
        filesToDelete.push(file.path);
      });
  
      res.send('Files uploaded successfully!');
  
      // Schedule file cleanup after 5 minutes
      setTimeout(() => {
        filesToDelete.forEach((file) => {
          fs.unlink(file, (err) => {
            if (err) {
              console.error(`Error deleting file: ${file}`, err);
            } else {
              console.log(`File deleted: ${file}`);
            }
          });
        });
      }, 5 * 60 * 1000); // 5 minutes (converted to milliseconds)
    }
  });

app.listen(port, () => {            //server starts listening for any attempts from a client to connect at port: {port}
    console.log(`Now listening on port ${port}`); 
});