# 文字起こしからfirebsseにアップロード

import requests
import openai
import firebase_admin
from firebase_admin import credentials, firestore
import datetime
from datetime import datetime

# Whisper API
openai.api_key =  ''

# Firebase SDK
cred = credentials.Certificate('/home/a/linklog-d2eb6-firebase-adminsdk-kbljv-a1665230f2.json') # jsonのパス
firebase_admin.initialize_app(cred)

# Firebaseのクライアント
db = firestore.client()

# 音声ファイルのパス
audio_file = '/home/a/test.mp3'

def transcribe_audio(file_path):
    try:
        # 音声ファイルを開く
        with open(file_path, 'rb') as audio_file:
            # Whisper APIで音声ファイルを文字起こし
            transcript = openai.Audio.transcribe(
                model="whisper-1",
                file=audio_file
            )

        # 結果の文字起こしを取得
        transcription_text = transcript['text']
        print("Transcription result:")
        print(transcription_text)

        # Cloud Firestoreにアップロード
        upload_to_firestore(transcription_text)

    except Exception as e:
        print(f"An error occurred: {e}")

def upload_to_firestore(text):
    try:
        # 現在の日時を取得
        now = datetime.now()
        document_id = now.strftime('%Y%m%d%H%M')

        # "voice"コレクション日時を作成
        doc_ref = db.collection('voice').document(document_id)

        # サブコレクションに文字起こしの結果を追加
        subcollection_ref = doc_ref.collection('transcriptions').document()
        subcollection_ref.set({
            'transcription': text,
            'timestamp': now
        })


        print("Transcription uploaded to Firestore successfully.")

    except Exception as e:
        print(f"An error occurred while uploading to Firestore: {e}")

# 文字起こしを実行
transcribe_audio(audio_file)
