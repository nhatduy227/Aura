import time, logging
from datetime import datetime
import threading, os, os.path
import deepspeech
import numpy as np
import wave
from halo import Halo
from scipy import signal
from vadAudio import VADAudio
from inputOutput import initSpeakEngine, speak
from intentValidator import *
from executor import *
from utility import *

logging.basicConfig(level=20)

def processQuery(engine, query, curMode):
    foundIntent = False
    for isIntent, execute in COMMANDS:
        if isIntent(query):
            return execute(engine, query)

    executeUnknownCommand(engine)
    return Modes.Waiting

COMMANDS = [(isGreetingCommand, executeGreeting), (isByeCommand, executeByeCommand), (isSelectModeCommand, executeSelectModeCommand),
            (isShowInstructionCommand, executeShowInstructionCommand)]


def main(ARGS):
    # Load DeepSpeech model
    if os.path.isdir(ARGS.model):
        model_dir = ARGS.model
        ARGS.model = os.path.join(model_dir, 'output_graph.pb')
        ARGS.scorer = os.path.join(model_dir, ARGS.scorer)

    print('Initializing model...')
    logging.info("ARGS.model: %s", ARGS.model)
    model = deepspeech.Model(ARGS.model)
    if ARGS.scorer:
        logging.info("ARGS.scorer: %s", ARGS.scorer)
        model.enableExternalScorer(ARGS.scorer)

    # Init ttsx engine
    engine = initSpeakEngine('male')
    # TODO: Change initial mode to Modes.Iddle, Modes.Waiting is only for testing purpose
    curMode = Modes.Waiting

    # Start audio with VAD
    vad_audio = VADAudio(aggressiveness=ARGS.vad_aggressiveness,
                         device=ARGS.device,
                         input_rate=ARGS.rate,
                         file=ARGS.file)
    print("Listening (ctrl-C to exit)...")
    frames = vad_audio.vad_collector()

    # Stream from microphone to DeepSpeech using VAD
    spinner = None
    if not ARGS.nospinner:
        spinner = Halo(spinner='line')
    stream_context = model.createStream()
    wav_data = bytearray()
    for frame in frames:
        if frame is not None:
            if spinner: spinner.start()
            logging.debug("streaming frame")
            stream_context.feedAudioContent(np.frombuffer(frame, np.int16))
            if ARGS.savewav: wav_data.extend(frame)
        else:
            if spinner: spinner.stop()
            logging.debug("end utterence")
            if ARGS.savewav:
                vad_audio.write_wav(os.path.join(ARGS.savewav, datetime.now().strftime("savewav_%Y-%m-%d_%H-%M-%S_%f.wav")), wav_data)
                wav_data = bytearray()
            query = stream_context.finishStream().lower()
            if query is not '' and query is not None:
                print("Recognized: %s" % query)
                processQuery(engine, query, curMode)
            stream_context = model.createStream()

if __name__ == '__main__':
    DEFAULT_SAMPLE_RATE = 16000

    import argparse
    parser = argparse.ArgumentParser(description="Stream from microphone to DeepSpeech using VAD")

    parser.add_argument('-v', '--vad_aggressiveness', type=int, default=3,
                        help="Set aggressiveness of VAD: an integer between 0 and 3, 0 being the least aggressive about filtering out non-speech, 3 the most aggressive. Default: 3")
    parser.add_argument('--nospinner', action='store_true',
                        help="Disable spinner")
    parser.add_argument('-w', '--savewav',
                        help="Save .wav files of utterences to given directory")
    parser.add_argument('-f', '--file',
                        help="Read from .wav file instead of microphone")

    parser.add_argument('-m', '--model', required=True,
                        help="Path to the model (protocol buffer binary file, or entire directory containing all standard-named files for model)")
    parser.add_argument('-s', '--scorer',
                        help="Path to the external scorer file.")
    parser.add_argument('-d', '--device', type=int, default=None,
                        help="Device input index (Int) as listed by pyaudio.PyAudio.get_device_info_by_index(). If not provided, falls back to PyAudio.get_default_device().")
    parser.add_argument('-r', '--rate', type=int, default=DEFAULT_SAMPLE_RATE,
                        help=f"Input device sample rate. Default: {DEFAULT_SAMPLE_RATE}. Your device may require 44100.")

    ARGS = parser.parse_args()
    if ARGS.savewav: os.makedirs(ARGS.savewav, exist_ok=True)
    main(ARGS)
