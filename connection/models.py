from django.db import models
from django.contrib.auth.models import User

class Connection(models.Model):
    """
    Represents a connection between two users.

    Attributes:
        to_user (User): The user to whom the friend request is sent.
        from_user (User): The user who sent the friend request.
        created_time (datetime): The timestamp when the connection was created.
        accepted (bool): Indicates whether the friend request is accepted.
    """

    to_user = models.ForeignKey(User, related_name='received_connection', on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, related_name='sent_connection', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Connection from {self.from_user.username} to {self.to_user.username}"

class UserConnectionIntermediateTable(models.Model):
    """
    Represents the intermediate table for user connections.

    Attributes:
        user (User): The user to whom this record belongs.
        friends (ManyToManyField): The friends of the user.
        sent_requests (ManyToManyField): The friend requests sent by the user.
        pending_requests (ManyToManyField): The friend requests received by the user.
    """
    user = models.OneToOneField(User, related_name='connections', on_delete=models.CASCADE)
    friends = models.ManyToManyField(User, related_name='friends')
    sent_requests = models.ManyToManyField(User, related_name='sent_requests')
    pending_requests = models.ManyToManyField(User, related_name='pending_requests')


    def __str__(self):
        return f"{self.user.username}'s connection details"
