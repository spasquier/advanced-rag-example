v6.1.7.10

**More at [rubyonrails.org:](https://rubyonrails.org/)**
More Ruby on Rails


- [Blog](https://rubyonrails.org/blog)
- [Guides](https://guides.rubyonrails.org/)
- [API](https://api.rubyonrails.org/)
- [Forum](https://discuss.rubyonrails.org/)
- [Contribute on GitHub](https://github.com/rails/rails)

* * *

## Action Mailer Basics

This guide provides you with all you need to get started in sending
emails from and to your application, and many internals of Action
Mailer. It also covers how to test your mailers.

After reading this guide, you will know:

- How to send email within a Rails application.
- How to generate and edit an Action Mailer class and mailer view.
- How to configure Action Mailer for your environment.
- How to test your Action Mailer classes.

### ![](https://guides.rubyonrails.org/v6.1/images/chapters_icon.gif)Chapters

1. [What is Action Mailer?](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html#what-is-action-mailer-questionmark)
2. [Sending Emails](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html#sending-emails)   - [Walkthrough to Generating a Mailer](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html#walkthrough-to-generating-a-mailer)
   - [Auto encoding header values](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html#auto-encoding-header-values)
   - [Complete List of Action Mailer Methods](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html#complete-list-of-action-mailer-methods)
   - [Mailer Views](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html#mailer-views)
   - [Action Mailer Layouts](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html#action-mailer-layouts)
   - [Previewing Emails](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html#previewing-emails)
   - [Generating URLs in Action Mailer Views](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html#generating-urls-in-action-mailer-views)
   - [Adding images in Action Mailer Views](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html#adding-images-in-action-mailer-views)
   - [Sending Multipart Emails](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html#sending-multipart-emails)
   - [Sending Emails with Dynamic Delivery Options](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html#sending-emails-with-dynamic-delivery-options)
   - [Sending Emails without Template Rendering](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html#sending-emails-without-template-rendering)
3. [Action Mailer Callbacks](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html#action-mailer-callbacks)
4. [Using Action Mailer Helpers](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html#using-action-mailer-helpers)
5. [Action Mailer Configuration](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html#action-mailer-configuration)   - [Example Action Mailer Configuration](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html#example-action-mailer-configuration)
   - [Action Mailer Configuration for Gmail](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html#action-mailer-configuration-for-gmail)
6. [Mailer Testing](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html#mailer-testing)
7. [Intercepting and Observing Emails](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html#intercepting-and-observing-emails)   - [Intercepting Emails](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html#intercepting-emails)
   - [Observing Emails](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html#observing-emails)

### [1 What is Action Mailer?](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html\#what-is-action-mailer-questionmark)

Action Mailer allows you to send emails from your application using mailer classes
and views.

##### [1.1 Mailers are similar to controllers](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html\#mailers-are-similar-to-controllers)

They inherit from `ActionMailer::Base` and live in `app/mailers`. Mailers also work
very similarly to controllers. Some examples of similarities are enumerated below.
Mailers have:

- Actions, and also, associated views that appear in `app/views`.
- Instance variables that are accessible in views.
- The ability to utilise layouts and partials.
- The ability to access a params hash.

### [2 Sending Emails](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html\#sending-emails)

This section will provide a step-by-step guide to creating a mailer and its
views.

#### [2.1 Walkthrough to Generating a Mailer](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html\#walkthrough-to-generating-a-mailer)

##### [2.1.1 Create the Mailer](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html\#create-the-mailer)

```
$ bin/rails generate mailer User
create  app/mailers/user_mailer.rb
create  app/mailers/application_mailer.rb
invoke  erb
create    app/views/user_mailer
create    app/views/layouts/mailer.text.erb
create    app/views/layouts/mailer.html.erb
invoke  test_unit
create    test/mailers/user_mailer_test.rb
create    test/mailers/previews/user_mailer_preview.rb
```

Copy

```
# app/mailers/application_mailer.rb
class ApplicationMailer < ActionMailer::Base
  default from: "from@example.com"
  layout 'mailer'
end
```

Copy

```
# app/mailers/user_mailer.rb
class UserMailer < ApplicationMailer
end
```

Copy

As you can see, you can generate mailers just like you use other generators with
Rails.

If you didn't want to use a generator, you could create your own file inside of
`app/mailers`, just make sure that it inherits from `ActionMailer::Base`:

```
class MyMailer < ActionMailer::Base
end
```

Copy

##### [2.1.2 Edit the Mailer](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html\#edit-the-mailer)

Mailers have methods called "actions" and they use views to structure their content.
Where a controller generates content like HTML to send back to the client, a Mailer
creates a message to be delivered via email.

`app/mailers/user_mailer.rb` contains an empty mailer:

```
class UserMailer < ApplicationMailer
end
```

Copy

Let's add a method called `welcome_email`, that will send an email to the user's
registered email address:

```
class UserMailer < ApplicationMailer
  default from: 'notifications@example.com'

  def welcome_email
    @user = params[:user]
    @url  = 'http://example.com/login'
    mail(to: @user.email, subject: 'Welcome to My Awesome Site')
  end
end
```

Copy

Here is a quick explanation of the items presented in the preceding method. For
a full list of all available options, please have a look further down at the
Complete List of Action Mailer user-settable attributes section.

- `default Hash` \- This is a hash of default values for any email you send from
this mailer. In this case we are setting the `:from` header to a value for all
messages in this class. This can be overridden on a per-email basis.
- `mail` \- The actual email message, we are passing the `:to` and `:subject`
headers in.

##### [2.1.3 Create a Mailer View](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html\#create-a-mailer-view)

Create a file called `welcome_email.html.erb` in `app/views/user_mailer/`. This
will be the template used for the email, formatted in HTML:

```
<!DOCTYPE html>
<html>
  <head>
    <meta content='text/html; charset=UTF-8' http-equiv='Content-Type' />
  </head>
  <body>
    <h1>Welcome to example.com, <%= @user.name %></h1>
    <p>
      You have successfully signed up to example.com,
      your username is: <%= @user.login %>.<br>
    </p>
    <p>
      To login to the site, just follow this link: <%= @url %>.
    </p>
    <p>Thanks for joining and have a great day!</p>
  </body>
</html>
```

Copy

Let's also make a text part for this email. Not all clients prefer HTML emails,
and so sending both is best practice. To do this, create a file called
`welcome_email.text.erb` in `app/views/user_mailer/`:

```
Welcome to example.com, <%= @user.name %>
===============================================

You have successfully signed up to example.com,
your username is: <%= @user.login %>.

To login to the site, just follow this link: <%= @url %>.

Thanks for joining and have a great day!
```

Copy

When you call the `mail` method now, Action Mailer will detect the two templates
(text and HTML) and automatically generate a `multipart/alternative` email.

##### [2.1.4 Calling the Mailer](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html\#calling-the-mailer)

Mailers are really just another way to render a view. Instead of rendering a
view and sending it over the HTTP protocol, they are sending it out through
the email protocols instead. Due to this, it makes sense to have your
controller tell the Mailer to send an email when a user is successfully created.

Setting this up is simple.

First, let's create a `User` scaffold:

```
$ bin/rails generate scaffold user name email login
$ bin/rails db:migrate
```

Copy

Now that we have a user model to play with, we will edit the
`app/controllers/users_controller.rb` file, make it instruct the `UserMailer` to deliver
an email to the newly created user by editing the create action and inserting a
call to `UserMailer.with(user: @user).welcome_email` right after the user is successfully saved.

Action Mailer is nicely integrated with Active Job so you can send emails outside
of the request-response cycle, so the user doesn't have to wait on it:

```
class UsersController < ApplicationController
  # POST /users
  # POST /users.json
  def create
    @user = User.new(params[:user])

    respond_to do |format|
      if @user.save
        # Tell the UserMailer to send a welcome email after save
        UserMailer.with(user: @user).welcome_email.deliver_later

        format.html { redirect_to(@user, notice: 'User was successfully created.') }
        format.json { render json: @user, status: :created, location: @user }
      else
        format.html { render action: 'new' }
        format.json { render json: @user.errors, status: :unprocessable_entity }
      end
    end
  end
end
```

Copy

Active Job's default behavior is to execute jobs via the `:async` adapter.
So, you can use `deliver_later` to send emails asynchronously.
Active Job's default adapter runs jobs with an in-process thread pool.
It's well-suited for the development/test environments, since it doesn't require
any external infrastructure, but it's a poor fit for production since it drops
pending jobs on restart.
If you need a persistent backend, you will need to use an Active Job adapter
that has a persistent backend (Sidekiq, Resque, etc).

If you want to send emails right away (from a cronjob for example) just call
`deliver_now`:

```
class SendWeeklySummary
  def run
    User.find_each do |user|
      UserMailer.with(user: user).weekly_summary.deliver_now
    end
  end
end
```

Copy

Any key value pair passed to `with` just becomes the `params` for the mailer
action. So `with(user: @user, account: @user.account)` makes `params[:user]` and
`params[:account]` available in the mailer action. Just like controllers have
params.

The method `welcome_email` returns an `ActionMailer::MessageDelivery` object which
can then be told to `deliver_now` or `deliver_later` to send itself out. The
`ActionMailer::MessageDelivery` object is a wrapper around a `Mail::Message`. If
you want to inspect, alter, or do anything else with the `Mail::Message` object you can
access it with the `message` method on the `ActionMailer::MessageDelivery` object.

#### [2.2 Auto encoding header values](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html\#auto-encoding-header-values)

Action Mailer handles the auto encoding of multibyte characters inside of
headers and bodies.

For more complex examples such as defining alternate character sets or
self-encoding text first, please refer to the
[Mail](https://github.com/mikel/mail) library.

#### [2.3 Complete List of Action Mailer Methods](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html\#complete-list-of-action-mailer-methods)

There are just three methods that you need to send pretty much any email
message:

- `headers` \- Specifies any header on the email you want. You can pass a hash of
header field names and value pairs, or you can call `headers[:field_name] =
'value'`.
- `attachments` \- Allows you to add attachments to your email. For example,
`attachments['file-name.jpg'] = File.read('file-name.jpg')`.
- `mail` \- Creates the actual email itself. You can pass in headers as a hash to
the `mail` method as a parameter. `mail` will create an email — either plain
text or multipart — depending on what email templates you have defined.

##### [2.3.1 Adding Attachments](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html\#adding-attachments)

Action Mailer makes it very easy to add attachments.

- Pass the file name and content and Action Mailer and the
[Mail gem](https://github.com/mikel/mail) will automatically guess the
`mime_type`, set the `encoding`, and create the attachment.



```
attachments['filename.jpg'] = File.read('/path/to/filename.jpg')
```

Copy


When the `mail` method will be triggered, it will send a multipart email with
an attachment, properly nested with the top level being `multipart/mixed` and
the first part being a `multipart/alternative` containing the plain text and
HTML email messages.

Mail will automatically Base64 encode an attachment. If you want something
different, encode your content and pass in the encoded content and encoding in a
`Hash` to the `attachments` method.

- Pass the file name and specify headers and content and Action Mailer and Mail
will use the settings you pass in.



```
encoded_content = SpecialEncode(File.read('/path/to/filename.jpg'))
attachments['filename.jpg'] = {
    mime_type: 'application/gzip',
    encoding: 'SpecialEncoding',
    content: encoded_content
}
```

Copy


If you specify an encoding, Mail will assume that your content is already
encoded and not try to Base64 encode it.

##### [2.3.2 Making Inline Attachments](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html\#making-inline-attachments)

Action Mailer 3.0 makes inline attachments, which involved a lot of hacking in pre 3.0 versions, much simpler and trivial as they should be.

- First, to tell Mail to turn an attachment into an inline attachment, you just call `#inline` on the attachments method within your Mailer:



```
def welcome
    attachments.inline['image.jpg'] = File.read('/path/to/image.jpg')
end
```

Copy

- Then in your view, you can just reference `attachments` as a hash and specify
which attachment you want to show, calling `url` on it and then passing the
result into the `image_tag` method:



```
<p>Hello there, this is our image</p>

<%= image_tag attachments['image.jpg'].url %>
```

Copy

- As this is a standard call to `image_tag` you can pass in an options hash
after the attachment URL as you could for any other image:



```
<p>Hello there, this is our image</p>

<%= image_tag attachments['image.jpg'].url, alt: 'My Photo', class: 'photos' %>
```

Copy


##### [2.3.3 Sending Email To Multiple Recipients](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html\#sending-email-to-multiple-recipients)

It is possible to send email to one or more recipients in one email (e.g.,
informing all admins of a new signup) by setting the list of emails to the `:to`
key. The list of emails can be an array of email addresses or a single string
with the addresses separated by commas.

```
class AdminMailer < ApplicationMailer
  default to: -> { Admin.pluck(:email) },
          from: 'notification@example.com'

  def new_registration(user)
    @user = user
    mail(subject: "New User Signup: #{@user.email}")
  end
end
```

Copy

The same format can be used to set carbon copy (Cc:) and blind carbon copy
(Bcc:) recipients, by using the `:cc` and `:bcc` keys respectively.

##### [2.3.4 Sending Email With Name](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html\#sending-email-with-name)

Sometimes you wish to show the name of the person instead of just their email
address when they receive the email. You can use `email_address_with_name` for
that:

```
def welcome_email
  @user = params[:user]
  mail(
    to: email_address_with_name(@user.email, @user.name),
    subject: 'Welcome to My Awesome Site'
  )
end
```

Copy

#### [2.4 Mailer Views](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html\#mailer-views)

Mailer views are located in the `app/views/name_of_mailer_class` directory. The
specific mailer view is known to the class because its name is the same as the
mailer method. In our example from above, our mailer view for the
`welcome_email` method will be in `app/views/user_mailer/welcome_email.html.erb`
for the HTML version and `welcome_email.text.erb` for the plain text version.

To change the default mailer view for your action you do something like:

```
class UserMailer < ApplicationMailer
  default from: 'notifications@example.com'

  def welcome_email
    @user = params[:user]
    @url  = 'http://example.com/login'
    mail(to: @user.email,
         subject: 'Welcome to My Awesome Site',
         template_path: 'notifications',
         template_name: 'another')
  end
end
```

Copy

In this case it will look for templates at `app/views/notifications` with name
`another`. You can also specify an array of paths for `template_path`, and they
will be searched in order.

If you want more flexibility you can also pass a block and render specific
templates or even render inline or text without using a template file:

```
class UserMailer < ApplicationMailer
  default from: 'notifications@example.com'

  def welcome_email
    @user = params[:user]
    @url  = 'http://example.com/login'
    mail(to: @user.email,
         subject: 'Welcome to My Awesome Site') do |format|
      format.html { render 'another_template' }
      format.text { render plain: 'Render text' }
    end
  end
end
```

Copy

This will render the template 'another\_template.html.erb' for the HTML part and
use the rendered text for the text part. The render command is the same one used
inside of Action Controller, so you can use all the same options, such as
`:text`, `:inline`, etc.

If you would like to render a template located outside of the default `app/views/mailer_name/` directory, you can apply the `prepend_view_path`, like so:

```
class UserMailer < ApplicationMailer
  prepend_view_path "custom/path/to/mailer/view"

  # This will try to load "custom/path/to/mailer/view/welcome_email" template
  def welcome_email
    # ...
  end
end
```

Copy

You can also consider using the [append\_view\_path](https://guides.rubyonrails.org/action_view_overview.html#view-paths) method.

##### [2.4.1 Caching mailer view](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html\#caching-mailer-view)

You can perform fragment caching in mailer views like in application views using the `cache` method.

```
<% cache do %>
  <%= @company.name %>
<% end %>
```

Copy

And in order to use this feature, you need to configure your application with this:

```
config.action_mailer.perform_caching = true
```

Copy

Fragment caching is also supported in multipart emails.
Read more about caching in the [Rails caching guide](https://guides.rubyonrails.org/v6.1/caching_with_rails.html).

#### [2.5 Action Mailer Layouts](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html\#action-mailer-layouts)

Just like controller views, you can also have mailer layouts. The layout name
needs to be the same as your mailer, such as `user_mailer.html.erb` and
`user_mailer.text.erb` to be automatically recognized by your mailer as a
layout.

In order to use a different file, call `layout` in your mailer:

```
class UserMailer < ApplicationMailer
  layout 'awesome' # use awesome.(html|text).erb as the layout
end
```

Copy

Just like with controller views, use `yield` to render the view inside the
layout.

You can also pass in a `layout: 'layout_name'` option to the render call inside
the format block to specify different layouts for different formats:

```
class UserMailer < ApplicationMailer
  def welcome_email
    mail(to: params[:user].email) do |format|
      format.html { render layout: 'my_layout' }
      format.text
    end
  end
end
```

Copy

Will render the HTML part using the `my_layout.html.erb` file and the text part
with the usual `user_mailer.text.erb` file if it exists.

#### [2.6 Previewing Emails](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html\#previewing-emails)

Action Mailer previews provide a way to see how emails look by visiting a
special URL that renders them. In the above example, the preview class for
`UserMailer` should be named `UserMailerPreview` and located in
`test/mailers/previews/user_mailer_preview.rb`. To see the preview of
`welcome_email`, implement a method that has the same name and call
`UserMailer.welcome_email`:

```
class UserMailerPreview < ActionMailer::Preview
  def welcome_email
    UserMailer.with(user: User.first).welcome_email
  end
end
```

Copy

Then the preview will be available in [http://localhost:3000/rails/mailers/user\_mailer/welcome\_email](http://localhost:3000/rails/mailers/user_mailer/welcome_email).

If you change something in `app/views/user_mailer/welcome_email.html.erb`
or the mailer itself, it'll automatically reload and render it so you can
visually see the new style instantly. A list of previews are also available
in [http://localhost:3000/rails/mailers](http://localhost:3000/rails/mailers).

By default, these preview classes live in `test/mailers/previews`.
This can be configured using the `preview_path` option. For example, if you
want to change it to `lib/mailer_previews`, you can configure it in
`config/application.rb`:

```
config.action_mailer.preview_path = "#{Rails.root}/lib/mailer_previews"
```

Copy

#### [2.7 Generating URLs in Action Mailer Views](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html\#generating-urls-in-action-mailer-views)

Unlike controllers, the mailer instance doesn't have any context about the
incoming request so you'll need to provide the `:host` parameter yourself.

As the `:host` usually is consistent across the application you can configure it
globally in `config/application.rb`:

```
config.action_mailer.default_url_options = { host: 'example.com' }
```

Copy

Because of this behavior you cannot use any of the `*_path` helpers inside of
an email. Instead you will need to use the associated `*_url` helper. For example
instead of using

```
<%= link_to 'welcome', welcome_path %>
```

Copy

You will need to use:

```
<%= link_to 'welcome', welcome_url %>
```

Copy

By using the full URL, your links will now work in your emails.

##### [2.7.1 Generating URLs with `url_for`](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html\#generating-urls-with-url-for)

`url_for` generates a full URL by default in templates.

If you did not configure the `:host` option globally make sure to pass it to
`url_for`.

```
<%= url_for(host: 'example.com',
            controller: 'welcome',
            action: 'greeting') %>
```

Copy

##### [2.7.2 Generating URLs with Named Routes](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html\#generating-urls-with-named-routes)

Email clients have no web context and so paths have no base URL to form complete
web addresses. Thus, you should always use the `*_url` variant of named route
helpers.

If you did not configure the `:host` option globally make sure to pass it to the
URL helper.

```
<%= user_url(@user, host: 'example.com') %>
```

Copy

non-`GET` links require [rails-ujs](https://github.com/rails/rails/blob/main/actionview/app/assets/javascripts) or
[jQuery UJS](https://github.com/rails/jquery-ujs), and won't work in mailer templates.
They will result in normal `GET` requests.

#### [2.8 Adding images in Action Mailer Views](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html\#adding-images-in-action-mailer-views)

Unlike controllers, the mailer instance doesn't have any context about the
incoming request so you'll need to provide the `:asset_host` parameter yourself.

As the `:asset_host` usually is consistent across the application you can
configure it globally in `config/application.rb`:

```
config.asset_host = 'http://example.com'
```

Copy

Now you can display an image inside your email.

```
<%= image_tag 'image.jpg' %>
```

Copy

#### [2.9 Sending Multipart Emails](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html\#sending-multipart-emails)

Action Mailer will automatically send multipart emails if you have different
templates for the same action. So, for our `UserMailer` example, if you have
`welcome_email.text.erb` and `welcome_email.html.erb` in
`app/views/user_mailer`, Action Mailer will automatically send a multipart email
with the HTML and text versions setup as different parts.

The order of the parts getting inserted is determined by the `:parts_order`
inside of the `ActionMailer::Base.default` method.

#### [2.10 Sending Emails with Dynamic Delivery Options](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html\#sending-emails-with-dynamic-delivery-options)

If you wish to override the default delivery options (e.g. SMTP credentials)
while delivering emails, you can do this using `delivery_method_options` in the
mailer action.

```
class UserMailer < ApplicationMailer
  def welcome_email
    @user = params[:user]
    @url  = user_url(@user)
    delivery_options = { user_name: params[:company].smtp_user,
                         password: params[:company].smtp_password,
                         address: params[:company].smtp_host }
    mail(to: @user.email,
         subject: "Please see the Terms and Conditions attached",
         delivery_method_options: delivery_options)
  end
end
```

Copy

#### [2.11 Sending Emails without Template Rendering](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html\#sending-emails-without-template-rendering)

There may be cases in which you want to skip the template rendering step and
supply the email body as a string. You can achieve this using the `:body`
option. In such cases don't forget to add the `:content_type` option. Rails
will default to `text/plain` otherwise.

```
class UserMailer < ApplicationMailer
  def welcome_email
    mail(to: params[:user].email,
         body: params[:email_body],
         content_type: "text/html",
         subject: "Already rendered!")
  end
end
```

Copy

### [3 Action Mailer Callbacks](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html\#action-mailer-callbacks)

Action Mailer allows for you to specify a `before_action`, `after_action` and
`around_action`.

- Filters can be specified with a block or a symbol to a method in the mailer
class similar to controllers.

- You could use a `before_action` to set instance variables, populate the mail
object with defaults, or insert default headers and attachments.


```
class InvitationsMailer < ApplicationMailer
  before_action :set_inviter_and_invitee
  before_action { @account = params[:inviter].account }

  default to:       -> { @invitee.email_address },
          from:     -> { common_address(@inviter) },
          reply_to: -> { @inviter.email_address_with_name }

  def account_invitation
    mail subject: "#{@inviter.name} invited you to their Basecamp (#{@account.name})"
  end

  def project_invitation
    @project    = params[:project]
    @summarizer = ProjectInvitationSummarizer.new(@project.bucket)

    mail subject: "#{@inviter.name.familiar} added you to a project in Basecamp (#{@account.name})"
  end

  private

  def set_inviter_and_invitee
    @inviter = params[:inviter]
    @invitee = params[:invitee]
  end
end
```

Copy

- You could use an `after_action` to do similar setup as a `before_action` but
using instance variables set in your mailer action.

- Using an `after_action` callback also enables you to override delivery method
settings by updating `mail.delivery_method.settings`.


```
class UserMailer < ApplicationMailer
  before_action { @business, @user = params[:business], params[:user] }

  after_action :set_delivery_options,
               :prevent_delivery_to_guests,
               :set_business_headers

  def feedback_message
  end

  def campaign_message
  end

  private

    def set_delivery_options
      # You have access to the mail instance,
      # @business and @user instance variables here
      if @business && @business.has_smtp_settings?
        mail.delivery_method.settings.merge!(@business.smtp_settings)
      end
    end

    def prevent_delivery_to_guests
      if @user && @user.guest?
        mail.perform_deliveries = false
      end
    end

    def set_business_headers
      if @business
        headers["X-SMTPAPI-CATEGORY"] = @business.code
      end
    end
end
```

Copy

- Mailer Filters abort further processing if body is set to a non-nil value.

### [4 Using Action Mailer Helpers](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html\#using-action-mailer-helpers)

Action Mailer inherits from `AbstractController`, so you have access to most
of the same helpers as you do in Action Controller.

There are also some Action Mailer-specific helper methods available in
`ActionMailer::MailHelper`. For example, these allow accessing the mailer
instance from your view with `mailer`, and accessing the message as `message`:

```
<%= stylesheet_link_tag mailer.name.underscore %>
<h1><%= message.subject %></h1>
```

Copy

### [5 Action Mailer Configuration](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html\#action-mailer-configuration)

The following configuration options are best made in one of the environment
files (environment.rb, production.rb, etc...)

| Configuration | Description |
| --- | --- |
| `logger` | Generates information on the mailing run if available. Can be set to `nil` for no logging. Compatible with both Ruby's own `Logger` and `Log4r` loggers. |
| `smtp_settings` | Allows detailed configuration for `:smtp` delivery method:<br>- `:address` \- Allows you to use a remote mail server. Just change it from its default `"localhost"` setting.<br>- `:port` \- On the off chance that your mail server doesn't run on port 25, you can change it.<br>- `:domain` \- If you need to specify a HELO domain, you can do it here.<br>- `:user_name` \- If your mail server requires authentication, set the username in this setting.<br>- `:password` \- If your mail server requires authentication, set the password in this setting.<br>- `:authentication` \- If your mail server requires authentication, you need to specify the authentication type here. This is a symbol and one of `:plain` (will send the password in the clear), `:login` (will send password Base64 encoded) or `:cram_md5` (combines a Challenge/Response mechanism to exchange information and a cryptographic Message Digest 5 algorithm to hash important information)<br>- `:enable_starttls_auto` \- Detects if STARTTLS is enabled in your SMTP server and starts to use it. Defaults to `true`.<br>- `:openssl_verify_mode` \- When using TLS, you can set how OpenSSL checks the certificate. This is really useful if you need to validate a self-signed and/or a wildcard certificate. You can use the name of an OpenSSL verify constant ('none' or 'peer') or directly the constant (`OpenSSL::SSL::VERIFY_NONE` or `OpenSSL::SSL::VERIFY_PEER`).<br>- `:ssl/:tls` \- Enables the SMTP connection to use SMTP/TLS (SMTPS: SMTP over direct TLS connection) |
| `sendmail_settings` | Allows you to override options for the `:sendmail` delivery method.<br>- `:location` \- The location of the sendmail executable. Defaults to `/usr/sbin/sendmail`.<br>- `:arguments` \- The command line arguments to be passed to sendmail. Defaults to `-i`. |
| `raise_delivery_errors` | Whether or not errors should be raised if the email fails to be delivered. This only works if the external email server is configured for immediate delivery. |
| `delivery_method` | Defines a delivery method. Possible values are:<br>- `:smtp` (default), can be configured by using `config.action_mailer.smtp_settings`.<br>- `:sendmail`, can be configured by using `config.action_mailer.sendmail_settings`.<br>- `:file`: save emails to files; can be configured by using `config.action_mailer.file_settings`.<br>- `:test`: save emails to `ActionMailer::Base.deliveries` array.<br>See [API docs](https://api.rubyonrails.org/v6.1.7.10/classes/ActionMailer/Base.html) for more info. |
| `perform_deliveries` | Determines whether deliveries are actually carried out when the `deliver` method is invoked on the Mail message. By default they are, but this can be turned off to help functional testing. If this value is `false`, `deliveries` array will not be populated even if `delivery_method` is `:test`. |
| `deliveries` | Keeps an array of all the emails sent out through the Action Mailer with delivery\_method :test. Most useful for unit and functional testing. |
| `default_options` | Allows you to set default values for the `mail` method options (`:from`, `:reply_to`, etc.). |

For a complete writeup of possible configurations see the
[Configuring Action Mailer](https://guides.rubyonrails.org/v6.1/configuring.html#configuring-action-mailer) in
our Configuring Rails Applications guide.

#### [5.1 Example Action Mailer Configuration](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html\#example-action-mailer-configuration)

An example would be adding the following to your appropriate
`config/environments/$RAILS_ENV.rb` file:

```
config.action_mailer.delivery_method = :sendmail
# Defaults to:
# config.action_mailer.sendmail_settings = {
#   location: '/usr/sbin/sendmail',
#   arguments: '-i'
# }
config.action_mailer.perform_deliveries = true
config.action_mailer.raise_delivery_errors = true
config.action_mailer.default_options = {from: 'no-reply@example.com'}
```

Copy

#### [5.2 Action Mailer Configuration for Gmail](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html\#action-mailer-configuration-for-gmail)

As Action Mailer now uses the [Mail gem](https://github.com/mikel/mail), this
becomes as simple as adding to your `config/environments/$RAILS_ENV.rb` file:

```
config.action_mailer.delivery_method = :smtp
config.action_mailer.smtp_settings = {
  address:              'smtp.gmail.com',
  port:                 587,
  domain:               'example.com',
  user_name:            '<username>',
  password:             '<password>',
  authentication:       'plain',
  enable_starttls_auto: true }
```

Copy

As of July 15, 2014, Google increased [its security measures](https://support.google.com/accounts/answer/6010255) and now blocks attempts from apps it deems less secure.
You can change your Gmail settings [here](https://www.google.com/settings/security/lesssecureapps) to allow the attempts. If your Gmail account has 2-factor authentication enabled,
then you will need to set an [app password](https://myaccount.google.com/apppasswords) and use that instead of your regular password. Alternatively, you can
use another ESP to send email by replacing 'smtp.gmail.com' above with the address of your provider.

### [6 Mailer Testing](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html\#mailer-testing)

You can find detailed instructions on how to test your mailers in the
[testing guide](https://guides.rubyonrails.org/v6.1/testing.html#testing-your-mailers).

### [7 Intercepting and Observing Emails](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html\#intercepting-and-observing-emails)

Action Mailer provides hooks into the Mail observer and interceptor methods. These allow you to register classes that are called during the mail delivery life cycle of every email sent.

#### [7.1 Intercepting Emails](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html\#intercepting-emails)

Interceptors allow you to make modifications to emails before they are handed off to the delivery agents. An interceptor class must implement the `::delivering_email(message)` method which will be called before the email is sent.

```
class SandboxEmailInterceptor
  def self.delivering_email(message)
    message.to = ['sandbox@example.com']
  end
end
```

Copy

Before the interceptor can do its job you need to register it using
`register_interceptor`. You can do this in an initializer file like
`config/initializers/sandbox_email_interceptor.rb`:

```
if Rails.env.staging?
  ActionMailer::Base.register_interceptor(SandboxEmailInterceptor)
end
```

Copy

The example above uses a custom environment called "staging" for a
production like server but for testing purposes. You can read
[Creating Rails Environments](https://guides.rubyonrails.org/v6.1/configuring.html#creating-rails-environments)
for more information about custom Rails environments.

#### [7.2 Observing Emails](https://guides.rubyonrails.org/v6.1/action_mailer_basics.html\#observing-emails)

Observers give you access to the email message after it has been sent. An observer class must implement the `:delivered_email(message)` method, which will be called after the email is sent.

```
class EmailDeliveryObserver
  def self.delivered_email(message)
    EmailDelivery.log(message)
  end
end
```

Copy

Similar to interceptors, you must register observers using `register_observer`. You can do this in an initializer file
like `config/initializers/email_delivery_observer.rb`:

```
ActionMailer::Base.register_observer(EmailDeliveryObserver)
```

Copy

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