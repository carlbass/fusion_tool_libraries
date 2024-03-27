import adsk.core, adsk.fusion, adsk.cam, traceback
import os
import time
import base64

import json
global text_palette 
global ui

def run(context):
    global text_palette
    global ui

    app = adsk.core.Application.get()
    ui  = app.userInterface
    text_palette = ui.palettes.itemById('TextCommands')
    
    try:

        # start by seeing what tool libraries are in the github repository

        repo_url = "https://api.github.com/repos/carlbass/fusion_tool_libraries/contents"

        request = adsk.core.HttpRequest.create(repo_url, adsk.core.HttpMethods.GetMethod)
        request.setHeader ('accept', 'application/vnd.github+json')
        response = request.executeSync()

        if response.statusCode == 200:
            #text_palette.writeText (f'data: {response.data}')
            #tool_library_names = parse_github_json (response.data)

            jdata = json.loads(response.data)
    
            if jdata:
                for jd in jdata:
                    #text_palette.writeText (f'{jd["name"]} ====> {jd["sha"]}')
                    if jd['name'] == 'OMAX.json':
                        omax_sha = jd["sha"]
                        text_palette.writeText (f'{jd["name"]} ====> {jd["sha"]}')

        download_url = "https://raw.githubusercontent.com/carlbass/fusion_tool_libraries/main/OMAX.json"
    
        text_palette.writeText (f'Requesting: {download_url}')

        request = adsk.core.HttpRequest.create(download_url, adsk.core.HttpMethods.GetMethod)
        response = request.executeSync()
        
        if response.statusCode == 200:
            file_contents = response.data
            text_palette.writeText (file_contents)

            text_palette.writeText ('_____________________________')

            file_contents = '{"first_name": "Michael"}'
            encoded_file_contents = base64.b64encode(file_contents.encode("utf-8"))


        else:
            text_palette.writeText (f'ERROR: {response.statusCode}')

        # now try to update it
        
        github_token = os.getenv ('GITHUB_TOKEN')
        text_palette.writeText (f'token = {github_token}')
        github_token_string = f'Bearer {github_token}'
        text_palette.writeText (f'token string = {github_token_string}')

        text_palette.writeText ('_____________________________')

        json_request_data = {
            "message": "tool library push",
            "content": base64.b64encode(file_contents.encode()).decode(),
            "sha": omax_sha
            }
        
        json_request_string = json.dumps (json_request_data)


        text_palette.writeText (f'json_request_string = {json_request_string}')

        text_palette.writeText ('_____________________________')

        text_palette.writeText (f'token string = {github_token_string}')

        text_palette.writeText ('_____________________________')

        put_url = "https://api.github.com/repos/carlbass/fusion_tool_libraries/contents/OMAX.json"
        put_request = adsk.core.HttpRequest.create(put_url, adsk.core.HttpMethods.PutMethod)
        put_request.data = json_request_string
        
        put_request.setHeader ('accept', 'application/vnd.github+json')
        put_request.setHeader ('Authorization', github_token_string)
        
        put_response = put_request.executeSync()

        text_palette.writeText (f'put response code: {put_response.statusCode}')
        text_palette.writeText (f'put response: {put_response.data}')
    
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

