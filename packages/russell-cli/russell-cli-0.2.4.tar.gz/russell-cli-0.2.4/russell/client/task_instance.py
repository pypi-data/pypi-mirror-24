from russell.client.base import RussellHttpClient
from russell.model.task_instance import TaskInstance


class TaskInstanceClient(RussellHttpClient):
    """
    Client to interact with TaskInstance api
    """
    def __init__(self):
        self.url = "/taskinstances/"
        super(TaskInstanceClient, self).__init__()

    def get(self, id):
        response = self.request("GET",
                                "{}{}".format(self.url, id))
        task_instance_dict = response.json()
        ti = TaskInstance.from_dict(task_instance_dict)
        return ti
