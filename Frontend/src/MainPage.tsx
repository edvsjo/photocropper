import React, { useState } from 'react';
import Folder from './folder';
import { Options, PythonShell } from 'python-shell';
import Placeholder from '../assets/Placeholder.jpg';
import ProgressBar from './progressbar';

const electron = window.require('electron');
const remote = electron.remote;
const app = remote.app;

const rootPath = app.getAppPath()
  .slice(0, app.getAppPath().length - '/Frontend/src'.length);

function runCropper(updateImage: Function, updateProgress: Function, path1: string, path2?: string) {
  let options: Options = {
    mode: 'text',
    pythonOptions: ['-u'],
    scriptPath: rootPath,
    args: [path1, path2],
  };
  const pyshell = new PythonShell('main.py', options);
  const progressregex = new RegExp('(0*1*2*3*4*5*6*7*8*9*)[/](0*1*2*3*4*5*6*7*8*9*)');
  pyshell.on('message', function(message) {
    if (progressregex.test(message)) {
      updateProgress(message)
    }
    else {
      console.log(message);
      updateImage(message);
    }
  });
}

function renderImage(inputPath: string, filename: string) {
  if (filename != '') {
    return(
      <img
        className="image Correct"
        src={inputPath + '/' + filename}
        alt="Not started yet😇"
      />
    );
  }
  else {
    return (
      <img
        className="image Placeholder"
        src={Placeholder}
        alt="Something very wrong happend 😭"
      />
    )
  }
};

const MainPage = () => {
  const [inputPath, setInputPath] = useState<string>("");
  const [outputPath, setOutputPath] = useState<string>("");
  const [progress, setProgress] = useState<string>("0/0");
  const [image, setImage] = useState<string>("");
  return (
    <div className="Main-Parrent">
      <div className="BtnGroup Input">
        <Folder buttonText="Input Folder" callback={setInputPath}></Folder>
        <div className="folderText">
          {inputPath ? inputPath : 'No folder selected 😞'}
        </div>
      </div>
      <div className="BtnGroup Output">
        <Folder buttonText="Output Folder" callback={setOutputPath}></Folder>
        <div className="folderText">
          {outputPath ? outputPath : 'No folder selected 😞'}
        </div>
      </div>
      <button
        className={"Btn"}
        onClick={() => runCropper(setImage, setProgress, inputPath, outputPath)}
        disabled={(inputPath != "") && (outputPath != "")}
      >
        {'Run Cropper 😁'}
      </button>
      <ProgressBar progress={progress}/>
      <div className="imagesContainer">
        {renderImage(inputPath, image)}
        {renderImage(outputPath, image)}
      </div>
    </div>
  );
};

export default MainPage;
