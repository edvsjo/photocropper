import React from 'react';
const electron = window.require('electron');
const remote = electron.remote;
const { dialog } = remote;

type folderProps = {
  buttonText: string;
  callback: Function;
};


const Folder = ({ buttonText, callback }: folderProps) => {
  function openDialog() {
    dialog
      .showOpenDialog({
        title: 'Open Dialogue',
        message: 'First Dialog',
        properties: ['openDirectory'],
      })
      .then((result: { filePaths: string[] }) => {
        console.log(result.filePaths[0]);
        callback(result.filePaths[0])
      });
  }
  return (
    <>
      <button className="fileBtn" onClick={() => openDialog()}>
        {buttonText ? buttonText : 'Choose a folder'}
      </button>
    </>
  );
};

export default Folder;
