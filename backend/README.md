# "Show-skills"

Backend is part of the "Show-skills" application, which allows you to `demonstrate your skills`, `share your knowledge` with other users. Also for moderation in the application there is an administration that has interaction with users.

***
<h2><a  href="https://show-skills.deta.dev/docs#/">Live Demo</a></h2>


# Domain model

# Authorization and access to methods

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
