# Chat IRL

#### Video Demo:
[Available on YouTube](https://www.youtube.com/watch?v=YqZmGvLdqGo)

#### Description:
A real-time chat application where users can join and create chat rooms to talk to other users or send private messages to whoever they meet.

## Installation
Clone the repository and then from within the project directory execute the following commands:
```
pip install django djangorestframework django-cors-headers daphne channels channels_redis python-dotenv

python3 manage.py makemigrations users
python3 manage.py makemigrations chat
python3 manage.py migrate
python3 manage.py runserver
```

## Directories / Files

>***The files included in the decriptions below are those that have been modified or written by me. Any files that have not been included in this section are unmodified default files built upon creating a Django project.***

### main/ 
- **asgi.py**
    - Applies the settings module (settings.py) to the ASGI server.
    - Initializes Django's public ASGI interface.
    - Sets the "http" protocol to interface with Django ASGI.
    - Sets the host origin validator and authentication middleware to be utilized upon receiving "websocket" (ws://) protocol requests, with verified requests being passed on to the websocket url patterns I've defined in the application, using Channels' URLRouter class.
    

- **urls.py**

    - Maps Chat IRL's chat/urls.py and users/urls.py, as well as Django's built-in auth urls and admin urls, so their respective views and templates are accessible from the appropriate url paths.

- **settings.py**

    - Specifies the libraries, middleware and databases being used by Chat IRL.
    - Maps the specified user model to login/logout endpoints and their respective templates through each given template namespace.
    - Sets the path to Chat IRL's static, media and template directories.
    - Sets the default channel layer for Django Channels.
    - Applies CORS middleware settings to allow cross-origin requests.
    - Loads environment variables and secrets from .env file.

### users/
- **models.py**
    
    - A custom user manager is defined to adjust the way both users and superusers are created, requiring both an email address and a username before attempting to save a new user to the database.
    - A custom user model is defined, setting the email field as a replacement credential for the default username credential, and extending the user model with a color choice field, in order to set the color of the chat bubbles produced when the user sends a message in Chat IRL.

- **serializers.py**
    
    - A basic model serializer is used to automatically generate an appropriate JSON representation of user objects, as well as save new users to the database upon receiving valid JSON data.

- **views.py**
    
    - The login view checks for missing or incorrect credentials before signing in the user using their email and password.
    - The signup view contains the appropriate logic to validate the request data, handling cases in which form data received is missing, invalid, or the selected username or email have already been taken.
    - The profile view requires a username argument to be passed into the function by means of url path, returning a template with user data context as a response. If a POST request is received from the user matching the profile, the user's chat bubble color and username can be updated after data validation.

- **urls.py**

    - Url patterns have been defined to map Chat IRL's custom login and signup views to their respective url paths, and to dynamically generate url paths to each user's profile through their username.

- **admin.py**

    - The user model has been registered with Django admin.

### chat/

- **models.py**

    - Chat room model defined with fields for each room's metadata, room type and hashed invitation keys intended to be appended to url parameters to gain access to private rooms, as well as relationships with the user model in order to generate a list of users registered with the room, and the room owner - generally the room creator, but room ownership can be transferred manually from one user to another, or automatically upon user deletion or surrender of ownership.

    - Chat message model to temporarily store the messages sent in each chat room in order to generate a chat history upon entry to a room. Stores the text, time of creation, and foreign keys to the user and chat room models. Each time a new message is saved, a truncated copy of the message is automatically saved to the chat room model for display in the chat room's card in the room list view.

    - A private chat model is defined as a simplified version of chat rooms in which only two users interact. Shares historical message behavior of the chat room model.

    - Private message model has typical text, timestamp, user and private chat foreign key fields, and behaves in the same way as the chat message model.

- **serializers.py**

    - Chat room serializer is a simple model serializer with default behaviors.

    - Private chat serializer model serializer is extended to return the usernames of each user in the model's many to many relationship for dynamic generation of unique web socket channel names.

    - Chat message and private message serializers are model serializers both extended to return the usernames and chat bubble colors of each user to be appended to websocket response payloads.

- **views.py**

    - The index view is the application's home page, which requires the user to be logged in (otherwise being redirected to the login page), and retrieves and categorizes chat rooms into sticky rooms created by administrators, rooms for which the user has registered, and user-generated public rooms, with this data being returned as context for the index.html template.

    - The create view returns the chat room creation template (create_room.html) in response to GET requests. If form data is sent in a POST request, it validates and performs the necessary checks on the request data before creating a new chat room instance, redirecting the user to the newly created room.

    - The room view returns the details and messages of a specific chat room identified by its unique slug, and retrieves room details, messages, and additional rooms the user has access to for rendering in the chat room template. If a room matching the given slug does not exist, the user is redirected to the home page.

    - The private list view is checks the private room table of the database for private chats that include the user sending the request, returning all private chat instances to be rendered in the private_list template.

    - Retrieves the the chat history and user details for the chat between the requesting user and the target user, returning the data as context for rendering within the private.html template.

- **urls.py**

    - Defines the url patterns that map each of the chat app's views to their respective templates, with the chat room and private chat urls using dynamic url paths dependant upon the respective arguments passed into the url.

- **consumers.py**

    - ***ChatRoomConsumer():***

        - The connect method extracts the room name from the URL route and constructs a group name for the chat room, adding the consumer to the room group and accepting the websocket connection. Each new user is added to the room's active user list, as well as a site-wide online user list, and the connecting user is sent the current list of online users in order to render an asynchronously updated user list for the room.

        - The disconnect method removes the user from the online users list and the connected user list for the chat room, sending an updated user list to each user in the chat room and removing the consumer from the room group.

        - The receive method parses received JSON data to extract the sent message, calling the save_message() method to save the message to the database, and sends the message to the entire chat room group.

        - The chat message method sends the received chat message to the WebSocket.

        - The save message method saves the chat message to the database asynchronously.

        - The send initial connect users method sends the initial list of connected users in the chat room to newly connected users.

    - ***PrivateChatConsumer():***

        - The connect method retrieves the requesting user and the target user from the URL route, adding the requesting user to the online users list and constructing a room name for the private chat, adding the consumer to the private chat room group.

        - Removes the user from the online users list and the private chat room group.

        - The receive method parses received JSON data to extract a private chat message, and calls the save message method to save the message to the database before sending the private chat message to the entire private chat room.

        - The chat message method forwards the received message to the websocket.

        - The get target user method retrieves the target user from the database asynchronously.

        - The save message method retrieves the private chat, creating a private chat instance if one is not found, and saves the private message to the database.

- **routing.py**
    
    - Maps websocket url patterns to each of the consumers defined in consumers.py in order for users to send and receive data asynchronously.

- **admin.py**

    - Registers the chat room, chat messsage and private chat models with Django admin, excluding the private message model for privacy purposes.

### templates/

- **base.html**

    - The base template for the Chat IRL application, which imports the necessary packages in order to use Bootstrap 5, as well as custom fonts and SVG image repositories, throughout the application's templates, and creates the responsive, collapsible navbar for each of the applications pages. Jinja blocks are defined in the body and title portions of the template for customization in each of the app's templates.

### templates/users/

- **login.html**

    - A simple login form with email and password inputs that renders error descriptions when necessary using the Django's Messages library.

- **registration.html**

    - A typical user registration form with inputs for email, username, password, and password re-entry. This form integrates the Messages library for error rendering as well.

- **profile.html**

    - When a user visit's their own profile, a form is rendered allowing the user to change their username and chat bubble color. If another user's profile is visited, the target user's username and chat bubble color are displayed, as well as a link to generate a private chat with the user.

### templates/chat/

- **index.html**

    - The home page of Chat IRL. This page displays chat room cards, making each room available on-click. The layout seperates the rooms into Sticky, My Rooms, User-Generated and Private lists, generating each card through the context data provided by the Index view.

- **room.html**

    - The chat room template seperates the page into three sections.

        - The room list is the left-side section on desktop, or can be navigated to with a swipe-left gesture on mobile devices.

        - The user list is the right-side section on desktop, navigated to with a swipe-right gesture on mobile devices. Renders a list of active users in the room. Updated asynchronously by websocket, allowing the user to see when other users enter and leave the room.

        - The chat room's text-messenger is the central section on desktop, and the main screen on mobile devices. The chat input bar is fixed to the bottom of the screen, and the scrollable chat box contains a history of up to the last 50 messages sent within the room. Chat messages are sent and received through websocket connections created through the templates JavaScript code, which allows each message and user action to be rendered asynchronously as the client's websocket connection streams data to and from the Django server's websocket consumers.

- **private_list.html**

    - The private chat list template renders cards linked to each available private chat the user is a part of, or a message telling the user they have no available private chats. Function's like the home page, excluding the seperate chat categories.

- **private.html**

    - The private chat template contains the same asynchronous JavaScript logic as the chat room template's text messenger, including websocket functionality and a chat log.

- **create_room.html**

    - The room creation template allows the user to create new chat rooms through an HTML form with inputs for the room's title, description, and a checkbox to toggle between private and public. If accessing this page with administrator privileges, a second checkbox is rendered, allowing the admin to toggle between sticky and user-generated room types.

### static/

- Contains the app's logo, fonts, and a CSS stylesheet containing style constants to apply to the HTML and BODY elements of each page, as well as custom username and chat bubble style values to be applied based upon each user's selected color.

#### requirements.txt
- Contains a list of the Python library dependencies of the project and their versions.