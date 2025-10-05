import os, subprocess, uuid
from typing import List

# Funciones utilitarias: segmentar audio, transcribir con whisper local, diarización

def segment_audio(input_audio: str, start: float, end: float, max_chunk_seconds: int = 600) -> List[str]:
    """Corta el rango start-end en chunks de max_chunk_seconds y devuelve rutas a files WAV"""
    duration = end - start
    if duration <= 0:
        return []
    chunks = []
    offset = start
    idx = 0
    while offset < end:
        chunk_end = min(end, offset + max_chunk_seconds)
        out = f"/tmp/{uuid.uuid4().hex}_{idx}.wav"
        cmd = [
            'ffmpeg', '-y', '-i', input_audio, '-ss', str(offset), '-to', str(chunk_end),
            '-ar', '16000', '-ac', '1', '-sample_fmt', 's16', out
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        chunks.append(out)
        offset = chunk_end
        idx += 1
    return chunks

def transcribe_segment_with_whisper(wav_path: str) -> str:
    try:
        import whisper
        model = whisper.load_model('small')
        res = model.transcribe(wav_path, language='es')
        return res.get('text', '')
    except Exception as e:
        # si falla, intenta usar OpenAI API si está configurada (no implementado aquí)
        return ''

def diarize_audio(audio_path: str):
    """Usa pyannote.audio para realizar diarización.
    Devuelve lista de dicts: {start, end, speaker}
    """
    try:
        from pyannote.audio import Pipeline
        import os
        hf_token = os.getenv('HF_TOKEN')
        pipeline = Pipeline.from_pretrained('pyannote/speaker-diarization', use_auth_token=hf_token)
        diarization = pipeline(audio_path)
        turns = []
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            turns.append({'start': turn.start, 'end': turn.end, 'speaker': speaker})
        return turns
    except Exception as e:
        # En caso de fallo, fallback: tratar todo como un único speaker
        import wave, contextlib
        with contextlib.closing(wave.open(audio_path,'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
        return [{'start': 0.0, 'end': duration, 'speaker': 'Speaker_1'}]