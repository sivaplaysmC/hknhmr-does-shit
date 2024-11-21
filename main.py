from fastapi import FastAPI, File, UploadFile, HTTPException, Response

app = FastAPI()

# In-memory data structure to store notes associated with each ID
notes_store = {}


@app.get("/{id}", response_class=Response)
async def get_note(id: str):
    """
    Retrieves and displays the associated note for the given ID.
    """
    note = notes_store.get(id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return Response(content=note, media_type="text/plain")


@app.post("/{id}", response_class=Response)
async def append_note(id: str, note_file: UploadFile = File(...)):
    """
    Appends to the existing note for the given ID.
    Accepts a file upload containing the note content.
    """
    try:
        new_note_content = (await note_file.read()).decode("utf-8")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error reading uploaded file")

    if id in notes_store:
        notes_store[id] += f"\n{new_note_content}"
    else:
        notes_store[id] = new_note_content

    return Response(content="Note appended successfully", media_type="text/plain")


@app.delete("/{id}", response_class=Response)
async def delete_note(id: str):
    """
    Deletes the associated note for the given ID.
    """
    if id not in notes_store:
        raise HTTPException(status_code=404, detail="Note not found")

    del notes_store[id]
    return Response(content="Note deleted successfully", media_type="text/plain")
