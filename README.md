# OrgChat
One on One chat for Organization

## Setup Instruction

**Build:** Use `make up` command and you will find all command in `Makefile`.

**Create superuser:**  `docker exec -it [orgchat-web container id] python orgchat/manage.py createsuperuser` 

**Bulk insert:** Bulk insert some `organization`. Only super user can do that.

**User registration:**  After user registration user need to update his/her role by selectring his/her position in organization and need to add ogranization id. 

## API

