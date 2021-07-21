import React, { useState } from 'react';
import Folder from './folder';
import { Options, PythonShell } from 'python-shell';

const electron = window.require('electron');
const remote = electron.remote;
const app = remote.app;

const rootPath = app.getAppPath()
  .slice(0, app.getAppPath().length - '/Frontend/src'.length);

function runCropper(updateFunction: Function, path1: string, path2?: string) {
  let options: Options = {
    mode: 'text',
    pythonOptions: ['-u'], // get print results in real-time
    scriptPath: rootPath,
    args: [path1, path2],
  };
  const pyshell = new PythonShell('main.py', options);
  pyshell.on('message', function(message) {
    updateFunction(message)
  });
}

const MainPage = () => {
  const [inputPath, setInputPath] = useState<string>("");
  const [outputPath, setOutputPath] = useState<string>("");
  const [progress, setProgress] = useState<string>("0/0");
  return (
    <div className="Main-Parrent">
      <Folder buttonText="Input Folder" callback={setInputPath}></Folder>
      <div>{inputPath}</div>
      <Folder buttonText="Output Folder" callback={setOutputPath}></Folder>
      <div>{outputPath}</div>
      <button onClick={() => runCropper(setProgress, inputPath, outputPath)}>
        {'Run Cropper 😁'}
      </button>
      <div>
        {'progress:' + progress}
      </div>
    </div>
  );
};

export default MainPage;
