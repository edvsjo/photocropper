import React from 'react';
import path from 'path';
import fs from 'fs';

type imageProps = {
  folder: string
}

function fileInDirectory(folder: string){
  fs.readdir(folder, function (err,files) {
    console.log("starting to read!");
    if (err) {
      console.log("ran into an error");
      return folder
    }
    console.log(folder + '/' + files[0]);
    return (folder + '/' + files[0]);
  })
}

const Image = ({folder}: imageProps) => {
  const filename: string | void = fileInDirectory(folder)

  const image: string | void = typeof(filename) == typeof([]) ? filename : "../assets/icon.png";

  return (
    <div className="ImageContainer">
      <img src={require(image)} alt="No image found :)"></img>
    </div>
  );
};

export default Image;
