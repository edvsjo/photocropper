import React, { useState } from 'react';
const electron = window.require('electron');
const remote = electron.remote;
const { dialog } = remote;

type folderProps = {
  buttonText: string;
  callback: Function;
};


const Folder = ({ buttonText, callback }: folderProps) => {
  const [folder, setFolder] = useState<string>("");
  function openDialog() {
    dialog
      .showOpenDialog({
        title: 'Open Dialogue',
        message: buttonText,
        properties: ['openDirectory'],
      })
      .then((result: { filePaths: string[] }) => {
        callback(result.filePaths[0])
        setFolder(result.filePaths[0])
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
