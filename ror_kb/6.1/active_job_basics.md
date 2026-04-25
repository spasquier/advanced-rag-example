v6.1.7.10

**More at [rubyonrails.org:](https://rubyonrails.org/)**
More Ruby on Rails


- [Blog](https://rubyonrails.org/blog)
- [Guides](https://guides.rubyonrails.org/)
- [API](https://api.rubyonrails.org/)
- [Forum](https://discuss.rubyonrails.org/)
- [Contribute on GitHub](https://github.com/rails/rails)

* * *

## Active Job Basics

This guide provides you with all you need to get started in creating,
enqueuing and executing background jobs.

After reading this guide, you will know:

- How to create jobs.
- How to enqueue jobs.
- How to run jobs in the background.
- How to send emails from your application asynchronously.

### ![](https://guides.rubyonrails.org/v6.1/images/chapters_icon.gif)Chapters

01. [What is Active Job?](https://guides.rubyonrails.org/v6.1/active_job_basics.html#what-is-active-job-questionmark)
02. [The Purpose of Active Job](https://guides.rubyonrails.org/v6.1/active_job_basics.html#the-purpose-of-active-job)
03. [Creating a Job](https://guides.rubyonrails.org/v6.1/active_job_basics.html#creating-a-job)    - [Create the Job](https://guides.rubyonrails.org/v6.1/active_job_basics.html#create-the-job)
    - [Enqueue the Job](https://guides.rubyonrails.org/v6.1/active_job_basics.html#enqueue-the-job)
04. [Job Execution](https://guides.rubyonrails.org/v6.1/active_job_basics.html#job-execution)    - [Backends](https://guides.rubyonrails.org/v6.1/active_job_basics.html#backends)
    - [Setting the Backend](https://guides.rubyonrails.org/v6.1/active_job_basics.html#setting-the-backend)
    - [Starting the Backend](https://guides.rubyonrails.org/v6.1/active_job_basics.html#starting-the-backend)
05. [Queues](https://guides.rubyonrails.org/v6.1/active_job_basics.html#queues)
06. [Callbacks](https://guides.rubyonrails.org/v6.1/active_job_basics.html#callbacks)    - [Available callbacks](https://guides.rubyonrails.org/v6.1/active_job_basics.html#available-callbacks)
07. [Action Mailer](https://guides.rubyonrails.org/v6.1/active_job_basics.html#action-mailer)
08. [Internationalization](https://guides.rubyonrails.org/v6.1/active_job_basics.html#internationalization)
09. [Supported types for arguments](https://guides.rubyonrails.org/v6.1/active_job_basics.html#supported-types-for-arguments)    - [GlobalID](https://guides.rubyonrails.org/v6.1/active_job_basics.html#globalid)
    - [Serializers](https://guides.rubyonrails.org/v6.1/active_job_basics.html#serializers)
10. [Exceptions](https://guides.rubyonrails.org/v6.1/active_job_basics.html#exceptions)    - [Retrying or Discarding failed jobs](https://guides.rubyonrails.org/v6.1/active_job_basics.html#retrying-or-discarding-failed-jobs)
    - [Deserialization](https://guides.rubyonrails.org/v6.1/active_job_basics.html#deserialization)
11. [Job Testing](https://guides.rubyonrails.org/v6.1/active_job_basics.html#job-testing)

### [1 What is Active Job?](https://guides.rubyonrails.org/v6.1/active_job_basics.html\#what-is-active-job-questionmark)

Active Job is a framework for declaring jobs and making them run on a variety
of queuing backends. These jobs can be everything from regularly scheduled
clean-ups, to billing charges, to mailings. Anything that can be chopped up
into small units of work and run in parallel, really.

### [2 The Purpose of Active Job](https://guides.rubyonrails.org/v6.1/active_job_basics.html\#the-purpose-of-active-job)

The main point is to ensure that all Rails apps will have a job infrastructure
in place. We can then have framework features and other gems build on top of that,
without having to worry about API differences between various job runners such as
Delayed Job and Resque. Picking your queuing backend becomes more of an operational
concern, then. And you'll be able to switch between them without having to rewrite
your jobs.

Rails by default comes with an asynchronous queuing implementation that
runs jobs with an in-process thread pool. Jobs will run asynchronously, but any
jobs in the queue will be dropped upon restart.

### [3 Creating a Job](https://guides.rubyonrails.org/v6.1/active_job_basics.html\#creating-a-job)

This section will provide a step-by-step guide to creating a job and enqueuing it.

#### [3.1 Create the Job](https://guides.rubyonrails.org/v6.1/active_job_basics.html\#create-the-job)

Active Job provides a Rails generator to create jobs. The following will create a
job in `app/jobs` (with an attached test case under `test/jobs`):

```
$ bin/rails generate job guests_cleanup
invoke  test_unit
create    test/jobs/guests_cleanup_job_test.rb
create  app/jobs/guests_cleanup_job.rb
```

Copy

You can also create a job that will run on a specific queue:

```
$ bin/rails generate job guests_cleanup --queue urgent
```

Copy

If you don't want to use a generator, you could create your own file inside of
`app/jobs`, just make sure that it inherits from `ApplicationJob`.

Here's what a job looks like:

```
class GuestsCleanupJob < ApplicationJob
  queue_as :default

  def perform(*guests)
    # Do something later
  end
end
```

Copy

Note that you can define `perform` with as many arguments as you want.

#### [3.2 Enqueue the Job](https://guides.rubyonrails.org/v6.1/active_job_basics.html\#enqueue-the-job)

Enqueue a job like so:

```
# Enqueue a job to be performed as soon as the queuing system is
# free.
GuestsCleanupJob.perform_later guest
```

Copy

```
# Enqueue a job to be performed tomorrow at noon.
GuestsCleanupJob.set(wait_until: Date.tomorrow.noon).perform_later(guest)
```

Copy

```
# Enqueue a job to be performed 1 week from now.
GuestsCleanupJob.set(wait: 1.week).perform_later(guest)
```

Copy

```
# `perform_now` and `perform_later` will call `perform` under the hood so
# you can pass as many arguments as defined in the latter.
GuestsCleanupJob.perform_later(guest1, guest2, filter: 'some_filter')
```

Copy

That's it!

### [4 Job Execution](https://guides.rubyonrails.org/v6.1/active_job_basics.html\#job-execution)

For enqueuing and executing jobs in production you need to set up a queuing backend,
that is to say you need to decide on a 3rd-party queuing library that Rails should use.
Rails itself only provides an in-process queuing system, which only keeps the jobs in RAM.
If the process crashes or the machine is reset, then all outstanding jobs are lost with the
default async backend. This may be fine for smaller apps or non-critical jobs, but most
production apps will need to pick a persistent backend.

#### [4.1 Backends](https://guides.rubyonrails.org/v6.1/active_job_basics.html\#backends)

Active Job has built-in adapters for multiple queuing backends (Sidekiq,
Resque, Delayed Job, and others). To get an up-to-date list of the adapters
see the API Documentation for [ActiveJob::QueueAdapters](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveJob/QueueAdapters.html).

#### [4.2 Setting the Backend](https://guides.rubyonrails.org/v6.1/active_job_basics.html\#setting-the-backend)

You can easily set your queuing backend:

```
# config/application.rb
module YourApp
  class Application < Rails::Application
    # Be sure to have the adapter's gem in your Gemfile
    # and follow the adapter's specific installation
    # and deployment instructions.
    config.active_job.queue_adapter = :sidekiq
  end
end
```

Copy

You can also configure your backend on a per job basis:

```
class GuestsCleanupJob < ApplicationJob
  self.queue_adapter = :resque
  # ...
end

# Now your job will use `resque` as its backend queue adapter, overriding what
# was configured in `config.active_job.queue_adapter`.
```

Copy

#### [4.3 Starting the Backend](https://guides.rubyonrails.org/v6.1/active_job_basics.html\#starting-the-backend)

Since jobs run in parallel to your Rails application, most queuing libraries
require that you start a library-specific queuing service (in addition to
starting your Rails app) for the job processing to work. Refer to library
documentation for instructions on starting your queue backend.

Here is a noncomprehensive list of documentation:

- [Sidekiq](https://github.com/mperham/sidekiq/wiki/Active-Job)
- [Resque](https://github.com/resque/resque/wiki/ActiveJob)
- [Sneakers](https://github.com/jondot/sneakers/wiki/How-To:-Rails-Background-Jobs-with-ActiveJob)
- [Sucker Punch](https://github.com/brandonhilkert/sucker_punch#active-job)
- [Queue Classic](https://github.com/QueueClassic/queue_classic#active-job)
- [Delayed Job](https://github.com/collectiveidea/delayed_job#active-job)
- [Que](https://github.com/que-rb/que#additional-rails-specific-setup)

### [5 Queues](https://guides.rubyonrails.org/v6.1/active_job_basics.html\#queues)

Most of the adapters support multiple queues. With Active Job you can schedule
the job to run on a specific queue:

```
class GuestsCleanupJob < ApplicationJob
  queue_as :low_priority
  # ...
end
```

Copy

You can prefix the queue name for all your jobs using
`config.active_job.queue_name_prefix` in `application.rb`:

```
# config/application.rb
module YourApp
  class Application < Rails::Application
    config.active_job.queue_name_prefix = Rails.env
  end
end
```

Copy

```
# app/jobs/guests_cleanup_job.rb
class GuestsCleanupJob < ApplicationJob
  queue_as :low_priority
  # ...
end

# Now your job will run on queue production_low_priority on your
# production environment and on staging_low_priority
# on your staging environment
```

Copy

You can also configure the prefix on a per job basis.

```
class GuestsCleanupJob < ApplicationJob
  queue_as :low_priority
  self.queue_name_prefix = nil
  # ...
end

# Now your job's queue won't be prefixed, overriding what
# was configured in `config.active_job.queue_name_prefix`.
```

Copy

The default queue name prefix delimiter is '\_'. This can be changed by setting
`config.active_job.queue_name_delimiter` in `application.rb`:

```
# config/application.rb
module YourApp
  class Application < Rails::Application
    config.active_job.queue_name_prefix = Rails.env
    config.active_job.queue_name_delimiter = '.'
  end
end
```

Copy

```
# app/jobs/guests_cleanup_job.rb
class GuestsCleanupJob < ApplicationJob
  queue_as :low_priority
  # ...
end

# Now your job will run on queue production.low_priority on your
# production environment and on staging.low_priority
# on your staging environment
```

Copy

If you want more control on what queue a job will be run you can pass a `:queue`
option to `set`:

```
MyJob.set(queue: :another_queue).perform_later(record)
```

Copy

To control the queue from the job level you can pass a block to `queue_as`. The
block will be executed in the job context (so it can access `self.arguments`),
and it must return the queue name:

```
class ProcessVideoJob < ApplicationJob
  queue_as do
    video = self.arguments.first
    if video.owner.premium?
      :premium_videojobs
    else
      :videojobs
    end
  end

  def perform(video)
    # Do process video
  end
end
```

Copy

```
ProcessVideoJob.perform_later(Video.last)
```

Copy

Make sure your queuing backend "listens" on your queue name. For some
backends you need to specify the queues to listen to.

### [6 Callbacks](https://guides.rubyonrails.org/v6.1/active_job_basics.html\#callbacks)

Active Job provides hooks to trigger logic during the life cycle of a job. Like
other callbacks in Rails, you can implement the callbacks as ordinary methods
and use a macro-style class method to register them as callbacks:

```
class GuestsCleanupJob < ApplicationJob
  queue_as :default

  around_perform :around_cleanup

  def perform
    # Do something later
  end

  private
    def around_cleanup
      # Do something before perform
      yield
      # Do something after perform
    end
end
```

Copy

The macro-style class methods can also receive a block. Consider using this
style if the code inside your block is so short that it fits in a single line.
For example, you could send metrics for every job enqueued:

```
class ApplicationJob < ActiveJob::Base
  before_enqueue { |job| $statsd.increment "#{job.class.name.underscore}.enqueue" }
end
```

Copy

#### [6.1 Available callbacks](https://guides.rubyonrails.org/v6.1/active_job_basics.html\#available-callbacks)

- `before_enqueue`
- `around_enqueue`
- `after_enqueue`
- `before_perform`
- `around_perform`
- `after_perform`

### [7 Action Mailer](https://guides.rubyonrails.org/v6.1/active_job_basics.html\#action-mailer)

One of the most common jobs in a modern web application is sending emails outside
of the request-response cycle, so the user doesn't have to wait on it. Active Job
is integrated with Action Mailer so you can easily send emails asynchronously:

```
# If you want to send the email now use #deliver_now
UserMailer.welcome(@user).deliver_now

# If you want to send the email through Active Job use #deliver_later
UserMailer.welcome(@user).deliver_later
```

Copy

Using the asynchronous queue from a Rake task (for example, to
send an email using `.deliver_later`) will generally not work because Rake will
likely end, causing the in-process thread pool to be deleted, before any/all
of the `.deliver_later` emails are processed. To avoid this problem, use
`.deliver_now` or run a persistent queue in development.

### [8 Internationalization](https://guides.rubyonrails.org/v6.1/active_job_basics.html\#internationalization)

Each job uses the `I18n.locale` set when the job was created. This is useful if you send
emails asynchronously:

```
I18n.locale = :eo

UserMailer.welcome(@user).deliver_later # Email will be localized to Esperanto.
```

Copy

### [9 Supported types for arguments](https://guides.rubyonrails.org/v6.1/active_job_basics.html\#supported-types-for-arguments)

ActiveJob supports the following types of arguments by default:

- Basic types (`NilClass`, `String`, `Integer`, `Float`, `BigDecimal`, `TrueClass`, `FalseClass`)
- `Symbol`
- `Date`
- `Time`
- `DateTime`
- `ActiveSupport::TimeWithZone`
- `ActiveSupport::Duration`
- `Hash` (Keys should be of `String` or `Symbol` type)
- `ActiveSupport::HashWithIndifferentAccess`
- `Array`
- `Module`
- `Class`

#### [9.1 GlobalID](https://guides.rubyonrails.org/v6.1/active_job_basics.html\#globalid)

Active Job supports [GlobalID](https://github.com/rails/globalid/blob/master/README.md) for parameters. This makes it possible to pass live
Active Record objects to your job instead of class/id pairs, which you then have
to manually deserialize. Before, jobs would look like this:

```
class TrashableCleanupJob < ApplicationJob
  def perform(trashable_class, trashable_id, depth)
    trashable = trashable_class.constantize.find(trashable_id)
    trashable.cleanup(depth)
  end
end
```

Copy

Now you can simply do:

```
class TrashableCleanupJob < ApplicationJob
  def perform(trashable, depth)
    trashable.cleanup(depth)
  end
end
```

Copy

This works with any class that mixes in `GlobalID::Identification`, which
by default has been mixed into Active Record classes.

#### [9.2 Serializers](https://guides.rubyonrails.org/v6.1/active_job_basics.html\#serializers)

You can extend the list of supported argument types. You just need to define your own serializer:

```
class MoneySerializer < ActiveJob::Serializers::ObjectSerializer
  # Checks if an argument should be serialized by this serializer.
  def serialize?(argument)
    argument.is_a? Money
  end

  # Converts an object to a simpler representative using supported object types.
  # The recommended representative is a Hash with a specific key. Keys can be of basic types only.
  # You should call `super` to add the custom serializer type to the hash.
  def serialize(money)
    super(
      "amount" => money.amount,
      "currency" => money.currency
    )
  end

  # Converts serialized value into a proper object.
  def deserialize(hash)
    Money.new(hash["amount"], hash["currency"])
  end
end
```

Copy

and add this serializer to the list:

```
Rails.application.config.active_job.custom_serializers << MoneySerializer
```

Copy

### [10 Exceptions](https://guides.rubyonrails.org/v6.1/active_job_basics.html\#exceptions)

Active Job provides a way to catch exceptions raised during the execution of the
job:

```
class GuestsCleanupJob < ApplicationJob
  queue_as :default

  rescue_from(ActiveRecord::RecordNotFound) do |exception|
    # Do something with the exception
  end

  def perform
    # Do something later
  end
end
```

Copy

If an exception from a job is not rescued, then the job is referred to as "failed".

#### [10.1 Retrying or Discarding failed jobs](https://guides.rubyonrails.org/v6.1/active_job_basics.html\#retrying-or-discarding-failed-jobs)

A failed job will not be retried, unless configured otherwise.

It's also possible to retry or discard a job if an exception is raised during execution.
For example:

```
class RemoteServiceJob < ApplicationJob
  retry_on CustomAppException # defaults to 3s wait, 5 attempts

  discard_on ActiveJob::DeserializationError

  def perform(*args)
    # Might raise CustomAppException or ActiveJob::DeserializationError
  end
end
```

Copy

To get more details see the API Documentation for [ActiveJob::Exceptions](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveJob/Exceptions/ClassMethods.html).

#### [10.2 Deserialization](https://guides.rubyonrails.org/v6.1/active_job_basics.html\#deserialization)

GlobalID allows serializing full Active Record objects passed to `#perform`.

If a passed record is deleted after the job is enqueued but before the `#perform`
method is called Active Job will raise an `ActiveJob::DeserializationError`
exception.

### [11 Job Testing](https://guides.rubyonrails.org/v6.1/active_job_basics.html\#job-testing)

You can find detailed instructions on how to test your jobs in the
[testing guide](https://guides.rubyonrails.org/v6.1/testing.html#testing-jobs).

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