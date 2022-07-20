# "Show-skills"

Backend is part of the "Show-skills" application, which allows you to `demonstrate your skills`, `share your knowledge` with other users. Also for moderation in the application there is an administration that has interaction with users.

![logo](https://user-images.githubusercontent.com/78900834/179995939-36a85425-f78d-43e4-8f05-d4ec7b2ed8e3.png)

***
<h2><a  href="https://show-skills.deta.dev/docs#/">Live Demo</a></h2>


# Domain model
One of the main models is the `User` representing the user in the system. The user can have `links` to accounts in other social networks. 
A user can `subscribe` to other users and can also find out that someone created an `event`.
Users can also add to themselves the `skills` they own. Users get access to the methods of the application, in accordance with its `role`. 

Also, one of the main classes is `posts` that users can create. Posts include `comments` and `likes`, `skills` related to this post and the `author` of the post.

![Пользователь](https://user-images.githubusercontent.com/78900834/179996044-47bf6af7-8719-406d-879e-d6418880b7b3.png)

# Authorization and access to methods
`Access tokens` are used to grant access to protected system resources only to authorized users. After authorization, the user receives a pair of `access` and `refresh` tokens.

The system assumes the presence of several roles: `super-administrator`, `administrators` and `users`, therefore, an access matrix was created to differentiate access rights to various methods and data of the system.

<table cellpadding="5" border="1">
    <thead>
        <tr>
            <th>Object\Role</th>
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

# Methods on user account data
To get information about users, there are two API methods, one of which returns the data of all accounts stored in the database 
and is intended for the administration of the system. The second method allows you to get the data of one user by username or a unique alias. 
The account is deleted from the application using the account key in the database. 
There is a separate endpoint API for changing optional user data, such as date of birth and place of residence.
The date of birth is transmitted as a number in the form of the number of milliseconds since the beginning of the Unix epoch GMT.
For a successful change, the user's age cannot be less than 14 years and not more than 100.

# Methods on skills
For various suggestions from users to the administration, for example, to add a new skill, there is a separate API method. 
Administrators can then review these proposals and mark them as read or completed. 

Skills can only be created by the administration of the application, and everyone can view them.
Also, according to the skill key, they can be added to or deleted by the users of the application, thereby marking the competencies they own.

# Methods on posts and events
When creating posts, images are uploaded separately and added to the content by URL. 
The content of the post itself is loaded separately as a string and stored as an html file. 
The post only stores a link to the file. The methods allow you to get all the posts and posts by the name of the skill presented in them. 
Also, the post can be deleted by the creator and the administration of the application, and only the author can edit it.

The user can inform subscribers about the upcoming event using events. The administration can get all the events and delete them. 
The user can also delete or edit the event. You can also get a list of events of a single user.
