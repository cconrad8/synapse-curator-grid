from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from synapseclient import Synapse
from synapseclient.models import Folder, RecordSet

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_synapse(token: str) -> Synapse:
    syn = Synapse()
    syn.login(authToken=token, silent=True)
    return syn


@app.get("/")
def root():
    return {"status": "ok"}


# ======================================================
# Request model
# ======================================================

class BindSchemaRequest(BaseModel):
    schemaUri: str
    entityType: str  # "folder" or "recordset"
    entityId: str


# ======================================================
# Bind JSON Schema endpoint
# ======================================================

@app.post("/bind-json-schema")
def bind_json_schema(
    payload: BindSchemaRequest,
    Authorization: str = Header(...)
):
    try:
        token = Authorization.replace("Bearer ", "")
        syn = get_synapse(token)

        if payload.entityType == "folder":
            entity = Folder(id=payload.entityId)
            result = entity.bind_schema_async(
                json_schema_uri=payload.schemaUri,
                enable_derived_annotations=True,
                synapse_client=syn,
            )

        elif payload.entityType == "recordset":
            entity = RecordSet(id=payload.entityId)
            result = entity.bind_schema_async(
                json_schema_uri=payload.schemaUri,
                enable_derived_annotations=True,
                synapse_client=syn,
            )

        else:
            raise HTTPException(
                status_code=400,
                detail="entityType must be 'folder' or 'recordset'"
            )

        return f"Successfully bound schema {payload.schemaUri} to {payload.entityType} {payload.entityId}"

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
