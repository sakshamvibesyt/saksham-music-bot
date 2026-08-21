from pyrogram import Client

API_ID = int(input("Enter API_ID: "))
API_HASH = input("Enter API_HASH: ")

with Client(
    "saksham_music",
    api_id=API_ID,
    api_hash=API_HASH,
    in_memory=True
) as app:
    print("\nYour SESSION_STRING:\n")
    print(app.export_session_string())
