import { ReactMic, ReactMicStopEvent } from 'react-mic';
import React from 'react';

export class Example extends React.Component<{}, {record:boolean, buffer: string, timestamp:number}> {
  constructor(props: any) {
    super(props);
    this.state = {
      record: false,
      buffer: "",
      timestamp: Date.now(),
    };
  }

  startRecording = () => {
    this.setState({ record: true });
  };

  stopRecording = () => {
    this.setState({ record: false });
  };

  async onData(recordedBlob:Blob) {
    const blobText = await recordedBlob.text();

    this.setState((state) => { return {
      buffer: state.buffer + blobText,
    };});

    if (Date.now() !== this.state.timestamp) {
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
    }
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
