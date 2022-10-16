import { ReactMic, ReactMicStopEvent } from 'react-mic';
import { Component } from 'react';
import { blobToBase64 } from '../utils/blobToBase64';

export class Example extends Component<{}, {record:boolean, buffer: string, timestamp:number}> {
  constructor(props: any) {
    super(props);
    this.state = {
      record: false,
      buffer: "",
      timestamp: Math.floor(Date.now() /1000),
    };

    this.onData = this.onData.bind(this);
    this.onStop = this.onStop.bind(this);
  }

  startRecording = () => {
    this.setState({ record: true });
  };

  stopRecording = () => {
    this.setState({ record: false });
  };

  async onData(recordedBlob:Blob) {
    const base64Blob = await blobToBase64(recordedBlob);

    this.setState((state) => { return {
      buffer: state.buffer + base64Blob,
    };});

    const currentTimestamp = Math.floor(Date.now()/1000);
    if (currentTimestamp === this.state.timestamp) return;
    
    fetch("http://localhost:5000/transcript", {
        method: "POST", 
        mode: "cors",
        headers: {
          "Content-Type": "text/plain"
        },
        body: this.state.buffer
      });

    this.setState(() => { return {
      buffer: "",
      timestamp: currentTimestamp
    };}); 
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
