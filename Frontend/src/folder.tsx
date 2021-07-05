import React, {useState} from 'react';

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
    </>
  );
};

export default SearchBar;
