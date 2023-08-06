
"""
Client for Messaging Content Store HTTP services APIs.

"""
from .seed_services import SeedServicesApiClient


class SchedulerApiClient(SeedServicesApiClient):
    """
    Client for Scheduler Service.
    """

    def get_schedules(self, params=None):
        return self.session.get('/schedule/', params=params)

    def get_schedule(self, schedule_id):
        return self.session.get('/schedule/%s/' % schedule_id)

    def create_schedule(self, schedule):
        return self.session.post('/schedule/', data=schedule)

    def update_schedule(self, schedule_id, schedule):
        return self.session.patch('/schedule/%s/' % schedule_id,
                                  data=schedule)

    def delete_schedule(self, schedule_id):
        return self.session.delete('/schedule/%s/' % schedule_id)

    def get_failed_tasks(self, params=None):
        return self.session.get('/failed-tasks/', params=params)

    def requeue_failed_tasks(self):
        return self.session.post('/failed-tasks/')
