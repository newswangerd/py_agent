import re
import logging

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
                logging.info(content)
                m = re.search(r'\[([^\[]+)\]\((.*)\)', content)

                # The todoist app stores links as either a markdown formatted link or "title - url"
                # if markdown links fail, try to parse the "title - url" format.
                if m:
                    logging.info("markdown group")
                    title = m.group(1)
                    url = m.group(2)
                    logging.info(title)
                    logging.info(url)
                else:
                    logging.info("hyphen group")
                    content_components = content.split(" - ")
                    if len(content_components) > 1:
                        title = ''.join(content_components[:-1])
                        url = content_components[-1].strip()
                        logging.info(title)
                        logging.info(url)
                    else:
                        task.update(content="FAILED TO PARSE: " + content)
                        task.move(parent_id=reading_list['id'])

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




