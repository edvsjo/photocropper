import React, { useState } from 'react';
import Folder from './folder';
import { Options, PythonShell } from 'python-shell';

const electron = window.require('electron');
const remote = electron.remote;
const app = remote.app;

const rootPath = app.getAppPath()
  .slice(0, app.getAppPath().length - '/Frontend/src'.length);

function runCropper(updateImage: Function, updateProgress: Function, path1: string, path2?: string) {
  let options: Options = {
    mode: 'text',
    pythonOptions: ['-u'], // get print results in real-time
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

const MainPage = () => {
  const [inputPath, setInputPath] = useState<string>("");
  const [outputPath, setOutputPath] = useState<string>("");
  const [progress, setProgress] = useState<string>("0/0");
  const [image, setImage] = useState<string>("");
  return (
    <div className="Main-Parrent">
      <Folder buttonText="Input Folder" callback={setInputPath}></Folder>
      <div>{inputPath}</div>
      <Folder buttonText="Output Folder" callback={setOutputPath}></Folder>
      <div>{outputPath}</div>
      <button onClick={() => runCropper(setImage, setProgress, inputPath, outputPath)}>
        {'Run Cropper 😁'}
      </button>
      <div>
        {'progress:' + progress}
      </div>
      <img className="image" src={inputPath + '/' + image} alt="Not started yet😇" ></img>
      <img className="image" src={outputPath + '/' + image} alt="Not started yet😇"></img>
    </div>
  );
};

export default MainPage;
