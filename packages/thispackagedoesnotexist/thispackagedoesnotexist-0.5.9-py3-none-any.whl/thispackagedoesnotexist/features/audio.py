import pyaudio
import base64

def start_audio_stream(self, client, converter):
    try:
        p = pyaudio.PyAudio()

        input_device_count = p.get_device_count()
        input_device_found = False
        for i in range(input_device_count):
            if p.get_device_info_by_index(i).get('maxInputChannels') > 0:
                input_device_found = True
                break

        if not input_device_found:
            client.emit('message', converter.encode({"audio_logger": "From Client: No input device found"}))
            return

        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=44100,
                        input=True,
                        frames_per_buffer=1024)
        
        while self.audio_handler:
            audio_data = stream.read(1024)
            audio_data_base64 = base64.b64encode(audio_data).decode("utf-8")
            client.emit('message', converter.encode({"audio": audio_data_base64}))

    except Exception as e:
        client.emit('message', converter.encode({"audio_logger": str(e)}))