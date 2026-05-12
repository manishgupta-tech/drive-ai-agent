from fastapi import FastAPI
from pydantic import BaseModel
from google.oauth2 import service_account
from googleapiclient.discovery import build

app = FastAPI()

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'credentials.json'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=SCOPES
)

service = build('drive', 'v3', credentials=credentials)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(request: ChatRequest):

    query = request.message.lower()

    # Conversational Query Handling

    if "pdf" in query:
        drive_query = "name contains '.pdf'"

    elif "image" in query or "png" in query:
        drive_query = "name contains '.png'"

    elif "invoice" in query:
        drive_query = "name contains 'invoice'"

    elif "report" in query:
        drive_query = "name contains 'Report'"

    elif "qr" in query:
        drive_query = "name contains 'qr'"

    else:
        drive_query = f"name contains '{request.message}'"

    results = service.files().list(
        q=drive_query,
        fields="files(id, name, webViewLink)"
    ).execute()

    files = results.get('files', [])

    return {
        "query_used": drive_query,
        "results": files
    }