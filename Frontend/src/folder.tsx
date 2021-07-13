import React from 'react';
const electron = window.require('electron');
const { shell } = window.require('electron');
const remote = electron.remote;
const { dialog } = remote;

type folderProps = {
  buttonText: string;
};

function openDialog() {
  dialog
    .showOpenDialog({
      title: 'Open Dialogue',
      message: 'First Dialog',
      properties: ['openDirectory'],
    })
    .then((result: { filePaths: string[] }) => {
      console.log(result);
      shell.openPath(result.filePaths[0]);
      console.log(result.filePaths[0]);
    });
}

const Folder = ({ buttonText }: folderProps) => {
  return (
    <>
      <button className="fileBtn" onClick={() => openDialog()}>
        {buttonText ? buttonText : 'Choose a folder'}
      </button>
    </>
  );
};

export default Folder;
