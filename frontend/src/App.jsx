import React, { useState } from 'react'


export default function App(){
const [file, setFile] = useState(null)
const [loading, setLoading] = useState(false)
const [transcript, setTranscript] = useState([])


const upload = async () => {
if(!file) return
setLoading(true)
const fd = new FormData()
fd.append('file', file)
const res = await fetch('http://localhost:8000/transcribir', { method: 'POST', body: fd })
const data = await res.json()
setTranscript(data.transcripcion || [])
setLoading(false)
}


return (
<div style={{padding: 24}}>
<h1>Transcriptor con Diarización</h1>
<input type="file" accept="audio/*" onChange={e=>setFile(e.target.files[0])} />
<button onClick={upload} disabled={loading} style={{marginLeft:12}}>{loading? 'Transcribiendo...':'Subir y transcribir'}</button>


<div style={{marginTop:20}}>
{transcript.map((s,i)=> (
<div key={i} style={{marginBottom:12}}>
<b>{s.speaker}</b> [{s.start.toFixed(1)}s - {s.end.toFixed(1)}s]:<br />
{s.text}
</div>
))}
</div>
</div>
)
}