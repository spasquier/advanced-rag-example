v6.1.7.10

**More at [rubyonrails.org:](https://rubyonrails.org/)**
More Ruby on Rails


- [Blog](https://rubyonrails.org/blog)
- [Guides](https://guides.rubyonrails.org/)
- [API](https://api.rubyonrails.org/)
- [Forum](https://discuss.rubyonrails.org/)
- [Contribute on GitHub](https://github.com/rails/rails)

* * *

## Action Mailbox Basics

This guide provides you with all you need to get started in receiving
emails to your application.

After reading this guide, you will know:

- How to receive email within a Rails application.
- How to configure Action Mailbox.
- How to generate and route emails to a mailbox.
- How to test incoming emails.

### ![](https://guides.rubyonrails.org/v6.1/images/chapters_icon.gif)Chapters

1. [What is Action Mailbox?](https://guides.rubyonrails.org/v6.1/action_mailbox_basics.html#what-is-action-mailbox-questionmark)
2. [Setup](https://guides.rubyonrails.org/v6.1/action_mailbox_basics.html#setup)
3. [Configuration](https://guides.rubyonrails.org/v6.1/action_mailbox_basics.html#configuration)   - [Exim](https://guides.rubyonrails.org/v6.1/action_mailbox_basics.html#exim)
   - [Mailgun](https://guides.rubyonrails.org/v6.1/action_mailbox_basics.html#mailgun)
   - [Mandrill](https://guides.rubyonrails.org/v6.1/action_mailbox_basics.html#mandrill)
   - [Postfix](https://guides.rubyonrails.org/v6.1/action_mailbox_basics.html#postfix)
   - [Postmark](https://guides.rubyonrails.org/v6.1/action_mailbox_basics.html#postmark)
   - [Qmail](https://guides.rubyonrails.org/v6.1/action_mailbox_basics.html#qmail)
   - [SendGrid](https://guides.rubyonrails.org/v6.1/action_mailbox_basics.html#sendgrid)
4. [Examples](https://guides.rubyonrails.org/v6.1/action_mailbox_basics.html#examples)
5. [Incineration of InboundEmails](https://guides.rubyonrails.org/v6.1/action_mailbox_basics.html#incineration-of-inboundemails)
6. [Working with Action Mailbox in development](https://guides.rubyonrails.org/v6.1/action_mailbox_basics.html#working-with-action-mailbox-in-development)
7. [Testing mailboxes](https://guides.rubyonrails.org/v6.1/action_mailbox_basics.html#testing-mailboxes)

### [1 What is Action Mailbox?](https://guides.rubyonrails.org/v6.1/action_mailbox_basics.html\#what-is-action-mailbox-questionmark)

Action Mailbox routes incoming emails to controller-like mailboxes for
processing in Rails. It ships with ingresses for Mailgun, Mandrill, Postmark,
and SendGrid. You can also handle inbound mails directly via the built-in Exim,
Postfix, and Qmail ingresses.

The inbound emails are turned into `InboundEmail` records using Active Record
and feature lifecycle tracking, storage of the original email on cloud storage
via Active Storage, and responsible data handling with
on-by-default incineration.

These inbound emails are routed asynchronously using Active Job to one or
several dedicated mailboxes, which are capable of interacting directly
with the rest of your domain model.

### [2 Setup](https://guides.rubyonrails.org/v6.1/action_mailbox_basics.html\#setup)

Install migrations needed for `InboundEmail` and ensure Active Storage is set up:

```
$ bin/rails action_mailbox:install
$ bin/rails db:migrate
```

Copy

### [3 Configuration](https://guides.rubyonrails.org/v6.1/action_mailbox_basics.html\#configuration)

#### [3.1 Exim](https://guides.rubyonrails.org/v6.1/action_mailbox_basics.html\#exim)

Tell Action Mailbox to accept emails from an SMTP relay:

```
# config/environments/production.rb
config.action_mailbox.ingress = :relay
```

Copy

Generate a strong password that Action Mailbox can use to authenticate requests to the relay ingress.

Use `bin/rails credentials:edit` to add the password to your application's encrypted credentials under
`action_mailbox.ingress_password`, where Action Mailbox will automatically find it:

```
action_mailbox:
  ingress_password: ...
```

Copy

Alternatively, provide the password in the `RAILS_INBOUND_EMAIL_PASSWORD` environment variable.

Configure Exim to pipe inbound emails to `bin/rails action_mailbox:ingress:exim`,
providing the `URL` of the relay ingress and the `INGRESS_PASSWORD` you
previously generated. If your application lived at `https://example.com`, the
full command would look like this:

```
$ bin/rails action_mailbox:ingress:exim URL=https://example.com/rails/action_mailbox/relay/inbound_emails INGRESS_PASSWORD=...
```

Copy

#### [3.2 Mailgun](https://guides.rubyonrails.org/v6.1/action_mailbox_basics.html\#mailgun)

Give Action Mailbox your
Mailgun Signing key (which you can find under Settings -> Security & Users -> API security in Mailgun)
so it can authenticate requests to the Mailgun ingress.

Use `bin/rails credentials:edit` to add your Signing key to your application's
encrypted credentials under `action_mailbox.mailgun_signing_key`,
where Action Mailbox will automatically find it:

```
action_mailbox:
  mailgun_signing_key: ...
```

Copy

Alternatively, provide your Signing key in the `MAILGUN_INGRESS_SIGNING_KEY` environment
variable.

Tell Action Mailbox to accept emails from Mailgun:

```
# config/environments/production.rb
config.action_mailbox.ingress = :mailgun
```

Copy

[Configure Mailgun](https://documentation.mailgun.com/en/latest/user_manual.html#receiving-forwarding-and-storing-messages)
to forward inbound emails to `/rails/action_mailbox/mailgun/inbound_emails/mime`.
If your application lived at `https://example.com`, you would specify the
fully-qualified URL `https://example.com/rails/action_mailbox/mailgun/inbound_emails/mime`.

#### [3.3 Mandrill](https://guides.rubyonrails.org/v6.1/action_mailbox_basics.html\#mandrill)

Give Action Mailbox your Mandrill API key so it can authenticate requests to
the Mandrill ingress.

Use `bin/rails credentials:edit` to add your API key to your application's
encrypted credentials under `action_mailbox.mandrill_api_key`,
where Action Mailbox will automatically find it:

```
action_mailbox:
  mandrill_api_key: ...
```

Copy

Alternatively, provide your API key in the `MANDRILL_INGRESS_API_KEY`
environment variable.

Tell Action Mailbox to accept emails from Mandrill:

```
# config/environments/production.rb
config.action_mailbox.ingress = :mandrill
```

Copy

[Configure Mandrill](https://mandrill.zendesk.com/hc/en-us/articles/205583197-Inbound-Email-Processing-Overview)
to route inbound emails to `/rails/action_mailbox/mandrill/inbound_emails`.
If your application lived at `https://example.com`, you would specify
the fully-qualified URL `https://example.com/rails/action_mailbox/mandrill/inbound_emails`.

#### [3.4 Postfix](https://guides.rubyonrails.org/v6.1/action_mailbox_basics.html\#postfix)

Tell Action Mailbox to accept emails from an SMTP relay:

```
# config/environments/production.rb
config.action_mailbox.ingress = :relay
```

Copy

Generate a strong password that Action Mailbox can use to authenticate requests to the relay ingress.

Use `bin/rails credentials:edit` to add the password to your application's encrypted credentials under
`action_mailbox.ingress_password`, where Action Mailbox will automatically find it:

```
action_mailbox:
  ingress_password: ...
```

Copy

Alternatively, provide the password in the `RAILS_INBOUND_EMAIL_PASSWORD` environment variable.

[Configure Postfix](https://serverfault.com/questions/258469/how-to-configure-postfix-to-pipe-all-incoming-email-to-a-script)
to pipe inbound emails to `bin/rails action_mailbox:ingress:postfix`, providing
the `URL` of the Postfix ingress and the `INGRESS_PASSWORD` you previously
generated. If your application lived at `https://example.com`, the full command
would look like this:

```
$ bin/rails action_mailbox:ingress:postfix URL=https://example.com/rails/action_mailbox/relay/inbound_emails INGRESS_PASSWORD=...
```

Copy

#### [3.5 Postmark](https://guides.rubyonrails.org/v6.1/action_mailbox_basics.html\#postmark)

Tell Action Mailbox to accept emails from Postmark:

```
# config/environments/production.rb
config.action_mailbox.ingress = :postmark
```

Copy

Generate a strong password that Action Mailbox can use to authenticate
requests to the Postmark ingress.

Use `bin/rails credentials:edit` to add the password to your application's
encrypted credentials under `action_mailbox.ingress_password`,
where Action Mailbox will automatically find it:

```
action_mailbox:
  ingress_password: ...
```

Copy

Alternatively, provide the password in the `RAILS_INBOUND_EMAIL_PASSWORD`
environment variable.

[Configure Postmark inbound webhook](https://postmarkapp.com/manual#configure-your-inbound-webhook-url)
to forward inbound emails to `/rails/action_mailbox/postmark/inbound_emails` with the username `actionmailbox`
and the password you previously generated. If your application lived at `https://example.com`, you would
configure Postmark with the following fully-qualified URL:

```
https://actionmailbox:PASSWORD@example.com/rails/action_mailbox/postmark/inbound_emails
```

Copy

When configuring your Postmark inbound webhook, be sure to check the box labeled **"Include raw email content in JSON payload"**.
Action Mailbox needs the raw email content to work.

#### [3.6 Qmail](https://guides.rubyonrails.org/v6.1/action_mailbox_basics.html\#qmail)

Tell Action Mailbox to accept emails from an SMTP relay:

```
# config/environments/production.rb
config.action_mailbox.ingress = :relay
```

Copy

Generate a strong password that Action Mailbox can use to authenticate requests to the relay ingress.

Use `bin/rails credentials:edit` to add the password to your application's encrypted credentials under
`action_mailbox.ingress_password`, where Action Mailbox will automatically find it:

```
action_mailbox:
  ingress_password: ...
```

Copy

Alternatively, provide the password in the `RAILS_INBOUND_EMAIL_PASSWORD` environment variable.

Configure Qmail to pipe inbound emails to `bin/rails action_mailbox:ingress:qmail`,
providing the `URL` of the relay ingress and the `INGRESS_PASSWORD` you
previously generated. If your application lived at `https://example.com`, the
full command would look like this:

```
$ bin/rails action_mailbox:ingress:qmail URL=https://example.com/rails/action_mailbox/relay/inbound_emails INGRESS_PASSWORD=...
```

Copy

#### [3.7 SendGrid](https://guides.rubyonrails.org/v6.1/action_mailbox_basics.html\#sendgrid)

Tell Action Mailbox to accept emails from SendGrid:

```
# config/environments/production.rb
config.action_mailbox.ingress = :sendgrid
```

Copy

Generate a strong password that Action Mailbox can use to authenticate
requests to the SendGrid ingress.

Use `bin/rails credentials:edit` to add the password to your application's
encrypted credentials under `action_mailbox.ingress_password`,
where Action Mailbox will automatically find it:

```
action_mailbox:
  ingress_password: ...
```

Copy

Alternatively, provide the password in the `RAILS_INBOUND_EMAIL_PASSWORD`
environment variable.

[Configure SendGrid Inbound Parse](https://sendgrid.com/docs/for-developers/parsing-email/setting-up-the-inbound-parse-webhook/)
to forward inbound emails to
`/rails/action_mailbox/sendgrid/inbound_emails` with the username `actionmailbox`
and the password you previously generated. If your application lived at `https://example.com`,
you would configure SendGrid with the following URL:

```
https://actionmailbox:PASSWORD@example.com/rails/action_mailbox/sendgrid/inbound_emails
```

Copy

When configuring your SendGrid Inbound Parse webhook, be sure to check the box labeled **“Post the raw, full MIME message.”** Action Mailbox needs the raw MIME message to work.

### [4 Examples](https://guides.rubyonrails.org/v6.1/action_mailbox_basics.html\#examples)

Configure basic routing:

```
# app/mailboxes/application_mailbox.rb
class ApplicationMailbox < ActionMailbox::Base
  routing /^save@/i     => :forwards
  routing /@replies\./i => :replies
end
```

Copy

Then set up a mailbox:

```
# Generate new mailbox
$ bin/rails generate mailbox forwards
```

Copy

```
# app/mailboxes/forwards_mailbox.rb
class ForwardsMailbox < ApplicationMailbox
  # Callbacks specify prerequisites to processing
  before_processing :require_projects

  def process
    # Record the forward on the one project, or…
    if forwarder.projects.one?
      record_forward
    else
      # …involve a second Action Mailer to ask which project to forward into.
      request_forwarding_project
    end
  end

  private
    def require_projects
      if forwarder.projects.none?
        # Use Action Mailers to bounce incoming emails back to sender – this halts processing
        bounce_with Forwards::BounceMailer.no_projects(inbound_email, forwarder: forwarder)
      end
    end

    def record_forward
      forwarder.forwards.create subject: mail.subject, content: mail.content
    end

    def request_forwarding_project
      Forwards::RoutingMailer.choose_project(inbound_email, forwarder: forwarder).deliver_now
    end

    def forwarder
      @forwarder ||= User.find_by(email_address: mail.from)
    end
end
```

Copy

### [5 Incineration of InboundEmails](https://guides.rubyonrails.org/v6.1/action_mailbox_basics.html\#incineration-of-inboundemails)

By default, an InboundEmail that has been successfully processed will be
incinerated after 30 days. This ensures you're not holding on to people's data
willy-nilly after they may have canceled their accounts or deleted their
content. The intention is that after you've processed an email, you should have
extracted all the data you needed and turned it into domain models and content
on your side of the application. The InboundEmail simply stays in the system
for the extra time to provide debugging and forensics options.

The actual incineration is done via the `IncinerationJob` that's scheduled
to run after `config.action_mailbox.incinerate_after` time. This value is
by default set to `30.days`, but you can change it in your production.rb
configuration. (Note that this far-future incineration scheduling relies on
your job queue being able to hold jobs for that long.)

### [6 Working with Action Mailbox in development](https://guides.rubyonrails.org/v6.1/action_mailbox_basics.html\#working-with-action-mailbox-in-development)

It's helpful to be able to test incoming emails in development without actually
sending and receiving real emails. To accomplish this, there's a conductor
controller mounted at `/rails/conductor/action_mailbox/inbound_emails`,
which gives you an index of all the InboundEmails in the system, their
state of processing, and a form to create a new InboundEmail as well.

### [7 Testing mailboxes](https://guides.rubyonrails.org/v6.1/action_mailbox_basics.html\#testing-mailboxes)

Example:

```
class ForwardsMailboxTest < ActionMailbox::TestCase
  test "directly recording a client forward for a forwarder and forwardee corresponding to one project" do
    assert_difference -> { people(:david).buckets.first.recordings.count } do
      receive_inbound_email_from_mail \
        to: 'save@example.com',
        from: people(:david).email_address,
        subject: "Fwd: Status update?",
        body: <<~BODY
          --- Begin forwarded message ---
          From: Frank Holland <frank@microsoft.com>

          What's the status?
        BODY
    end

    recording = people(:david).buckets.first.recordings.last
    assert_equal people(:david), recording.creator
    assert_equal "Status update?", recording.forward.subject
    assert_match "What's the status?", recording.forward.content.to_s
  end
end
```

Copy

Please refer to the [ActionMailbox::TestHelper API](https://api.rubyonrails.org/v6.1.7.10/classes/ActionMailbox/TestHelper.html) for further test helper methods.

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