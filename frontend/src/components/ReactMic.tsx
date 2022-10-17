import { ReactMic, ReactMicStopEvent } from 'react-mic';
import { Component } from 'react';
import { blobToBase64 } from '../utils/blobToBase64';

export class Example extends Component<{}, {record:boolean, buffer: Array<Blob>, timestamp: number}> {
  constructor(props: any) {
    super(props);
    this.state = {
      record: false,
      buffer: [],
      timestamp: Math.floor(Date.now() /1000)
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
    this.setState((state) => { return {
      buffer: [...state.buffer, recordedBlob]
    };});

    const currentTimestamp = Math.floor(Date.now()/1000);
    if (currentTimestamp === this.state.timestamp) return;
    
    const blob = new Blob(this.state.buffer, { type: "audio/wav"});
    
    fetch("http://localhost:5000/transcript", {
        method: "POST", 
        mode: "cors",
        headers: {
          "Content-Type": "text/plain"
        },
        body: await blobToBase64(blob)
    });

    this.setState(() => { return {
      // buffer: [],
      timestamp: currentTimestamp
    };}); 
  }

  async onStop(recordedBlob:ReactMicStopEvent) {
    this.setState({
      buffer: []
    });
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
          mimeType="audio/wav"
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
