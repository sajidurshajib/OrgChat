from channels.middleware import BaseMiddleware
import jwt
from django.contrib.auth.models import AnonymousUser
from channels.exceptions import DenyConnection
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from accounts.models import Role 
import os
import re

class JWTAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        token = self.get_token_from_scope(scope)

        # Log the token to verify it’s extracted correctly
        print(f"Extracted token: {token}")

        if token:
            user = await self.get_user_from_token(token)
            if isinstance(user, AnonymousUser):
                await self.deny_connection(send)
                return  
        else:
            user = AnonymousUser() 
            await self.deny_connection(send)
            return 

        # Extract sender and receiver IDs from the path using a regular expression
        path = scope.get("path", "")
        print(f"Path received: {path}")

        match = re.match(r'^/ws/chat/(\d+)/(\d+)/$', path)

        if match:
            sender_id, receiver_id = match.groups()
            print(f"Extracted sender_id: {sender_id}, receiver_id: {receiver_id}")
        else:
            print(f"Invalid path format: {path}")
            await self.deny_connection(send)
            return

        # Check if both users belong to the same organization
        try:
            sender = await sync_to_async(get_user_model().objects.get)(id=sender_id)
            receiver = await sync_to_async(get_user_model().objects.get)(id=receiver_id)

            sender_role = await sync_to_async(Role.objects.filter(user=sender).first)()
            receiver_role = await sync_to_async(Role.objects.filter(user=receiver).first)()

            # Log roles and organizations for debugging
            print(f"Sender Role: {sender_role}, Receiver Role: {receiver_role}")

            if not sender_role or not receiver_role:
                print("Missing roles for one or both users")
                await self.deny_connection(send)
                return

            if sender_role.organization_id != receiver_role.organization_id:
                print(f"Different organizations: Sender Org ID: {sender_role.organization_id}, Receiver Org ID: {receiver_role.organization_id}")
                await self.deny_connection(send)
                return
        except Exception as e:
            print(f"Error fetching users or roles: {e}")
            await self.deny_connection(send)
            return

        # Success: users belong to the same organization
        scope['user'] = user
        return await super().__call__(scope, receive, send)

    # async def __call__(self, scope, receive, send):
    #     token = self.get_token_from_scope(scope)

    #     if token:
    #         user = await self.get_user_from_token(token)
    #         if isinstance(user, AnonymousUser):
    #             await self.deny_connection(send)
    #             return  
    #     else:
    #         user = AnonymousUser() 
    #         await self.deny_connection(send)
    #         return 

    #     scope['user'] = user
    #     return await super().__call__(scope, receive, send)

    
    def get_token_from_scope(self, scope):
        query_string = scope.get('query_string', b'').decode('utf-8')
        token = None
        if 'token=' in query_string:
            token = query_string.split('token=')[-1]
        return token

    async def get_user_from_token(self, token):
        from django.contrib.auth import get_user_model
        from asgiref.sync import sync_to_async

        try:
            payload = jwt.decode(token, os.environ.get('SECRET_KEY'), algorithms=['HS256'])

            User = get_user_model()

            user = await sync_to_async(User.objects.get)(id=payload['user_id'])
            return user
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return AnonymousUser()  
        except User.DoesNotExist:
            return AnonymousUser()  

    async def deny_connection(self, send):
        await send({
            "type": "websocket.close",
            "code": 4000
        })
