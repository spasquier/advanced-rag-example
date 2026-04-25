v6.1.7.10

**More at [rubyonrails.org:](https://rubyonrails.org/)**
More Ruby on Rails


- [Blog](https://rubyonrails.org/blog)
- [Guides](https://guides.rubyonrails.org/)
- [API](https://api.rubyonrails.org/)
- [Forum](https://discuss.rubyonrails.org/)
- [Contribute on GitHub](https://github.com/rails/rails)

* * *

## Active Support Instrumentation

Active Support is a part of core Rails that provides Ruby language extensions, utilities, and other things. One of the things it includes is an instrumentation API that can be used inside an application to measure certain actions that occur within Ruby code, such as that inside a Rails application or the framework itself. It is not limited to Rails, however. It can be used independently in other Ruby scripts if it is so desired.

In this guide, you will learn how to use the instrumentation API inside of Active Support to measure events inside of Rails and other Ruby code.

After reading this guide, you will know:

- What instrumentation can provide.
- How to add a subscriber to a hook.
- The hooks inside the Rails framework for instrumentation.
- How to build a custom instrumentation implementation.

### ![](https://guides.rubyonrails.org/v6.1/images/chapters_icon.gif)Chapters

01. [Introduction to instrumentation](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#introduction-to-instrumentation)
02. [Subscribing to an event](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#subscribing-to-an-event)
03. [Rails framework hooks](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#rails-framework-hooks)
04. [Action Controller](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#action-controller)    - [write\_fragment.action\_controller](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#write-fragment-action-controller)
    - [read\_fragment.action\_controller](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#read-fragment-action-controller)
    - [expire\_fragment.action\_controller](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#expire-fragment-action-controller)
    - [exist\_fragment?.action\_controller](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#exist-fragment-questionmark-action-controller)
    - [write\_page.action\_controller](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#write-page-action-controller)
    - [expire\_page.action\_controller](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#expire-page-action-controller)
    - [start\_processing.action\_controller](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#start-processing-action-controller)
    - [process\_action.action\_controller](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#process-action-action-controller)
    - [send\_file.action\_controller](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#send-file-action-controller)
    - [send\_data.action\_controller](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#send-data-action-controller)
    - [redirect\_to.action\_controller](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#redirect-to-action-controller)
    - [halted\_callback.action\_controller](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#halted-callback-action-controller)
    - [unpermitted\_parameters.action\_controller](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#unpermitted-parameters-action-controller)
05. [Action Dispatch](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#action-dispatch)    - [process\_middleware.action\_dispatch](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#process-middleware-action-dispatch)
06. [Action View](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#action-view)    - [render\_template.action\_view](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#render-template-action-view)
    - [render\_partial.action\_view](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#render-partial-action-view)
    - [render\_collection.action\_view](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#render-collection-action-view)
07. [Active Record](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#active-record)    - [sql.active\_record](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#sql-active-record)
    - [instantiation.active\_record](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#instantiation-active-record)
08. [Action Mailer](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#action-mailer)    - [deliver.action\_mailer](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#deliver-action-mailer)
    - [process.action\_mailer](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#process-action-mailer)
09. [Active Support](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#active-support)    - [cache\_read.active\_support](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#cache-read-active-support)
    - [cache\_generate.active\_support](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#cache-generate-active-support)
    - [cache\_fetch\_hit.active\_support](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#cache-fetch-hit-active-support)
    - [cache\_write.active\_support](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#cache-write-active-support)
    - [cache\_delete.active\_support](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#cache-delete-active-support)
    - [cache\_exist?.active\_support](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#cache-exist-questionmark-active-support)
10. [Active Job](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#active-job)    - [enqueue\_at.active\_job](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#enqueue-at-active-job)
    - [enqueue.active\_job](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#enqueue-active-job)
    - [enqueue\_retry.active\_job](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#enqueue-retry-active-job)
    - [perform\_start.active\_job](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#perform-start-active-job)
    - [perform.active\_job](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#perform-active-job)
    - [retry\_stopped.active\_job](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#retry-stopped-active-job)
    - [discard.active\_job](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#discard-active-job)
11. [Action Cable](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#action-cable)    - [perform\_action.action\_cable](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#perform-action-action-cable)
    - [transmit.action\_cable](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#transmit-action-cable)
    - [transmit\_subscription\_confirmation.action\_cable](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#transmit-subscription-confirmation-action-cable)
    - [transmit\_subscription\_rejection.action\_cable](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#transmit-subscription-rejection-action-cable)
    - [broadcast.action\_cable](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#broadcast-action-cable)
12. [Active Storage](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#active-storage)    - [service\_upload.active\_storage](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#service-upload-active-storage)
    - [service\_streaming\_download.active\_storage](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#service-streaming-download-active-storage)
    - [service\_download\_chunk.active\_storage](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#service-download-chunk-active-storage)
    - [service\_download.active\_storage](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#service-download-active-storage)
    - [service\_delete.active\_storage](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#service-delete-active-storage)
    - [service\_delete\_prefixed.active\_storage](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#service-delete-prefixed-active-storage)
    - [service\_exist.active\_storage](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#service-exist-active-storage)
    - [service\_url.active\_storage](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#service-url-active-storage)
    - [service\_update\_metadata.active\_storage](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#service-update-metadata-active-storage)
    - [preview.active\_storage](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#preview-active-storage)
    - [transform.active\_storage](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#transform-active-storage)
13. [Railties](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#railties)    - [load\_config\_initializer.railties](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#load-config-initializer-railties)
14. [Rails](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#rails)    - [deprecation.rails](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#deprecation-rails)
15. [Exceptions](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#exceptions)
16. [Creating custom events](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#creating-custom-events)

### [1 Introduction to instrumentation](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#introduction-to-instrumentation)

The instrumentation API provided by Active Support allows developers to provide hooks which other developers may hook into. There are several of these within the [Rails framework](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#rails-framework-hooks). With this API, developers can choose to be notified when certain events occur inside their application or another piece of Ruby code.

For example, there is a hook provided within Active Record that is called every time Active Record uses an SQL query on a database. This hook could be **subscribed** to, and used to track the number of queries during a certain action. There's another hook around the processing of an action of a controller. This could be used, for instance, to track how long a specific action has taken.

You are even able to [create your own events](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html#creating-custom-events) inside your application which you can later subscribe to.

### [2 Subscribing to an event](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#subscribing-to-an-event)

Subscribing to an event is easy. Use `ActiveSupport::Notifications.subscribe` with a block to
listen to any notification.

The block receives the following arguments:

- The name of the event
- Time when it started
- Time when it finished
- A unique ID for the instrumenter that fired the event
- The payload (described in future sections)

```
ActiveSupport::Notifications.subscribe "process_action.action_controller" do |name, started, finished, unique_id, data|
  # your own custom stuff
  Rails.logger.info "#{name} Received! (started: #{started}, finished: #{finished})" # process_action.action_controller Received (started: 2019-05-05 13:43:57 -0800, finished: 2019-05-05 13:43:58 -0800)
end
```

Copy

If you are concerned about the accuracy of `started` and `finished` to compute a precise elapsed time then use `ActiveSupport::Notifications.monotonic_subscribe`. The given block would receive the same arguments as above but the `started` and `finished` will have values with an accurate monotonic time instead of wall-clock time.

```
ActiveSupport::Notifications.monotonic_subscribe "process_action.action_controller" do |name, started, finished, unique_id, data|
  # your own custom stuff
  Rails.logger.info "#{name} Received! (started: #{started}, finished: #{finished})" # process_action.action_controller Received (started: 1560978.425334, finished: 1560979.429234)
end
```

Copy

Defining all those block arguments each time can be tedious. You can easily create an `ActiveSupport::Notifications::Event`
from block arguments like this:

```
ActiveSupport::Notifications.subscribe "process_action.action_controller" do |*args|
  event = ActiveSupport::Notifications::Event.new *args

  event.name      # => "process_action.action_controller"
  event.duration  # => 10 (in milliseconds)
  event.payload   # => {:extra=>information}

  Rails.logger.info "#{event} Received!"
end
```

Copy

You may also pass a block that accepts only one argument, and it will receive an event object:

```
ActiveSupport::Notifications.subscribe "process_action.action_controller" do |event|
  event.name      # => "process_action.action_controller"
  event.duration  # => 10 (in milliseconds)
  event.payload   # => {:extra=>information}

  Rails.logger.info "#{event} Received!"
end
```

Copy

Most times you only care about the data itself. Here is a shortcut to just get the data.

```
ActiveSupport::Notifications.subscribe "process_action.action_controller" do |*args|
  data = args.extract_options!
  data # { extra: :information }
end
```

Copy

You may also subscribe to events matching a regular expression. This enables you to subscribe to
multiple events at once. Here's how to subscribe to everything from `ActionController`.

```
ActiveSupport::Notifications.subscribe /action_controller/ do |*args|
  # inspect all ActionController events
end
```

Copy

### [3 Rails framework hooks](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#rails-framework-hooks)

Within the Ruby on Rails framework, there are a number of hooks provided for common events. These are detailed below.

### [4 Action Controller](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#action-controller)

#### [4.1 write\_fragment.action\_controller](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#write-fragment-action-controller)

| Key | Value |
| --- | --- |
| `:key` | The complete key |

```
{
  key: 'posts/1-dashboard-view'
}
```

Copy

#### [4.2 read\_fragment.action\_controller](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#read-fragment-action-controller)

| Key | Value |
| --- | --- |
| `:key` | The complete key |

```
{
  key: 'posts/1-dashboard-view'
}
```

Copy

#### [4.3 expire\_fragment.action\_controller](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#expire-fragment-action-controller)

| Key | Value |
| --- | --- |
| `:key` | The complete key |

```
{
  key: 'posts/1-dashboard-view'
}
```

Copy

#### [4.4 exist\_fragment?.action\_controller](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#exist-fragment-questionmark-action-controller)

| Key | Value |
| --- | --- |
| `:key` | The complete key |

```
{
  key: 'posts/1-dashboard-view'
}
```

Copy

#### [4.5 write\_page.action\_controller](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#write-page-action-controller)

| Key | Value |
| --- | --- |
| `:path` | The complete path |

```
{
  path: '/users/1'
}
```

Copy

#### [4.6 expire\_page.action\_controller](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#expire-page-action-controller)

| Key | Value |
| --- | --- |
| `:path` | The complete path |

```
{
  path: '/users/1'
}
```

Copy

#### [4.7 start\_processing.action\_controller](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#start-processing-action-controller)

| Key | Value |
| --- | --- |
| `:controller` | The controller name |
| `:action` | The action |
| `:params` | Hash of request parameters without any filtered parameter |
| `:headers` | Request headers |
| `:format` | html/js/json/xml etc |
| `:method` | HTTP request verb |
| `:path` | Request path |

```
{
  controller: "PostsController",
  action: "new",
  params: { "action" => "new", "controller" => "posts" },
  headers: #<ActionDispatch::Http::Headers:0x0055a67a519b88>,
  format: :html,
  method: "GET",
  path: "/posts/new"
}
```

Copy

#### [4.8 process\_action.action\_controller](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#process-action-action-controller)

| Key | Value |
| --- | --- |
| `:controller` | The controller name |
| `:action` | The action |
| `:params` | Hash of request parameters without any filtered parameter |
| `:headers` | Request headers |
| `:format` | html/js/json/xml etc |
| `:method` | HTTP request verb |
| `:path` | Request path |
| `:request` | The `ActionDispatch::Request` |
| `:status` | HTTP status code |
| `:location` | Location response header |
| `:view_runtime` | Amount spent in view in ms |
| `:db_runtime` | Amount spent executing database queries in ms |

```
{
  controller: "PostsController",
  action: "index",
  params: {"action" => "index", "controller" => "posts"},
  headers: #<ActionDispatch::Http::Headers:0x0055a67a519b88>,
  format: :html,
  method: "GET",
  path: "/posts",
  request: #<ActionDispatch::Request:0x00007ff1cb9bd7b8>,
  status: 200,
  view_runtime: 46.848,
  db_runtime: 0.157
}
```

Copy

#### [4.9 send\_file.action\_controller](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#send-file-action-controller)

| Key | Value |
| --- | --- |
| `:path` | Complete path to the file |

Additional keys may be added by the caller.

#### [4.10 send\_data.action\_controller](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#send-data-action-controller)

`ActionController` does not add any specific information to the payload. All options are passed through to the payload.

#### [4.11 redirect\_to.action\_controller](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#redirect-to-action-controller)

| Key | Value |
| --- | --- |
| `:status` | HTTP response code |
| `:location` | URL to redirect to |
| `:request` | The `ActionDispatch::Request` |

```
{
  status: 302,
  location: "http://localhost:3000/posts/new",
  request: #<ActionDispatch::Request:0x00007ff1cb9bd7b8>
}
```

Copy

#### [4.12 halted\_callback.action\_controller](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#halted-callback-action-controller)

| Key | Value |
| --- | --- |
| `:filter` | Filter that halted the action |

```
{
  filter: ":halting_filter"
}
```

Copy

#### [4.13 unpermitted\_parameters.action\_controller](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#unpermitted-parameters-action-controller)

| Key | Value |
| --- | --- |
| `:keys` | Unpermitted keys |

### [5 Action Dispatch](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#action-dispatch)

#### [5.1 process\_middleware.action\_dispatch](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#process-middleware-action-dispatch)

| Key | Value |
| --- | --- |
| `:middleware` | Name of the middleware |

### [6 Action View](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#action-view)

#### [6.1 render\_template.action\_view](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#render-template-action-view)

| Key | Value |
| --- | --- |
| `:identifier` | Full path to template |
| `:layout` | Applicable layout |

```
{
  identifier: "/Users/adam/projects/notifications/app/views/posts/index.html.erb",
  layout: "layouts/application"
}
```

Copy

#### [6.2 render\_partial.action\_view](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#render-partial-action-view)

| Key | Value |
| --- | --- |
| `:identifier` | Full path to template |

```
{
  identifier: "/Users/adam/projects/notifications/app/views/posts/_form.html.erb"
}
```

Copy

#### [6.3 render\_collection.action\_view](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#render-collection-action-view)

| Key | Value |
| --- | --- |
| `:identifier` | Full path to template |
| `:count` | Size of collection |
| `:cache_hits` | Number of partials fetched from cache |

`:cache_hits` is only included if the collection is rendered with `cached: true`.

```
{
  identifier: "/Users/adam/projects/notifications/app/views/posts/_post.html.erb",
  count: 3,
  cache_hits: 0
}
```

Copy

### [7 Active Record](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#active-record)

#### [7.1 sql.active\_record](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#sql-active-record)

| Key | Value |
| --- | --- |
| `:sql` | SQL statement |
| `:name` | Name of the operation |
| `:connection` | Connection object |
| `:binds` | Bind parameters |
| `:type_casted_binds` | Typecasted bind parameters |
| `:statement_name` | SQL Statement name |
| `:cached` | `true` is added when cached queries used |

The adapters will add their own data as well.

```
{
  sql: "SELECT \"posts\".* FROM \"posts\" ",
  name: "Post Load",
  connection: #<ActiveRecord::ConnectionAdapters::SQLite3Adapter:0x00007f9f7a838850>,
  binds: [#<ActiveModel::Attribute::WithCastValue:0x00007fe19d15dc00>],
  type_casted_binds: [11],
  statement_name: nil
}
```

Copy

#### [7.2 instantiation.active\_record](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#instantiation-active-record)

| Key | Value |
| --- | --- |
| `:record_count` | Number of records that instantiated |
| `:class_name` | Record's class |

```
{
  record_count: 1,
  class_name: "User"
}
```

Copy

### [8 Action Mailer](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#action-mailer)

#### [8.1 deliver.action\_mailer](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#deliver-action-mailer)

| Key | Value |
| --- | --- |
| `:mailer` | Name of the mailer class |
| `:message_id` | ID of the message, generated by the Mail gem |
| `:subject` | Subject of the mail |
| `:to` | To address(es) of the mail |
| `:from` | From address of the mail |
| `:bcc` | BCC addresses of the mail |
| `:cc` | CC addresses of the mail |
| `:date` | Date of the mail |
| `:mail` | The encoded form of the mail |
| `:perform_deliveries` | Whether delivery of this message is performed or not |

```
{
  mailer: "Notification",
  message_id: "4f5b5491f1774_181b23fc3d4434d38138e5@mba.local.mail",
  subject: "Rails Guides",
  to: ["users@rails.com", "dhh@rails.com"],
  from: ["me@rails.com"],
  date: Sat, 10 Mar 2012 14:18:09 +0100,
  mail: "...", # omitted for brevity
  perform_deliveries: true
}
```

Copy

#### [8.2 process.action\_mailer](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#process-action-mailer)

| Key | Value |
| --- | --- |
| `:mailer` | Name of the mailer class |
| `:action` | The action |
| `:args` | The arguments |

```
{
  mailer: "Notification",
  action: "welcome_email",
  args: []
}
```

Copy

### [9 Active Support](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#active-support)

#### [9.1 cache\_read.active\_support](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#cache-read-active-support)

| Key | Value |
| --- | --- |
| `:key` | Key used in the store |
| `:store` | Name of the store class |
| `:hit` | If this read is a hit |
| `:super_operation` | :fetch is added when a read is used with `#fetch` |

#### [9.2 cache\_generate.active\_support](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#cache-generate-active-support)

This event is only used when `#fetch` is called with a block.

| Key | Value |
| --- | --- |
| `:key` | Key used in the store |
| `:store` | Name of the store class |

Options passed to fetch will be merged with the payload when writing to the store

```
{
  key: "name-of-complicated-computation",
  store: "ActiveSupport::Cache::MemCacheStore"
}
```

Copy

#### [9.3 cache\_fetch\_hit.active\_support](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#cache-fetch-hit-active-support)

This event is only used when `#fetch` is called with a block.

| Key | Value |
| --- | --- |
| `:key` | Key used in the store |
| `:store` | Name of the store class |

Options passed to fetch will be merged with the payload.

```
{
  key: "name-of-complicated-computation",
  store: "ActiveSupport::Cache::MemCacheStore"
}
```

Copy

#### [9.4 cache\_write.active\_support](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#cache-write-active-support)

| Key | Value |
| --- | --- |
| `:key` | Key used in the store |
| `:store` | Name of the store class |

Cache stores may add their own keys

```
{
  key: "name-of-complicated-computation",
  store: "ActiveSupport::Cache::MemCacheStore"
}
```

Copy

#### [9.5 cache\_delete.active\_support](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#cache-delete-active-support)

| Key | Value |
| --- | --- |
| `:key` | Key used in the store |
| `:store` | Name of the store class |

```
{
  key: "name-of-complicated-computation",
  store: "ActiveSupport::Cache::MemCacheStore"
}
```

Copy

#### [9.6 cache\_exist?.active\_support](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#cache-exist-questionmark-active-support)

| Key | Value |
| --- | --- |
| `:key` | Key used in the store |
| `:store` | Name of the store class |

```
{
  key: "name-of-complicated-computation",
  store: "ActiveSupport::Cache::MemCacheStore"
}
```

Copy

### [10 Active Job](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#active-job)

#### [10.1 enqueue\_at.active\_job](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#enqueue-at-active-job)

| Key | Value |
| --- | --- |
| `:adapter` | QueueAdapter object processing the job |
| `:job` | Job object |

#### [10.2 enqueue.active\_job](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#enqueue-active-job)

| Key | Value |
| --- | --- |
| `:adapter` | QueueAdapter object processing the job |
| `:job` | Job object |

#### [10.3 enqueue\_retry.active\_job](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#enqueue-retry-active-job)

| Key | Value |
| --- | --- |
| `:job` | Job object |
| `:adapter` | QueueAdapter object processing the job |
| `:error` | The error that caused the retry |
| `:wait` | The delay of the retry |

#### [10.4 perform\_start.active\_job](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#perform-start-active-job)

| Key | Value |
| --- | --- |
| `:adapter` | QueueAdapter object processing the job |
| `:job` | Job object |

#### [10.5 perform.active\_job](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#perform-active-job)

| Key | Value |
| --- | --- |
| `:adapter` | QueueAdapter object processing the job |
| `:job` | Job object |

#### [10.6 retry\_stopped.active\_job](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#retry-stopped-active-job)

| Key | Value |
| --- | --- |
| `:adapter` | QueueAdapter object processing the job |
| `:job` | Job object |
| `:error` | The error that caused the retry |

#### [10.7 discard.active\_job](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#discard-active-job)

| Key | Value |
| --- | --- |
| `:adapter` | QueueAdapter object processing the job |
| `:job` | Job object |
| `:error` | The error that caused the discard |

### [11 Action Cable](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#action-cable)

#### [11.1 perform\_action.action\_cable](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#perform-action-action-cable)

| Key | Value |
| --- | --- |
| `:channel_class` | Name of the channel class |
| `:action` | The action |
| `:data` | A hash of data |

#### [11.2 transmit.action\_cable](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#transmit-action-cable)

| Key | Value |
| --- | --- |
| `:channel_class` | Name of the channel class |
| `:data` | A hash of data |
| `:via` | Via |

#### [11.3 transmit\_subscription\_confirmation.action\_cable](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#transmit-subscription-confirmation-action-cable)

| Key | Value |
| --- | --- |
| `:channel_class` | Name of the channel class |

#### [11.4 transmit\_subscription\_rejection.action\_cable](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#transmit-subscription-rejection-action-cable)

| Key | Value |
| --- | --- |
| `:channel_class` | Name of the channel class |

#### [11.5 broadcast.action\_cable](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#broadcast-action-cable)

| Key | Value |
| --- | --- |
| `:broadcasting` | A named broadcasting |
| `:message` | A hash of message |
| `:coder` | The coder |

### [12 Active Storage](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#active-storage)

#### [12.1 service\_upload.active\_storage](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#service-upload-active-storage)

| Key | Value |
| --- | --- |
| `:key` | Secure token |
| `:service` | Name of the service |
| `:checksum` | Checksum to ensure integrity |

#### [12.2 service\_streaming\_download.active\_storage](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#service-streaming-download-active-storage)

| Key | Value |
| --- | --- |
| `:key` | Secure token |
| `:service` | Name of the service |

#### [12.3 service\_download\_chunk.active\_storage](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#service-download-chunk-active-storage)

| Key | Value |
| --- | --- |
| `:key` | Secure token |
| `:service` | Name of the service |
| `:range` | Byte range attempted to be read |

#### [12.4 service\_download.active\_storage](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#service-download-active-storage)

| Key | Value |
| --- | --- |
| `:key` | Secure token |
| `:service` | Name of the service |

#### [12.5 service\_delete.active\_storage](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#service-delete-active-storage)

| Key | Value |
| --- | --- |
| `:key` | Secure token |
| `:service` | Name of the service |

#### [12.6 service\_delete\_prefixed.active\_storage](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#service-delete-prefixed-active-storage)

| Key | Value |
| --- | --- |
| `:prefix` | Key prefix |
| `:service` | Name of the service |

#### [12.7 service\_exist.active\_storage](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#service-exist-active-storage)

| Key | Value |
| --- | --- |
| `:key` | Secure token |
| `:service` | Name of the service |
| `:exist` | File or blob exists or not |

#### [12.8 service\_url.active\_storage](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#service-url-active-storage)

| Key | Value |
| --- | --- |
| `:key` | Secure token |
| `:service` | Name of the service |
| `:url` | Generated URL |

#### [12.9 service\_update\_metadata.active\_storage](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#service-update-metadata-active-storage)

| Key | Value |
| --- | --- |
| `:key` | Secure token |
| `:service` | Name of the service |
| `:content_type` | HTTP Content-Type field |
| `:disposition` | HTTP Content-Disposition field |

The only ActiveStorage service that provides this hook so far is GCS.

#### [12.10 preview.active\_storage](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#preview-active-storage)

| Key | Value |
| --- | --- |
| `:key` | Secure token |

#### [12.11 transform.active\_storage](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#transform-active-storage)

### [13 Railties](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#railties)

#### [13.1 load\_config\_initializer.railties](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#load-config-initializer-railties)

| Key | Value |
| --- | --- |
| `:initializer` | Path to loaded initializer from `config/initializers` |

### [14 Rails](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#rails)

#### [14.1 deprecation.rails](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#deprecation-rails)

| Key | Value |
| --- | --- |
| `:message` | The deprecation warning |
| `:callstack` | Where the deprecation came from |

### [15 Exceptions](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#exceptions)

If an exception happens during any instrumentation the payload will include
information about it.

| Key | Value |
| --- | --- |
| `:exception` | An array of two elements. Exception class name and the message |
| `:exception_object` | The exception object |

### [16 Creating custom events](https://guides.rubyonrails.org/v6.1/active_support_instrumentation.html\#creating-custom-events)

Adding your own events is easy as well. `ActiveSupport::Notifications` will take care of
all the heavy lifting for you. Simply call `instrument` with a `name`, `payload` and a block.
The notification will be sent after the block returns. `ActiveSupport` will generate the start and end times
and add the instrumenter's unique ID. All data passed into the `instrument` call will make
it into the payload.

Here's an example:

```
ActiveSupport::Notifications.instrument "my.custom.event", this: :data do
  # do your custom stuff here
end
```

Copy

Now you can listen to this event with:

```
ActiveSupport::Notifications.subscribe "my.custom.event" do |name, started, finished, unique_id, data|
  puts data.inspect # {:this=>:data}
end
```

Copy

You also have the option to call instrument without passing a block. This lets you leverage the
instrumentation infrastructure for other messaging uses.

```
ActiveSupport::Notifications.instrument "my.custom.event", this: :data

ActiveSupport::Notifications.subscribe "my.custom.event" do |name, started, finished, unique_id, data|
  puts data.inspect # {:this=>:data}
end
```

Copy

You should follow Rails conventions when defining your own events. The format is: `event.library`.
If your application is sending Tweets, you should create an event named `tweet.twitter`.

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