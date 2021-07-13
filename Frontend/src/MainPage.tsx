import React, { useState } from 'react';
import Folder from './folder';
import { Options, PythonShell } from 'python-shell';

const electron = window.require('electron');
const remote = electron.remote;
const app = remote.app;

const rootPath = app
  .getAppPath()
  .slice(0, app.getAppPath().length - '/Frontend/src'.length);

function runCropper(path1: string, path2?: string) {
  let options: Options = {
    mode: 'text',
    pythonOptions: ['-u'], // get print results in real-time
    scriptPath: rootPath,
    args: [path1, path2],
  };
  PythonShell.run('main.py', options, function (err: any, result: any) {
    if (err) throw err;
    console.log('results: %j', result);
  });
}

const MainPage = () => {
  const [inputPath, setInputPath] = useState<string>("");
  const [outputPath, setOutputPath] = useState<string>("")

  return (
    <div className="Main-Parrent">
      <Folder buttonText="Input Folder" callback={setInputPath}></Folder>
      <Folder buttonText="Output Folder" callback={setOutputPath}></Folder>
      <button onClick={() => runCropper(inputPath, outputPath)} >
        {'Run Cropper'}
      </button>
    </div>
  );
};

export default MainPage;
