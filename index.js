const express = require('express'); //Import the express dependency
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const sharp = require('sharp');
const {spawn} = require('child_process');
const bodyParser = require('body-parser');

const app = express();              //Instantiate an express app, the main work horse of this server
const port = 5000;                  //Save the port number where your server will be listening
const removal_mseconds = 10 * 1000;
const SCRIPT_NAME = 'test.py';

var results;
var resultsDone = false;

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));
app.set(bodyParser.urlencoded({ extended: true }));

//Idiomatic expression in express to route and respond to a client request
app.get('/', (req, res) => {        //get requests to the root ("/") will route here
  res.render('upload');                                                        //the .sendFile method needs the absolute path to the file, see: https://expressjs.com/en/4x/api.html#res.sendFile 
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
    limits: { files: 10} // Limiting to a maximum of 5 files
  }).array('images', 10);
  

// Serve static files
app.use(express.static('public'));

// Handle POST request to /upload
app.post('/upload', upload, (req, res) => {

    if (!req.files || req.files.length === 0) {

      res.status(400).send('No files uploaded.');
      return;

    }

    // Retrieve the form data
    const city = req.body.city;
    const neighborhood = req.body.neighborhood;
    const region = req.body.region;
    const quadraticMeters = req.body['quadratic-meters'];

    const formData = [];
    formData.push(city, neighborhood, region, quadraticMeters);

    const resizedImages = [];
    const resizedImagesUris = [];

    req.files.forEach((file) => {
      const filePath = file.path;
      const outputFileName = `${file.filename}`;
      const outputPath = `public/images/${outputFileName}`;
      resizedImagesUris.push('/images/'+outputFileName);

      sharp(filePath)
        .resize(800, 600, {fit: 'inside'})
        .toFile(outputPath, (err) => {
          if (err) {
            console.error(err);
            res.status(500).send('Error resizing the image.');
            return;
          } else {
            const resizedImage = {
              originalName: file.originalname,
              resizedFileName: outputFileName,
              resizedFilePath: outputPath
            };
            resizedImages.push(resizedImage);

            // Delete the original uploaded file
            fs.unlink(filePath, (err) => {
              if (err) {
                console.error(`Error deleting file: ${filePath}`, err);
              } else {
                console.log(`File deleted: ${filePath}`);

                // Schedule the removal of the resized image after 5 minutes
                setTimeout(() => {
                  fs.unlink(outputPath, (err) => {
                    if (err) {
                      console.error(`Error deleting file: ${outputPath}`, err);
                    } else {
                      console.log(`Resized image deleted: ${outputPath}`);
                    }
                  });
                }, removal_mseconds); // delete every mseconds
              }
            });
          }
        });
    });

    // Send the response with a success message
    const message = 'Now the images are being processed by our AI';
    res.render('upload-completed', { message });

    const pythonScript = spawn('python3', [SCRIPT_NAME, formData, resizedImagesUris]);
    
    pythonScript.stdout.on('data', function (data) {
      results = data.toString();
    });

    pythonScript.on('close', (resultCode) => {
      resultsDone = true;
    });
    
});

app.get('/get-result', (req, res) => {
  res.json({finished: resultsDone});
});

app.get('/results', (req, res) => {
  res.render('results', { results });
});

app.listen(port, () => {            //server starts listening for any attempts from a client to connect at port: {port}
    console.log(`Now listening on port ${port}`); 
});
