from py_agent.credentials import get_credential
from py_agent.utils import listen_for
import dropbox
import re

@listen_for({'event_type': ('==', 'archive_article')})
def add_article_to_dropbox(event=None, handler=None):
    print("adding article")
    dbx = dropbox.Dropbox(get_credential("dropbox"))
    data = event.data
    markdown = []

    markdown.append('## ' + data['title'])

    markdown.append('Category: #' + data['category'].lower().replace(" ", "_"))

    markdown.append('**Keywords**: ' + ', '.join(data['keywords']))
    markdown.append('url: ' + data['url'])
    if len(data['notes']) > 0:
        markdown.append('### Notes')
        for note in data['notes']:
            markdown.append('- ' + note)
        
    markdown.append('### Summary')
    markdown.append(data['summary'])

    sanitized_title = re.sub(r"[^a-zA-Z0-9]+", ' ', data['title'])
    upload_path='/notes/articles/{}/{}.md'.format(data['category'], sanitized_title)

    existing_file = None
    try:
        # if the file doesn't exist, the api throws an exception
        f = dbx.files_download(upload_path)[1]
        existing_file = f.content.decode('utf-8')
    except:
        pass

    to_upload = '\n\n'.join(markdown)
    if existing_file:
        to_upload = existing_file + '\n\n\n\n' + to_upload

    dbx.files_upload(to_upload.encode('utf-8'),
        upload_path, mode=dropbox.files.WriteMode.overwrite)