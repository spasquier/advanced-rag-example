v6.1.7.10

**More at [rubyonrails.org:](https://rubyonrails.org/)**
More Ruby on Rails


- [Blog](https://rubyonrails.org/blog)
- [Guides](https://guides.rubyonrails.org/)
- [API](https://api.rubyonrails.org/)
- [Forum](https://discuss.rubyonrails.org/)
- [Contribute on GitHub](https://github.com/rails/rails)

* * *

## Action View Helpers

After reading this guide, you will know:

- How to format dates, strings and numbers
- How to link to images, videos, stylesheets, etc...
- How to sanitize content
- How to localize content

### ![](https://guides.rubyonrails.org/v6.1/images/chapters_icon.gif)Chapters

1. [Overview of helpers provided by Action View](https://guides.rubyonrails.org/v6.1/action_view_helpers.html#overview-of-helpers-provided-by-action-view)   - [AssetTagHelper](https://guides.rubyonrails.org/v6.1/action_view_helpers.html#assettaghelper)
   - [AtomFeedHelper](https://guides.rubyonrails.org/v6.1/action_view_helpers.html#atomfeedhelper)
   - [BenchmarkHelper](https://guides.rubyonrails.org/v6.1/action_view_helpers.html#benchmarkhelper)
   - [CacheHelper](https://guides.rubyonrails.org/v6.1/action_view_helpers.html#cachehelper)
   - [CaptureHelper](https://guides.rubyonrails.org/v6.1/action_view_helpers.html#capturehelper)
   - [DateHelper](https://guides.rubyonrails.org/v6.1/action_view_helpers.html#datehelper)
   - [DebugHelper](https://guides.rubyonrails.org/v6.1/action_view_helpers.html#debughelper)
   - [FormHelper](https://guides.rubyonrails.org/v6.1/action_view_helpers.html#formhelper)
   - [JavaScriptHelper](https://guides.rubyonrails.org/v6.1/action_view_helpers.html#javascripthelper)
   - [NumberHelper](https://guides.rubyonrails.org/v6.1/action_view_helpers.html#numberhelper)
   - [SanitizeHelper](https://guides.rubyonrails.org/v6.1/action_view_helpers.html#sanitizehelper)
   - [UrlHelper](https://guides.rubyonrails.org/v6.1/action_view_helpers.html#urlhelper)
   - [CsrfHelper](https://guides.rubyonrails.org/v6.1/action_view_helpers.html#csrfhelper)

### [1 Overview of helpers provided by Action View](https://guides.rubyonrails.org/v6.1/action_view_helpers.html\#overview-of-helpers-provided-by-action-view)

WIP: Not all the helpers are listed here. For a full list see the [API documentation](https://api.rubyonrails.org/v6.1.7.10/classes/ActionView/Helpers.html)

The following is only a brief overview summary of the helpers available in Action View. It's recommended that you review the [API Documentation](https://api.rubyonrails.org/v6.1.7.10/classes/ActionView/Helpers.html), which covers all of the helpers in more detail, but this should serve as a good starting point.

#### [1.1 AssetTagHelper](https://guides.rubyonrails.org/v6.1/action_view_helpers.html\#assettaghelper)

This module provides methods for generating HTML that links views to assets such as images, JavaScript files, stylesheets, and feeds.

By default, Rails links to these assets on the current host in the public folder, but you can direct Rails to link to assets from a dedicated assets server by setting `config.asset_host` in the application configuration, typically in `config/environments/production.rb`. For example, let's say your asset host is `assets.example.com`:

```
config.asset_host = "assets.example.com"
image_tag("rails.png")
# => <img src="http://assets.example.com/images/rails.png" />
```

Copy

##### [1.1.1 auto\_discovery\_link\_tag](https://guides.rubyonrails.org/v6.1/action_view_helpers.html\#auto-discovery-link-tag)

Returns a link tag that browsers and feed readers can use to auto-detect an RSS, Atom, or JSON feed.

```
auto_discovery_link_tag(:rss, "http://www.example.com/feed.rss", { title: "RSS Feed" })
# => <link rel="alternate" type="application/rss+xml" title="RSS Feed" href="http://www.example.com/feed.rss" />
```

Copy

##### [1.1.2 image\_path](https://guides.rubyonrails.org/v6.1/action_view_helpers.html\#image-path)

Computes the path to an image asset in the `app/assets/images` directory. Full paths from the document root will be passed through. Used internally by `image_tag` to build the image path.

```
image_path("edit.png") # => /assets/edit.png
```

Copy

Fingerprint will be added to the filename if config.assets.digest is set to true.

```
image_path("edit.png")
# => /assets/edit-2d1a2db63fc738690021fedb5a65b68e.png
```

Copy

##### [1.1.3 image\_url](https://guides.rubyonrails.org/v6.1/action_view_helpers.html\#image-url)

Computes the URL to an image asset in the `app/assets/images` directory. This will call `image_path` internally and merge with your current host or your asset host.

```
image_url("edit.png") # => http://www.example.com/assets/edit.png
```

Copy

##### [1.1.4 image\_tag](https://guides.rubyonrails.org/v6.1/action_view_helpers.html\#image-tag)

Returns an HTML image tag for the source. The source can be a full path or a file that exists in your `app/assets/images` directory.

```
image_tag("icon.png") # => <img src="/assets/icon.png" />
```

Copy

##### [1.1.5 javascript\_include\_tag](https://guides.rubyonrails.org/v6.1/action_view_helpers.html\#javascript-include-tag)

Returns an HTML script tag for each of the sources provided. You can pass in the filename (`.js` extension is optional) of JavaScript files that exist in your `app/assets/javascripts` directory for inclusion into the current page or you can pass the full path relative to your document root.

```
javascript_include_tag "common"
# => <script src="/assets/common.js"></script>
```

Copy

##### [1.1.6 javascript\_path](https://guides.rubyonrails.org/v6.1/action_view_helpers.html\#javascript-path)

Computes the path to a JavaScript asset in the `app/assets/javascripts` directory. If the source filename has no extension, `.js` will be appended. Full paths from the document root will be passed through. Used internally by `javascript_include_tag` to build the script path.

```
javascript_path "common" # => /assets/common.js
```

Copy

##### [1.1.7 javascript\_url](https://guides.rubyonrails.org/v6.1/action_view_helpers.html\#javascript-url)

Computes the URL to a JavaScript asset in the `app/assets/javascripts` directory. This will call `javascript_path` internally and merge with your current host or your asset host.

```
javascript_url "common"
# => http://www.example.com/assets/common.js
```

Copy

##### [1.1.8 stylesheet\_link\_tag](https://guides.rubyonrails.org/v6.1/action_view_helpers.html\#stylesheet-link-tag)

Returns a stylesheet link tag for the sources specified as arguments. If you don't specify an extension, `.css` will be appended automatically.

```
stylesheet_link_tag "application"
# => <link href="/assets/application.css" media="screen" rel="stylesheet" />
```

Copy

##### [1.1.9 stylesheet\_path](https://guides.rubyonrails.org/v6.1/action_view_helpers.html\#stylesheet-path)

Computes the path to a stylesheet asset in the `app/assets/stylesheets` directory. If the source filename has no extension, `.css` will be appended. Full paths from the document root will be passed through. Used internally by `stylesheet_link_tag` to build the stylesheet path.

```
stylesheet_path "application" # => /assets/application.css
```

Copy

##### [1.1.10 stylesheet\_url](https://guides.rubyonrails.org/v6.1/action_view_helpers.html\#stylesheet-url)

Computes the URL to a stylesheet asset in the `app/assets/stylesheets` directory. This will call `stylesheet_path` internally and merge with your current host or your asset host.

```
stylesheet_url "application"
# => http://www.example.com/assets/application.css
```

Copy

#### [1.2 AtomFeedHelper](https://guides.rubyonrails.org/v6.1/action_view_helpers.html\#atomfeedhelper)

##### [1.2.1 atom\_feed](https://guides.rubyonrails.org/v6.1/action_view_helpers.html\#atom-feed)

This helper makes building an Atom feed easy. Here's a full usage example:

**config/routes.rb**

```
resources :articles
```

Copy

**app/controllers/articles\_controller.rb**

```
def index
  @articles = Article.all

  respond_to do |format|
    format.html
    format.atom
  end
end
```

Copy

**app/views/articles/index.atom.builder**

```
atom_feed do |feed|
  feed.title("Articles Index")
  feed.updated(@articles.first.created_at)

  @articles.each do |article|
    feed.entry(article) do |entry|
      entry.title(article.title)
      entry.content(article.body, type: 'html')

      entry.author do |author|
        author.name(article.author_name)
      end
    end
  end
end
```

Copy

#### [1.3 BenchmarkHelper](https://guides.rubyonrails.org/v6.1/action_view_helpers.html\#benchmarkhelper)

##### [1.3.1 benchmark](https://guides.rubyonrails.org/v6.1/action_view_helpers.html\#benchmark)

Allows you to measure the execution time of a block in a template and records the result to the log. Wrap this block around expensive operations or possible bottlenecks to get a time reading for the operation.

```
<% benchmark "Process data files" do %>
  <%= expensive_files_operation %>
<% end %>
```

Copy

This would add something like "Process data files (0.34523)" to the log, which you can then use to compare timings when optimizing your code.

#### [1.4 CacheHelper](https://guides.rubyonrails.org/v6.1/action_view_helpers.html\#cachehelper)

##### [1.4.1 cache](https://guides.rubyonrails.org/v6.1/action_view_helpers.html\#cache)

A method for caching fragments of a view rather than an entire action or page. This technique is useful for caching pieces like menus, lists of news topics, static HTML fragments, and so on. This method takes a block that contains the content you wish to cache. See `AbstractController::Caching::Fragments` for more information.

```
<% cache do %>
  <%= render "shared/footer" %>
<% end %>
```

Copy

#### [1.5 CaptureHelper](https://guides.rubyonrails.org/v6.1/action_view_helpers.html\#capturehelper)

##### [1.5.1 capture](https://guides.rubyonrails.org/v6.1/action_view_helpers.html\#capture)

The `capture` method allows you to extract part of a template into a variable. You can then use this variable anywhere in your templates or layout.

```
<% @greeting = capture do %>
  <p>Welcome! The date and time is <%= Time.now %></p>
<% end %>
```

Copy

The captured variable can then be used anywhere else.

```
<html>
  <head>
    <title>Welcome!</title>
  </head>
  <body>
    <%= @greeting %>
  </body>
</html>
```

Copy

##### [1.5.2 content\_for](https://guides.rubyonrails.org/v6.1/action_view_helpers.html\#content-for)

Calling `content_for` stores a block of markup in an identifier for later use. You can make subsequent calls to the stored content in other templates or the layout by passing the identifier as an argument to `yield`.

For example, let's say we have a standard application layout, but also a special page that requires certain JavaScript that the rest of the site doesn't need. We can use `content_for` to include this JavaScript on our special page without fattening up the rest of the site.

**app/views/layouts/application.html.erb**

```
<html>
  <head>
    <title>Welcome!</title>
    <%= yield :special_script %>
  </head>
  <body>
    <p>Welcome! The date and time is <%= Time.now %></p>
  </body>
</html>
```

Copy

**app/views/articles/special.html.erb**

```
<p>This is a special page.</p>

<% content_for :special_script do %>
  <script>alert('Hello!')</script>
<% end %>
```

Copy

#### [1.6 DateHelper](https://guides.rubyonrails.org/v6.1/action_view_helpers.html\#datehelper)

##### [1.6.1 distance\_of\_time\_in\_words](https://guides.rubyonrails.org/v6.1/action_view_helpers.html\#distance-of-time-in-words)

Reports the approximate distance in time between two Time or Date objects or integers as seconds. Set `include_seconds` to true if you want more detailed approximations.

```
distance_of_time_in_words(Time.now, Time.now + 15.seconds)
# => less than a minute
distance_of_time_in_words(Time.now, Time.now + 15.seconds, include_seconds: true)
# => less than 20 seconds
```

Copy

##### [1.6.2 time\_ago\_in\_words](https://guides.rubyonrails.org/v6.1/action_view_helpers.html\#time-ago-in-words)

Like `distance_of_time_in_words`, but where `to_time` is fixed to `Time.now`.

```
time_ago_in_words(3.minutes.from_now) # => 3 minutes
```

Copy

#### [1.7 DebugHelper](https://guides.rubyonrails.org/v6.1/action_view_helpers.html\#debughelper)

Returns a `pre` tag that has object dumped by YAML. This creates a very readable way to inspect an object.

```
my_hash = { 'first' => 1, 'second' => 'two', 'third' => [1,2,3] }
debug(my_hash)
```

Copy

```
<pre class='debug_dump'>---
first: 1
second: two
third:
- 1
- 2
- 3
</pre>
```

Copy

#### [1.8 FormHelper](https://guides.rubyonrails.org/v6.1/action_view_helpers.html\#formhelper)

Form helpers are designed to make working with models much easier compared to using just standard HTML elements by providing a set of methods for creating forms based on your models. This helper generates the HTML for forms, providing a method for each sort of input (e.g., text, password, select, and so on). When the form is submitted (i.e., when the user hits the submit button or form.submit is called via JavaScript), the form inputs will be bundled into the params object and passed back to the controller.

You can learn more about form helpers in the [Action View Form Helpers\\
Guide](https://guides.rubyonrails.org/v6.1/form_helpers.html).

#### [1.9 JavaScriptHelper](https://guides.rubyonrails.org/v6.1/action_view_helpers.html\#javascripthelper)

Provides functionality for working with JavaScript in your views.

##### [1.9.1 escape\_javascript](https://guides.rubyonrails.org/v6.1/action_view_helpers.html\#escape-javascript)

Escape carrier returns and single and double quotes for JavaScript segments.

##### [1.9.2 javascript\_tag](https://guides.rubyonrails.org/v6.1/action_view_helpers.html\#javascript-tag)

Returns a JavaScript tag wrapping the provided code.

```
javascript_tag "alert('All is good')"
```

Copy

```
<script>
//<![CDATA[\
alert('All is good')\
//]]>
</script>
```

Copy

#### [1.10 NumberHelper](https://guides.rubyonrails.org/v6.1/action_view_helpers.html\#numberhelper)

Provides methods for converting numbers into formatted strings. Methods are provided for phone numbers, currency, percentage, precision, positional notation, and file size.

##### [1.10.1 number\_to\_currency](https://guides.rubyonrails.org/v6.1/action_view_helpers.html\#number-to-currency)

Formats a number into a currency string (e.g., $13.65).

```
number_to_currency(1234567890.50) # => $1,234,567,890.50
```

Copy

##### [1.10.2 number\_to\_human\_size](https://guides.rubyonrails.org/v6.1/action_view_helpers.html\#number-to-human-size)

Formats the bytes in size into a more understandable representation; useful for reporting file sizes to users.

```
number_to_human_size(1234)    # => 1.2 KB
number_to_human_size(1234567) # => 1.2 MB
```

Copy

##### [1.10.3 number\_to\_percentage](https://guides.rubyonrails.org/v6.1/action_view_helpers.html\#number-to-percentage)

Formats a number as a percentage string.

```
number_to_percentage(100, precision: 0) # => 100%
```

Copy

##### [1.10.4 number\_to\_phone](https://guides.rubyonrails.org/v6.1/action_view_helpers.html\#number-to-phone)

Formats a number into a phone number (US by default).

```
number_to_phone(1235551234) # => 123-555-1234
```

Copy

##### [1.10.5 number\_with\_delimiter](https://guides.rubyonrails.org/v6.1/action_view_helpers.html\#number-with-delimiter)

Formats a number with grouped thousands using a delimiter.

```
number_with_delimiter(12345678) # => 12,345,678
```

Copy

##### [1.10.6 number\_with\_precision](https://guides.rubyonrails.org/v6.1/action_view_helpers.html\#number-with-precision)

Formats a number with the specified level of `precision`, which defaults to 3.

```
number_with_precision(111.2345)               # => 111.235
number_with_precision(111.2345, precision: 2) # => 111.23
```

Copy

#### [1.11 SanitizeHelper](https://guides.rubyonrails.org/v6.1/action_view_helpers.html\#sanitizehelper)

The SanitizeHelper module provides a set of methods for scrubbing text of undesired HTML elements.

##### [1.11.1 sanitize](https://guides.rubyonrails.org/v6.1/action_view_helpers.html\#sanitize)

This sanitize helper will HTML encode all tags and strip all attributes that aren't specifically allowed.

```
sanitize @article.body
```

Copy

If either the `:attributes` or `:tags` options are passed, only the mentioned attributes and tags are allowed and nothing else.

```
sanitize @article.body, tags: %w(table tr td), attributes: %w(id class style)
```

Copy

To change defaults for multiple uses, for example adding table tags to the default:

```
class Application < Rails::Application
  config.action_view.sanitized_allowed_tags = 'table', 'tr', 'td'
end
```

Copy

##### [1.11.2 sanitize\_css(style)](https://guides.rubyonrails.org/v6.1/action_view_helpers.html\#sanitize-css-style)

Sanitizes a block of CSS code.

##### [1.11.3 strip\_links(html)](https://guides.rubyonrails.org/v6.1/action_view_helpers.html\#strip-links-html)

Strips all link tags from text leaving just the link text.

```
strip_links('<a href="https://rubyonrails.org">Ruby on Rails</a>')
# => Ruby on Rails
```

Copy

```
strip_links('emails to <a href="mailto:me@email.com">me@email.com</a>.')
# => emails to me@email.com.
```

Copy

```
strip_links('Blog: <a href="http://myblog.com/">Visit</a>.')
# => Blog: Visit.
```

Copy

##### [1.11.4 strip\_tags(html)](https://guides.rubyonrails.org/v6.1/action_view_helpers.html\#strip-tags-html)

Strips all HTML tags from the html, including comments.
This functionality is powered by the rails-html-sanitizer gem.

```
strip_tags("Strip <i>these</i> tags!")
# => Strip these tags!
```

Copy

```
strip_tags("<b>Bold</b> no more!  <a href='more.html'>See more</a>")
# => Bold no more!  See more
```

Copy

NB: The output may still contain unescaped '<', '>', '&' characters and confuse browsers.

#### [1.12 UrlHelper](https://guides.rubyonrails.org/v6.1/action_view_helpers.html\#urlhelper)

Provides methods to make links and get URLs that depend on the routing subsystem.

##### [1.12.1 url\_for](https://guides.rubyonrails.org/v6.1/action_view_helpers.html\#url-for)

Returns the URL for the set of `options` provided.

###### [1.12.1.1 Examples](https://guides.rubyonrails.org/v6.1/action_view_helpers.html\#url-for-examples)

```
url_for @profile
# => /profiles/1

url_for [ @hotel, @booking, page: 2, line: 3 ]
# => /hotels/1/bookings/1?line=3&page=2
```

Copy

##### [1.12.2 link\_to](https://guides.rubyonrails.org/v6.1/action_view_helpers.html\#link-to)

Links to a URL derived from `url_for` under the hood. Primarily used to
create RESTful resource links, which for this example, boils down to
when passing models to `link_to`.

**Examples**

```
link_to "Profile", @profile
# => <a href="/profiles/1">Profile</a>
```

Copy

You can use a block as well if your link target can't fit in the name parameter. ERB example:

```
<%= link_to @profile do %>
  <strong><%= @profile.name %></strong> -- <span>Check it out!</span>
<% end %>
```

Copy

would output:

```
<a href="/profiles/1">
  <strong>David</strong> -- <span>Check it out!</span>
</a>
```

Copy

See [the API Documentation for more information](https://api.rubyonrails.org/v6.1.7.10/classes/ActionView/Helpers/UrlHelper.html#method-i-link_to)

##### [1.12.3 button\_to](https://guides.rubyonrails.org/v6.1/action_view_helpers.html\#button-to)

Generates a form that submits to the passed URL. The form has a submit button
with the value of the `name`.

###### [1.12.3.1 Examples](https://guides.rubyonrails.org/v6.1/action_view_helpers.html\#button-to-examples)

```
<%= button_to "Sign in", sign_in_path %>
```

Copy

would roughly output something like:

```
<form method="post" action="/sessions" class="button_to">
  <input type="submit" value="Sign in" />
</form>
```

Copy

See [the API Documentation for more information](https://api.rubyonrails.org/v6.1.7.10/classes/ActionView/Helpers/UrlHelper.html#method-i-button_to)

#### [1.13 CsrfHelper](https://guides.rubyonrails.org/v6.1/action_view_helpers.html\#csrfhelper)

Returns meta tags "csrf-param" and "csrf-token" with the name of the cross-site
request forgery protection parameter and token, respectively.

```
<%= csrf_meta_tags %>
```

Copy

Regular forms generate hidden fields so they do not use these tags. More
details can be found in the [Rails Security Guide](https://guides.rubyonrails.org/v6.1/security.html#cross-site-request-forgery-csrf).

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