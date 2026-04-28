v6.1.7.10

**More at [rubyonrails.org:](https://rubyonrails.org/)**
More Ruby on Rails


- [Blog](https://rubyonrails.org/blog)
- [Guides](https://guides.rubyonrails.org/)
- [API](https://api.rubyonrails.org/)
- [Forum](https://discuss.rubyonrails.org/)
- [Contribute on GitHub](https://github.com/rails/rails)

* * *

## Active Record and PostgreSQL

This guide covers PostgreSQL specific usage of Active Record.

After reading this guide, you will know:

- How to use PostgreSQL's datatypes.
- How to use UUID primary keys.
- How to implement full text search with PostgreSQL.
- How to back your Active Record models with database views.

### ![](https://guides.rubyonrails.org/v6.1/images/chapters_icon.gif)Chapters

1. [Datatypes](https://guides.rubyonrails.org/v6.1/active_record_postgresql.html#datatypes)   - [Bytea](https://guides.rubyonrails.org/v6.1/active_record_postgresql.html#bytea)
   - [Array](https://guides.rubyonrails.org/v6.1/active_record_postgresql.html#array)
   - [Hstore](https://guides.rubyonrails.org/v6.1/active_record_postgresql.html#hstore)
   - [JSON and JSONB](https://guides.rubyonrails.org/v6.1/active_record_postgresql.html#json-and-jsonb)
   - [Range Types](https://guides.rubyonrails.org/v6.1/active_record_postgresql.html#range-types)
   - [Composite Types](https://guides.rubyonrails.org/v6.1/active_record_postgresql.html#composite-types)
   - [Enumerated Types](https://guides.rubyonrails.org/v6.1/active_record_postgresql.html#enumerated-types)
   - [UUID](https://guides.rubyonrails.org/v6.1/active_record_postgresql.html#uuid)
   - [Bit String Types](https://guides.rubyonrails.org/v6.1/active_record_postgresql.html#bit-string-types)
   - [Network Address Types](https://guides.rubyonrails.org/v6.1/active_record_postgresql.html#network-address-types)
   - [Geometric Types](https://guides.rubyonrails.org/v6.1/active_record_postgresql.html#geometric-types)
   - [Interval](https://guides.rubyonrails.org/v6.1/active_record_postgresql.html#interval)
2. [UUID Primary Keys](https://guides.rubyonrails.org/v6.1/active_record_postgresql.html#uuid-primary-keys)
3. [Full Text Search](https://guides.rubyonrails.org/v6.1/active_record_postgresql.html#full-text-search)
4. [Database Views](https://guides.rubyonrails.org/v6.1/active_record_postgresql.html#database-views)

In order to use the PostgreSQL adapter you need to have at least version 9.3
installed. Older versions are not supported.

To get started with PostgreSQL have a look at the
[configuring Rails guide](https://guides.rubyonrails.org/v6.1/configuring.html#configuring-a-postgresql-database).
It describes how to properly set up Active Record for PostgreSQL.

### [1 Datatypes](https://guides.rubyonrails.org/v6.1/active_record_postgresql.html\#datatypes)

PostgreSQL offers a number of specific datatypes. Following is a list of types,
that are supported by the PostgreSQL adapter.

#### [1.1 Bytea](https://guides.rubyonrails.org/v6.1/active_record_postgresql.html\#bytea)

- [type definition](https://www.postgresql.org/docs/current/static/datatype-binary.html)
- [functions and operators](https://www.postgresql.org/docs/current/static/functions-binarystring.html)

```
# db/migrate/20140207133952_create_documents.rb
create_table :documents do |t|
  t.binary 'payload'
end
```

Copy

```
# app/models/document.rb
class Document < ApplicationRecord
end
```

Copy

```
# Usage
data = File.read(Rails.root + "tmp/output.pdf")
Document.create payload: data
```

Copy

#### [1.2 Array](https://guides.rubyonrails.org/v6.1/active_record_postgresql.html\#array)

- [type definition](https://www.postgresql.org/docs/current/static/arrays.html)
- [functions and operators](https://www.postgresql.org/docs/current/static/functions-array.html)

```
# db/migrate/20140207133952_create_books.rb
create_table :books do |t|
  t.string 'title'
  t.string 'tags', array: true
  t.integer 'ratings', array: true
end
add_index :books, :tags, using: 'gin'
add_index :books, :ratings, using: 'gin'
```

Copy

```
# app/models/book.rb
class Book < ApplicationRecord
end
```

Copy

```
# Usage
Book.create title: "Brave New World",
            tags: ["fantasy", "fiction"],
            ratings: [4, 5]

## Books for a single tag
Book.where("'fantasy' = ANY (tags)")

## Books for multiple tags
Book.where("tags @> ARRAY[?]::varchar[]", ["fantasy", "fiction"])

## Books with 3 or more ratings
Book.where("array_length(ratings, 1) >= 3")
```

Copy

#### [1.3 Hstore](https://guides.rubyonrails.org/v6.1/active_record_postgresql.html\#hstore)

- [type definition](https://www.postgresql.org/docs/current/static/hstore.html)
- [functions and operators](https://www.postgresql.org/docs/current/static/hstore.html#id-1.11.7.26.5)

You need to enable the `hstore` extension to use hstore.

```
# db/migrate/20131009135255_create_profiles.rb
ActiveRecord::Schema.define do
  enable_extension 'hstore' unless extension_enabled?('hstore')
  create_table :profiles do |t|
    t.hstore 'settings'
  end
end
```

Copy

```
# app/models/profile.rb
class Profile < ApplicationRecord
end
```

Copy

```
irb> Profile.create(settings: { "color" => "blue", "resolution" => "800x600" })

irb> profile = Profile.first
irb> profile.settings
=> {"color"=>"blue", "resolution"=>"800x600"}

irb> profile.settings = {"color" => "yellow", "resolution" => "1280x1024"}
irb> profile.save!

irb> Profile.where("settings->'color' = ?", "yellow")
=> #<ActiveRecord::Relation [#<Profile id: 1, settings: {"color"=>"yellow", "resolution"=>"1280x1024"}>]>
```

Copy

#### [1.4 JSON and JSONB](https://guides.rubyonrails.org/v6.1/active_record_postgresql.html\#json-and-jsonb)

- [type definition](https://www.postgresql.org/docs/current/static/datatype-json.html)
- [functions and operators](https://www.postgresql.org/docs/current/static/functions-json.html)

```
# db/migrate/20131220144913_create_events.rb
# ... for json datatype:
create_table :events do |t|
  t.json 'payload'
end
# ... or for jsonb datatype:
create_table :events do |t|
  t.jsonb 'payload'
end
```

Copy

```
# app/models/event.rb
class Event < ApplicationRecord
end
```

Copy

```
irb> Event.create(payload: { kind: "user_renamed", change: ["jack", "john"]})

irb> event = Event.first
irb> event.payload
=> {"kind"=>"user_renamed", "change"=>["jack", "john"]}

## Query based on JSON document
# The -> operator returns the original JSON type (which might be an object), whereas ->> returns text
irb> Event.where("payload->>'kind' = ?", "user_renamed")
```

Copy

#### [1.5 Range Types](https://guides.rubyonrails.org/v6.1/active_record_postgresql.html\#range-types)

- [type definition](https://www.postgresql.org/docs/current/static/rangetypes.html)
- [functions and operators](https://www.postgresql.org/docs/current/static/functions-range.html)

This type is mapped to Ruby [`Range`](https://ruby-doc.org/core-2.5.0/Range.html) objects.

```
# db/migrate/20130923065404_create_events.rb
create_table :events do |t|
  t.daterange 'duration'
end
```

Copy

```
# app/models/event.rb
class Event < ApplicationRecord
end
```

Copy

```
irb> Event.create(duration: Date.new(2014, 2, 11)..Date.new(2014, 2, 12))

irb> event = Event.first
irb> event.duration
=> Tue, 11 Feb 2014...Thu, 13 Feb 2014

## All Events on a given date
irb> Event.where("duration @> ?::date", Date.new(2014, 2, 12))

## Working with range bounds
irb> event = Event.select("lower(duration) AS starts_at").select("upper(duration) AS ends_at").first

irb> event.starts_at
=> Tue, 11 Feb 2014
irb> event.ends_at
=> Thu, 13 Feb 2014
```

Copy

#### [1.6 Composite Types](https://guides.rubyonrails.org/v6.1/active_record_postgresql.html\#composite-types)

- [type definition](https://www.postgresql.org/docs/current/static/rowtypes.html)

Currently there is no special support for composite types. They are mapped to
normal text columns:

```
CREATE TYPE full_address AS
(
  city VARCHAR(90),
  street VARCHAR(90)
);
```

Copy

```
# db/migrate/20140207133952_create_contacts.rb
execute <<-SQL
  CREATE TYPE full_address AS
  (
    city VARCHAR(90),
    street VARCHAR(90)
  );
SQL
create_table :contacts do |t|
  t.column :address, :full_address
end
```

Copy

```
# app/models/contact.rb
class Contact < ApplicationRecord
end
```

Copy

```
irb> Contact.create address: "(Paris,Champs-Élysées)"
irb> contact = Contact.first
irb> contact.address
=> "(Paris,Champs-Élysées)"
irb> contact.address = "(Paris,Rue Basse)"
irb> contact.save!
```

Copy

#### [1.7 Enumerated Types](https://guides.rubyonrails.org/v6.1/active_record_postgresql.html\#enumerated-types)

- [type definition](https://www.postgresql.org/docs/current/static/datatype-enum.html)

Currently there is no special support for enumerated types. They are mapped as
normal text columns:

```
# db/migrate/20131220144913_create_articles.rb
def up
  execute <<-SQL
    CREATE TYPE article_status AS ENUM ('draft', 'published');
  SQL
  create_table :articles do |t|
    t.column :status, :article_status
  end
end

# NOTE: It's important to drop table before dropping enum.
def down
  drop_table :articles

  execute <<-SQL
    DROP TYPE article_status;
  SQL
end
```

Copy

```
# app/models/article.rb
class Article < ApplicationRecord
end
```

Copy

```
irb> Article.create status: "draft"
irb> article = Article.first
irb> article.status
=> "draft"

irb> article.status = "published"
irb> article.save!
```

Copy

To add a new value before/after existing one you should use [ALTER TYPE](https://www.postgresql.org/docs/current/static/sql-altertype.html):

```
# db/migrate/20150720144913_add_new_state_to_articles.rb
# NOTE: ALTER TYPE ... ADD VALUE cannot be executed inside of a transaction block so here we are using disable_ddl_transaction!
disable_ddl_transaction!

def up
  execute <<-SQL
    ALTER TYPE article_status ADD VALUE IF NOT EXISTS 'archived' AFTER 'published';
  SQL
end
```

Copy

ENUM values can't be dropped currently. You can read why [here](https://www.postgresql.org/message-id/29F36C7C98AB09499B1A209D48EAA615B7653DBC8A@mail2a.alliedtesting.com).

Hint: to show all the values of the all enums you have, you should call this query in `bin/rails db` or `psql` console:

```
SELECT n.nspname AS enum_schema,
       t.typname AS enum_name,
       e.enumlabel AS enum_value
  FROM pg_type t
      JOIN pg_enum e ON t.oid = e.enumtypid
      JOIN pg_catalog.pg_namespace n ON n.oid = t.typnamespace
```

Copy

#### [1.8 UUID](https://guides.rubyonrails.org/v6.1/active_record_postgresql.html\#uuid)

- [type definition](https://www.postgresql.org/docs/current/static/datatype-uuid.html)
- [pgcrypto generator function](https://www.postgresql.org/docs/current/static/pgcrypto.html)
- [uuid-ossp generator functions](https://www.postgresql.org/docs/current/static/uuid-ossp.html)

You need to enable the `pgcrypto` (only PostgreSQL >= 9.4) or `uuid-ossp`
extension to use uuid.

```
# db/migrate/20131220144913_create_revisions.rb
create_table :revisions do |t|
  t.uuid :identifier
end
```

Copy

```
# app/models/revision.rb
class Revision < ApplicationRecord
end
```

Copy

```
irb> Revision.create identifier: "A0EEBC99-9C0B-4EF8-BB6D-6BB9BD380A11"

irb> revision = Revision.first
irb> revision.identifier
=> "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"
```

Copy

You can use `uuid` type to define references in migrations:

```
# db/migrate/20150418012400_create_blog.rb
enable_extension 'pgcrypto' unless extension_enabled?('pgcrypto')
create_table :posts, id: :uuid

create_table :comments, id: :uuid do |t|
  # t.belongs_to :post, type: :uuid
  t.references :post, type: :uuid
end
```

Copy

```
# app/models/post.rb
class Post < ApplicationRecord
  has_many :comments
end
```

Copy

```
# app/models/comment.rb
class Comment < ApplicationRecord
  belongs_to :post
end
```

Copy

See [this section](https://guides.rubyonrails.org/v6.1/active_record_postgresql.html#uuid-primary-keys) for more details on using UUIDs as primary key.

#### [1.9 Bit String Types](https://guides.rubyonrails.org/v6.1/active_record_postgresql.html\#bit-string-types)

- [type definition](https://www.postgresql.org/docs/current/static/datatype-bit.html)
- [functions and operators](https://www.postgresql.org/docs/current/static/functions-bitstring.html)

```
# db/migrate/20131220144913_create_users.rb
create_table :users, force: true do |t|
  t.column :settings, "bit(8)"
end
```

Copy

```
# app/models/user.rb
class User < ApplicationRecord
end
```

Copy

```
irb> User.create settings: "01010011"
irb> user = User.first
irb> user.settings
=> "01010011"
irb> user.settings = "0xAF"
irb> user.settings
=> 10101111
irb> user.save!
```

Copy

#### [1.10 Network Address Types](https://guides.rubyonrails.org/v6.1/active_record_postgresql.html\#network-address-types)

- [type definition](https://www.postgresql.org/docs/current/static/datatype-net-types.html)

The types `inet` and `cidr` are mapped to Ruby
[`IPAddr`](https://ruby-doc.org/stdlib-2.5.0/libdoc/ipaddr/rdoc/IPAddr.html)
objects. The `macaddr` type is mapped to normal text.

```
# db/migrate/20140508144913_create_devices.rb
create_table(:devices, force: true) do |t|
  t.inet 'ip'
  t.cidr 'network'
  t.macaddr 'address'
end
```

Copy

```
# app/models/device.rb
class Device < ApplicationRecord
end
```

Copy

```
irb> macbook = Device.create(ip: "192.168.1.12", network: "192.168.2.0/24", address: "32:01:16:6d:05:ef")

irb> macbook.ip
=> #<IPAddr: IPv4:192.168.1.12/255.255.255.255>

irb> macbook.network
=> #<IPAddr: IPv4:192.168.2.0/255.255.255.0>

irb> macbook.address
=> "32:01:16:6d:05:ef"
```

Copy

#### [1.11 Geometric Types](https://guides.rubyonrails.org/v6.1/active_record_postgresql.html\#geometric-types)

- [type definition](https://www.postgresql.org/docs/current/static/datatype-geometric.html)

All geometric types, with the exception of `points` are mapped to normal text.
A point is casted to an array containing `x` and `y` coordinates.

#### [1.12 Interval](https://guides.rubyonrails.org/v6.1/active_record_postgresql.html\#interval)

- [type definition](http://www.postgresql.org/docs/current/static/datatype-datetime.html#DATATYPE-INTERVAL-INPUT)
- [functions and operators](http://www.postgresql.org/docs/current/static/functions-datetime.html)

This type is mapped to [`ActiveSupport::Duration`](http://api.rubyonrails.org/v6.1.7.10/classes/ActiveSupport/Duration.html) objects.

```
# db/migrate/20200120000000_create_events.rb
create_table :events do |t|
  t.interval 'duration'
end
```

Copy

```
# app/models/event.rb
class Event < ApplicationRecord
end
```

Copy

```
irb> Event.create(duration: 2.days)

irb> event = Event.first
irb> event.duration
=> 2 days
```

Copy

### [2 UUID Primary Keys](https://guides.rubyonrails.org/v6.1/active_record_postgresql.html\#uuid-primary-keys)

You need to enable the `pgcrypto` (only PostgreSQL >= 9.4) or `uuid-ossp`
extension to generate random UUIDs.

```
# db/migrate/20131220144913_create_devices.rb
enable_extension 'pgcrypto' unless extension_enabled?('pgcrypto')
create_table :devices, id: :uuid do |t|
  t.string :kind
end
```

Copy

```
# app/models/device.rb
class Device < ApplicationRecord
end
```

Copy

```
irb> device = Device.create
irb> device.id
=> "814865cd-5a1d-4771-9306-4268f188fe9e"
```

Copy

`gen_random_uuid()` (from `pgcrypto`) is assumed if no `:default` option was
passed to `create_table`.

### [3 Full Text Search](https://guides.rubyonrails.org/v6.1/active_record_postgresql.html\#full-text-search)

```
# db/migrate/20131220144913_create_documents.rb
create_table :documents do |t|
  t.string 'title'
  t.string 'body'
end

add_index :documents, "to_tsvector('english', title || ' ' || body)", using: :gin, name: 'documents_idx'
```

Copy

```
# app/models/document.rb
class Document < ApplicationRecord
end
```

Copy

```
# Usage
Document.create(title: "Cats and Dogs", body: "are nice!")

## all documents matching 'cat & dog'
Document.where("to_tsvector('english', title || ' ' || body) @@ to_tsquery(?)",
                 "cat & dog")
```

Copy

### [4 Database Views](https://guides.rubyonrails.org/v6.1/active_record_postgresql.html\#database-views)

- [view creation](https://www.postgresql.org/docs/current/static/sql-createview.html)

Imagine you need to work with a legacy database containing the following table:

```
rails_pg_guide=# \d "TBL_ART"
                                        Table "public.TBL_ART"
   Column   |            Type             |                         Modifiers
------------+-----------------------------+------------------------------------------------------------
 INT_ID     | integer                     | not null default nextval('"TBL_ART_INT_ID_seq"'::regclass)
 STR_TITLE  | character varying           |
 STR_STAT   | character varying           | default 'draft'::character varying
 DT_PUBL_AT | timestamp without time zone |
 BL_ARCH    | boolean                     | default false
Indexes:
    "TBL_ART_pkey" PRIMARY KEY, btree ("INT_ID")
```

Copy

This table does not follow the Rails conventions at all.
Because simple PostgreSQL views are updateable by default,
we can wrap it as follows:

```
# db/migrate/20131220144913_create_articles_view.rb
execute <<-SQL
CREATE VIEW articles AS
  SELECT "INT_ID" AS id,
         "STR_TITLE" AS title,
         "STR_STAT" AS status,
         "DT_PUBL_AT" AS published_at,
         "BL_ARCH" AS archived
  FROM "TBL_ART"
  WHERE "BL_ARCH" = 'f'
  SQL
```

Copy

```
# app/models/article.rb
class Article < ApplicationRecord
  self.primary_key = "id"
  def archive!
    update_attribute :archived, true
  end
end
```

Copy

```
irb> first = Article.create! title: "Winter is coming", status: "published", published_at: 1.year.ago
irb> second = Article.create! title: "Brace yourself", status: "draft", published_at: 1.month.ago

irb> Article.count
=> 2
irb> first.archive!
irb> Article.count
=> 1
```

Copy

This application only cares about non-archived `Articles`. A view also
allows for conditions so we can exclude the archived `Articles` directly.

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