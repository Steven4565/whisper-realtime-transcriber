import { ReactMic, ReactMicStopEvent } from 'react-mic';
import React from 'react';

export class Example extends React.Component<{}, {record:boolean}> {
  constructor(props: any) {
    super(props);
    this.state = {
      record: false,
    };
  }

  startRecording = () => {
    this.setState({ record: true });
  };

  stopRecording = () => {
    this.setState({ record: false });
  };

  onData(recordedBlob:Blob) {
    (async function (){
      var reader = new FileReader();
      reader.readAsDataURL(recordedBlob); 
      reader.onloadend = function() {
        var base64data = reader.result;                
        fetch("http://localhost:5000/transcript", {
          method: "POST", 
          mode: "cors",
          headers: {
            "Content-Type": "text/plain"
          },
          body: base64data
        });
      }
    })()
  }

  onStop(recordedBlob:ReactMicStopEvent) {
    console.log('recordedBlob is: ', recordedBlob);
  }

  render() {
    return (
      <div>
        <ReactMic
          record={this.state.record}
          className="sound-wave"
          onStop={this.onStop}
          onData={this.onData}
          strokeColor="#000000"
          backgroundColor="#FF4081"
        />
        <button onClick={this.startRecording} type="button">
          Start
        </button>
        <button onClick={this.stopRecording} type="button">
          Stop
        </button>
      </div>
    );
  }
}
