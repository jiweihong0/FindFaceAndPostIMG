def get_credentials():
    from oauth2client.file import Storage
    from oauth2client import client
    from oauth2client import tools

    try:
        import argparse
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    except ImportError:
        flags = None

    SCOPES = 'https://www.googleapis.com/auth/drive'
    CLIENT_SECRET_FILE = './poimgLib/client_id.json'
    credential_path = "./poimgLib/google-postimg.json"
    APPLICATION_NAME = 'postIMGtoLine'
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
    return credentials

def postimg(imgfile):
    from apiclient.http import MediaFileUpload
    from apiclient import discovery
    import httplib2
    import requests
    import json

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    media = MediaFileUpload(imgfile, mimetype='image/jpg')
    res = service.files().create(body={'name':'upload.jpg','parents': ["1g6_9Oi-2Mue5slrYoMiyadzGue4CkFEk"]},media_body=media,fields='id').execute()
    requests.post(url="https://script.google.com/macros/s/AKfycbzvD6WQT_TBZvC_NqU0T5ie8APljxlyOXz_8Z2xoFKN8129jJOK/exec",data=json.dumps({"imgurl":'https://drive.google.com/uc?export=download&id=' + res['id']}))
    
