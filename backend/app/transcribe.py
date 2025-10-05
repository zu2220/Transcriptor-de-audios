import os, tempfile, math
from utils import segment_audio, transcribe_segment_with_whisper, diarize_audio


# Flujo principal: 1) Diarizar 2) Segmentar por hablante 3) Transcribir segmentos 4) Unir


def transcribe_file(audio_path: str):
    # 1) Diarización: devuelve lista de turnos (start, end, speaker)
    diarization = diarize_audio(audio_path)

    results = []
    for turn in diarization:
        start, end, speaker = turn['start'], turn['end'], turn['speaker']
        # extraer segmento (por seguridad, limitar chunk a 10 min si es necesario)
        segments = segment_audio(audio_path, start, end, max_chunk_seconds=600)
        texts = []
        for seg_path in segments:
            text = transcribe_segment_with_whisper(seg_path)
            texts.append(text)
            try:
                os.remove(seg_path)
            except:
                pass
        results.append({
            'speaker': speaker,
            'start': start,
            'end': end,
            'text': ' '.join(t.strip() for t in texts)
        })
    return results