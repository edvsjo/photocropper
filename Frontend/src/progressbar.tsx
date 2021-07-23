import React from 'react';
import CSS from 'csstype';

type ProgressBarProps = {
  progress: string;
}

const ProgressBar = ({progress}: ProgressBarProps) => {
  const arr = progress.split("/");
  const current = parseInt(arr[0]);
  const total = parseInt(arr[1]);
  const percent = (total==0) ? 0 : Math.round((current/total)*100);

  const fillerStyle: CSS.Properties = {
    height: '100%',
    width: `${percent}%`,
    textAlign: 'right',
    backgroundColor: "rgb(0, 175, 175)",
    borderRadius: '0.5rem/0.5rem',
  };

  return (
    <div className={"containerStyles"}>
      <div style={fillerStyle}>
        <span className={"labelStyles"}>{`${percent}%`}</span>
      </div>
    </div>
  );
}

export default ProgressBar;
