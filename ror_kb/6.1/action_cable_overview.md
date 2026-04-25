v6.1.7.10

**More at [rubyonrails.org:](https://rubyonrails.org/)**
More Ruby on Rails


- [Blog](https://rubyonrails.org/blog)
- [Guides](https://guides.rubyonrails.org/)
- [API](https://api.rubyonrails.org/)
- [Forum](https://discuss.rubyonrails.org/)
- [Contribute on GitHub](https://github.com/rails/rails)

* * *

## Action Cable Overview

In this guide, you will learn how Action Cable works and how to use WebSockets to
incorporate real-time features into your Rails application.

After reading this guide, you will know:

- What Action Cable is and its integration backend and frontend
- How to set up Action Cable
- How to set up channels
- Deployment and Architecture setup for running Action Cable

### ![](https://guides.rubyonrails.org/v6.1/images/chapters_icon.gif)Chapters

01. [What is Action Cable?](https://guides.rubyonrails.org/v6.1/action_cable_overview.html#what-is-action-cable-questionmark)
02. [Terminology](https://guides.rubyonrails.org/v6.1/action_cable_overview.html#terminology)    - [Connections](https://guides.rubyonrails.org/v6.1/action_cable_overview.html#terminology-connections)
    - [Consumers](https://guides.rubyonrails.org/v6.1/action_cable_overview.html#consumers)
    - [Channels](https://guides.rubyonrails.org/v6.1/action_cable_overview.html#terminology-channels)
    - [Subscribers](https://guides.rubyonrails.org/v6.1/action_cable_overview.html#subscribers)
    - [Pub/Sub](https://guides.rubyonrails.org/v6.1/action_cable_overview.html#pub-sub)
    - [Broadcastings](https://guides.rubyonrails.org/v6.1/action_cable_overview.html#terminology-broadcastings)
03. [Server-Side Components](https://guides.rubyonrails.org/v6.1/action_cable_overview.html#server-side-components)    - [Connections](https://guides.rubyonrails.org/v6.1/action_cable_overview.html#server-side-components-connections)
    - [Channels](https://guides.rubyonrails.org/v6.1/action_cable_overview.html#server-side-components-channels)
04. [Client-Side Components](https://guides.rubyonrails.org/v6.1/action_cable_overview.html#client-side-components)    - [Connections](https://guides.rubyonrails.org/v6.1/action_cable_overview.html#connections)
05. [Client-Server Interactions](https://guides.rubyonrails.org/v6.1/action_cable_overview.html#client-server-interactions)    - [Streams](https://guides.rubyonrails.org/v6.1/action_cable_overview.html#streams)
    - [Broadcastings](https://guides.rubyonrails.org/v6.1/action_cable_overview.html#client-server-interactions-broadcastings)
    - [Subscriptions](https://guides.rubyonrails.org/v6.1/action_cable_overview.html#client-server-interactions-subscriptions)
    - [Passing Parameters to Channels](https://guides.rubyonrails.org/v6.1/action_cable_overview.html#passing-parameters-to-channels)
    - [Rebroadcasting a Message](https://guides.rubyonrails.org/v6.1/action_cable_overview.html#rebroadcasting-a-message)
06. [Full-Stack Examples](https://guides.rubyonrails.org/v6.1/action_cable_overview.html#full-stack-examples)    - [Example 1: User Appearances](https://guides.rubyonrails.org/v6.1/action_cable_overview.html#example-1-user-appearances)
    - [Example 2: Receiving New Web Notifications](https://guides.rubyonrails.org/v6.1/action_cable_overview.html#example-2-receiving-new-web-notifications)
    - [More Complete Examples](https://guides.rubyonrails.org/v6.1/action_cable_overview.html#more-complete-examples)
07. [Configuration](https://guides.rubyonrails.org/v6.1/action_cable_overview.html#configuration)    - [Subscription Adapter](https://guides.rubyonrails.org/v6.1/action_cable_overview.html#subscription-adapter)
    - [Allowed Request Origins](https://guides.rubyonrails.org/v6.1/action_cable_overview.html#allowed-request-origins)
    - [Consumer Configuration](https://guides.rubyonrails.org/v6.1/action_cable_overview.html#consumer-configuration)
    - [Worker Pool Configuration](https://guides.rubyonrails.org/v6.1/action_cable_overview.html#worker-pool-configuration)
    - [Client side logging](https://guides.rubyonrails.org/v6.1/action_cable_overview.html#client-side-logging)
    - [Other Configurations](https://guides.rubyonrails.org/v6.1/action_cable_overview.html#other-configurations)
08. [Running Standalone Cable Servers](https://guides.rubyonrails.org/v6.1/action_cable_overview.html#running-standalone-cable-servers)    - [In App](https://guides.rubyonrails.org/v6.1/action_cable_overview.html#in-app)
    - [Standalone](https://guides.rubyonrails.org/v6.1/action_cable_overview.html#standalone)
    - [Notes](https://guides.rubyonrails.org/v6.1/action_cable_overview.html#notes)
09. [Dependencies](https://guides.rubyonrails.org/v6.1/action_cable_overview.html#dependencies)
10. [Deployment](https://guides.rubyonrails.org/v6.1/action_cable_overview.html#deployment)
11. [Testing](https://guides.rubyonrails.org/v6.1/action_cable_overview.html#testing)

### [1 What is Action Cable?](https://guides.rubyonrails.org/v6.1/action_cable_overview.html\#what-is-action-cable-questionmark)

Action Cable seamlessly integrates
[WebSockets](https://en.wikipedia.org/wiki/WebSocket) with the rest of your
Rails application. It allows for real-time features to be written in Ruby in the
same style and form as the rest of your Rails application, while still being
performant and scalable. It's a full-stack offering that provides both a
client-side JavaScript framework and a server-side Ruby framework. You have
access to your full domain model written with Active Record or your ORM of
choice.

### [2 Terminology](https://guides.rubyonrails.org/v6.1/action_cable_overview.html\#terminology)

Action Cable uses WebSockets instead of the HTTP request-response protocol.
Both Action Cable and WebSockets introduce some less familiar terminology:

#### [2.1 Connections](https://guides.rubyonrails.org/v6.1/action_cable_overview.html\#terminology-connections)

_Connections_ form the foundation of the client-server relationship.
A single Action Cable server can handle multiple connection instances. It has one
connection instance per WebSocket connection. A single user may have multiple
WebSockets open to your application if they use multiple browser tabs or devices.

#### [2.2 Consumers](https://guides.rubyonrails.org/v6.1/action_cable_overview.html\#consumers)

The client of a WebSocket connection is called the _consumer_. In Action Cable
the consumer is created by the client-side JavaScript framework.

#### [2.3 Channels](https://guides.rubyonrails.org/v6.1/action_cable_overview.html\#terminology-channels)

Each consumer can in turn subscribe to multiple _channels_. Each channel
encapsulates a logical unit of work, similar to what a controller does in
a regular MVC setup. For example, you could have a `ChatChannel` and
an `AppearancesChannel`, and a consumer could be subscribed to either
or to both of these channels. At the very least, a consumer should be subscribed
to one channel.

#### [2.4 Subscribers](https://guides.rubyonrails.org/v6.1/action_cable_overview.html\#subscribers)

When the consumer is subscribed to a channel, they act as a _subscriber_.
The connection between the subscriber and the channel is, surprise-surprise,
called a subscription. A consumer can act as a subscriber to a given channel
any number of times. For example, a consumer could subscribe to multiple chat rooms
at the same time. (And remember that a physical user may have multiple consumers,
one per tab/device open to your connection).

#### [2.5 Pub/Sub](https://guides.rubyonrails.org/v6.1/action_cable_overview.html\#pub-sub)

[Pub/Sub](https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern), or
Publish-Subscribe, refers to a message queue paradigm whereby senders of
information (publishers), send data to an abstract class of recipients
(subscribers), without specifying individual recipients. Action Cable uses this
approach to communicate between the server and many clients.

#### [2.6 Broadcastings](https://guides.rubyonrails.org/v6.1/action_cable_overview.html\#terminology-broadcastings)

A broadcasting is a pub/sub link where anything transmitted by the broadcaster is
sent directly to the channel subscribers who are streaming that named broadcasting.
Each channel can be streaming zero or more broadcastings.

### [3 Server-Side Components](https://guides.rubyonrails.org/v6.1/action_cable_overview.html\#server-side-components)

#### [3.1 Connections](https://guides.rubyonrails.org/v6.1/action_cable_overview.html\#server-side-components-connections)

For every WebSocket accepted by the server, a connection object is instantiated. This
object becomes the parent of all the _channel subscriptions_ that are created
from there on. The connection itself does not deal with any specific application
logic beyond authentication and authorization. The client of a WebSocket
connection is called the connection _consumer_. An individual user will create
one consumer-connection pair per browser tab, window, or device they have open.

Connections are instances of `ApplicationCable::Connection`, which extends
[`ActionCable::Connection::Base`](https://api.rubyonrails.org/v6.1.7.10/classes/ActionCable/Connection/Base.html). In `ApplicationCable::Connection`, you
authorize the incoming connection, and proceed to establish it if the user can
be identified.

##### [3.1.1 Connection Setup](https://guides.rubyonrails.org/v6.1/action_cable_overview.html\#connection-setup)

```
# app/channels/application_cable/connection.rb
module ApplicationCable
  class Connection < ActionCable::Connection::Base
    identified_by :current_user

    def connect
      self.current_user = find_verified_user
    end

    private
      def find_verified_user
        if verified_user = User.find_by(id: cookies.encrypted[:user_id])
          verified_user
        else
          reject_unauthorized_connection
        end
      end
  end
end
```

Copy

Here [`identified_by`](https://api.rubyonrails.org/v6.1.7.10/classes/ActionCable/Connection/Identification/ClassMethods.html#method-i-identified_by) designates a connection identifier that can be used to find the
specific connection later. Note that anything marked as an identifier will automatically
create a delegate by the same name on any channel instances created off the connection.

This example relies on the fact that you will already have handled authentication of the user
somewhere else in your application, and that a successful authentication sets an encrypted
cookie with the user ID.

The cookie is then automatically sent to the connection instance when a new connection
is attempted, and you use that to set the `current_user`. By identifying the connection
by this same current user, you're also ensuring that you can later retrieve all open
connections by a given user (and potentially disconnect them all if the user is deleted
or unauthorized).

If your authentication approach includes using a session, you use cookie store for the
session, your session cookie is named `_session` and the user ID key is `user_id` you
can use this approach:

```
verified_user = User.find_by(id: cookies.encrypted['_session']['user_id'])
```

Copy

##### [3.1.2 Exception Handling](https://guides.rubyonrails.org/v6.1/action_cable_overview.html\#server-side-components-connections-exception-handling)

By default, unhandled exceptions are caught and logged to Rails' logger. If you would like to
globally intercept these exceptions and report them to an external bug tracking service, for
example, you can do so with [`rescue_from`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveSupport/Rescuable/ClassMethods.html#method-i-rescue_from):

```
# app/channels/application_cable/connection.rb
module ApplicationCable
  class Connection < ActionCable::Connection::Base
    rescue_from StandardError, with: :report_error

    private

    def report_error(e)
      SomeExternalBugtrackingService.notify(e)
    end
  end
end
```

Copy

#### [3.2 Channels](https://guides.rubyonrails.org/v6.1/action_cable_overview.html\#server-side-components-channels)

A _channel_ encapsulates a logical unit of work, similar to what a controller does in a
regular MVC setup. By default, Rails creates a parent `ApplicationCable::Channel` class
(which extends [`ActionCable::Channel::Base`](https://api.rubyonrails.org/v6.1.7.10/classes/ActionCable/Channel/Base.html)) for encapsulating shared logic between your channels.

##### [3.2.1 Parent Channel Setup](https://guides.rubyonrails.org/v6.1/action_cable_overview.html\#parent-channel-setup)

```
# app/channels/application_cable/channel.rb
module ApplicationCable
  class Channel < ActionCable::Channel::Base
  end
end
```

Copy

Then you would create your own channel classes. For example, you could have a
`ChatChannel` and an `AppearanceChannel`:

```
# app/channels/chat_channel.rb
class ChatChannel < ApplicationCable::Channel
end
```

Copy

```
# app/channels/appearance_channel.rb
class AppearanceChannel < ApplicationCable::Channel
end
```

Copy

A consumer could then be subscribed to either or both of these channels.

##### [3.2.2 Subscriptions](https://guides.rubyonrails.org/v6.1/action_cable_overview.html\#server-side-components-channels-subscriptions)

Consumers subscribe to channels, acting as _subscribers_. Their connection is
called a _subscription_. Produced messages are then routed to these channel
subscriptions based on an identifier sent by the channel consumer.

```
# app/channels/chat_channel.rb
class ChatChannel < ApplicationCable::Channel
  # Called when the consumer has successfully
  # become a subscriber to this channel.
  def subscribed
  end
end
```

Copy

##### [3.2.3 Exception Handling](https://guides.rubyonrails.org/v6.1/action_cable_overview.html\#server-side-components-channels-exception-handling)

As with `ApplicationCable::Connection`, you can also use [`rescue_from`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveSupport/Rescuable/ClassMethods.html#method-i-rescue_from) on a
specific channel to handle raised exceptions:

```
# app/channels/chat_channel.rb
class ChatChannel < ApplicationCable::Channel
  rescue_from 'MyError', with: :deliver_error_message

  private

  def deliver_error_message(e)
    broadcast_to(...)
  end
end
```

Copy

### [4 Client-Side Components](https://guides.rubyonrails.org/v6.1/action_cable_overview.html\#client-side-components)

#### [4.1 Connections](https://guides.rubyonrails.org/v6.1/action_cable_overview.html\#connections)

Consumers require an instance of the connection on their side. This can be
established using the following JavaScript, which is generated by default by Rails:

##### [4.1.1 Connect Consumer](https://guides.rubyonrails.org/v6.1/action_cable_overview.html\#connect-consumer)

```
// app/javascript/channels/consumer.js
// Action Cable provides the framework to deal with WebSockets in Rails.
// You can generate new channels where WebSocket features live using the `bin/rails generate channel` command.

import { createConsumer } from "@rails/actioncable"

export default createConsumer()
```

Copy

This will ready a consumer that'll connect against `/cable` on your server by default.
The connection won't be established until you've also specified at least one subscription
you're interested in having.

The consumer can optionally take an argument that specifies the URL to connect to. This
can be a string, or a function that returns a string that will be called when the
WebSocket is opened.

```
// Specify a different URL to connect to
createConsumer('https://ws.example.com/cable')

// Use a function to dynamically generate the URL
createConsumer(getWebSocketURL)

function getWebSocketURL {
  const token = localStorage.get('auth-token')
  return `https://ws.example.com/cable?token=${token}`
}
```

Copy

##### [4.1.2 Subscriber](https://guides.rubyonrails.org/v6.1/action_cable_overview.html\#subscriber)

A consumer becomes a subscriber by creating a subscription to a given channel:

```
// app/javascript/channels/chat_channel.js
import consumer from "./consumer"

consumer.subscriptions.create({ channel: "ChatChannel", room: "Best Room" })

// app/javascript/channels/appearance_channel.js
import consumer from "./consumer"

consumer.subscriptions.create({ channel: "AppearanceChannel" })
```

Copy

While this creates the subscription, the functionality needed to respond to
received data will be described later on.

A consumer can act as a subscriber to a given channel any number of times. For
example, a consumer could subscribe to multiple chat rooms at the same time:

```
// app/javascript/channels/chat_channel.js
import consumer from "./consumer"

consumer.subscriptions.create({ channel: "ChatChannel", room: "1st Room" })
consumer.subscriptions.create({ channel: "ChatChannel", room: "2nd Room" })
```

Copy

### [5 Client-Server Interactions](https://guides.rubyonrails.org/v6.1/action_cable_overview.html\#client-server-interactions)

#### [5.1 Streams](https://guides.rubyonrails.org/v6.1/action_cable_overview.html\#streams)

_Streams_ provide the mechanism by which channels route published content
(broadcasts) to their subscribers. For example, the following code uses
[`stream_from`](https://api.rubyonrails.org/v6.1.7.10/classes/ActionCable/Channel/Streams.html#method-i-stream_from) to subscribe to the broadcasting named `chat_Best Room` when
the value of the `:room` parameter is `"Best Room"`:

```
# app/channels/chat_channel.rb
class ChatChannel < ApplicationCable::Channel
  def subscribed
    stream_from "chat_#{params[:room]}"
  end
end
```

Copy

Then, elsewhere in your Rails application, you can broadcast to such a room by
calling [`broadcast`](https://api.rubyonrails.org/v6.1.7.10/classes/ActionCable/Server/Broadcasting.html#method-i-broadcast):

```
ActionCable.server.broadcast("chat_Best Room", { body: "This Room is Best Room." })
```

Copy

If you have a stream that is related to a model, then the broadcasting name
can be generated from the channel and model. For example, the following code
uses [`stream_for`](https://api.rubyonrails.org/v6.1.7.10/classes/ActionCable/Channel/Streams.html#method-i-stream_for) to subscribe to a broadcasting like
`comments:Z2lkOi8vVGVzdEFwcC9Qb3N0LzE`, where `Z2lkOi8vVGVzdEFwcC9Qb3N0LzE` is
the GlobalID of the Post model.

```
class CommentsChannel < ApplicationCable::Channel
  def subscribed
    post = Post.find(params[:id])
    stream_for post
  end
end
```

Copy

You can then broadcast to this channel by calling [`broadcast_to`](https://api.rubyonrails.org/v6.1.7.10/classes/ActionCable/Channel/Broadcasting/ClassMethods.html#method-i-broadcast_to):

```
CommentsChannel.broadcast_to(@post, @comment)
```

Copy

#### [5.2 Broadcastings](https://guides.rubyonrails.org/v6.1/action_cable_overview.html\#client-server-interactions-broadcastings)

A _broadcasting_ is a pub/sub link where anything transmitted by a publisher
is routed directly to the channel subscribers who are streaming that named
broadcasting. Each channel can be streaming zero or more broadcastings.

Broadcastings are purely an online queue and time-dependent. If a consumer is
not streaming (subscribed to a given channel), they'll not get the broadcast
should they connect later.

#### [5.3 Subscriptions](https://guides.rubyonrails.org/v6.1/action_cable_overview.html\#client-server-interactions-subscriptions)

When a consumer is subscribed to a channel, they act as a subscriber. This
connection is called a subscription. Incoming messages are then routed to
these channel subscriptions based on an identifier sent by the cable consumer.

```
// app/javascript/channels/chat_channel.js
// Assumes you've already requested the right to send web notifications
import consumer from "./consumer"

consumer.subscriptions.create({ channel: "ChatChannel", room: "Best Room" }, {
  received(data) {
    this.appendLine(data)
  },

  appendLine(data) {
    const html = this.createLine(data)
    const element = document.querySelector("[data-chat-room='Best Room']")
    element.insertAdjacentHTML("beforeend", html)
  },

  createLine(data) {
    return `
      <article class="chat-line">
        <span class="speaker">${data["sent_by"]}</span>
        <span class="body">${data["body"]}</span>
      </article>
    `
  }
})
```

Copy

#### [5.4 Passing Parameters to Channels](https://guides.rubyonrails.org/v6.1/action_cable_overview.html\#passing-parameters-to-channels)

You can pass parameters from the client side to the server side when creating a
subscription. For example:

```
# app/channels/chat_channel.rb
class ChatChannel < ApplicationCable::Channel
  def subscribed
    stream_from "chat_#{params[:room]}"
  end
end
```

Copy

An object passed as the first argument to `subscriptions.create` becomes the
params hash in the cable channel. The keyword `channel` is required:

```
// app/javascript/channels/chat_channel.js
import consumer from "./consumer"

consumer.subscriptions.create({ channel: "ChatChannel", room: "Best Room" }, {
  received(data) {
    this.appendLine(data)
  },

  appendLine(data) {
    const html = this.createLine(data)
    const element = document.querySelector("[data-chat-room='Best Room']")
    element.insertAdjacentHTML("beforeend", html)
  },

  createLine(data) {
    return `
      <article class="chat-line">
        <span class="speaker">${data["sent_by"]}</span>
        <span class="body">${data["body"]}</span>
      </article>
    `
  }
})
```

Copy

```
# Somewhere in your app this is called, perhaps
# from a NewCommentJob.
ActionCable.server.broadcast(
  "chat_#{room}",
  {
    sent_by: 'Paul',
    body: 'This is a cool chat app.'
  }
)
```

Copy

#### [5.5 Rebroadcasting a Message](https://guides.rubyonrails.org/v6.1/action_cable_overview.html\#rebroadcasting-a-message)

A common use case is to _rebroadcast_ a message sent by one client to any
other connected clients.

```
# app/channels/chat_channel.rb
class ChatChannel < ApplicationCable::Channel
  def subscribed
    stream_from "chat_#{params[:room]}"
  end

  def receive(data)
    ActionCable.server.broadcast("chat_#{params[:room]}", data)
  end
end
```

Copy

```
// app/javascript/channels/chat_channel.js
import consumer from "./consumer"

const chatChannel = consumer.subscriptions.create({ channel: "ChatChannel", room: "Best Room" }, {
  received(data) {
    // data => { sent_by: "Paul", body: "This is a cool chat app." }
  }
}

chatChannel.send({ sent_by: "Paul", body: "This is a cool chat app." })
```

Copy

The rebroadcast will be received by all connected clients, _including_ the
client that sent the message. Note that params are the same as they were when
you subscribed to the channel.

### [6 Full-Stack Examples](https://guides.rubyonrails.org/v6.1/action_cable_overview.html\#full-stack-examples)

The following setup steps are common to both examples:

1. [Setup your connection](https://guides.rubyonrails.org/v6.1/action_cable_overview.html#connection-setup).
2. [Setup your parent channel](https://guides.rubyonrails.org/v6.1/action_cable_overview.html#parent-channel-setup).
3. [Connect your consumer](https://guides.rubyonrails.org/v6.1/action_cable_overview.html#connect-consumer).

#### [6.1 Example 1: User Appearances](https://guides.rubyonrails.org/v6.1/action_cable_overview.html\#example-1-user-appearances)

Here's a simple example of a channel that tracks whether a user is online or not
and what page they're on. (This is useful for creating presence features like showing
a green dot next to a user name if they're online).

Create the server-side appearance channel:

```
# app/channels/appearance_channel.rb
class AppearanceChannel < ApplicationCable::Channel
  def subscribed
    current_user.appear
  end

  def unsubscribed
    current_user.disappear
  end

  def appear(data)
    current_user.appear(on: data['appearing_on'])
  end

  def away
    current_user.away
  end
end
```

Copy

When a subscription is initiated the `subscribed` callback gets fired and we
take that opportunity to say "the current user has indeed appeared". That
appear/disappear API could be backed by Redis, a database, or whatever else.

Create the client-side appearance channel subscription:

```
// app/javascript/channels/appearance_channel.js
import consumer from "./consumer"

consumer.subscriptions.create("AppearanceChannel", {
  // Called once when the subscription is created.
  initialized() {
    this.update = this.update.bind(this)
  },

  // Called when the subscription is ready for use on the server.
  connected() {
    this.install()
    this.update()
  },

  // Called when the WebSocket connection is closed.
  disconnected() {
    this.uninstall()
  },

  // Called when the subscription is rejected by the server.
  rejected() {
    this.uninstall()
  },

  update() {
    this.documentIsActive ? this.appear() : this.away()
  },

  appear() {
    // Calls `AppearanceChannel#appear(data)` on the server.
    this.perform("appear", { appearing_on: this.appearingOn })
  },

  away() {
    // Calls `AppearanceChannel#away` on the server.
    this.perform("away")
  },

  install() {
    window.addEventListener("focus", this.update)
    window.addEventListener("blur", this.update)
    document.addEventListener("turbolinks:load", this.update)
    document.addEventListener("visibilitychange", this.update)
  },

  uninstall() {
    window.removeEventListener("focus", this.update)
    window.removeEventListener("blur", this.update)
    document.removeEventListener("turbolinks:load", this.update)
    document.removeEventListener("visibilitychange", this.update)
  },

  get documentIsActive() {
    return document.visibilityState == "visible" && document.hasFocus()
  },

  get appearingOn() {
    const element = document.querySelector("[data-appearing-on]")
    return element ? element.getAttribute("data-appearing-on") : null
  }
})
```

Copy

###### [6.1.1 Client-Server Interaction](https://guides.rubyonrails.org/v6.1/action_cable_overview.html\#client-server-interaction)

1. **Client** connects to the **Server** via `App.cable =
ActionCable.createConsumer("ws://cable.example.com")`. (`cable.js`). The
**Server** identifies this connection by `current_user`.

2. **Client** subscribes to the appearance channel via
`consumer.subscriptions.create({ channel: "AppearanceChannel" })`. (`appearance_channel.js`)

3. **Server** recognizes a new subscription has been initiated for the
appearance channel and runs its `subscribed` callback, calling the `appear`
method on `current_user`. (`appearance_channel.rb`)

4. **Client** recognizes that a subscription has been established and calls
`connected` (`appearance_channel.js`) which in turn calls `install` and `appear`.
`appear` calls `AppearanceChannel#appear(data)` on the server, and supplies a
data hash of `{ appearing_on: this.appearingOn }`. This is
possible because the server-side channel instance automatically exposes all
public methods declared on the class (minus the callbacks), so that these can be
reached as remote procedure calls via a subscription's `perform` method.

5. **Server** receives the request for the `appear` action on the appearance
channel for the connection identified by `current_user`
(`appearance_channel.rb`). **Server** retrieves the data with the
`:appearing_on` key from the data hash and sets it as the value for the `:on`
key being passed to `current_user.appear`.


#### [6.2 Example 2: Receiving New Web Notifications](https://guides.rubyonrails.org/v6.1/action_cable_overview.html\#example-2-receiving-new-web-notifications)

The appearance example was all about exposing server functionality to
client-side invocation over the WebSocket connection. But the great thing
about WebSockets is that it's a two-way street. So now let's show an example
where the server invokes an action on the client.

This is a web notification channel that allows you to trigger client-side
web notifications when you broadcast to the right streams:

Create the server-side web notifications channel:

```
# app/channels/web_notifications_channel.rb
class WebNotificationsChannel < ApplicationCable::Channel
  def subscribed
    stream_for current_user
  end
end
```

Copy

Create the client-side web notifications channel subscription:

```
// app/javascript/channels/web_notifications_channel.js
// Client-side which assumes you've already requested
// the right to send web notifications.
import consumer from "./consumer"

consumer.subscriptions.create("WebNotificationsChannel", {
  received(data) {
    new Notification(data["title"], body: data["body"])
  }
})
```

Copy

Broadcast content to a web notification channel instance from elsewhere in your
application:

```
# Somewhere in your app this is called, perhaps from a NewCommentJob
WebNotificationsChannel.broadcast_to(
  current_user,
  title: 'New things!',
  body: 'All the news fit to print'
)
```

Copy

The `WebNotificationsChannel.broadcast_to` call places a message in the current
subscription adapter's pubsub queue under a separate broadcasting name for each
user. For a user with an ID of 1, the broadcasting name would be
`web_notifications:1`.

The channel has been instructed to stream everything that arrives at
`web_notifications:1` directly to the client by invoking the `received`
callback. The data passed as argument is the hash sent as the second parameter
to the server-side broadcast call, JSON encoded for the trip across the wire
and unpacked for the data argument arriving as `received`.

#### [6.3 More Complete Examples](https://guides.rubyonrails.org/v6.1/action_cable_overview.html\#more-complete-examples)

See the [rails/actioncable-examples](https://github.com/rails/actioncable-examples)
repository for a full example of how to set up Action Cable in a Rails app and adding channels.

### [7 Configuration](https://guides.rubyonrails.org/v6.1/action_cable_overview.html\#configuration)

Action Cable has two required configurations: a subscription adapter and allowed request origins.

#### [7.1 Subscription Adapter](https://guides.rubyonrails.org/v6.1/action_cable_overview.html\#subscription-adapter)

By default, Action Cable looks for a configuration file in `config/cable.yml`.
The file must specify an adapter for each Rails environment. See the
[Dependencies](https://guides.rubyonrails.org/v6.1/action_cable_overview.html#dependencies) section for additional information on adapters.

```
development:
  adapter: async

test:
  adapter: async

production:
  adapter: redis
  url: redis://10.10.3.153:6381
  channel_prefix: appname_production
```

Copy

##### [7.1.1 Adapter Configuration](https://guides.rubyonrails.org/v6.1/action_cable_overview.html\#adapter-configuration)

Below is a list of the subscription adapters available for end users.

###### [7.1.1.1 Async Adapter](https://guides.rubyonrails.org/v6.1/action_cable_overview.html\#async-adapter)

The async adapter is intended for development/testing and should not be used in production.

###### [7.1.1.2 Redis Adapter](https://guides.rubyonrails.org/v6.1/action_cable_overview.html\#redis-adapter)

The Redis adapter requires users to provide a URL pointing to the Redis server.
Additionally, a `channel_prefix` may be provided to avoid channel name collisions
when using the same Redis server for multiple applications. See the [Redis PubSub documentation](https://redis.io/topics/pubsub#database-amp-scoping) for more details.

###### [7.1.1.3 PostgreSQL Adapter](https://guides.rubyonrails.org/v6.1/action_cable_overview.html\#postgresql-adapter)

The PostgreSQL adapter uses Active Record's connection pool, and thus the
application's `config/database.yml` database configuration, for its connection.
This may change in the future. [#27214](https://github.com/rails/rails/issues/27214)

#### [7.2 Allowed Request Origins](https://guides.rubyonrails.org/v6.1/action_cable_overview.html\#allowed-request-origins)

Action Cable will only accept requests from specified origins, which are
passed to the server config as an array. The origins can be instances of
strings or regular expressions, against which a check for the match will be performed.

```
config.action_cable.allowed_request_origins = ['https://rubyonrails.com', %r{http://ruby.*}]
```

Copy

To disable and allow requests from any origin:

```
config.action_cable.disable_request_forgery_protection = true
```

Copy

By default, Action Cable allows all requests from localhost:3000 when running
in the development environment.

#### [7.3 Consumer Configuration](https://guides.rubyonrails.org/v6.1/action_cable_overview.html\#consumer-configuration)

To configure the URL, add a call to [`action_cable_meta_tag`](https://api.rubyonrails.org/v6.1.7.10/classes/ActionCable/Helpers/ActionCableHelper.html#method-i-action_cable_meta_tag) in your HTML layout
HEAD. This uses a URL or path typically set via `config.action_cable.url` in the
environment configuration files.

#### [7.4 Worker Pool Configuration](https://guides.rubyonrails.org/v6.1/action_cable_overview.html\#worker-pool-configuration)

The worker pool is used to run connection callbacks and channel actions in
isolation from the server's main thread. Action Cable allows the application
to configure the number of simultaneously processed threads in the worker pool.

```
config.action_cable.worker_pool_size = 4
```

Copy

Also, note that your server must provide at least the same number of database
connections as you have workers. The default worker pool size is set to 4, so
that means you have to make at least 4 database connections available.
You can change that in `config/database.yml` through the `pool` attribute.

#### [7.5 Client side logging](https://guides.rubyonrails.org/v6.1/action_cable_overview.html\#client-side-logging)

Client side logging is disabled by default. You can enable this by setting the `ActionCable.logger.enabled` to true.

```
import * as ActionCable from '@rails/actioncable'

ActionCable.logger.enabled = true
```

Copy

#### [7.6 Other Configurations](https://guides.rubyonrails.org/v6.1/action_cable_overview.html\#other-configurations)

The other common option to configure is the log tags applied to the
per-connection logger. Here's an example that uses
the user account id if available, else "no-account" while tagging:

```
config.action_cable.log_tags = [\
  -> request { request.env['user_account_id'] || "no-account" },\
  :action_cable,\
  -> request { request.uuid }\
]
```

Copy

For a full list of all configuration options, see the
`ActionCable::Server::Configuration` class.

### [8 Running Standalone Cable Servers](https://guides.rubyonrails.org/v6.1/action_cable_overview.html\#running-standalone-cable-servers)

#### [8.1 In App](https://guides.rubyonrails.org/v6.1/action_cable_overview.html\#in-app)

Action Cable can run alongside your Rails application. For example, to
listen for WebSocket requests on `/websocket`, specify that path to
`config.action_cable.mount_path`:

```
# config/application.rb
class Application < Rails::Application
  config.action_cable.mount_path = '/websocket'
end
```

Copy

You can use `ActionCable.createConsumer()` to connect to the cable
server if `action_cable_meta_tag` is invoked in the layout. Otherwise, A path is
specified as first argument to `createConsumer` (e.g. `ActionCable.createConsumer("/websocket")`).

For every instance of your server you create and for every worker your server
spawns, you will also have a new instance of Action Cable, but the use of Redis
keeps messages synced across connections.

#### [8.2 Standalone](https://guides.rubyonrails.org/v6.1/action_cable_overview.html\#standalone)

The cable servers can be separated from your normal application server. It's
still a Rack application, but it is its own Rack application. The recommended
basic setup is as follows:

```
# cable/config.ru
require_relative "../config/environment"
Rails.application.eager_load!

run ActionCable.server
```

Copy

Then you start the server using a binstub in `bin/cable` ala:

```
#!/bin/bash
bundle exec puma -p 28080 cable/config.ru
```

Copy

The above will start a cable server on port 28080.

#### [8.3 Notes](https://guides.rubyonrails.org/v6.1/action_cable_overview.html\#notes)

The WebSocket server doesn't have access to the session, but it has
access to the cookies. This can be used when you need to handle
authentication. You can see one way of doing that with Devise in this [article](https://greg.molnar.io/blog/actioncable-devise-authentication/).

### [9 Dependencies](https://guides.rubyonrails.org/v6.1/action_cable_overview.html\#dependencies)

Action Cable provides a subscription adapter interface to process its
pubsub internals. By default, asynchronous, inline, PostgreSQL, and Redis
adapters are included. The default adapter
in new Rails applications is the asynchronous (`async`) adapter.

The Ruby side of things is built on top of [websocket-driver](https://github.com/faye/websocket-driver-ruby),
[nio4r](https://github.com/celluloid/nio4r), and [concurrent-ruby](https://github.com/ruby-concurrency/concurrent-ruby).

### [10 Deployment](https://guides.rubyonrails.org/v6.1/action_cable_overview.html\#deployment)

Action Cable is powered by a combination of WebSockets and threads. Both the
framework plumbing and user-specified channel work are handled internally by
utilizing Ruby's native thread support. This means you can use all your regular
Rails models with no problem, as long as you haven't committed any thread-safety sins.

The Action Cable server implements the Rack socket hijacking API,
thereby allowing the use of a multithreaded pattern for managing connections
internally, irrespective of whether the application server is multi-threaded or not.

Accordingly, Action Cable works with popular servers like Unicorn, Puma, and
Passenger.

### [11 Testing](https://guides.rubyonrails.org/v6.1/action_cable_overview.html\#testing)

You can find detailed instructions on how to test your Action Cable functionality in the
[testing guide](https://guides.rubyonrails.org/v6.1/testing.html#testing-action-cable).

### Feedback

You're encouraged to help improve the quality of this guide.


Please contribute if you see any typos or factual errors.
To get started, you can read our [documentation contributions](https://edgeguides.rubyonrails.org/contributing_to_ruby_on_rails.html#contributing-to-the-rails-documentation) section.


You may also find incomplete content or stuff that is not up to date.
Please do add any missing documentation for main. Make sure to check
[Edge Guides](https://edgeguides.rubyonrails.org/) first to verify
if the issues are already fixed or not on the main branch.
Check the [Ruby on Rails Guides Guidelines](https://guides.rubyonrails.org/v6.1/ruby_on_rails_guides_guidelines.html)
for style and conventions.


If for whatever reason you spot something to fix but cannot patch it yourself, please
[open an issue](https://github.com/rails/rails/issues).


And last but not least, any kind of discussion regarding Ruby on Rails
documentation is very welcome on the [rubyonrails-docs mailing list](https://discuss.rubyonrails.org/c/rubyonrails-docs).


* * *