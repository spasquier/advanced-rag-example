v6.1.7.10

**More at [rubyonrails.org:](https://rubyonrails.org/)**
More Ruby on Rails


- [Blog](https://rubyonrails.org/blog)
- [Guides](https://guides.rubyonrails.org/)
- [API](https://api.rubyonrails.org/)
- [Forum](https://discuss.rubyonrails.org/)
- [Contribute on GitHub](https://github.com/rails/rails)

* * *

## Active Record Associations

This guide covers the association features of Active Record.

After reading this guide, you will know:

- How to declare associations between Active Record models.
- How to understand the various types of Active Record associations.
- How to use the methods added to your models by creating associations.

### ![](https://guides.rubyonrails.org/v6.1/images/chapters_icon.gif)Chapters

1. [Why Associations?](https://guides.rubyonrails.org/v6.1/association_basics.html#why-associations-questionmark)
2. [The Types of Associations](https://guides.rubyonrails.org/v6.1/association_basics.html#the-types-of-associations)   - [The `belongs_to` Association](https://guides.rubyonrails.org/v6.1/association_basics.html#the-belongs-to-association)
   - [The `has_one` Association](https://guides.rubyonrails.org/v6.1/association_basics.html#the-has-one-association)
   - [The `has_many` Association](https://guides.rubyonrails.org/v6.1/association_basics.html#the-has-many-association)
   - [The `has_many :through` Association](https://guides.rubyonrails.org/v6.1/association_basics.html#the-has-many-through-association)
   - [The `has_one :through` Association](https://guides.rubyonrails.org/v6.1/association_basics.html#the-has-one-through-association)
   - [The `has_and_belongs_to_many` Association](https://guides.rubyonrails.org/v6.1/association_basics.html#the-has-and-belongs-to-many-association)
   - [Choosing Between `belongs_to` and `has_one`](https://guides.rubyonrails.org/v6.1/association_basics.html#choosing-between-belongs-to-and-has-one)
   - [Choosing Between `has_many :through` and `has_and_belongs_to_many`](https://guides.rubyonrails.org/v6.1/association_basics.html#choosing-between-has-many-through-and-has-and-belongs-to-many)
   - [Polymorphic Associations](https://guides.rubyonrails.org/v6.1/association_basics.html#polymorphic-associations)
   - [Self Joins](https://guides.rubyonrails.org/v6.1/association_basics.html#self-joins)
3. [Tips, Tricks, and Warnings](https://guides.rubyonrails.org/v6.1/association_basics.html#tips-tricks-and-warnings)   - [Controlling Caching](https://guides.rubyonrails.org/v6.1/association_basics.html#controlling-caching)
   - [Avoiding Name Collisions](https://guides.rubyonrails.org/v6.1/association_basics.html#avoiding-name-collisions)
   - [Updating the Schema](https://guides.rubyonrails.org/v6.1/association_basics.html#updating-the-schema)
   - [Controlling Association Scope](https://guides.rubyonrails.org/v6.1/association_basics.html#controlling-association-scope)
   - [Bi-directional Associations](https://guides.rubyonrails.org/v6.1/association_basics.html#bi-directional-associations)
4. [Detailed Association Reference](https://guides.rubyonrails.org/v6.1/association_basics.html#detailed-association-reference)   - [`belongs_to` Association Reference](https://guides.rubyonrails.org/v6.1/association_basics.html#belongs-to-association-reference)
   - [`has_one` Association Reference](https://guides.rubyonrails.org/v6.1/association_basics.html#has-one-association-reference)
   - [`has_many` Association Reference](https://guides.rubyonrails.org/v6.1/association_basics.html#has-many-association-reference)
   - [`has_and_belongs_to_many` Association Reference](https://guides.rubyonrails.org/v6.1/association_basics.html#has-and-belongs-to-many-association-reference)
   - [Association Callbacks](https://guides.rubyonrails.org/v6.1/association_basics.html#association-callbacks)
   - [Association Extensions](https://guides.rubyonrails.org/v6.1/association_basics.html#association-extensions)
5. [Single Table Inheritance (STI)](https://guides.rubyonrails.org/v6.1/association_basics.html#single-table-inheritance-sti)

### [1 Why Associations?](https://guides.rubyonrails.org/v6.1/association_basics.html\#why-associations-questionmark)

In Rails, an _association_ is a connection between two Active Record models. Why do we need associations between models? Because they make common operations simpler and easier in your code. For example, consider a simple Rails application that includes a model for authors and a model for books. Each author can have many books. Without associations, the model declarations would look like this:

```
class Author < ApplicationRecord
end

class Book < ApplicationRecord
end
```

Copy

Now, suppose we wanted to add a new book for an existing author. We'd need to do something like this:

```
@book = Book.create(published_at: Time.now, author_id: @author.id)
```

Copy

Or consider deleting an author, and ensuring that all of its books get deleted as well:

```
@books = Book.where(author_id: @author.id)
@books.each do |book|
  book.destroy
end
@author.destroy
```

Copy

With Active Record associations, we can streamline these - and other - operations by declaratively telling Rails that there is a connection between the two models. Here's the revised code for setting up authors and books:

```
class Author < ApplicationRecord
  has_many :books, dependent: :destroy
end

class Book < ApplicationRecord
  belongs_to :author
end
```

Copy

With this change, creating a new book for a particular author is easier:

```
@book = @author.books.create(published_at: Time.now)
```

Copy

Deleting an author and all of its books is _much_ easier:

```
@author.destroy
```

Copy

To learn more about the different types of associations, read the next section of this guide. That's followed by some tips and tricks for working with associations, and then by a complete reference to the methods and options for associations in Rails.

### [2 The Types of Associations](https://guides.rubyonrails.org/v6.1/association_basics.html\#the-types-of-associations)

Rails supports six types of associations:

- [`belongs_to`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/ClassMethods.html#method-i-belongs_to)
- [`has_one`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/ClassMethods.html#method-i-has_one)
- [`has_many`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/ClassMethods.html#method-i-has_many)
- [`has_many :through`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/ClassMethods.html#method-i-has_many)
- [`has_one :through`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/ClassMethods.html#method-i-has_one)
- [`has_and_belongs_to_many`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/ClassMethods.html#method-i-has_and_belongs_to_many)

Associations are implemented using macro-style calls, so that you can declaratively add features to your models. For example, by declaring that one model `belongs_to` another, you instruct Rails to maintain [Primary Key](https://en.wikipedia.org/wiki/Unique_key)- [Foreign Key](https://en.wikipedia.org/wiki/Foreign_key) information between instances of the two models, and you also get a number of utility methods added to your model.

In the remainder of this guide, you'll learn how to declare and use the various forms of associations. But first, a quick introduction to the situations where each association type is appropriate.

#### [2.1 The `belongs_to` Association](https://guides.rubyonrails.org/v6.1/association_basics.html\#the-belongs-to-association)

A [`belongs_to`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/ClassMethods.html#method-i-belongs_to) association sets up a connection with another model, such that each instance of the declaring model "belongs to" one instance of the other model. For example, if your application includes authors and books, and each book can be assigned to exactly one author, you'd declare the book model this way:

```
class Book < ApplicationRecord
  belongs_to :author
end
```

Copy

![belongs_to Association Diagram](https://guides.rubyonrails.org/v6.1/images/association_basics/belongs_to.png)

`belongs_to` associations _must_ use the singular term. If you used the pluralized form in the above example for the `author` association in the `Book` model and tried to create the instance by `Book.create(authors: @author)`, you would be told that there was an "uninitialized constant Book::Authors". This is because Rails automatically infers the class name from the association name. If the association name is wrongly pluralized, then the inferred class will be wrongly pluralized too.

The corresponding migration might look like this:

```
class CreateBooks < ActiveRecord::Migration[6.0]
  def change
    create_table :authors do |t|
      t.string :name
      t.timestamps
    end

    create_table :books do |t|
      t.belongs_to :author
      t.datetime :published_at
      t.timestamps
    end
  end
end
```

Copy

When used alone, `belongs_to` produces a one-directional one-to-one connection. Therefore each book in the above example "knows" its author, but the authors don't know about their books.
To setup a [bi-directional association](https://guides.rubyonrails.org/v6.1/association_basics.html#bi-directional-associations) \- use `belongs_to` in combination with a `has_one` or `has_many` on the other model.

`belongs_to` does not ensure reference consistency, so depending on the use case, you might also need to add a database-level foreign key constraint on the reference column, like this:

```
create_table :books do |t|
  t.belongs_to :author, foreign_key: true
  # ...
end
```

Copy

#### [2.2 The `has_one` Association](https://guides.rubyonrails.org/v6.1/association_basics.html\#the-has-one-association)

A [`has_one`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/ClassMethods.html#method-i-has_one) association indicates that one other model has a reference to this model. That model can be fetched through this association.

For example, if each supplier in your application has only one account, you'd declare the supplier model like this:

```
class Supplier < ApplicationRecord
  has_one :account
end
```

Copy

The main difference from `belongs_to` is that the link column `supplier_id` is located in the other table:

![has_one Association Diagram](https://guides.rubyonrails.org/v6.1/images/association_basics/has_one.png)

The corresponding migration might look like this:

```
class CreateSuppliers < ActiveRecord::Migration[6.0]
  def change
    create_table :suppliers do |t|
      t.string :name
      t.timestamps
    end

    create_table :accounts do |t|
      t.belongs_to :supplier
      t.string :account_number
      t.timestamps
    end
  end
end
```

Copy

Depending on the use case, you might also need to create a unique index and/or
a foreign key constraint on the supplier column for the accounts table. In this
case, the column definition might look like this:

```
create_table :accounts do |t|
  t.belongs_to :supplier, index: { unique: true }, foreign_key: true
  # ...
end
```

Copy

This relation can be [bi-directional](https://guides.rubyonrails.org/v6.1/association_basics.html#bi-directional-associations) when used in combination with `belongs_to` on the other model.

#### [2.3 The `has_many` Association](https://guides.rubyonrails.org/v6.1/association_basics.html\#the-has-many-association)

A [`has_many`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/ClassMethods.html#method-i-has_many) association is similar to `has_one`, but indicates a one-to-many connection with another model. You'll often find this association on the "other side" of a `belongs_to` association. This association indicates that each instance of the model has zero or more instances of another model. For example, in an application containing authors and books, the author model could be declared like this:

```
class Author < ApplicationRecord
  has_many :books
end
```

Copy

The name of the other model is pluralized when declaring a `has_many` association.

![has_many Association Diagram](https://guides.rubyonrails.org/v6.1/images/association_basics/has_many.png)

The corresponding migration might look like this:

```
class CreateAuthors < ActiveRecord::Migration[6.0]
  def change
    create_table :authors do |t|
      t.string :name
      t.timestamps
    end

    create_table :books do |t|
      t.belongs_to :author
      t.datetime :published_at
      t.timestamps
    end
  end
end
```

Copy

Depending on the use case, it's usually a good idea to create a non-unique index and optionally
a foreign key constraint on the author column for the books table:

```
create_table :books do |t|
  t.belongs_to :author, index: true, foreign_key: true
  # ...
end
```

Copy

#### [2.4 The `has_many :through` Association](https://guides.rubyonrails.org/v6.1/association_basics.html\#the-has-many-through-association)

A [`has_many :through`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/ClassMethods.html#method-i-has_many) association is often used to set up a many-to-many connection with another model. This association indicates that the declaring model can be matched with zero or more instances of another model by proceeding _through_ a third model. For example, consider a medical practice where patients make appointments to see physicians. The relevant association declarations could look like this:

```
class Physician < ApplicationRecord
  has_many :appointments
  has_many :patients, through: :appointments
end

class Appointment < ApplicationRecord
  belongs_to :physician
  belongs_to :patient
end

class Patient < ApplicationRecord
  has_many :appointments
  has_many :physicians, through: :appointments
end
```

Copy

![has_many :through Association Diagram](https://guides.rubyonrails.org/v6.1/images/association_basics/has_many_through.png)

The corresponding migration might look like this:

```
class CreateAppointments < ActiveRecord::Migration[6.0]
  def change
    create_table :physicians do |t|
      t.string :name
      t.timestamps
    end

    create_table :patients do |t|
      t.string :name
      t.timestamps
    end

    create_table :appointments do |t|
      t.belongs_to :physician
      t.belongs_to :patient
      t.datetime :appointment_date
      t.timestamps
    end
  end
end
```

Copy

The collection of join models can be managed via the [`has_many` association methods](https://guides.rubyonrails.org/v6.1/association_basics.html#has-many-association-reference).
For example, if you assign:

```
physician.patients = patients
```

Copy

Then new join models are automatically created for the newly associated objects.
If some that existed previously are now missing, then their join rows are automatically deleted.

Automatic deletion of join models is direct, no destroy callbacks are triggered.

The `has_many :through` association is also useful for setting up "shortcuts" through nested `has_many` associations. For example, if a document has many sections, and a section has many paragraphs, you may sometimes want to get a simple collection of all paragraphs in the document. You could set that up this way:

```
class Document < ApplicationRecord
  has_many :sections
  has_many :paragraphs, through: :sections
end

class Section < ApplicationRecord
  belongs_to :document
  has_many :paragraphs
end

class Paragraph < ApplicationRecord
  belongs_to :section
end
```

Copy

With `through: :sections` specified, Rails will now understand:

```
@document.paragraphs
```

Copy

#### [2.5 The `has_one :through` Association](https://guides.rubyonrails.org/v6.1/association_basics.html\#the-has-one-through-association)

A [`has_one :through`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/ClassMethods.html#method-i-has_one) association sets up a one-to-one connection with another model. This association indicates
that the declaring model can be matched with one instance of another model by proceeding _through_ a third model.
For example, if each supplier has one account, and each account is associated with one account history, then the
supplier model could look like this:

```
class Supplier < ApplicationRecord
  has_one :account
  has_one :account_history, through: :account
end

class Account < ApplicationRecord
  belongs_to :supplier
  has_one :account_history
end

class AccountHistory < ApplicationRecord
  belongs_to :account
end
```

Copy

![has_one :through Association Diagram](https://guides.rubyonrails.org/v6.1/images/association_basics/has_one_through.png)

The corresponding migration might look like this:

```
class CreateAccountHistories < ActiveRecord::Migration[6.0]
  def change
    create_table :suppliers do |t|
      t.string :name
      t.timestamps
    end

    create_table :accounts do |t|
      t.belongs_to :supplier
      t.string :account_number
      t.timestamps
    end

    create_table :account_histories do |t|
      t.belongs_to :account
      t.integer :credit_rating
      t.timestamps
    end
  end
end
```

Copy

#### [2.6 The `has_and_belongs_to_many` Association](https://guides.rubyonrails.org/v6.1/association_basics.html\#the-has-and-belongs-to-many-association)

A [`has_and_belongs_to_many`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/ClassMethods.html#method-i-has_and_belongs_to_many) association creates a direct many-to-many connection with another model, with no intervening model.
This association indicates that each instance of the declaring model refers to zero or more instances of another model.
For example, if your application includes assemblies and parts, with each assembly having many parts and each part appearing in many assemblies, you could declare the models this way:

```
class Assembly < ApplicationRecord
  has_and_belongs_to_many :parts
end

class Part < ApplicationRecord
  has_and_belongs_to_many :assemblies
end
```

Copy

![has_and_belongs_to_many Association Diagram](https://guides.rubyonrails.org/v6.1/images/association_basics/habtm.png)

The corresponding migration might look like this:

```
class CreateAssembliesAndParts < ActiveRecord::Migration[6.0]
  def change
    create_table :assemblies do |t|
      t.string :name
      t.timestamps
    end

    create_table :parts do |t|
      t.string :part_number
      t.timestamps
    end

    create_table :assemblies_parts, id: false do |t|
      t.belongs_to :assembly
      t.belongs_to :part
    end
  end
end
```

Copy

#### [2.7 Choosing Between `belongs_to` and `has_one`](https://guides.rubyonrails.org/v6.1/association_basics.html\#choosing-between-belongs-to-and-has-one)

If you want to set up a one-to-one relationship between two models, you'll need to add `belongs_to` to one, and `has_one` to the other. How do you know which is which?

The distinction is in where you place the foreign key (it goes on the table for the class declaring the `belongs_to` association), but you should give some thought to the actual meaning of the data as well. The `has_one` relationship says that one of something is yours - that is, that something points back to you. For example, it makes more sense to say that a supplier owns an account than that an account owns a supplier. This suggests that the correct relationships are like this:

```
class Supplier < ApplicationRecord
  has_one :account
end

class Account < ApplicationRecord
  belongs_to :supplier
end
```

Copy

The corresponding migration might look like this:

```
class CreateSuppliers < ActiveRecord::Migration[6.0]
  def change
    create_table :suppliers do |t|
      t.string :name
      t.timestamps
    end

    create_table :accounts do |t|
      t.bigint  :supplier_id
      t.string  :account_number
      t.timestamps
    end

    add_index :accounts, :supplier_id
  end
end
```

Copy

Using `t.bigint :supplier_id` makes the foreign key naming obvious and explicit. In current versions of Rails, you can abstract away this implementation detail by using `t.references :supplier` instead.

#### [2.8 Choosing Between `has_many :through` and `has_and_belongs_to_many`](https://guides.rubyonrails.org/v6.1/association_basics.html\#choosing-between-has-many-through-and-has-and-belongs-to-many)

Rails offers two different ways to declare a many-to-many relationship between models. The first way is to use `has_and_belongs_to_many`, which allows you to make the association directly:

```
class Assembly < ApplicationRecord
  has_and_belongs_to_many :parts
end

class Part < ApplicationRecord
  has_and_belongs_to_many :assemblies
end
```

Copy

The second way to declare a many-to-many relationship is to use `has_many :through`. This makes the association indirectly, through a join model:

```
class Assembly < ApplicationRecord
  has_many :manifests
  has_many :parts, through: :manifests
end

class Manifest < ApplicationRecord
  belongs_to :assembly
  belongs_to :part
end

class Part < ApplicationRecord
  has_many :manifests
  has_many :assemblies, through: :manifests
end
```

Copy

The simplest rule of thumb is that you should set up a `has_many :through` relationship if you need to work with the relationship model as an independent entity. If you don't need to do anything with the relationship model, it may be simpler to set up a `has_and_belongs_to_many` relationship (though you'll need to remember to create the joining table in the database).

You should use `has_many :through` if you need validations, callbacks, or extra attributes on the join model.

#### [2.9 Polymorphic Associations](https://guides.rubyonrails.org/v6.1/association_basics.html\#polymorphic-associations)

A slightly more advanced twist on associations is the _polymorphic association_. With polymorphic associations, a model can belong to more than one other model, on a single association. For example, you might have a picture model that belongs to either an employee model or a product model. Here's how this could be declared:

```
class Picture < ApplicationRecord
  belongs_to :imageable, polymorphic: true
end

class Employee < ApplicationRecord
  has_many :pictures, as: :imageable
end

class Product < ApplicationRecord
  has_many :pictures, as: :imageable
end
```

Copy

You can think of a polymorphic `belongs_to` declaration as setting up an interface that any other model can use. From an instance of the `Employee` model, you can retrieve a collection of pictures: `@employee.pictures`.

Similarly, you can retrieve `@product.pictures`.

If you have an instance of the `Picture` model, you can get to its parent via `@picture.imageable`. To make this work, you need to declare both a foreign key column and a type column in the model that declares the polymorphic interface:

```
class CreatePictures < ActiveRecord::Migration[6.0]
  def change
    create_table :pictures do |t|
      t.string  :name
      t.bigint  :imageable_id
      t.string  :imageable_type
      t.timestamps
    end

    add_index :pictures, [:imageable_type, :imageable_id]
  end
end
```

Copy

This migration can be simplified by using the `t.references` form:

```
class CreatePictures < ActiveRecord::Migration[6.0]
  def change
    create_table :pictures do |t|
      t.string :name
      t.references :imageable, polymorphic: true
      t.timestamps
    end
  end
end
```

Copy

![Polymorphic Association Diagram](https://guides.rubyonrails.org/v6.1/images/association_basics/polymorphic.png)

#### [2.10 Self Joins](https://guides.rubyonrails.org/v6.1/association_basics.html\#self-joins)

In designing a data model, you will sometimes find a model that should have a relation to itself. For example, you may want to store all employees in a single database model, but be able to trace relationships such as between manager and subordinates. This situation can be modeled with self-joining associations:

```
class Employee < ApplicationRecord
  has_many :subordinates, class_name: "Employee",
                          foreign_key: "manager_id"

  belongs_to :manager, class_name: "Employee", optional: true
end
```

Copy

With this setup, you can retrieve `@employee.subordinates` and `@employee.manager`.

In your migrations/schema, you will add a references column to the model itself.

```
class CreateEmployees < ActiveRecord::Migration[6.0]
  def change
    create_table :employees do |t|
      t.references :manager, foreign_key: { to_table: :employees }
      t.timestamps
    end
  end
end
```

Copy

### [3 Tips, Tricks, and Warnings](https://guides.rubyonrails.org/v6.1/association_basics.html\#tips-tricks-and-warnings)

Here are a few things you should know to make efficient use of Active Record associations in your Rails applications:

- Controlling caching
- Avoiding name collisions
- Updating the schema
- Controlling association scope
- Bi-directional associations

#### [3.1 Controlling Caching](https://guides.rubyonrails.org/v6.1/association_basics.html\#controlling-caching)

All of the association methods are built around caching, which keeps the result of the most recent query available for further operations. The cache is even shared across methods. For example:

```
# retrieves books from the database
author.books.load

# uses the cached copy of books
author.books.size

# uses the cached copy of books
author.books.empty?
```

Copy

But what if you want to reload the cache, because data might have been changed by some other part of the application? Just call `reload` on the association:

```
# retrieves books from the database
author.books.load

# uses the cached copy of books
author.books.size

# discards the cached copy of books and goes back to the database
author.books.reload.empty?
```

Copy

#### [3.2 Avoiding Name Collisions](https://guides.rubyonrails.org/v6.1/association_basics.html\#avoiding-name-collisions)

You are not free to use just any name for your associations. Because creating an association adds a method with that name to the model, it is a bad idea to give an association a name that is already used for an instance method of `ActiveRecord::Base`. The association method would override the base method and break things. For instance, `attributes` or `connection` are bad names for associations.

#### [3.3 Updating the Schema](https://guides.rubyonrails.org/v6.1/association_basics.html\#updating-the-schema)

Associations are extremely useful, but they are not magic. You are responsible for maintaining your database schema to match your associations. In practice, this means two things, depending on what sort of associations you are creating. For `belongs_to` associations you need to create foreign keys, and for `has_and_belongs_to_many` associations you need to create the appropriate join table.

##### [3.3.1 Creating Foreign Keys for `belongs_to` Associations](https://guides.rubyonrails.org/v6.1/association_basics.html\#creating-foreign-keys-for-belongs-to-associations)

When you declare a `belongs_to` association, you need to create foreign keys as appropriate. For example, consider this model:

```
class Book < ApplicationRecord
  belongs_to :author
end
```

Copy

This declaration needs to be backed up by a corresponding foreign key column in the books table. For a brand new table, the migration might look something like this:

```
class CreateBooks < ActiveRecord::Migration[6.0]
  def change
    create_table :books do |t|
      t.datetime   :published_at
      t.string     :book_number
      t.references :author
    end
  end
end
```

Copy

Whereas for an existing table, it might look like this:

```
class AddAuthorToBooks < ActiveRecord::Migration[6.0]
  def change
    add_reference :books, :author
  end
end
```

Copy

If you wish to [enforce referential integrity at the database level](https://guides.rubyonrails.org/active_record_migrations.html#foreign-keys), add the `foreign_key: true` option to the ‘reference’ column declarations above.

##### [3.3.2 Creating Join Tables for `has_and_belongs_to_many` Associations](https://guides.rubyonrails.org/v6.1/association_basics.html\#creating-join-tables-for-has-and-belongs-to-many-associations)

If you create a `has_and_belongs_to_many` association, you need to explicitly create the joining table. Unless the name of the join table is explicitly specified by using the `:join_table` option, Active Record creates the name by using the lexical order of the class names. So a join between author and book models will give the default join table name of "authors\_books" because "a" outranks "b" in lexical ordering.

The precedence between model names is calculated using the `<=>` operator for `String`. This means that if the strings are of different lengths, and the strings are equal when compared up to the shortest length, then the longer string is considered of higher lexical precedence than the shorter one. For example, one would expect the tables "paper\_boxes" and "papers" to generate a join table name of "papers\_paper\_boxes" because of the length of the name "paper\_boxes", but it in fact generates a join table name of "paper\_boxes\_papers" (because the underscore '\_' is lexicographically _less_ than 's' in common encodings).

Whatever the name, you must manually generate the join table with an appropriate migration. For example, consider these associations:

```
class Assembly < ApplicationRecord
  has_and_belongs_to_many :parts
end

class Part < ApplicationRecord
  has_and_belongs_to_many :assemblies
end
```

Copy

These need to be backed up by a migration to create the `assemblies_parts` table. This table should be created without a primary key:

```
class CreateAssembliesPartsJoinTable < ActiveRecord::Migration[6.0]
  def change
    create_table :assemblies_parts, id: false do |t|
      t.bigint :assembly_id
      t.bigint :part_id
    end

    add_index :assemblies_parts, :assembly_id
    add_index :assemblies_parts, :part_id
  end
end
```

Copy

We pass `id: false` to `create_table` because that table does not represent a model. That's required for the association to work properly. If you observe any strange behavior in a `has_and_belongs_to_many` association like mangled model IDs, or exceptions about conflicting IDs, chances are you forgot that bit.

You can also use the method `create_join_table`

```
class CreateAssembliesPartsJoinTable < ActiveRecord::Migration[6.0]
  def change
    create_join_table :assemblies, :parts do |t|
      t.index :assembly_id
      t.index :part_id
    end
  end
end
```

Copy

#### [3.4 Controlling Association Scope](https://guides.rubyonrails.org/v6.1/association_basics.html\#controlling-association-scope)

By default, associations look for objects only within the current module's scope. This can be important when you declare Active Record models within a module. For example:

```
module MyApplication
  module Business
    class Supplier < ApplicationRecord
      has_one :account
    end

    class Account < ApplicationRecord
      belongs_to :supplier
    end
  end
end
```

Copy

This will work fine, because both the `Supplier` and the `Account` class are defined within the same scope. But the following will _not_ work, because `Supplier` and `Account` are defined in different scopes:

```
module MyApplication
  module Business
    class Supplier < ApplicationRecord
      has_one :account
    end
  end

  module Billing
    class Account < ApplicationRecord
      belongs_to :supplier
    end
  end
end
```

Copy

To associate a model with a model in a different namespace, you must specify the complete class name in your association declaration:

```
module MyApplication
  module Business
    class Supplier < ApplicationRecord
      has_one :account,
        class_name: "MyApplication::Billing::Account"
    end
  end

  module Billing
    class Account < ApplicationRecord
      belongs_to :supplier,
        class_name: "MyApplication::Business::Supplier"
    end
  end
end
```

Copy

#### [3.5 Bi-directional Associations](https://guides.rubyonrails.org/v6.1/association_basics.html\#bi-directional-associations)

It's normal for associations to work in two directions, requiring declaration on two different models:

```
class Author < ApplicationRecord
  has_many :books
end

class Book < ApplicationRecord
  belongs_to :author
end
```

Copy

Active Record will attempt to automatically identify that these two models share a bi-directional association based on the association name. In this way, Active Record will only load one copy of the `Author` object, making your application more efficient and preventing inconsistent data:

```
irb> a = Author.first
irb> b = a.books.first
irb> a.first_name == b.author.first_name
=> true
irb> a.first_name = 'David'
irb> a.first_name == b.author.first_name
=> true
```

Copy

Active Record supports automatic identification for most associations with standard names. However, Active Record will not automatically identify bi-directional associations that contain a scope or any of the following options:

- `:through`
- `:foreign_key`

For example, consider the following model declarations:

```
class Author < ApplicationRecord
  has_many :books
end

class Book < ApplicationRecord
  belongs_to :writer, class_name: 'Author', foreign_key: 'author_id'
end
```

Copy

Active Record will no longer automatically recognize the bi-directional association:

```
irb> a = Author.first
irb> b = a.books.first
irb> a.first_name == b.writer.first_name
=> true
irb> a.first_name = 'David'
irb> a.first_name == b.writer.first_name
=> false
```

Copy

Active Record provides the `:inverse_of` option so you can explicitly declare bi-directional associations:

```
class Author < ApplicationRecord
  has_many :books, inverse_of: 'writer'
end

class Book < ApplicationRecord
  belongs_to :writer, class_name: 'Author', foreign_key: 'author_id'
end
```

Copy

By including the `:inverse_of` option in the `has_many` association declaration, Active Record will now recognize the bi-directional association:

```
irb> a = Author.first
irb> b = a.books.first
irb> a.first_name == b.writer.first_name
=> true
irb> a.first_name = 'David'
irb> a.first_name == b.writer.first_name
=> true
```

Copy

### [4 Detailed Association Reference](https://guides.rubyonrails.org/v6.1/association_basics.html\#detailed-association-reference)

The following sections give the details of each type of association, including the methods that they add and the options that you can use when declaring an association.

#### [4.1 `belongs_to` Association Reference](https://guides.rubyonrails.org/v6.1/association_basics.html\#belongs-to-association-reference)

In database terms, the `belongs_to` association says that this model's table contains a column which represents a reference to another table.
This can be used to set up one-to-one or one-to-many relations, depending on the setup.
If the table of the other class contains the reference in a one-to-one relation, then you should use `has_one` instead.

##### [4.1.1 Methods Added by `belongs_to`](https://guides.rubyonrails.org/v6.1/association_basics.html\#methods-added-by-belongs-to)

When you declare a `belongs_to` association, the declaring class automatically gains 6 methods related to the association:

- `association`
- `association=(associate)`
- `build_association(attributes = {})`
- `create_association(attributes = {})`
- `create_association!(attributes = {})`
- `reload_association`

In all of these methods, `association` is replaced with the symbol passed as the first argument to `belongs_to`. For example, given the declaration:

```
class Book < ApplicationRecord
  belongs_to :author
end
```

Copy

Each instance of the `Book` model will have these methods:

```
author
author=
build_author
create_author
create_author!
reload_author
```

Copy

When initializing a new `has_one` or `belongs_to` association you must use the `build_` prefix to build the association, rather than the `association.build` method that would be used for `has_many` or `has_and_belongs_to_many` associations. To create one, use the `create_` prefix.

###### [4.1.1.1 `association`](https://guides.rubyonrails.org/v6.1/association_basics.html\#methods-added-by-belongs-to-association)

The `association` method returns the associated object, if any. If no associated object is found, it returns `nil`.

```
@author = @book.author
```

Copy

If the associated object has already been retrieved from the database for this object, the cached version will be returned. To override this behavior (and force a database read), call `#reload_association` on the parent object.

```
@author = @book.reload_author
```

Copy

###### [4.1.1.2 `association=(associate)`](https://guides.rubyonrails.org/v6.1/association_basics.html\#methods-added-by-belongs-to-association-associate)

The `association=` method assigns an associated object to this object. Behind the scenes, this means extracting the primary key from the associated object and setting this object's foreign key to the same value.

```
@book.author = @author
```

Copy

###### [4.1.1.3 `build_association(attributes = {})`](https://guides.rubyonrails.org/v6.1/association_basics.html\#methods-added-by-belongs-to-build-association-attributes)

The `build_association` method returns a new object of the associated type. This object will be instantiated from the passed attributes, and the link through this object's foreign key will be set, but the associated object will _not_ yet be saved.

```
@author = @book.build_author(author_number: 123,
                             author_name: "John Doe")
```

Copy

###### [4.1.1.4 `create_association(attributes = {})`](https://guides.rubyonrails.org/v6.1/association_basics.html\#methods-added-by-belongs-to-create-association-attributes)

The `create_association` method returns a new object of the associated type. This object will be instantiated from the passed attributes, the link through this object's foreign key will be set, and, once it passes all of the validations specified on the associated model, the associated object _will_ be saved.

```
@author = @book.create_author(author_number: 123,
                              author_name: "John Doe")
```

Copy

###### [4.1.1.5 `create_association!(attributes = {})`](https://guides.rubyonrails.org/v6.1/association_basics.html\#methods-added-by-belongs-to-create-association-bang-attributes)

Does the same as `create_association` above, but raises `ActiveRecord::RecordInvalid` if the record is invalid.

##### [4.1.2 Options for `belongs_to`](https://guides.rubyonrails.org/v6.1/association_basics.html\#options-for-belongs-to)

While Rails uses intelligent defaults that will work well in most situations, there may be times when you want to customize the behavior of the `belongs_to` association reference. Such customizations can easily be accomplished by passing options and scope blocks when you create the association. For example, this association uses two such options:

```
class Book < ApplicationRecord
  belongs_to :author, touch: :books_updated_at,
    counter_cache: true
end
```

Copy

The [`belongs_to`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/ClassMethods.html#method-i-belongs_to) association supports these options:

- `:autosave`
- `:class_name`
- `:counter_cache`
- `:dependent`
- `:foreign_key`
- `:primary_key`
- `:inverse_of`
- `:polymorphic`
- `:touch`
- `:validate`
- `:optional`

###### [4.1.2.1 `:autosave`](https://guides.rubyonrails.org/v6.1/association_basics.html\#options-for-belongs-to-autosave)

If you set the `:autosave` option to `true`, Rails will save any loaded association members and destroy members that are marked for destruction whenever you save the parent object. Setting `:autosave` to `false` is not the same as not setting the `:autosave` option. If the `:autosave` option is not present, then new associated objects will be saved, but updated associated objects will not be saved.

###### [4.1.2.2 `:class_name`](https://guides.rubyonrails.org/v6.1/association_basics.html\#options-for-belongs-to-class-name)

If the name of the other model cannot be derived from the association name, you can use the `:class_name` option to supply the model name. For example, if a book belongs to an author, but the actual name of the model containing authors is `Patron`, you'd set things up this way:

```
class Book < ApplicationRecord
  belongs_to :author, class_name: "Patron"
end
```

Copy

###### [4.1.2.3 `:counter_cache`](https://guides.rubyonrails.org/v6.1/association_basics.html\#options-for-belongs-to-counter-cache)

The `:counter_cache` option can be used to make finding the number of belonging objects more efficient. Consider these models:

```
class Book < ApplicationRecord
  belongs_to :author
end

class Author < ApplicationRecord
  has_many :books
end
```

Copy

With these declarations, asking for the value of `@author.books.size` requires making a call to the database to perform a `COUNT(*)` query. To avoid this call, you can add a counter cache to the _belonging_ model:

```
class Book < ApplicationRecord
  belongs_to :author, counter_cache: true
end

class Author < ApplicationRecord
  has_many :books
end
```

Copy

With this declaration, Rails will keep the cache value up to date, and then return that value in response to the `size` method.

Although the `:counter_cache` option is specified on the model that includes
the `belongs_to` declaration, the actual column must be added to the
_associated_ (`has_many`) model. In the case above, you would need to add a
column named `books_count` to the `Author` model.

You can override the default column name by specifying a custom column name in
the `counter_cache` declaration instead of `true`. For example, to use
`count_of_books` instead of `books_count`:

```
class Book < ApplicationRecord
  belongs_to :author, counter_cache: :count_of_books
end

class Author < ApplicationRecord
  has_many :books
end
```

Copy

You only need to specify the `:counter_cache` option on the `belongs_to`
side of the association.

Counter cache columns are added to the containing model's list of read-only attributes through `attr_readonly`.

###### [4.1.2.4 `:dependent`](https://guides.rubyonrails.org/v6.1/association_basics.html\#options-for-belongs-to-dependent)

If you set the `:dependent` option to:

- `:destroy`, when the object is destroyed, `destroy` will be called on its
associated objects.
- `:delete`, when the object is destroyed, all its associated objects will be
deleted directly from the database without calling their `destroy` method.
- `:destroy_async`: when the object is destroyed, an `ActiveRecord::DestroyAssociationAsyncJob`
job is enqueued which will call destroy on its associated objects. Active Job must be set up
for this to work.

You should not specify this option on a `belongs_to` association that is connected with a `has_many` association on the other class. Doing so can lead to orphaned records in your database.

###### [4.1.2.5 `:foreign_key`](https://guides.rubyonrails.org/v6.1/association_basics.html\#options-for-belongs-to-foreign-key)

By convention, Rails assumes that the column used to hold the foreign key on this model is the name of the association with the suffix `_id` added. The `:foreign_key` option lets you set the name of the foreign key directly:

```
class Book < ApplicationRecord
  belongs_to :author, class_name: "Patron",
                      foreign_key: "patron_id"
end
```

Copy

In any case, Rails will not create foreign key columns for you. You need to explicitly define them as part of your migrations.

###### [4.1.2.6 `:primary_key`](https://guides.rubyonrails.org/v6.1/association_basics.html\#options-for-belongs-to-primary-key)

By convention, Rails assumes that the `id` column is used to hold the primary key
of its tables. The `:primary_key` option allows you to specify a different column.

For example, given we have a `users` table with `guid` as the primary key. If we want a separate `todos` table to hold the foreign key `user_id` in the `guid` column, then we can use `primary_key` to achieve this like so:

```
class User < ApplicationRecord
  self.primary_key = 'guid' # primary key is guid and not id
end

class Todo < ApplicationRecord
  belongs_to :user, primary_key: 'guid'
end
```

Copy

When we execute `@user.todos.create` then the `@todo` record will have its
`user_id` value as the `guid` value of `@user`.

###### [4.1.2.7 `:inverse_of`](https://guides.rubyonrails.org/v6.1/association_basics.html\#options-for-belongs-to-inverse-of)

The `:inverse_of` option specifies the name of the `has_many` or `has_one` association that is the inverse of this association.

```
class Author < ApplicationRecord
  has_many :books, inverse_of: :author
end

class Book < ApplicationRecord
  belongs_to :author, inverse_of: :books
end
```

Copy

###### [4.1.2.8 `:polymorphic`](https://guides.rubyonrails.org/v6.1/association_basics.html\#polymorphic)

Passing `true` to the `:polymorphic` option indicates that this is a polymorphic association. Polymorphic associations were discussed in detail [earlier in this guide](https://guides.rubyonrails.org/v6.1/association_basics.html#polymorphic-associations).

###### [4.1.2.9 `:touch`](https://guides.rubyonrails.org/v6.1/association_basics.html\#options-for-belongs-to-touch)

If you set the `:touch` option to `true`, then the `updated_at` or `updated_on` timestamp on the associated object will be set to the current time whenever this object is saved or destroyed:

```
class Book < ApplicationRecord
  belongs_to :author, touch: true
end

class Author < ApplicationRecord
  has_many :books
end
```

Copy

In this case, saving or destroying a book will update the timestamp on the associated author. You can also specify a particular timestamp attribute to update:

```
class Book < ApplicationRecord
  belongs_to :author, touch: :books_updated_at
end
```

Copy

###### [4.1.2.10 `:validate`](https://guides.rubyonrails.org/v6.1/association_basics.html\#options-for-belongs-to-validate)

If you set the `:validate` option to `true`, then associated objects will be validated whenever you save this object. By default, this is `false`: associated objects will not be validated when this object is saved.

###### [4.1.2.11 `:optional`](https://guides.rubyonrails.org/v6.1/association_basics.html\#optional)

If you set the `:optional` option to `true`, then the presence of the associated
object won't be validated. By default, this option is set to `false`.

##### [4.1.3 Scopes for `belongs_to`](https://guides.rubyonrails.org/v6.1/association_basics.html\#scopes-for-belongs-to)

There may be times when you wish to customize the query used by `belongs_to`. Such customizations can be achieved via a scope block. For example:

```
class Book < ApplicationRecord
  belongs_to :author, -> { where active: true }
end
```

Copy

You can use any of the standard [querying methods](https://guides.rubyonrails.org/v6.1/active_record_querying.html) inside the scope block. The following ones are discussed below:

- `where`
- `includes`
- `readonly`
- `select`

###### [4.1.3.1 `where`](https://guides.rubyonrails.org/v6.1/association_basics.html\#scopes-for-belongs-to-where)

The `where` method lets you specify the conditions that the associated object must meet.

```
class Book < ApplicationRecord
  belongs_to :author, -> { where active: true }
end
```

Copy

###### [4.1.3.2 `includes`](https://guides.rubyonrails.org/v6.1/association_basics.html\#scopes-for-belongs-to-includes)

You can use the `includes` method to specify second-order associations that should be eager-loaded when this association is used. For example, consider these models:

```
class Chapter < ApplicationRecord
  belongs_to :book
end

class Book < ApplicationRecord
  belongs_to :author
  has_many :chapters
end

class Author < ApplicationRecord
  has_many :books
end
```

Copy

If you frequently retrieve authors directly from chapters (`@chapter.book.author`), then you can make your code somewhat more efficient by including authors in the association from chapters to books:

```
class Chapter < ApplicationRecord
  belongs_to :book, -> { includes :author }
end

class Book < ApplicationRecord
  belongs_to :author
  has_many :chapters
end

class Author < ApplicationRecord
  has_many :books
end
```

Copy

There's no need to use `includes` for immediate associations - that is, if you have `Book belongs_to :author`, then the author is eager-loaded automatically when it's needed.

###### [4.1.3.3 `readonly`](https://guides.rubyonrails.org/v6.1/association_basics.html\#scopes-for-belongs-to-readonly)

If you use `readonly`, then the associated object will be read-only when retrieved via the association.

###### [4.1.3.4 `select`](https://guides.rubyonrails.org/v6.1/association_basics.html\#scopes-for-belongs-to-select)

The `select` method lets you override the SQL `SELECT` clause that is used to retrieve data about the associated object. By default, Rails retrieves all columns.

If you use the `select` method on a `belongs_to` association, you should also set the `:foreign_key` option to guarantee the correct results.

##### [4.1.4 Do Any Associated Objects Exist?](https://guides.rubyonrails.org/v6.1/association_basics.html\#belongs-to-association-reference-do-any-associated-objects-exist-questionmark)

You can see if any associated objects exist by using the `association.nil?` method:

```
if @book.author.nil?
  @msg = "No author found for this book"
end
```

Copy

##### [4.1.5 When are Objects Saved?](https://guides.rubyonrails.org/v6.1/association_basics.html\#belongs-to-association-reference-when-are-objects-saved-questionmark)

Assigning an object to a `belongs_to` association does _not_ automatically save the object. It does not save the associated object either.

#### [4.2 `has_one` Association Reference](https://guides.rubyonrails.org/v6.1/association_basics.html\#has-one-association-reference)

The `has_one` association creates a one-to-one match with another model. In database terms, this association says that the other class contains the foreign key. If this class contains the foreign key, then you should use `belongs_to` instead.

##### [4.2.1 Methods Added by `has_one`](https://guides.rubyonrails.org/v6.1/association_basics.html\#methods-added-by-has-one)

When you declare a `has_one` association, the declaring class automatically gains 6 methods related to the association:

- `association`
- `association=(associate)`
- `build_association(attributes = {})`
- `create_association(attributes = {})`
- `create_association!(attributes = {})`
- `reload_association`

In all of these methods, `association` is replaced with the symbol passed as the first argument to `has_one`. For example, given the declaration:

```
class Supplier < ApplicationRecord
  has_one :account
end
```

Copy

Each instance of the `Supplier` model will have these methods:

```
account
account=
build_account
create_account
create_account!
reload_account
```

Copy

When initializing a new `has_one` or `belongs_to` association you must use the `build_` prefix to build the association, rather than the `association.build` method that would be used for `has_many` or `has_and_belongs_to_many` associations. To create one, use the `create_` prefix.

###### [4.2.1.1 `association`](https://guides.rubyonrails.org/v6.1/association_basics.html\#methods-added-by-has-one-association)

The `association` method returns the associated object, if any. If no associated object is found, it returns `nil`.

```
@account = @supplier.account
```

Copy

If the associated object has already been retrieved from the database for this object, the cached version will be returned. To override this behavior (and force a database read), call `#reload_association` on the parent object.

```
@account = @supplier.reload_account
```

Copy

###### [4.2.1.2 `association=(associate)`](https://guides.rubyonrails.org/v6.1/association_basics.html\#methods-added-by-has-one-association-associate)

The `association=` method assigns an associated object to this object. Behind the scenes, this means extracting the primary key from this object and setting the associated object's foreign key to the same value.

```
@supplier.account = @account
```

Copy

###### [4.2.1.3 `build_association(attributes = {})`](https://guides.rubyonrails.org/v6.1/association_basics.html\#methods-added-by-has-one-build-association-attributes)

The `build_association` method returns a new object of the associated type. This object will be instantiated from the passed attributes, and the link through its foreign key will be set, but the associated object will _not_ yet be saved.

```
@account = @supplier.build_account(terms: "Net 30")
```

Copy

###### [4.2.1.4 `create_association(attributes = {})`](https://guides.rubyonrails.org/v6.1/association_basics.html\#methods-added-by-has-one-create-association-attributes)

The `create_association` method returns a new object of the associated type. This object will be instantiated from the passed attributes, the link through its foreign key will be set, and, once it passes all of the validations specified on the associated model, the associated object _will_ be saved.

```
@account = @supplier.create_account(terms: "Net 30")
```

Copy

###### [4.2.1.5 `create_association!(attributes = {})`](https://guides.rubyonrails.org/v6.1/association_basics.html\#methods-added-by-has-one-create-association-bang-attributes)

Does the same as `create_association` above, but raises `ActiveRecord::RecordInvalid` if the record is invalid.

##### [4.2.2 Options for `has_one`](https://guides.rubyonrails.org/v6.1/association_basics.html\#options-for-has-one)

While Rails uses intelligent defaults that will work well in most situations, there may be times when you want to customize the behavior of the `has_one` association reference. Such customizations can easily be accomplished by passing options when you create the association. For example, this association uses two such options:

```
class Supplier < ApplicationRecord
  has_one :account, class_name: "Billing", dependent: :nullify
end
```

Copy

The [`has_one`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/ClassMethods.html#method-i-has_one) association supports these options:

- `:as`
- `:autosave`
- `:class_name`
- `:dependent`
- `:foreign_key`
- `:inverse_of`
- `:primary_key`
- `:source`
- `:source_type`
- `:through`
- `:touch`
- `:validate`

###### [4.2.2.1 `:as`](https://guides.rubyonrails.org/v6.1/association_basics.html\#options-for-has-one-as)

Setting the `:as` option indicates that this is a polymorphic association. Polymorphic associations were discussed in detail [earlier in this guide](https://guides.rubyonrails.org/v6.1/association_basics.html#polymorphic-associations).

###### [4.2.2.2 `:autosave`](https://guides.rubyonrails.org/v6.1/association_basics.html\#options-for-has-one-autosave)

If you set the `:autosave` option to `true`, Rails will save any loaded association members and destroy members that are marked for destruction whenever you save the parent object. Setting `:autosave` to `false` is not the same as not setting the `:autosave` option. If the `:autosave` option is not present, then new associated objects will be saved, but updated associated objects will not be saved.

###### [4.2.2.3 `:class_name`](https://guides.rubyonrails.org/v6.1/association_basics.html\#options-for-has-one-class-name)

If the name of the other model cannot be derived from the association name, you can use the `:class_name` option to supply the model name. For example, if a supplier has an account, but the actual name of the model containing accounts is `Billing`, you'd set things up this way:

```
class Supplier < ApplicationRecord
  has_one :account, class_name: "Billing"
end
```

Copy

###### [4.2.2.4 `:dependent`](https://guides.rubyonrails.org/v6.1/association_basics.html\#options-for-has-one-dependent)

Controls what happens to the associated object when its owner is destroyed:

- `:destroy` causes the associated object to also be destroyed
- `:delete` causes the associated object to be deleted directly from the database (so callbacks will not execute)
- `:destroy_async`: when the object is destroyed, an `ActiveRecord::DestroyAssociationAsyncJob` job is enqueued which will call destroy on its associated objects. Active Job must be set up for this to work.
- `:nullify` causes the foreign key to be set to `NULL`. Polymorphic type column is also nullified on polymorphic associations. Callbacks are not executed.
- `:restrict_with_exception` causes an `ActiveRecord::DeleteRestrictionError` exception to be raised if there is an associated record
- `:restrict_with_error` causes an error to be added to the owner if there is an associated object

It's necessary not to set or leave `:nullify` option for those associations
that have `NOT NULL` database constraints. If you don't set `dependent` to
destroy such associations you won't be able to change the associated object
because the initial associated object's foreign key will be set to the
unallowed `NULL` value.

###### [4.2.2.5 `:foreign_key`](https://guides.rubyonrails.org/v6.1/association_basics.html\#options-for-has-one-foreign-key)

By convention, Rails assumes that the column used to hold the foreign key on the other model is the name of this model with the suffix `_id` added. The `:foreign_key` option lets you set the name of the foreign key directly:

```
class Supplier < ApplicationRecord
  has_one :account, foreign_key: "supp_id"
end
```

Copy

In any case, Rails will not create foreign key columns for you. You need to explicitly define them as part of your migrations.

###### [4.2.2.6 `:inverse_of`](https://guides.rubyonrails.org/v6.1/association_basics.html\#options-for-has-one-inverse-of)

The `:inverse_of` option specifies the name of the `belongs_to` association that is the inverse of this association.

```
class Supplier < ApplicationRecord
  has_one :account, inverse_of: :supplier
end

class Account < ApplicationRecord
  belongs_to :supplier, inverse_of: :account
end
```

Copy

###### [4.2.2.7 `:primary_key`](https://guides.rubyonrails.org/v6.1/association_basics.html\#options-for-has-one-primary-key)

By convention, Rails assumes that the column used to hold the primary key of this model is `id`. You can override this and explicitly specify the primary key with the `:primary_key` option.

###### [4.2.2.8 `:source`](https://guides.rubyonrails.org/v6.1/association_basics.html\#options-for-has-one-source)

The `:source` option specifies the source association name for a `has_one :through` association.

###### [4.2.2.9 `:source_type`](https://guides.rubyonrails.org/v6.1/association_basics.html\#options-for-has-one-source-type)

The `:source_type` option specifies the source association type for a `has_one :through` association that proceeds through a polymorphic association.

```
class Author < ApplicationRecord
  has_one :book
  has_one :hardback, through: :book, source: :format, source_type: "Hardback"
  has_one :dust_jacket, through: :hardback
end

class Book < ApplicationRecord
  belongs_to :format, polymorphic: true
end

class Paperback < ApplicationRecord; end

class Hardback < ApplicationRecord
  has_one :dust_jacket
end

class DustJacket < ApplicationRecord; end
```

Copy

###### [4.2.2.10 `:through`](https://guides.rubyonrails.org/v6.1/association_basics.html\#options-for-has-one-through)

The `:through` option specifies a join model through which to perform the query. `has_one :through` associations were discussed in detail [earlier in this guide](https://guides.rubyonrails.org/v6.1/association_basics.html#the-has-one-through-association).

###### [4.2.2.11 `:touch`](https://guides.rubyonrails.org/v6.1/association_basics.html\#options-for-has-one-touch)

If you set the `:touch` option to `true`, then the `updated_at` or `updated_on` timestamp on the associated object will be set to the current time whenever this object is saved or destroyed:

```
class Supplier < ApplicationRecord
  has_one :account, touch: true
end

class Account < ApplicationRecord
  belongs_to :supplier
end
```

Copy

In this case, saving or destroying a supplier will update the timestamp on the associated account. You can also specify a particular timestamp attribute to update:

```
class Supplier < ApplicationRecord
  has_one :account, touch: :suppliers_updated_at
end
```

Copy

###### [4.2.2.12 `:validate`](https://guides.rubyonrails.org/v6.1/association_basics.html\#options-for-has-one-validate)

If you set the `:validate` option to `true`, then associated objects will be validated whenever you save this object. By default, this is `false`: associated objects will not be validated when this object is saved.

##### [4.2.3 Scopes for `has_one`](https://guides.rubyonrails.org/v6.1/association_basics.html\#scopes-for-has-one)

There may be times when you wish to customize the query used by `has_one`. Such customizations can be achieved via a scope block. For example:

```
class Supplier < ApplicationRecord
  has_one :account, -> { where active: true }
end
```

Copy

You can use any of the standard [querying methods](https://guides.rubyonrails.org/v6.1/active_record_querying.html) inside the scope block. The following ones are discussed below:

- `where`
- `includes`
- `readonly`
- `select`

###### [4.2.3.1 `where`](https://guides.rubyonrails.org/v6.1/association_basics.html\#scopes-for-has-one-where)

The `where` method lets you specify the conditions that the associated object must meet.

```
class Supplier < ApplicationRecord
  has_one :account, -> { where "confirmed = 1" }
end
```

Copy

###### [4.2.3.2 `includes`](https://guides.rubyonrails.org/v6.1/association_basics.html\#scopes-for-has-one-includes)

You can use the `includes` method to specify second-order associations that should be eager-loaded when this association is used. For example, consider these models:

```
class Supplier < ApplicationRecord
  has_one :account
end

class Account < ApplicationRecord
  belongs_to :supplier
  belongs_to :representative
end

class Representative < ApplicationRecord
  has_many :accounts
end
```

Copy

If you frequently retrieve representatives directly from suppliers (`@supplier.account.representative`), then you can make your code somewhat more efficient by including representatives in the association from suppliers to accounts:

```
class Supplier < ApplicationRecord
  has_one :account, -> { includes :representative }
end

class Account < ApplicationRecord
  belongs_to :supplier
  belongs_to :representative
end

class Representative < ApplicationRecord
  has_many :accounts
end
```

Copy

###### [4.2.3.3 `readonly`](https://guides.rubyonrails.org/v6.1/association_basics.html\#scopes-for-has-one-readonly)

If you use the `readonly` method, then the associated object will be read-only when retrieved via the association.

###### [4.2.3.4 `select`](https://guides.rubyonrails.org/v6.1/association_basics.html\#scopes-for-has-one-select)

The `select` method lets you override the SQL `SELECT` clause that is used to retrieve data about the associated object. By default, Rails retrieves all columns.

##### [4.2.4 Do Any Associated Objects Exist?](https://guides.rubyonrails.org/v6.1/association_basics.html\#has-one-association-reference-do-any-associated-objects-exist-questionmark)

You can see if any associated objects exist by using the `association.nil?` method:

```
if @supplier.account.nil?
  @msg = "No account found for this supplier"
end
```

Copy

##### [4.2.5 When are Objects Saved?](https://guides.rubyonrails.org/v6.1/association_basics.html\#has-one-association-reference-when-are-objects-saved-questionmark)

When you assign an object to a `has_one` association, that object is automatically saved (in order to update its foreign key). In addition, any object being replaced is also automatically saved, because its foreign key will change too.

If either of these saves fails due to validation errors, then the assignment statement returns `false` and the assignment itself is cancelled.

If the parent object (the one declaring the `has_one` association) is unsaved (that is, `new_record?` returns `true`) then the child objects are not saved. They will automatically when the parent object is saved.

If you want to assign an object to a `has_one` association without saving the object, use the `build_association` method.

#### [4.3 `has_many` Association Reference](https://guides.rubyonrails.org/v6.1/association_basics.html\#has-many-association-reference)

The `has_many` association creates a one-to-many relationship with another model. In database terms, this association says that the other class will have a foreign key that refers to instances of this class.

##### [4.3.1 Methods Added by `has_many`](https://guides.rubyonrails.org/v6.1/association_basics.html\#methods-added-by-has-many)

When you declare a `has_many` association, the declaring class automatically gains 17 methods related to the association:

- `collection`
- [`collection<<(object, ...)`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/CollectionProxy.html#method-i-3C-3C)
- [`collection.delete(object, ...)`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/CollectionProxy.html#method-i-delete)
- [`collection.destroy(object, ...)`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/CollectionProxy.html#method-i-destroy)
- `collection=(objects)`
- `collection_singular_ids`
- `collection_singular_ids=(ids)`
- [`collection.clear`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/CollectionProxy.html#method-i-clear)
- [`collection.empty?`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/CollectionProxy.html#method-i-empty-3F)
- [`collection.size`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/CollectionProxy.html#method-i-size)
- [`collection.find(...)`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/CollectionProxy.html#method-i-find)
- [`collection.where(...)`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/QueryMethods.html#method-i-where)
- [`collection.exists?(...)`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/FinderMethods.html#method-i-exists-3F)
- [`collection.build(attributes = {})`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/CollectionProxy.html#method-i-build)
- [`collection.create(attributes = {})`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/CollectionProxy.html#method-i-create)
- [`collection.create!(attributes = {})`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/CollectionProxy.html#method-i-create-21)
- [`collection.reload`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/CollectionProxy.html#method-i-reload)

In all of these methods, `collection` is replaced with the symbol passed as the first argument to `has_many`, and `collection_singular` is replaced with the singularized version of that symbol. For example, given the declaration:

```
class Author < ApplicationRecord
  has_many :books
end
```

Copy

Each instance of the `Author` model will have these methods:

```
books
books<<(object, ...)
books.delete(object, ...)
books.destroy(object, ...)
books=(objects)
book_ids
book_ids=(ids)
books.clear
books.empty?
books.size
books.find(...)
books.where(...)
books.exists?(...)
books.build(attributes = {}, ...)
books.create(attributes = {})
books.create!(attributes = {})
books.reload
```

Copy

###### [4.3.1.1 `collection`](https://guides.rubyonrails.org/v6.1/association_basics.html\#methods-added-by-has-many-collection)

The `collection` method returns a Relation of all of the associated objects. If there are no associated objects, it returns an empty Relation.

```
@books = @author.books
```

Copy

###### [4.3.1.2 `collection<<(object, ...)`](https://guides.rubyonrails.org/v6.1/association_basics.html\#methods-added-by-has-many-collection-object)

The [`collection<<`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/CollectionProxy.html#method-i-3C-3C) method adds one or more objects to the collection by setting their foreign keys to the primary key of the calling model.

```
@author.books << @book1
```

Copy

###### [4.3.1.3 `collection.delete(object, ...)`](https://guides.rubyonrails.org/v6.1/association_basics.html\#methods-added-by-has-many-collection-delete-object)

The [`collection.delete`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/CollectionProxy.html#method-i-delete) method removes one or more objects from the collection by setting their foreign keys to `NULL`.

```
@author.books.delete(@book1)
```

Copy

Additionally, objects will be destroyed if they're associated with `dependent: :destroy`, and deleted if they're associated with `dependent: :delete_all`.

###### [4.3.1.4 `collection.destroy(object, ...)`](https://guides.rubyonrails.org/v6.1/association_basics.html\#methods-added-by-has-many-collection-destroy-object)

The [`collection.destroy`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/CollectionProxy.html#method-i-destroy) method removes one or more objects from the collection by running `destroy` on each object.

```
@author.books.destroy(@book1)
```

Copy

Objects will _always_ be removed from the database, ignoring the `:dependent` option.

###### [4.3.1.5 `collection=(objects)`](https://guides.rubyonrails.org/v6.1/association_basics.html\#methods-added-by-has-many-collection-objects)

The `collection=` method makes the collection contain only the supplied objects, by adding and deleting as appropriate. The changes are persisted to the database.

###### [4.3.1.6 `collection_singular_ids`](https://guides.rubyonrails.org/v6.1/association_basics.html\#methods-added-by-has-many-collection-singular-ids)

The `collection_singular_ids` method returns an array of the ids of the objects in the collection.

```
@book_ids = @author.book_ids
```

Copy

###### [4.3.1.7 `collection_singular_ids=(ids)`](https://guides.rubyonrails.org/v6.1/association_basics.html\#methods-added-by-has-many-collection-singular-ids-ids)

The `collection_singular_ids=` method makes the collection contain only the objects identified by the supplied primary key values, by adding and deleting as appropriate. The changes are persisted to the database.

###### [4.3.1.8 `collection.clear`](https://guides.rubyonrails.org/v6.1/association_basics.html\#methods-added-by-has-many-collection-clear)

The [`collection.clear`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/CollectionProxy.html#method-i-clear) method removes all objects from the collection according to the strategy specified by the `dependent` option. If no option is given, it follows the default strategy. The default strategy for `has_many :through` associations is `delete_all`, and for `has_many` associations is to set the foreign keys to `NULL`.

```
@author.books.clear
```

Copy

Objects will be deleted if they're associated with `dependent: :destroy` or `dependent: :destroy_async`,
just like `dependent: :delete_all`.

###### [4.3.1.9 `collection.empty?`](https://guides.rubyonrails.org/v6.1/association_basics.html\#methods-added-by-has-many-collection-empty-questionmark)

The [`collection.empty?`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/CollectionProxy.html#method-i-empty-3F) method returns `true` if the collection does not contain any associated objects.

```
<% if @author.books.empty? %>
  No Books Found
<% end %>
```

Copy

###### [4.3.1.10 `collection.size`](https://guides.rubyonrails.org/v6.1/association_basics.html\#methods-added-by-has-many-collection-size)

The [`collection.size`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/CollectionProxy.html#method-i-size) method returns the number of objects in the collection.

```
@book_count = @author.books.size
```

Copy

###### [4.3.1.11 `collection.find(...)`](https://guides.rubyonrails.org/v6.1/association_basics.html\#methods-added-by-has-many-collection-find)

The [`collection.find`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/CollectionProxy.html#method-i-find) method finds objects within the collection's table.

```
@available_book = @author.books.find(1)
```

Copy

###### [4.3.1.12 `collection.where(...)`](https://guides.rubyonrails.org/v6.1/association_basics.html\#methods-added-by-has-many-collection-where)

The [`collection.where`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/QueryMethods.html#method-i-where) method finds objects within the collection based on the conditions supplied but the objects are loaded lazily meaning that the database is queried only when the object(s) are accessed.

```
@available_books = @author.books.where(available: true) # No query yet
@available_book = @available_books.first # Now the database will be queried
```

Copy

###### [4.3.1.13 `collection.exists?(...)`](https://guides.rubyonrails.org/v6.1/association_basics.html\#methods-added-by-has-many-collection-exists-questionmark)

The [`collection.exists?`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/FinderMethods.html#method-i-exists-3F) method checks whether an object meeting the supplied
conditions exists in the collection's table.

###### [4.3.1.14 `collection.build(attributes = {})`](https://guides.rubyonrails.org/v6.1/association_basics.html\#methods-added-by-has-many-collection-build-attributes)

The [`collection.build`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/CollectionProxy.html#method-i-build) method returns a single or array of new objects of the associated type. The object(s) will be instantiated from the passed attributes, and the link through their foreign key will be created, but the associated objects will _not_ yet be saved.

```
@book = @author.books.build(published_at: Time.now,
                            book_number: "A12345")

@books = @author.books.build([\
  { published_at: Time.now, book_number: "A12346" },\
  { published_at: Time.now, book_number: "A12347" }\
])
```

Copy

###### [4.3.1.15 `collection.create(attributes = {})`](https://guides.rubyonrails.org/v6.1/association_basics.html\#methods-added-by-has-many-collection-create-attributes)

The [`collection.create`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/CollectionProxy.html#method-i-create) method returns a single or array of new objects of the associated type. The object(s) will be instantiated from the passed attributes, the link through its foreign key will be created, and, once it passes all of the validations specified on the associated model, the associated object _will_ be saved.

```
@book = @author.books.create(published_at: Time.now,
                             book_number: "A12345")

@books = @author.books.create([\
  { published_at: Time.now, book_number: "A12346" },\
  { published_at: Time.now, book_number: "A12347" }\
])
```

Copy

###### [4.3.1.16 `collection.create!(attributes = {})`](https://guides.rubyonrails.org/v6.1/association_basics.html\#methods-added-by-has-many-collection-create-bang-attributes)

Does the same as `collection.create` above, but raises `ActiveRecord::RecordInvalid` if the record is invalid.

###### [4.3.1.17 `collection.reload`](https://guides.rubyonrails.org/v6.1/association_basics.html\#methods-added-by-has-many-collection-reload)

The [`collection.reload`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/CollectionProxy.html#method-i-reload) method returns a Relation of all of the associated objects, forcing a database read. If there are no associated objects, it returns an empty Relation.

```
@books = @author.books.reload
```

Copy

##### [4.3.2 Options for `has_many`](https://guides.rubyonrails.org/v6.1/association_basics.html\#options-for-has-many)

While Rails uses intelligent defaults that will work well in most situations, there may be times when you want to customize the behavior of the `has_many` association reference. Such customizations can easily be accomplished by passing options when you create the association. For example, this association uses two such options:

```
class Author < ApplicationRecord
  has_many :books, dependent: :delete_all, validate: false
end
```

Copy

The [`has_many`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/ClassMethods.html#method-i-has_many) association supports these options:

- `:as`
- `:autosave`
- `:class_name`
- `:counter_cache`
- `:dependent`
- `:foreign_key`
- `:inverse_of`
- `:primary_key`
- `:source`
- `:source_type`
- `:through`
- `:validate`

###### [4.3.2.1 `:as`](https://guides.rubyonrails.org/v6.1/association_basics.html\#options-for-has-many-as)

Setting the `:as` option indicates that this is a polymorphic association, as discussed [earlier in this guide](https://guides.rubyonrails.org/v6.1/association_basics.html#polymorphic-associations).

###### [4.3.2.2 `:autosave`](https://guides.rubyonrails.org/v6.1/association_basics.html\#options-for-has-many-autosave)

If you set the `:autosave` option to `true`, Rails will save any loaded association members and destroy members that are marked for destruction whenever you save the parent object. Setting `:autosave` to `false` is not the same as not setting the `:autosave` option. If the `:autosave` option is not present, then new associated objects will be saved, but updated associated objects will not be saved.

###### [4.3.2.3 `:class_name`](https://guides.rubyonrails.org/v6.1/association_basics.html\#options-for-has-many-class-name)

If the name of the other model cannot be derived from the association name, you can use the `:class_name` option to supply the model name. For example, if an author has many books, but the actual name of the model containing books is `Transaction`, you'd set things up this way:

```
class Author < ApplicationRecord
  has_many :books, class_name: "Transaction"
end
```

Copy

###### [4.3.2.4 `:counter_cache`](https://guides.rubyonrails.org/v6.1/association_basics.html\#options-for-has-many-counter-cache)

This option can be used to configure a custom named `:counter_cache`. You only need this option when you customized the name of your `:counter_cache` on the [belongs\_to association](https://guides.rubyonrails.org/v6.1/association_basics.html#options-for-belongs-to).

###### [4.3.2.5 `:dependent`](https://guides.rubyonrails.org/v6.1/association_basics.html\#dependent)

Controls what happens to the associated objects when their owner is destroyed:

- `:destroy` causes all the associated objects to also be destroyed
- `:delete_all` causes all the associated objects to be deleted directly from the database (so callbacks will not execute)
- `:destroy_async`: when the object is destroyed, an `ActiveRecord::DestroyAssociationAsyncJob` job is enqueued which will call destroy on its associated objects. Active Job must be set up for this to work.
- `:nullify` causes the foreign key to be set to `NULL`. Polymorphic type column is also nullified on polymorphic associations. Callbacks are not executed.
- `:restrict_with_exception` causes an `ActiveRecord::DeleteRestrictionError` exception to be raised if there are any associated records
- `:restrict_with_error` causes an error to be added to the owner if there are any associated objects

The `:destroy` and `:delete_all` options also affect the semantics of the `collection.delete` and `collection=` methods by causing them to destroy associated objects when they are removed from the collection.

###### [4.3.2.6 `:foreign_key`](https://guides.rubyonrails.org/v6.1/association_basics.html\#options-for-has-many-foreign-key)

By convention, Rails assumes that the column used to hold the foreign key on the other model is the name of this model with the suffix `_id` added. The `:foreign_key` option lets you set the name of the foreign key directly:

```
class Author < ApplicationRecord
  has_many :books, foreign_key: "cust_id"
end
```

Copy

In any case, Rails will not create foreign key columns for you. You need to explicitly define them as part of your migrations.

###### [4.3.2.7 `:inverse_of`](https://guides.rubyonrails.org/v6.1/association_basics.html\#inverse-of)

The `:inverse_of` option specifies the name of the `belongs_to` association that is the inverse of this association.

```
class Author < ApplicationRecord
  has_many :books, inverse_of: :author
end

class Book < ApplicationRecord
  belongs_to :author, inverse_of: :books
end
```

Copy

###### [4.3.2.8 `:primary_key`](https://guides.rubyonrails.org/v6.1/association_basics.html\#primary-key)

By convention, Rails assumes that the column used to hold the primary key of the association is `id`. You can override this and explicitly specify the primary key with the `:primary_key` option.

Let's say the `users` table has `id` as the primary\_key but it also
has a `guid` column. The requirement is that the `todos` table should
hold the `guid` column value as the foreign key and not `id`
value. This can be achieved like this:

```
class User < ApplicationRecord
  has_many :todos, primary_key: :guid
end
```

Copy

Now if we execute `@todo = @user.todos.create` then the `@todo`
record's `user_id` value will be the `guid` value of `@user`.

###### [4.3.2.9 `:source`](https://guides.rubyonrails.org/v6.1/association_basics.html\#options-for-has-many-source)

The `:source` option specifies the source association name for a `has_many :through` association. You only need to use this option if the name of the source association cannot be automatically inferred from the association name.

###### [4.3.2.10 `:source_type`](https://guides.rubyonrails.org/v6.1/association_basics.html\#options-for-has-many-source-type)

The `:source_type` option specifies the source association type for a `has_many :through` association that proceeds through a polymorphic association.

```
class Author < ApplicationRecord
  has_many :books
  has_many :paperbacks, through: :books, source: :format, source_type: "Paperback"
end

class Book < ApplicationRecord
  belongs_to :format, polymorphic: true
end

class Hardback < ApplicationRecord; end
class Paperback < ApplicationRecord; end
```

Copy

###### [4.3.2.11 `:through`](https://guides.rubyonrails.org/v6.1/association_basics.html\#options-for-has-many-through)

The `:through` option specifies a join model through which to perform the query. `has_many :through` associations provide a way to implement many-to-many relationships, as discussed [earlier in this guide](https://guides.rubyonrails.org/v6.1/association_basics.html#the-has-many-through-association).

###### [4.3.2.12 `:validate`](https://guides.rubyonrails.org/v6.1/association_basics.html\#options-for-has-many-validate)

If you set the `:validate` option to `false`, then associated objects will not be validated whenever you save this object. By default, this is `true`: associated objects will be validated when this object is saved.

##### [4.3.3 Scopes for `has_many`](https://guides.rubyonrails.org/v6.1/association_basics.html\#scopes-for-has-many)

There may be times when you wish to customize the query used by `has_many`. Such customizations can be achieved via a scope block. For example:

```
class Author < ApplicationRecord
  has_many :books, -> { where processed: true }
end
```

Copy

You can use any of the standard [querying methods](https://guides.rubyonrails.org/v6.1/active_record_querying.html) inside the scope block. The following ones are discussed below:

- `where`
- `extending`
- `group`
- `includes`
- `limit`
- `offset`
- `order`
- `readonly`
- `select`
- `distinct`

###### [4.3.3.1 `where`](https://guides.rubyonrails.org/v6.1/association_basics.html\#scopes-for-has-many-where)

The `where` method lets you specify the conditions that the associated object must meet.

```
class Author < ApplicationRecord
  has_many :confirmed_books, -> { where "confirmed = 1" },
    class_name: "Book"
end
```

Copy

You can also set conditions via a hash:

```
class Author < ApplicationRecord
  has_many :confirmed_books, -> { where confirmed: true },
    class_name: "Book"
end
```

Copy

If you use a hash-style `where` option, then record creation via this association will be automatically scoped using the hash. In this case, using `@author.confirmed_books.create` or `@author.confirmed_books.build` will create books where the confirmed column has the value `true`.

###### [4.3.3.2 `extending`](https://guides.rubyonrails.org/v6.1/association_basics.html\#scopes-for-has-many-extending)

The `extending` method specifies a named module to extend the association proxy. Association extensions are discussed in detail [later in this guide](https://guides.rubyonrails.org/v6.1/association_basics.html#association-extensions).

###### [4.3.3.3 `group`](https://guides.rubyonrails.org/v6.1/association_basics.html\#scopes-for-has-many-group)

The `group` method supplies an attribute name to group the result set by, using a `GROUP BY` clause in the finder SQL.

```
class Author < ApplicationRecord
  has_many :chapters, -> { group 'books.id' },
                      through: :books
end
```

Copy

###### [4.3.3.4 `includes`](https://guides.rubyonrails.org/v6.1/association_basics.html\#scopes-for-has-many-includes)

You can use the `includes` method to specify second-order associations that should be eager-loaded when this association is used. For example, consider these models:

```
class Author < ApplicationRecord
  has_many :books
end

class Book < ApplicationRecord
  belongs_to :author
  has_many :chapters
end

class Chapter < ApplicationRecord
  belongs_to :book
end
```

Copy

If you frequently retrieve chapters directly from authors (`@author.books.chapters`), then you can make your code somewhat more efficient by including chapters in the association from authors to books:

```
class Author < ApplicationRecord
  has_many :books, -> { includes :chapters }
end

class Book < ApplicationRecord
  belongs_to :author
  has_many :chapters
end

class Chapter < ApplicationRecord
  belongs_to :book
end
```

Copy

###### [4.3.3.5 `limit`](https://guides.rubyonrails.org/v6.1/association_basics.html\#scopes-for-has-many-limit)

The `limit` method lets you restrict the total number of objects that will be fetched through an association.

```
class Author < ApplicationRecord
  has_many :recent_books,
    -> { order('published_at desc').limit(100) },
    class_name: "Book"
end
```

Copy

###### [4.3.3.6 `offset`](https://guides.rubyonrails.org/v6.1/association_basics.html\#scopes-for-has-many-offset)

The `offset` method lets you specify the starting offset for fetching objects via an association. For example, `-> { offset(11) }` will skip the first 11 records.

###### [4.3.3.7 `order`](https://guides.rubyonrails.org/v6.1/association_basics.html\#scopes-for-has-many-order)

The `order` method dictates the order in which associated objects will be received (in the syntax used by an SQL `ORDER BY` clause).

```
class Author < ApplicationRecord
  has_many :books, -> { order "date_confirmed DESC" }
end
```

Copy

###### [4.3.3.8 `readonly`](https://guides.rubyonrails.org/v6.1/association_basics.html\#scopes-for-has-many-readonly)

If you use the `readonly` method, then the associated objects will be read-only when retrieved via the association.

###### [4.3.3.9 `select`](https://guides.rubyonrails.org/v6.1/association_basics.html\#scopes-for-has-many-select)

The `select` method lets you override the SQL `SELECT` clause that is used to retrieve data about the associated objects. By default, Rails retrieves all columns.

If you specify your own `select`, be sure to include the primary key and foreign key columns of the associated model. If you do not, Rails will throw an error.

###### [4.3.3.10 `distinct`](https://guides.rubyonrails.org/v6.1/association_basics.html\#scopes-for-has-many-distinct)

Use the `distinct` method to keep the collection free of duplicates. This is
mostly useful together with the `:through` option.

```
class Person < ApplicationRecord
  has_many :readings
  has_many :articles, through: :readings
end
```

Copy

```
irb> person = Person.create(name: 'John')
irb> article = Article.create(name: 'a1')
irb> person.articles << article
irb> person.articles << article
irb> person.articles.to_a
=> [#<Article id: 5, name: "a1">, #<Article id: 5, name: "a1">]
irb> Reading.all.to_a
=> [#<Reading id: 12, person_id: 5, article_id: 5>, #<Reading id: 13, person_id: 5, article_id: 5>]
```

Copy

In the above case there are two readings and `person.articles` brings out both of
them even though these records are pointing to the same article.

Now let's set `distinct`:

```
class Person
  has_many :readings
  has_many :articles, -> { distinct }, through: :readings
end
```

Copy

```
irb> person = Person.create(name: 'Honda')
irb> article = Article.create(name: 'a1')
irb> person.articles << article
irb> person.articles << article
irb> person.articles.to_a
=> [#<Article id: 7, name: "a1">]
irb> Reading.all.to_a
=> [#<Reading id: 16, person_id: 7, article_id: 7>, #<Reading id: 17, person_id: 7, article_id: 7>]
```

Copy

In the above case there are still two readings. However `person.articles` shows
only one article because the collection loads only unique records.

If you want to make sure that, upon insertion, all of the records in the
persisted association are distinct (so that you can be sure that when you
inspect the association that you will never find duplicate records), you should
add a unique index on the table itself. For example, if you have a table named
`readings` and you want to make sure the articles can only be added to a person once,
you could add the following in a migration:

```
add_index :readings, [:person_id, :article_id], unique: true
```

Copy

Once you have this unique index, attempting to add the article to a person twice
will raise an `ActiveRecord::RecordNotUnique` error:

```
irb> person = Person.create(name: 'Honda')
irb> article = Article.create(name: 'a1')
irb> person.articles << article
irb> person.articles << article
ActiveRecord::RecordNotUnique
```

Copy

Note that checking for uniqueness using something like `include?` is subject
to race conditions. Do not attempt to use `include?` to enforce distinctness
in an association. For instance, using the article example from above, the
following code would be racy because multiple users could be attempting this
at the same time:

```
person.articles << article unless person.articles.include?(article)
```

Copy

##### [4.3.4 When are Objects Saved?](https://guides.rubyonrails.org/v6.1/association_basics.html\#has-many-association-reference-when-are-objects-saved-questionmark)

When you assign an object to a `has_many` association, that object is automatically saved (in order to update its foreign key). If you assign multiple objects in one statement, then they are all saved.

If any of these saves fails due to validation errors, then the assignment statement returns `false` and the assignment itself is cancelled.

If the parent object (the one declaring the `has_many` association) is unsaved (that is, `new_record?` returns `true`) then the child objects are not saved when they are added. All unsaved members of the association will automatically be saved when the parent is saved.

If you want to assign an object to a `has_many` association without saving the object, use the `collection.build` method.

#### [4.4 `has_and_belongs_to_many` Association Reference](https://guides.rubyonrails.org/v6.1/association_basics.html\#has-and-belongs-to-many-association-reference)

The `has_and_belongs_to_many` association creates a many-to-many relationship with another model. In database terms, this associates two classes via an intermediate join table that includes foreign keys referring to each of the classes.

##### [4.4.1 Methods Added by `has_and_belongs_to_many`](https://guides.rubyonrails.org/v6.1/association_basics.html\#methods-added-by-has-and-belongs-to-many)

When you declare a `has_and_belongs_to_many` association, the declaring class automatically gains several methods related to the association:

- `collection`
- [`collection<<(object, ...)`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/CollectionProxy.html#method-i-3C-3C)
- [`collection.delete(object, ...)`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/CollectionProxy.html#method-i-delete)
- [`collection.destroy(object, ...)`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/CollectionProxy.html#method-i-destroy)
- `collection=(objects)`
- `collection_singular_ids`
- `collection_singular_ids=(ids)`
- [`collection.clear`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/CollectionProxy.html#method-i-clear)
- [`collection.empty?`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/CollectionProxy.html#method-i-empty-3F)
- [`collection.size`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/CollectionProxy.html#method-i-size)
- [`collection.find(...)`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/CollectionProxy.html#method-i-find)
- [`collection.where(...)`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/QueryMethods.html#method-i-where)
- [`collection.exists?(...)`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/FinderMethods.html#method-i-exists-3F)
- [`collection.build(attributes = {})`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/CollectionProxy.html#method-i-build)
- [`collection.create(attributes = {})`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/CollectionProxy.html#method-i-create)
- [`collection.create!(attributes = {})`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/CollectionProxy.html#method-i-create-21)
- [`collection.reload`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/CollectionProxy.html#method-i-reload)

In all of these methods, `collection` is replaced with the symbol passed as the first argument to `has_and_belongs_to_many`, and `collection_singular` is replaced with the singularized version of that symbol. For example, given the declaration:

```
class Part < ApplicationRecord
  has_and_belongs_to_many :assemblies
end
```

Copy

Each instance of the `Part` model will have these methods:

```
assemblies
assemblies<<(object, ...)
assemblies.delete(object, ...)
assemblies.destroy(object, ...)
assemblies=(objects)
assembly_ids
assembly_ids=(ids)
assemblies.clear
assemblies.empty?
assemblies.size
assemblies.find(...)
assemblies.where(...)
assemblies.exists?(...)
assemblies.build(attributes = {}, ...)
assemblies.create(attributes = {})
assemblies.create!(attributes = {})
assemblies.reload
```

Copy

###### [4.4.1.1 Additional Column Methods](https://guides.rubyonrails.org/v6.1/association_basics.html\#additional-column-methods)

If the join table for a `has_and_belongs_to_many` association has additional columns beyond the two foreign keys, these columns will be added as attributes to records retrieved via that association. Records returned with additional attributes will always be read-only, because Rails cannot save changes to those attributes.

The use of extra attributes on the join table in a `has_and_belongs_to_many` association is deprecated. If you require this sort of complex behavior on the table that joins two models in a many-to-many relationship, you should use a `has_many :through` association instead of `has_and_belongs_to_many`.

###### [4.4.1.2 `collection`](https://guides.rubyonrails.org/v6.1/association_basics.html\#methods-added-by-has-and-belongs-to-many-collection)

The `collection` method returns a Relation of all of the associated objects. If there are no associated objects, it returns an empty Relation.

```
@assemblies = @part.assemblies
```

Copy

###### [4.4.1.3 `collection<<(object, ...)`](https://guides.rubyonrails.org/v6.1/association_basics.html\#methods-added-by-has-and-belongs-to-many-collection-object)

The [`collection<<`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/CollectionProxy.html#method-i-3C-3C) method adds one or more objects to the collection by creating records in the join table.

```
@part.assemblies << @assembly1
```

Copy

This method is aliased as `collection.concat` and `collection.push`.

###### [4.4.1.4 `collection.delete(object, ...)`](https://guides.rubyonrails.org/v6.1/association_basics.html\#methods-added-by-has-and-belongs-to-many-collection-delete-object)

The [`collection.delete`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/CollectionProxy.html#method-i-delete) method removes one or more objects from the collection by deleting records in the join table. This does not destroy the objects.

```
@part.assemblies.delete(@assembly1)
```

Copy

###### [4.4.1.5 `collection.destroy(object, ...)`](https://guides.rubyonrails.org/v6.1/association_basics.html\#methods-added-by-has-and-belongs-to-many-collection-destroy-object)

The [`collection.destroy`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/CollectionProxy.html#method-i-destroy) method removes one or more objects from the collection by deleting records in the join table. This does not destroy the objects.

```
@part.assemblies.destroy(@assembly1)
```

Copy

###### [4.4.1.6 `collection=(objects)`](https://guides.rubyonrails.org/v6.1/association_basics.html\#methods-added-by-has-and-belongs-to-many-collection-objects)

The `collection=` method makes the collection contain only the supplied objects, by adding and deleting as appropriate. The changes are persisted to the database.

###### [4.4.1.7 `collection_singular_ids`](https://guides.rubyonrails.org/v6.1/association_basics.html\#methods-added-by-has-and-belongs-to-many-collection-singular-ids)

The `collection_singular_ids` method returns an array of the ids of the objects in the collection.

```
@assembly_ids = @part.assembly_ids
```

Copy

###### [4.4.1.8 `collection_singular_ids=(ids)`](https://guides.rubyonrails.org/v6.1/association_basics.html\#methods-added-by-has-and-belongs-to-many-collection-singular-ids-ids)

The `collection_singular_ids=` method makes the collection contain only the objects identified by the supplied primary key values, by adding and deleting as appropriate. The changes are persisted to the database.

###### [4.4.1.9 `collection.clear`](https://guides.rubyonrails.org/v6.1/association_basics.html\#methods-added-by-has-and-belongs-to-many-collection-clear)

The [`collection.clear`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/CollectionProxy.html#method-i-clear) method removes every object from the collection by deleting the rows from the joining table. This does not destroy the associated objects.

###### [4.4.1.10 `collection.empty?`](https://guides.rubyonrails.org/v6.1/association_basics.html\#methods-added-by-has-and-belongs-to-many-collection-empty-questionmark)

The [`collection.empty?`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/CollectionProxy.html#method-i-empty-3F) method returns `true` if the collection does not contain any associated objects.

```
<% if @part.assemblies.empty? %>
  This part is not used in any assemblies
<% end %>
```

Copy

###### [4.4.1.11 `collection.size`](https://guides.rubyonrails.org/v6.1/association_basics.html\#methods-added-by-has-and-belongs-to-many-collection-size)

The [`collection.size`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/CollectionProxy.html#method-i-size) method returns the number of objects in the collection.

```
@assembly_count = @part.assemblies.size
```

Copy

###### [4.4.1.12 `collection.find(...)`](https://guides.rubyonrails.org/v6.1/association_basics.html\#methods-added-by-has-and-belongs-to-many-collection-find)

The [`collection.find`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/CollectionProxy.html#method-i-find) method finds objects within the collection's table.

```
@assembly = @part.assemblies.find(1)
```

Copy

###### [4.4.1.13 `collection.where(...)`](https://guides.rubyonrails.org/v6.1/association_basics.html\#methods-added-by-has-and-belongs-to-many-collection-where)

The [`collection.where`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/QueryMethods.html#method-i-where) method finds objects within the collection based on the conditions supplied but the objects are loaded lazily meaning that the database is queried only when the object(s) are accessed.

```
@new_assemblies = @part.assemblies.where("created_at > ?", 2.days.ago)
```

Copy

###### [4.4.1.14 `collection.exists?(...)`](https://guides.rubyonrails.org/v6.1/association_basics.html\#methods-added-by-has-and-belongs-to-many-collection-exists-questionmark)

The [`collection.exists?`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/FinderMethods.html#method-i-exists-3F) method checks whether an object meeting the supplied
conditions exists in the collection's table.

###### [4.4.1.15 `collection.build(attributes = {})`](https://guides.rubyonrails.org/v6.1/association_basics.html\#methods-added-by-has-and-belongs-to-many-collection-build-attributes)

The [`collection.build`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/CollectionProxy.html#method-i-build) method returns a new object of the associated type. This object will be instantiated from the passed attributes, and the link through the join table will be created, but the associated object will _not_ yet be saved.

```
@assembly = @part.assemblies.build({assembly_name: "Transmission housing"})
```

Copy

###### [4.4.1.16 `collection.create(attributes = {})`](https://guides.rubyonrails.org/v6.1/association_basics.html\#methods-added-by-has-and-belongs-to-many-collection-create-attributes)

The [`collection.create`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/CollectionProxy.html#method-i-create) method returns a new object of the associated type. This object will be instantiated from the passed attributes, the link through the join table will be created, and, once it passes all of the validations specified on the associated model, the associated object _will_ be saved.

```
@assembly = @part.assemblies.create({assembly_name: "Transmission housing"})
```

Copy

###### [4.4.1.17 `collection.create!(attributes = {})`](https://guides.rubyonrails.org/v6.1/association_basics.html\#methods-added-by-has-and-belongs-to-many-collection-create-bang-attributes)

Does the same as `collection.create`, but raises `ActiveRecord::RecordInvalid` if the record is invalid.

###### [4.4.1.18 `collection.reload`](https://guides.rubyonrails.org/v6.1/association_basics.html\#methods-added-by-has-and-belongs-to-many-collection-reload)

The [`collection.reload`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/CollectionProxy.html#method-i-reload) method returns a Relation of all of the associated objects, forcing a database read. If there are no associated objects, it returns an empty Relation.

```
@assemblies = @part.assemblies.reload
```

Copy

##### [4.4.2 Options for `has_and_belongs_to_many`](https://guides.rubyonrails.org/v6.1/association_basics.html\#options-for-has-and-belongs-to-many)

While Rails uses intelligent defaults that will work well in most situations, there may be times when you want to customize the behavior of the `has_and_belongs_to_many` association reference. Such customizations can easily be accomplished by passing options when you create the association. For example, this association uses two such options:

```
class Parts < ApplicationRecord
  has_and_belongs_to_many :assemblies, -> { readonly },
                                       autosave: true
end
```

Copy

The [`has_and_belongs_to_many`](https://api.rubyonrails.org/v6.1.7.10/classes/ActiveRecord/Associations/ClassMethods.html#method-i-has_and_belongs_to_many) association supports these options:

- `:association_foreign_key`
- `:autosave`
- `:class_name`
- `:foreign_key`
- `:join_table`
- `:validate`

###### [4.4.2.1 `:association_foreign_key`](https://guides.rubyonrails.org/v6.1/association_basics.html\#association-foreign-key)

By convention, Rails assumes that the column in the join table used to hold the foreign key pointing to the other model is the name of that model with the suffix `_id` added. The `:association_foreign_key` option lets you set the name of the foreign key directly:

The `:foreign_key` and `:association_foreign_key` options are useful when setting up a many-to-many self-join. For example:

```
class User < ApplicationRecord
  has_and_belongs_to_many :friends,
      class_name: "User",
      foreign_key: "this_user_id",
      association_foreign_key: "other_user_id"
end
```

Copy

###### [4.4.2.2 `:autosave`](https://guides.rubyonrails.org/v6.1/association_basics.html\#options-for-has-and-belongs-to-many-autosave)

If you set the `:autosave` option to `true`, Rails will save any loaded association members and destroy members that are marked for destruction whenever you save the parent object. Setting `:autosave` to `false` is not the same as not setting the `:autosave` option. If the `:autosave` option is not present, then new associated objects will be saved, but updated associated objects will not be saved.

###### [4.4.2.3 `:class_name`](https://guides.rubyonrails.org/v6.1/association_basics.html\#options-for-has-and-belongs-to-many-class-name)

If the name of the other model cannot be derived from the association name, you can use the `:class_name` option to supply the model name. For example, if a part has many assemblies, but the actual name of the model containing assemblies is `Gadget`, you'd set things up this way:

```
class Parts < ApplicationRecord
  has_and_belongs_to_many :assemblies, class_name: "Gadget"
end
```

Copy

###### [4.4.2.4 `:foreign_key`](https://guides.rubyonrails.org/v6.1/association_basics.html\#options-for-has-and-belongs-to-many-foreign-key)

By convention, Rails assumes that the column in the join table used to hold the foreign key pointing to this model is the name of this model with the suffix `_id` added. The `:foreign_key` option lets you set the name of the foreign key directly:

```
class User < ApplicationRecord
  has_and_belongs_to_many :friends,
      class_name: "User",
      foreign_key: "this_user_id",
      association_foreign_key: "other_user_id"
end
```

Copy

###### [4.4.2.5 `:join_table`](https://guides.rubyonrails.org/v6.1/association_basics.html\#join-table)

If the default name of the join table, based on lexical ordering, is not what you want, you can use the `:join_table` option to override the default.

###### [4.4.2.6 `:validate`](https://guides.rubyonrails.org/v6.1/association_basics.html\#options-for-has-and-belongs-to-many-validate)

If you set the `:validate` option to `false`, then associated objects will not be validated whenever you save this object. By default, this is `true`: associated objects will be validated when this object is saved.

##### [4.4.3 Scopes for `has_and_belongs_to_many`](https://guides.rubyonrails.org/v6.1/association_basics.html\#scopes-for-has-and-belongs-to-many)

There may be times when you wish to customize the query used by `has_and_belongs_to_many`. Such customizations can be achieved via a scope block. For example:

```
class Parts < ApplicationRecord
  has_and_belongs_to_many :assemblies, -> { where active: true }
end
```

Copy

You can use any of the standard [querying methods](https://guides.rubyonrails.org/v6.1/active_record_querying.html) inside the scope block. The following ones are discussed below:

- `where`
- `extending`
- `group`
- `includes`
- `limit`
- `offset`
- `order`
- `readonly`
- `select`
- `distinct`

###### [4.4.3.1 `where`](https://guides.rubyonrails.org/v6.1/association_basics.html\#scopes-for-has-and-belongs-to-many-where)

The `where` method lets you specify the conditions that the associated object must meet.

```
class Parts < ApplicationRecord
  has_and_belongs_to_many :assemblies,
    -> { where "factory = 'Seattle'" }
end
```

Copy

You can also set conditions via a hash:

```
class Parts < ApplicationRecord
  has_and_belongs_to_many :assemblies,
    -> { where factory: 'Seattle' }
end
```

Copy

If you use a hash-style `where`, then record creation via this association will be automatically scoped using the hash. In this case, using `@parts.assemblies.create` or `@parts.assemblies.build` will create orders where the `factory` column has the value "Seattle".

###### [4.4.3.2 `extending`](https://guides.rubyonrails.org/v6.1/association_basics.html\#scopes-for-has-and-belongs-to-many-extending)

The `extending` method specifies a named module to extend the association proxy. Association extensions are discussed in detail [later in this guide](https://guides.rubyonrails.org/v6.1/association_basics.html#association-extensions).

###### [4.4.3.3 `group`](https://guides.rubyonrails.org/v6.1/association_basics.html\#scopes-for-has-and-belongs-to-many-group)

The `group` method supplies an attribute name to group the result set by, using a `GROUP BY` clause in the finder SQL.

```
class Parts < ApplicationRecord
  has_and_belongs_to_many :assemblies, -> { group "factory" }
end
```

Copy

###### [4.4.3.4 `includes`](https://guides.rubyonrails.org/v6.1/association_basics.html\#scopes-for-has-and-belongs-to-many-includes)

You can use the `includes` method to specify second-order associations that should be eager-loaded when this association is used.

###### [4.4.3.5 `limit`](https://guides.rubyonrails.org/v6.1/association_basics.html\#scopes-for-has-and-belongs-to-many-limit)

The `limit` method lets you restrict the total number of objects that will be fetched through an association.

```
class Parts < ApplicationRecord
  has_and_belongs_to_many :assemblies,
    -> { order("created_at DESC").limit(50) }
end
```

Copy

###### [4.4.3.6 `offset`](https://guides.rubyonrails.org/v6.1/association_basics.html\#scopes-for-has-and-belongs-to-many-offset)

The `offset` method lets you specify the starting offset for fetching objects via an association. For example, if you set `offset(11)`, it will skip the first 11 records.

###### [4.4.3.7 `order`](https://guides.rubyonrails.org/v6.1/association_basics.html\#scopes-for-has-and-belongs-to-many-order)

The `order` method dictates the order in which associated objects will be received (in the syntax used by an SQL `ORDER BY` clause).

```
class Parts < ApplicationRecord
  has_and_belongs_to_many :assemblies,
    -> { order "assembly_name ASC" }
end
```

Copy

###### [4.4.3.8 `readonly`](https://guides.rubyonrails.org/v6.1/association_basics.html\#scopes-for-has-and-belongs-to-many-readonly)

If you use the `readonly` method, then the associated objects will be read-only when retrieved via the association.

###### [4.4.3.9 `select`](https://guides.rubyonrails.org/v6.1/association_basics.html\#scopes-for-has-and-belongs-to-many-select)

The `select` method lets you override the SQL `SELECT` clause that is used to retrieve data about the associated objects. By default, Rails retrieves all columns.

###### [4.4.3.10 `distinct`](https://guides.rubyonrails.org/v6.1/association_basics.html\#scopes-for-has-and-belongs-to-many-distinct)

Use the `distinct` method to remove duplicates from the collection.

##### [4.4.4 When are Objects Saved?](https://guides.rubyonrails.org/v6.1/association_basics.html\#has-and-belongs-to-many-association-reference-when-are-objects-saved-questionmark)

When you assign an object to a `has_and_belongs_to_many` association, that object is automatically saved (in order to update the join table). If you assign multiple objects in one statement, then they are all saved.

If any of these saves fails due to validation errors, then the assignment statement returns `false` and the assignment itself is cancelled.

If the parent object (the one declaring the `has_and_belongs_to_many` association) is unsaved (that is, `new_record?` returns `true`) then the child objects are not saved when they are added. All unsaved members of the association will automatically be saved when the parent is saved.

If you want to assign an object to a `has_and_belongs_to_many` association without saving the object, use the `collection.build` method.

#### [4.5 Association Callbacks](https://guides.rubyonrails.org/v6.1/association_basics.html\#association-callbacks)

Normal callbacks hook into the life cycle of Active Record objects, allowing you to work with those objects at various points. For example, you can use a `:before_save` callback to cause something to happen just before an object is saved.

Association callbacks are similar to normal callbacks, but they are triggered by events in the life cycle of a collection. There are four available association callbacks:

- `before_add`
- `after_add`
- `before_remove`
- `after_remove`

You define association callbacks by adding options to the association declaration. For example:

```
class Author < ApplicationRecord
  has_many :books, before_add: :check_credit_limit

  def check_credit_limit(book)
    # ...
  end
end
```

Copy

Rails passes the object being added or removed to the callback.

You can stack callbacks on a single event by passing them as an array:

```
class Author < ApplicationRecord
  has_many :books,
    before_add: [:check_credit_limit, :calculate_shipping_charges]

  def check_credit_limit(book)
    # ...
  end

  def calculate_shipping_charges(book)
    # ...
  end
end
```

Copy

If a `before_add` callback throws `:abort`, the object does not get added to
the collection. Similarly, if a `before_remove` callback throws `:abort`, the
object does not get removed from the collection:

```
# book won't be added if the limit has been reached
def check_credit_limit(book)
  throw(:abort) if limit_reached?
end
```

Copy

These callbacks are called only when the associated objects are added or removed through the association collection:

```
# Triggers `before_add` callback
author.books << book
author.books = [book, book2]

# Does not trigger the `before_add` callback
book.update(author_id: 1)
```

Copy

#### [4.6 Association Extensions](https://guides.rubyonrails.org/v6.1/association_basics.html\#association-extensions)

You're not limited to the functionality that Rails automatically builds into association proxy objects. You can also extend these objects through anonymous modules, adding new finders, creators, or other methods. For example:

```
class Author < ApplicationRecord
  has_many :books do
    def find_by_book_prefix(book_number)
      find_by(category_id: book_number[0..2])
    end
  end
end
```

Copy

If you have an extension that should be shared by many associations, you can use a named extension module. For example:

```
module FindRecentExtension
  def find_recent
    where("created_at > ?", 5.days.ago)
  end
end

class Author < ApplicationRecord
  has_many :books, -> { extending FindRecentExtension }
end

class Supplier < ApplicationRecord
  has_many :deliveries, -> { extending FindRecentExtension }
end
```

Copy

Extensions can refer to the internals of the association proxy using these three attributes of the `proxy_association` accessor:

- `proxy_association.owner` returns the object that the association is a part of.
- `proxy_association.reflection` returns the reflection object that describes the association.
- `proxy_association.target` returns the associated object for `belongs_to` or `has_one`, or the collection of associated objects for `has_many` or `has_and_belongs_to_many`.

### [5 Single Table Inheritance (STI)](https://guides.rubyonrails.org/v6.1/association_basics.html\#single-table-inheritance-sti)

Sometimes, you may want to share fields and behavior between different models.
Let's say we have Car, Motorcycle, and Bicycle models. We will want to share
the `color` and `price` fields and some methods for all of them, but having some
specific behavior for each, and separated controllers too.

First, let's generate the base Vehicle model:

```
$ bin/rails generate model vehicle type:string color:string price:decimal{10.2}
```

Copy

Did you note we are adding a "type" field? Since all models will be saved in a
single database table, Rails will save in this column the name of the model that
is being saved. In our example, this can be "Car", "Motorcycle" or "Bicycle."
STI won't work without a "type" field in the table.

Next, we will generate the Car model that inherits from Vehicle. For this,
we can use the `--parent=PARENT` option, which will generate a model that
inherits from the specified parent and without equivalent migration (since the
table already exists).

For example, to generate the Car model:

```
$ bin/rails generate model car --parent=Vehicle
```

Copy

The generated model will look like this:

```
class Car < Vehicle
end
```

Copy

This means that all behavior added to Vehicle is available for Car too, as
associations, public methods, etc.

Creating a car will save it in the `vehicles` table with "Car" as the `type` field:

```
Car.create(color: 'Red', price: 10000)
```

Copy

will generate the following SQL:

```
INSERT INTO "vehicles" ("type", "color", "price") VALUES ('Car', 'Red', 10000)
```

Copy

Querying car records will search only for vehicles that are cars:

```
Car.all
```

Copy

will run a query like:

```
SELECT "vehicles".* FROM "vehicles" WHERE "vehicles"."type" IN ('Car')
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