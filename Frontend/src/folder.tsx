import React, {useState} from 'react';
import runScript from "runCropper";

const SearchBar = () => {
  const [folder, setFolder] = useState<string>('');
  return (
    <>
      <input
        type="file"
        value={folder}
        placeholder={'Pick a folder'}
        onChange={(e) => setFolder(e.target.value)}
      />
      <img src={folder} alt="testing picture"/>
      <input type="button" value="Run Script!" onChange={(e) => runScript()}></input>
    </>
  );
};

export default SearchBar;
