v6.1.7.10

**More at [rubyonrails.org:](https://rubyonrails.org/)**
More Ruby on Rails


- [Blog](https://rubyonrails.org/blog)
- [Guides](https://guides.rubyonrails.org/)
- [API](https://api.rubyonrails.org/)
- [Forum](https://discuss.rubyonrails.org/)
- [Contribute on GitHub](https://github.com/rails/rails)

* * *

## Working with JavaScript in Rails

This guide covers the built-in Ajax/JavaScript functionality of Rails (and
more); it will enable you to create rich and dynamic Ajax applications with
ease!

After reading this guide, you will know:

- The basics of Ajax.
- Unobtrusive JavaScript.
- How Rails' built-in helpers assist you.
- How to handle Ajax on the server side.
- The Turbolinks gem.
- How to include your Cross-Site Request Forgery token in request headers

### ![](https://guides.rubyonrails.org/v6.1/images/chapters_icon.gif)Chapters

1. [An Introduction to Ajax](https://guides.rubyonrails.org/v6.1/working_with_javascript_in_rails.html#an-introduction-to-ajax)
2. [Unobtrusive JavaScript](https://guides.rubyonrails.org/v6.1/working_with_javascript_in_rails.html#unobtrusive-javascript)
3. [Built-in Helpers](https://guides.rubyonrails.org/v6.1/working_with_javascript_in_rails.html#built-in-helpers)   - [Remote Elements](https://guides.rubyonrails.org/v6.1/working_with_javascript_in_rails.html#remote-elements)
   - [Customize Remote Elements](https://guides.rubyonrails.org/v6.1/working_with_javascript_in_rails.html#customize-remote-elements)
   - [Confirmations](https://guides.rubyonrails.org/v6.1/working_with_javascript_in_rails.html#confirmations)
   - [Automatic disabling](https://guides.rubyonrails.org/v6.1/working_with_javascript_in_rails.html#automatic-disabling)
   - [Rails-ujs event handlers](https://guides.rubyonrails.org/v6.1/working_with_javascript_in_rails.html#rails-ujs-event-handlers)
   - [Stoppable events](https://guides.rubyonrails.org/v6.1/working_with_javascript_in_rails.html#stoppable-events)
4. [Server-Side Concerns](https://guides.rubyonrails.org/v6.1/working_with_javascript_in_rails.html#server-side-concerns)   - [A Simple Example](https://guides.rubyonrails.org/v6.1/working_with_javascript_in_rails.html#a-simple-example)
5. [Turbolinks](https://guides.rubyonrails.org/v6.1/working_with_javascript_in_rails.html#turbolinks)   - [How Turbolinks Works](https://guides.rubyonrails.org/v6.1/working_with_javascript_in_rails.html#how-turbolinks-works)
   - [Page Change Events](https://guides.rubyonrails.org/v6.1/working_with_javascript_in_rails.html#page-change-events)
6. [Cross-Site Request Forgery (CSRF) token in Ajax](https://guides.rubyonrails.org/v6.1/working_with_javascript_in_rails.html#cross-site-request-forgery-csrf-token-in-ajax)
7. [Other Resources](https://guides.rubyonrails.org/v6.1/working_with_javascript_in_rails.html#other-resources)

### [1 An Introduction to Ajax](https://guides.rubyonrails.org/v6.1/working_with_javascript_in_rails.html\#an-introduction-to-ajax)

In order to understand Ajax, you must first understand what a web browser does
normally.

When you type `http://localhost:3000` into your browser's address bar and hit
'Go', the browser (your 'client') makes a request to the server. It parses the
response, then fetches all associated assets, like JavaScript files,
stylesheets and images. It then assembles the page. If you click a link, it
does the same process: fetch the page, fetch the assets, put it all together,
show you the results. This is called the 'request response cycle'.

JavaScript can also make requests to the server, and parse the response. It
also has the ability to update information on the page. Combining these two
powers, a JavaScript writer can make a web page that can update just parts of
itself, without needing to get the full page data from the server. This is a
powerful technique that we call Ajax.

As an example, here's some JavaScript code that makes an Ajax request:

```
fetch("/test")
  .then((data) => data.text())
  .then((html) => {
    const results = document.querySelector("#results");
    results.insertAdjacentHTML("beforeend", data);
  });
```

Copy

This code fetches data from "/test", and then appends the result to the element
with an id of `results`.

Rails provides quite a bit of built-in support for building web pages with this
technique. You rarely have to write this code yourself. The rest of this guide
will show you how Rails can help you write websites in this way, but it's
all built on top of this fairly simple technique.

### [2 Unobtrusive JavaScript](https://guides.rubyonrails.org/v6.1/working_with_javascript_in_rails.html\#unobtrusive-javascript)

Rails uses a technique called "Unobtrusive JavaScript" to handle attaching
JavaScript to the DOM. This is generally considered to be a best-practice
within the frontend community, but you may occasionally read tutorials that
demonstrate other ways.

Here's the simplest way to write JavaScript. You may see it referred to as
'inline JavaScript':

```
<a href="#" onclick="this.style.backgroundColor='#990000';event.preventDefault();">Paint it red</a>
```

Copy

When clicked, the link background will become red. Here's the problem: what
happens when we have lots of JavaScript we want to execute on a click?

```
<a href="#" onclick="this.style.backgroundColor='#009900';this.style.color='#FFFFFF';event.preventDefault();">Paint it green</a>
```

Copy

Awkward, right? We could pull the function definition out of the click handler,
and turn it a function:

```
window.paintIt = function(event, backgroundColor, textColor) {
  event.preventDefault();
  event.target.style.backgroundColor = backgroundColor;
  if (textColor) {
    event.target.style.color = textColor;
  }
}
```

Copy

And then on our page:

```
<a href="#" onclick="paintIt(event, '#990000')">Paint it red</a>
```

Copy

That's a little bit better, but what about multiple links that have the same
effect?

```
<a href="#" onclick="paintIt(event, '#990000')">Paint it red</a>
<a href="#" onclick="paintIt(event, '#009900', '#FFFFFF')">Paint it green</a>
<a href="#" onclick="paintIt(event, '#000099', '#FFFFFF')">Paint it blue</a>
```

Copy

Not very DRY, eh? We can fix this by using events instead. We'll add a `data-*`
attribute to our link, and then bind a handler to the click event of every link
that has that attribute:

```
function paintIt(element, backgroundColor, textColor) {
  element.style.backgroundColor = backgroundColor;
  if (textColor) {
    element.style.color = textColor;
  }
}

window.addEventListener("load", () => {
  const links = document.querySelectorAll(
    "a[data-background-color]"
  );
  links.forEach((element) => {
    element.addEventListener("click", (event) => {
      event.preventDefault();

      const {backgroundColor, textColor} = element.dataset;
      paintIt(element, backgroundColor, textColor);
    });
  });
});
```

Copy

```
<a href="#" data-background-color="#990000">Paint it red</a>
<a href="#" data-background-color="#009900" data-text-color="#FFFFFF">Paint it green</a>
<a href="#" data-background-color="#000099" data-text-color="#FFFFFF">Paint it blue</a>
```

Copy

We call this 'unobtrusive' JavaScript because we're no longer mixing our
JavaScript into our HTML. We've properly separated our concerns, making future
change easy. We can easily add behavior to any link by adding the data
attribute. We can run all of our JavaScript through a minimizer and
concatenator. We can serve our entire JavaScript bundle on every page, which
means that it'll get downloaded on the first page load and then be cached on
every page after that. Lots of little benefits really add up.

### [3 Built-in Helpers](https://guides.rubyonrails.org/v6.1/working_with_javascript_in_rails.html\#built-in-helpers)

#### [3.1 Remote Elements](https://guides.rubyonrails.org/v6.1/working_with_javascript_in_rails.html\#remote-elements)

Rails provides a bunch of view helper methods written in Ruby to assist you
in generating HTML. Sometimes, you want to add a little Ajax to those elements,
and Rails has got your back in those cases.

Because of Unobtrusive JavaScript, the Rails "Ajax helpers" are actually in two
parts: the JavaScript half and the Ruby half.

Unless you have disabled the Asset Pipeline,
[rails-ujs](https://github.com/rails/rails/tree/main/actionview/app/assets/javascripts)
provides the JavaScript half, and the regular Ruby view helpers add appropriate
tags to your DOM.

You can read below about the different events that are fired dealing with
remote elements inside your application.

##### [3.1.1 form\_with](https://guides.rubyonrails.org/v6.1/working_with_javascript_in_rails.html\#form-with)

[`form_with`](https://api.rubyonrails.org/v6.1.7.10/classes/ActionView/Helpers/FormHelper.html#method-i-form_with)
is a helper that assists with writing forms. To use Ajax for your form you can
pass the `:local` option to `form_with`.

```
<%= form_with(model: @article, id: "new-article", local: false) do |form| %>
  ...
<% end %>
```

Copy

This will generate the following HTML:

```
<form id="new-article" action="/articles" accept-charset="UTF-8" method="post" data-remote="true">
  ...
</form>
```

Copy

Note the `data-remote="true"`. Now, the form will be submitted by Ajax rather
than by the browser's normal submit mechanism.

You probably don't want to just sit there with a filled out `<form>`, though.
You probably want to do something upon a successful submission. To do that,
bind to the `ajax:success` event. On failure, use `ajax:error`. Check it out:

```
window.addEventListener("load", () => {
  const element = document.querySelector("#new-article");
  element.addEventListener("ajax:success", (event) => {
    const [_data, _status, xhr] = event.detail;
    element.insertAdjacentHTML("beforeend", xhr.responseText);
  });
  element.addEventListener("ajax:error", () => {
    element.insertAdjacentHTML("beforeend", "<p>ERROR</p>");
  });
});
```

Copy

Obviously, you'll want to be a bit more sophisticated than that, but it's a
start.

##### [3.1.2 link\_to](https://guides.rubyonrails.org/v6.1/working_with_javascript_in_rails.html\#link-to)

[`link_to`](https://api.rubyonrails.org/v6.1.7.10/classes/ActionView/Helpers/UrlHelper.html#method-i-link_to)
is a helper that assists with generating links. It has a `:remote` option you
can use like this:

```
<%= link_to "an article", @article, remote: true %>
```

Copy

which generates

```
<a href="/articles/1" data-remote="true">an article</a>
```

Copy

You can bind to the same Ajax events as `form_with`. Here's an example. Let's
assume that we have a list of articles that can be deleted with just one
click. We would generate some HTML like this:

```
<%= link_to "Delete article", @article, remote: true, method: :delete %>
```

Copy

and write some JavaScript like this:

```
window.addEventListener("load", () => {
  const links = document.querySelectorAll("a[data-remote]");
  links.forEach((element) => {
    element.addEventListener("ajax:success", () => {
      alert("The article was deleted.");
    });
  });
});
```

Copy

##### [3.1.3 button\_to](https://guides.rubyonrails.org/v6.1/working_with_javascript_in_rails.html\#button-to)

[`button_to`](https://api.rubyonrails.org/v6.1.7.10/classes/ActionView/Helpers/UrlHelper.html#method-i-button_to) is a helper that helps you create buttons. It has a `:remote` option that you can call like this:

```
<%= button_to "An article", @article, remote: true %>
```

Copy

this generates

```
<form action="/articles/1" class="button_to" data-remote="true" method="post">
  <input type="submit" value="An article" />
</form>
```

Copy

Since it's just a `<form>`, all of the information on `form_with` also applies.

#### [3.2 Customize Remote Elements](https://guides.rubyonrails.org/v6.1/working_with_javascript_in_rails.html\#customize-remote-elements)

It is possible to customize the behavior of elements with a `data-remote`
attribute without writing a line of JavaScript. You can specify extra `data-`
attributes to accomplish this.

##### [3.2.1 `data-method`](https://guides.rubyonrails.org/v6.1/working_with_javascript_in_rails.html\#data-method)

Activating hyperlinks always results in an HTTP GET request. However, if your
application is [RESTful](https://en.wikipedia.org/wiki/Representational_State_Transfer),
some links are in fact actions that change data on the server, and must be
performed with non-GET requests. This attribute allows marking up such links
with an explicit method such as "post", "put" or "delete".

The way it works is that, when the link is activated, it constructs a hidden form
in the document with the "action" attribute corresponding to "href" value of the
link, and the method corresponding to `data-method` value, and submits that form.

Because submitting forms with HTTP methods other than GET and POST isn't
widely supported across browsers, all other HTTP methods are actually sent over
POST with the intended method indicated in the `_method` parameter. Rails
automatically detects and compensates for this.

##### [3.2.2 `data-url` and `data-params`](https://guides.rubyonrails.org/v6.1/working_with_javascript_in_rails.html\#data-url-and-data-params)

Certain elements of your page aren't actually referring to any URL, but you may want
them to trigger Ajax calls. Specifying the `data-url` attribute along with
the `data-remote` one will trigger an Ajax call to the given URL. You can also
specify extra parameters through the `data-params` attribute.

This can be useful to trigger an action on check-boxes for instance:

```
<input type="checkbox" data-remote="true"
    data-url="/update" data-params="id=10" data-method="put">
```

Copy

##### [3.2.3 `data-type`](https://guides.rubyonrails.org/v6.1/working_with_javascript_in_rails.html\#data-type)

It is also possible to define the Ajax `dataType` explicitly while performing
requests for `data-remote` elements, by way of the `data-type` attribute.

#### [3.3 Confirmations](https://guides.rubyonrails.org/v6.1/working_with_javascript_in_rails.html\#confirmations)

You can ask for an extra confirmation of the user by adding a `data-confirm`
attribute on links and forms. The user will be presented with a JavaScript `confirm()`
dialog containing the attribute's text. If the user chooses to cancel, the action
doesn't take place.

Adding this attribute on links will trigger the dialog on click, and adding it
on forms will trigger it on submit. For example:

```
<%= link_to "Dangerous zone", dangerous_zone_path,
  data: { confirm: 'Are you sure?' } %>
```

Copy

This generates:

```
<a href="..." data-confirm="Are you sure?">Dangerous zone</a>
```

Copy

The attribute is also allowed on form submit buttons. This allows you to customize
the warning message depending on the button which was activated. In this case,
you should **not** have `data-confirm` on the form itself.

The default confirmation uses a JavaScript confirm dialog, but you can customize
this by listening to the `confirm` event, which is fired just before the confirmation
window appears to the user. To cancel this default confirmation, have the confirm
handler return `false`.

#### [3.4 Automatic disabling](https://guides.rubyonrails.org/v6.1/working_with_javascript_in_rails.html\#automatic-disabling)

It is also possible to automatically disable an input while the form is submitting
by using the `data-disable-with` attribute. This is to prevent accidental
double-clicks from the user, which could result in duplicate HTTP requests that
the backend may not detect as such. The value of the attribute is the text that will
become the new value of the button in its disabled state.

This also works for links with `data-method` attribute.

For example:

```
<%= form_with(model: Article.new) do |form| %>
  <%= form.submit data: { disable_with: "Saving..." } %>
<% end %>
```

Copy

This generates a form with:

```
<input data-disable-with="Saving..." type="submit">
```

Copy

#### [3.5 Rails-ujs event handlers](https://guides.rubyonrails.org/v6.1/working_with_javascript_in_rails.html\#rails-ujs-event-handlers)

Rails 5.1 introduced rails-ujs and dropped jQuery as a dependency.
As a result the Unobtrusive JavaScript (UJS) driver has been rewritten to operate without jQuery.
These introductions cause small changes to `custom events` fired during the request:

Signature of calls to UJS's event handlers has changed.
Unlike the version with jQuery, all custom events return only one parameter: `event`.
In this parameter, there is an additional attribute `detail` which contains an array of extra parameters.
For information about the previously used `jquery-ujs` in Rails 5 and earlier, read the [`jquery-ujs` wiki](https://github.com/rails/jquery-ujs/wiki/ajax).

| Event name | Extra parameters (event.detail) | Fired |
| --- | --- | --- |
| `ajax:before` |  | Before the whole ajax business. |
| `ajax:beforeSend` | \[xhr, options\] | Before the request is sent. |
| `ajax:send` | \[xhr\] | When the request is sent. |
| `ajax:stopped` |  | When the request is stopped. |
| `ajax:success` | \[response, status, xhr\] | After completion, if the response was a success. |
| `ajax:error` | \[response, status, xhr\] | After completion, if the response was an error. |
| `ajax:complete` | \[xhr, status\] | After the request has been completed, no matter the outcome. |

Example usage:

```
document.body.addEventListener("ajax:success", (event) => {
  const [data, status, xhr] = event.detail;
});
```

Copy

#### [3.6 Stoppable events](https://guides.rubyonrails.org/v6.1/working_with_javascript_in_rails.html\#stoppable-events)

You can stop execution of the Ajax request by running `event.preventDefault()`
from the handlers methods `ajax:before` or `ajax:beforeSend`.
The `ajax:before` event can manipulate form data before serialization and the
`ajax:beforeSend` event is useful for adding custom request headers.

If you stop the `ajax:aborted:file` event, the default behavior of allowing the
browser to submit the form via normal means (i.e. non-Ajax submission) will be
canceled and the form will not be submitted at all. This is useful for
implementing your own Ajax file upload workaround.

Note, you should use `return false` to prevent an event for `jquery-ujs` and
`event.preventDefault()` for `rails-ujs`.

### [4 Server-Side Concerns](https://guides.rubyonrails.org/v6.1/working_with_javascript_in_rails.html\#server-side-concerns)

Ajax isn't just client-side, you also need to do some work on the server
side to support it. Often, people like their Ajax requests to return JSON
rather than HTML. Let's discuss what it takes to make that happen.

#### [4.1 A Simple Example](https://guides.rubyonrails.org/v6.1/working_with_javascript_in_rails.html\#a-simple-example)

Imagine you have a series of users that you would like to display and provide a
form on that same page to create a new user. The index action of your
controller looks like this:

```
class UsersController < ApplicationController
  def index
    @users = User.all
    @user = User.new
  end
  # ...
```

Copy

The index view (`app/views/users/index.html.erb`) contains:

```
<b>Users</b>

<ul id="users">
<%= render @users %>
</ul>

<br>

<%= form_with model: @user do |form| %>
  <%= form.label :name %><br>
  <%= form.text_field :name %>
  <%= form.submit %>
<% end %>
```

Copy

The `app/views/users/_user.html.erb` partial contains the following:

```
<li><%= user.name %></li>
```

Copy

The top portion of the index page displays the users. The bottom portion
provides a form to create a new user.

The bottom form will call the `create` action on the `UsersController`. Because
the form's remote option is set to true, the request will be posted to the
`UsersController` as an Ajax request, looking for JavaScript. In order to
serve that request, the `create` action of your controller would look like
this:

```
  # app/controllers/users_controller.rb
  # ......
  def create
    @user = User.new(params[:user])

    respond_to do |format|
      if @user.save
        format.html { redirect_to @user, notice: 'User was successfully created.' }
        format.js
        format.json { render json: @user, status: :created, location: @user }
      else
        format.html { render action: "new" }
        format.json { render json: @user.errors, status: :unprocessable_entity }
      end
    end
  end
```

Copy

Notice the `format.js` in the `respond_to` block: that allows the controller to
respond to your Ajax request. You then have a corresponding
`app/views/users/create.js.erb` view file that generates the actual JavaScript
code that will be sent and executed on the client side.

```
var users = document.querySelector("#users");
users.insertAdjacentHTML("beforeend", "<%= j render(@user) %>");
```

Copy

JavaScript view rendering doesn't do any preprocessing, so you shouldn't use ES6 syntax here.

### [5 Turbolinks](https://guides.rubyonrails.org/v6.1/working_with_javascript_in_rails.html\#turbolinks)

Rails ships with the [Turbolinks library](https://github.com/turbolinks/turbolinks),
which uses Ajax to speed up page rendering in most applications.

#### [5.1 How Turbolinks Works](https://guides.rubyonrails.org/v6.1/working_with_javascript_in_rails.html\#how-turbolinks-works)

Turbolinks attaches a click handler to all `<a>` tags on the page. If your browser
supports
[PushState](https://developer.mozilla.org/en-US/docs/Web/Guide/API/DOM/Manipulating_the_browser_history#The_pushState%28%29_method),
Turbolinks will make an Ajax request for the page, parse the response, and
replace the entire `<body>` of the page with the `<body>` of the response. It
will then use PushState to change the URL to the correct one, preserving
refresh semantics and giving you pretty URLs.

If you want to disable Turbolinks for certain links, add a `data-turbolinks="false"`
attribute to the tag:

```
<a href="..." data-turbolinks="false">No turbolinks here</a>.
```

Copy

#### [5.2 Page Change Events](https://guides.rubyonrails.org/v6.1/working_with_javascript_in_rails.html\#page-change-events)

You'll often want to do some sort of processing upon
page load. Using the DOM, you'd write something like this:

```
window.addEventListener("load", () => {
  alert("page has loaded!");
});
```

Copy

However, because Turbolinks overrides the normal page loading process, the
event that this relies upon will not be fired. If you have code that looks like
this, you must change your code to do this instead:

```
document.addEventListener("turbolinks:load", () => {
  alert("page has loaded!");
});
```

Copy

For more details, including other events you can bind to, check out [the\\
Turbolinks\\
README](https://github.com/turbolinks/turbolinks/blob/master/README.md).

### [6 Cross-Site Request Forgery (CSRF) token in Ajax](https://guides.rubyonrails.org/v6.1/working_with_javascript_in_rails.html\#cross-site-request-forgery-csrf-token-in-ajax)

When using another library to make Ajax calls, it is necessary to add
the security token as a default header for Ajax calls in your library. To get
the token:

```
const token = document.getElementsByName(
  "csrf-token"
)[0].content;
```

Copy

You can then submit this token as a `X-CSRF-Token` header for your
Ajax request. You do not need to add a CSRF token for GET requests,
only non-GET ones.

You can read more about about Cross-Site Request Forgery in the [Security guide](https://guides.rubyonrails.org/security.html#cross-site-request-forgery-csrf).

### [7 Other Resources](https://guides.rubyonrails.org/v6.1/working_with_javascript_in_rails.html\#other-resources)

Here are some helpful links to help you learn even more:

- [rails-ujs wiki](https://github.com/rails/rails/tree/main/actionview/app/assets/javascripts)
- [Railscasts: Unobtrusive JavaScript](http://railscasts.com/episodes/205-unobtrusive-javascript)
- [Railscasts: Turbolinks](http://railscasts.com/episodes/390-turbolinks)

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