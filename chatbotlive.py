import pyaudio
import os
from subprocess import call

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="credentials.json"


CHUNK = 4096
WIDTH = 2
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 15

def detect_intent_stream(project_id, session_id, audio_file_path,
                         language_code):
    """Returns the result of detect intent with streaming audio as input.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    import dialogflow_v2 as dialogflow
    session_client = dialogflow.SessionsClient()

    # Note: hard coding audio_encoding and sample_rate_hertz for simplicity.
    audio_encoding = dialogflow.enums.AudioEncoding.AUDIO_ENCODING_LINEAR_16
    sample_rate_hertz = 16000

    session_path = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session_path))

    def request_generator(audio_config, audio_file_path):
        query_input = dialogflow.types.QueryInput(audio_config=audio_config)

        # The first request contains the configuration.
        yield dialogflow.types.StreamingDetectIntentRequest(
            session=session_path, query_input=query_input)

        # Here we are reading small chunks of audio data from a local
        # audio file.  In practice these chunks should come from
        # an audio input device.

        with open(audio_file_path, 'rb') as audio_file:
           # while True:
            chunk = audio_file.read()
            #if not chunk:
             #   break
            # The later requests contains audio data.
            yield dialogflow.types.StreamingDetectIntentRequest(
                input_audio=chunk)





    audio_config = dialogflow.types.InputAudioConfig(
        audio_encoding=audio_encoding, language_code=language_code,
        sample_rate_hertz=sample_rate_hertz)

    requests = request_generator(audio_config, audio_file_path)
    #print("Got Request")
    responses = session_client.streaming_detect_intent(requests)

    print('=' * 20)
    for response in responses:
        print('Intermediate transcript: "{}".'.format(
                response.recognition_result.transcript))

    # Note: The result from the last response is the final transcript along
    # with the detected content.
    query_result = response.query_result

    print('=' * 20)
    print('Query text: {}'.format(query_result.query_text))
    print('Detected intent: {} (confidence: {})\n'.format(
        query_result.intent.display_name,
        query_result.intent_detection_confidence))
    print('Fulfillment text: {}\n'.format(
        query_result.fulfillment_text))
    #print(type(query_result.fulfillment_text))

    #if query_result.fulfillment_text != '0':
    #print("no response")
    with open("output/response.txt", 'w') as file:
        file.write(query_result.fulfillment_text)
    call("source 2.7venv/bin/activate; python pepper_say.py", shell=True)
    return query_result


if __name__ == "__main__":

    project_id = 'jokes-fvvqts'
    session_id = 'voice-trial'
    audio_file_path = 'output/file1.wav'
    language_code = 'en-US'
    result = detect_intent_stream(project_id, session_id, audio_file_path, language_code)
