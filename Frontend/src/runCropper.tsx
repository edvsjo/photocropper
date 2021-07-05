import React from 'react';
import {PythonShell} from 'python-shell';

const runScript = () => {
  PythonShell.run(
    '/Users/sportmannimac/Documents/photocropper/main.py',
    null,
    function (err: any, result: any) {
      if (err) throw err;
      console.log('results: %j', result);
    }
  );
  return (
    <div> Finshed m8</div>
  )
};

export default runScript;
