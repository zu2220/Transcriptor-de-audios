README.md (resumen de uso)

Copia .env.example a backend/.env y coloca tu HF_TOKEN (HuggingFace) si usarás pyannote.

Construir y levantar servicios:
    docker-compose build
    docker-compose up

Abre http://localhost:3000 para subir audios y comenzar la transcripción.

Consideraciones importantes

Recursos: La diarización y Whisper pueden ser pesados. Para 1 hora de audio en CPU puede tardar bastante. Si tienes GPU, adapta el Dockerfile para una imagen CUDA y la versión de torch con soporte CUDA.

Seguridad / Privacidad: Los audios se copian al contenedor y se procesan ahí. Si quieres evitar subir a terceros, usa el modo local y no configures OPENAI_API_KEY.

Mejoras posibles: diarización con clustering más fino, mejora de modelos whisper (medium/large), integración con subtítulos/exports (srt, vtt), cola de jobs (Redis + Celery) para procesar audios largos asíncronamente.