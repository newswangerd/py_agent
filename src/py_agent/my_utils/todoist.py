def get_project_by_name(client, project_name):
    for p in client.state['projects']:
        if p['name'].lower() == project_name.lower():
            return p


def get_child_projects(client, parent):
    children = []

    for p in client.state['projects']:
        if p['parent_id'] == parent['id']:
            children.append(p)

    return children


def get_comments_for_task(client, task):
    comments = []

    for note in client.state['notes']:
        if note['item_id'] == task['id']:
            comments.append(note['content'])
    
    return comments