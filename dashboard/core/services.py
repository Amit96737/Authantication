import random
from users.models.users import User

def generate_unique_username(first_name):
    username = f"{first_name.lower()}{random.randint(1000, 9999)}"

    while User.objects.filter(username=username).exists():
        username = f"{first_name.lower()}{random.randint(1000, 9999)}"

    return username