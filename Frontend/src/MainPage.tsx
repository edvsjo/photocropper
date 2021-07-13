import React from 'react';
import Folder from './folder';
import {Options, PythonShell} from 'python-shell';

const electron = window.require('electron');
const remote = electron.remote;
const app = remote.app;

const rootPath = app.getAppPath().slice(0, app.getAppPath().length - "/Frontend/src".length);

function runCropper(path1: string, path2?: string) {
  let options: Options = {
    mode: 'text',
    pythonOptions: ['-u'], // get print results in real-time
    scriptPath: rootPath,
    args: [path1, path2],
  };
  PythonShell.run(
    'main.py',
    options,
    function (err: any, result: any) {
      if (err) throw err;
      console.log('results: %j', result);
    }
  );
}



const MainPage = () => {
  return (
    <div className="Main-Parrent">
      <Folder buttonText="Input Folder"></Folder>
      <Folder buttonText="Output Folder"></Folder>
      {/* <button onClick={() => runCropper("/Users/sportmannimac/Downloads", "/Users/sportmannimac/Downloads/output")} > {'Run Cropper'}</button> */}
      <button
        onClick={() =>
          runCropper(
            '/Users/sportmannimac/Downloads/610881_Soft.jpg'
          )
        }
      >
        {'Run Cropper'}
      </button>
    </div>
  );
}

export default MainPage;
