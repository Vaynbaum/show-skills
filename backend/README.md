# "Show-skills"

Backend is part of the "Show-skills" application, which allows you to `demonstrate your skills`, `share your knowledge` with other users. Also for moderation in the application there is an administration that has interaction with users.

![logo](https://user-images.githubusercontent.com/78900834/179995939-36a85425-f78d-43e4-8f05-d4ec7b2ed8e3.png)

***
<h2><a  href="https://showskillsback-1-v1549677.deta.app/">Live Demo</a></h2>


# Domain model
One of the main models is the `User` representing the user in the system. The user can have `links` to accounts in other social networks. 
A user can `subscribe` to other users and can also find out that someone created an `event`.
Users can also add to themselves the `skills` they own. Users get access to the methods of the application, in accordance with its `role`. 

Also, one of the main classes is `posts` that users can create. Posts include `comments` and `likes`, `skills` related to this post and the `author` of the post.

<img width="700px" src="https://user-images.githubusercontent.com/78900834/180272104-da56ec5b-6467-4a4d-b603-7282cec34c5c.png">

# Authorization and access to methods
`Access tokens` are used to grant access to protected system resources only to authorized users. After authorization, the user receives a pair of `access` and `refresh` tokens.

The system assumes the presence of several roles: `super-administrator`, `administrators` and `users`, therefore, an access matrix was created to differentiate access rights to various methods and data of the system.

<table cellpadding="5" border="1">
    <thead>
        <tr>
            <th>Object \ Role</th>
            <th>Super Administrator</th>
            <th>Administrator</th>
            <th>User</th>
            <th>Guest</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <th>Skills</th>
            <td>create, upload icons, get all, get skill icons</td>
            <td>create, upload icons, get all, get skill icons</td>
            <td>get all, get skill icons, add to yourself, delete from yourself</td>
            <td>get all, get skill icons</td>
        </tr>
        <tr>
            <th>Comments</th>
            <td>delete any</td>
            <td>delete any</td>
            <td>create, delete your</td>
            <td></td>
        </tr>
        <tr>
            <th>Posts</th>
            <td>delete any, get all, get pictures of posts, get a field</td>
            <td>delete any, get all, get pictures of posts, get a field</td>
            <td>create, upload pictures to posts, delete your own, change your own, get all, get pictures of posts, get a field</td>
            <td>get all, get pictures of posts, get a field</td>
        </tr>
        <tr>
            <th>Likes</th>
            <td></td>
            <td></td>
            <td>put, remove yours</td>
            <td></td>
        </tr>
        <tr>
            <th>Subscriptions</th>
            <td></td>
            <td></td>
            <td>delete yours, create, get yours</td>
            <td></td>
        </tr>
        <tr>
            <th>Roles</th>
            <td>assign, receive</td>
            <td>assign, receive</td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <th>Events</th>
            <td>delete any, get all, get by field</td>
            <td>delete any, get all, get by field</td>
            <td>delete yours, create, change yours, get by field</td>
            <td></td>
        </tr>
        <tr>
            <th>Users</th>
            <td>get all, get by username, delete any</td>
            <td>get all, get by username, delete your</td>
            <td>delete your, get by username, change additional data</td>
            <td>create, get by username</td>
        </tr>
        <tr>
            <th>Liks</th>
            <td></td>
            <td></td>
            <td>add, delete yours</td>
            <td></td>
        </tr>
        <tr>
            <th>Suggestions</th>
            <td>get all, get by field, tick</td>
            <td>get all, get by field, tick</td>
            <td>send</td>
            <td></td>
        </tr>
    </tbody>
</table>

The implementation of the role-based access system is performed using decorating methods that can be "hung" on one or another API method. 
These methods can be used `as one at a time or combined`. The API method will be called only if all access checks are successfully passed.
The creator of the decorator can get the parameters necessary for verification.

Example of a method for creating decorators

**File: access_handler.py**
```python
def maker_role_access(
        self,
        token: str = None,
        roles: list[RoleAccess] = None,
        is_lact_decorator: bool = True,
    ):
        """Creating a user access decorator by role"""

        def decorator_role_access(func):
            async def wrapped_role_access(*args, **kwargs):
                kwargs, user, role = await self.__get_role_user_access(
                    kwargs, token, roles
                )
                # If the role is found, then call method
                kwargs = self.__clean_temp_vars(is_lact_decorator, kwargs)
                return await func(*args, **kwargs)

            return wrapped_role_access

        return decorator_role_access
```

Usage example

**File: user_router.py**
```python
@router.delete("/", summary="Deleting a user by key")
async def delete_user_by_key(
    key: str = Query(),
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: DatabaseHandler = Depends(get_db),
):
    access_handler = AccessHandler(db)

    @access_handler.maker_role_access(
        credentials.credentials,
        [
            RoleAccess(SUPER_ADMIN, owners=[AnyOwner()]),
            RoleAccess(ADMIN, owners=[OwnOwner()]),
            RoleAccess(USER, owners=[OwnOwner()]),
        ],
        False,
    )
    @access_handler.maker_owner_access(key)
    async def inside_func(key):
        user_controller = UserController(db)
        event_controller = EventController(db)
        await event_controller.delete_event_by_user(key)
        return await user_controller.delete_user_by_key(key)

    return await inside_func(key)
```

# Methods on user account data
To get information about users, there are two API methods, one of which returns the data of `all accounts` stored in the database 
and is intended for the administration of the system. The second method allows you to `get the data of one user by username`. 
The account is `deleted` from the application using the `account key` in the database. 
There is a endpoint API for `changing addional user data`, such as `date of birth` and `place of residence`.
The date of birth is passed as the `number of milliseconds` since the beginning of the `Unix epoch GMT`.
For a `successful` change, the user's `age` cannot be `less than 14 years and not more than 100`.

# Methods on skills
For various `suggestions` from users to the administration, for example, to add a new skill, there is a API method. 
Administrators can then `view` these suggestions and `tick` them as `read or completed`. 

`Skills` can only be `created` by the administration of the application, and everyone can view them.
Also, according to the skill key, they can be `added to or deleted` by the users of the application, thereby marking the competencies they own.

# Methods on posts and events
When `creating posts`, `images` are uploaded separately and `added` to the content by `URL`. 
The `content` of the post itself is loaded separately as a string and stored as an html file. 
The post only `stores a link to the file`. The methods allow you to `get all` the posts and posts `by the name of the skill` presented in them. 
Also, the post can be `deleted` by the creator and the administration of the application, and only the author can `edit` it.

The user can `inform subscribers` about the upcoming event `using events`. The administration can `get all` the events and `delete` them. 
The user can also `delete or edit` the event. You can also `get a list of events` of a single user.

# Technologies in the project
The application is written using the FastAPI web framework. 
Deta Base, which is NoSQL, was chosen for the database, and Deta Drive cloud storage was chosen for storing files.
Functional tests of API methods are written using the Pytest environment.

![image](https://user-images.githubusercontent.com/78900834/180003050-423c586f-05da-4d9d-98c9-c5ae4d419edf.png)

# How to use
Register on the <a href="https://www.deta.sh/">Deta Cloud</a> platform

Changing the values of the fields in the **.env** file (be sure to fill in **DETA_PROJECT_KEY** and **APP_SECRET_STRING**).

Install requirements
>pip install -r requirements.txt

Start application
>uvicorn main:app

Open your browser at http://127.0.0.1:8000

Run tests
>pytest
