import express from "express";
import { Remarkable } from "remarkable";
import fs from 'node:fs';

var md = new Remarkable();
const app = express();
const port = 3000;

app.get('/', (req, res) => {
  res.send('Welcome to my server!');
});

app.get('/:search', (req, res) => {
  var answer = "Oh no, my pancakes";
  console.log(req.params) 
  try {
    const data = fs.readFileSync(req.params.search, 'utf8');
    answer = md.render( data )
  } catch (err) {
    console.error(err);
  }

  res.send(answer);
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
