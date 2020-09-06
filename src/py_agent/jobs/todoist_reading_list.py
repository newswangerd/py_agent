import re

from todoist import TodoistAPI
from py_agent.credentials import get_credential
from py_agent.my_utils import todoist as t_utils, article_parser

def todoist_reading_list(handler=None):
    todoist = TodoistAPI(get_credential('todoist_token'))
    todoist.sync()

    reading_list = t_utils.get_project_by_name(todoist, 'reading list')
    categories = t_utils.get_child_projects(todoist, reading_list)

    for task in todoist.state['items']:
        for project in categories:
            if task['project_id'] == project['id']:
                content = task['content']
                m = re.search(r'\[([^\[]+)\]\((.*)\)', content)
                title = m.group(1)
                url = m.group(2)
                comments = t_utils.get_comments_for_task(todoist, task)

                article = article_parser.parse_url(url)

                data = {
                    'url': url,
                    'title': title,
                    'summary': article.summary,
                    'keywords': article.keywords,
                    'text': article.text,
                    'published_date': article.publish_date,
                    'notes': comments,
                    'category': project['name']
                }

                handler.publish('archive_article', url, data)
                
                task.complete()
    
    todoist.commit()




