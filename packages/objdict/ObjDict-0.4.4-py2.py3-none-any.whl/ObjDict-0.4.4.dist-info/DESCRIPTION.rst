.. ObjDict documentation master README file.

=======
ObjDict
=======

Uses_
-----

Why 'objdict'?  The reasons include:

    - All tools and Classes for simple and relable JSON for objects
    - `ObjDict: The ad-hoc structure/object 'swiss army knife' class`_.
    - `Struct: the leaner specialized object`_.
    - `OEnum: Base class for Enums with JSON send/recieve`_.
    - `Support for JSON message encoding and decoding`_.
    - `ObjDict in place of dictionaries as convenient ad-hoc data structures`_.
    - `Mutable equivalent to nametuple (or namedlist)`_.
    - `Adding JSON serialization to classes`_.
    - `OrderedDict alternative`_.

Background_
-----------

    - `History and acknowledgements`_.
    - `JsonWeb alternative to ObjDict JSON processing`_.
    - `Multiple uses of dictionaries`_.
    - `Introducing the ObjDict`_.
    - `Multiple modes of dictionary use and JSON`_.
    - `ObjDict JSON general`_.
    - `ObjDict JSON load tools`_.
    - `ObjDict JSON dump tools`_.

Instructions_
-------------

    - `General notes and restrictions`_.
    - `Initialisation and JSON load`_.
    - `'str' and JSON dumps`_.
    - `Custom classes and JSON`_.
    - `Maintaining order with custom classes and defaults`_.

_`Uses`
-------

ObjDict: The ad-hoc structure/object 'swiss army knife' class
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

As described in this 'uses' section, the ObjDict class has many uses, and can
be used in place of :code:`namedtuples`, :code:`namedlists`, :code:`OrderedDict` objects, as
well as for processing JSON data.  One single import gives this flexibility.

The one trade-off for this flexibility, compared to using the individual specialised
classes is performance. If you have performance critical code that is used in
massively iterative loops then, for example, namedtuples are far better, as long as
namedtuples provide all the functionality you require.  But every last nanosecond
is not of the essence and flexibility to adapt and simply code is desired, then
'ObjDict' can be a replacement for several other classes, plus provide best tools
for working with JSON data.

Struct: the leaner specialized object
+++++++++++++++++++++++++++++++++++++
A swiss army nife does everything, but sometimes a special purpose device 
is more elegant.  The 'Struct' class provides the leaner, more elegant solution
for creating your own classes.  ObjDict is perfect for decoding Json objects which
may be collections or maybe objects, but Struct is designed for building your own
object classes.  A :code:`__json__` method is provided, as well as useful 'str' and 'repr'
default methods.  The json default method provides easy overrides, passing the 
default method a dictionary of the data to be included in json::

    def __json__(self, **kwargs):
        return super().__json__(<dictionary of json data>, **kwargs)


OEnum: Base class for Enums with JSON send/recieve
++++++++++++++++++++++++++++++++++++++++++++++++++
Using the OEnum from this package, in place of Enum from enum package, adds
JSON encoding and decoding to Enumerated data.  Same as 'Enum', but codes to
JSON and decodes back the the original type. Example::

    @objdict.from_json()  #decorated require for decoding direct from json
    class MyEnum(objdict.OEnum):
        first = 1
        second = 2
        third = 3

    place = MyEnum(1)
    jsondata = { 'place': place }
    # as json '{ "place": { "__type__", "MyEnum", "n": "first"}}'

Note, "MyEnum" will decode direct value from 'n' key (by name) or 'v' key
by value.



Support for JSON message encoding and decoding
++++++++++++++++++++++++++++++++++++++++++++++

Where an application has the need to build JSON data to save or transmit, or
to decode and process JSON data loaded or received, the ObjDict structure provides all
the tools to achieve this, with clear object oriented code.  This usage has different
requirements than JSON serialisation (as discussed below), as it is necessary
to be able to produce not just a JSON representation of an object,  but create
objects that can describe any required possible
arbitrary JSON data to produce or decode specific messages.
For example, the order of fields may be significant in a
JSON message, although field order may not be significant for object
serialisation. The ObjDict class has
the tools to produce exactly the JSON data required by any application, and to decode
any possible incoming JSON messages for processing.  It was for this usage that
ObjDict was initially developed.

ObjDict in place of dictionaries as convenient ad-hoc data structures
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

See the text below on 'multiple uses of dictionaries' for background.
There is a significant amount of code where dictionaries have been used for
ad-hoc structures. The use case often arises where it can become useful if
these data structure can have elements accessed in the simpler are many.

Mutable equivalent to nametuple (or namedlist)
++++++++++++++++++++++++++++++++++++++++++++++

There are occasions where a 'namedtuple' cannot be used due to the need for
mutable objects. The ObjDict also fulfills this need and can be initialised
from list data. There are many other classes that also fill this need, but
the ObjDict combines this functionality with JSON processing, with dictionary
access to data and other functions.

Adding JSON serialization to classes
++++++++++++++++++++++++++++++++++++

Applications that have a need to serialise objects in order to restore those
objects either within the same application, or in an application connected
through a data-link, may desire JSON as the format for object storage or object
message format.  The ObjDict class and module provides the tools for this,
serialising the state of an object in order for that state to be later
loaded, either by an identical class, or a different class which has use
for some or all of the same 'object state' information.

OrderedDict alternative
+++++++++++++++++++++++

OrderedDicts do everything dictionaries can, and in some applications it can
be useful to simply move to OrderedDict classes for all dictionaries. 'ObjDict'
is another alternative, with a shorter name, even more flexibility and power,
and a much more readable 'str' representation that can also be used for clearer
initialisation. See instructions for details on 'str' and initialisation
flexibility.


_`Background`
-------------
    - `History and acknowledgements`_.
    - `JsonWeb alternative to ObjDict JSON processing`_.
    - `Multiple uses of dictionaries`_.
    - `Introducing the ObjDict`_.
    - `Multiple modes of dictionary use and JSON`_.
    - `ObjDict JSON general`_.
    - `ObjDict JSON load tools`_.
    - `ObjDict JSON dump tools`_.

History and acknowledgements
++++++++++++++++++++++++++++

The project emerged from a need for code to generate and decode JSON
messages. Originally the package `JsonWeb <http://www.JsonWeb.net/>`_  was
selected for the task, but it became clear the use case differed. 'JsonWeb' is
ideal for representing classes as JSON, and reloading classes from that JSON
and provides validation and tests and schema that are not reproduced in ObjDict.
However ObjDict provides specifically for classes created to generate or process
JSON as data, as
opposed to JSON as a representation of the class, and now the ObjDict and Struct
classes, with a wider range of uses. The whole issue of JSON data which ambiguously
may correspond to either a dictionary collection, or an object, arises from
general processing of JSON data and gives rise to the ObjDict. The ObjDict
project started out to add more control
over JSON as a fork of JsonWeb, but evolved over time to the different use cases.

A key result of the different use case is the JsonWeb focuses strongly on validation
that the JSON code exactly matches requirements, where as ObjDict takes the opposite
approach of specially being designed to allow for communication between software 
systems where one end of the link may be upgraded prior to the other end of the link,
which requires JSON messages designed to permitt data from future message formats 
without generating errors.  An 'upgrade tolerant' system.

JsonWeb alternative to ObjDict JSON processing
++++++++++++++++++++++++++++++++++++++++++++++

The project 'JsonWeb' overlaps is use cases with this project. The focus of
'JsonWeb' is to provide for serializing python object structures and instancing
python objects from the serialized form. ObjDict can be used for this role also,
but currently lacks the validation logic used by 'JsonWeb' to ensure JSON data
matches exactly the required format.

In fact, rather than an emphasis on validation, the original primary use case of
ObjDict is to allow maximum flexibility
for the JSON data representing an object. The ObjDict object itself is a generic
object to enable working with JSON data without having a matching object definition.
Beyond the ObjDict
class, the entire ObjDict-JSON processing philosophy is to provide for
information sent between
computer systems with flexible, adaptable message handling.
Where, for example, the message specification may evolve from version to
version.  This requires flexible interpretation of data, and the ability to
easily ignore additional data that may have been added in later versions,
providing easy backward compatibility.

The structure for JSON dump and load is a very flexible framework, and any feature
including more rigid validation could easily be added.

Multiple uses of dictionaries
+++++++++++++++++++++++++++++

In python, dictionaries are designed as 'collections' but are often used as
ad-hoc structures or objects.  In a true collection, the key for an entry does
not indicate properties
of the value associated with the key. For example, a collection of people,
keyed by names
would not normally infer the significance or type of data for each entry
(or in this case person) by the key.  The data has the same implications regardless
of whether the key is 'bob' or 'jane'. The data associated with 'bob' or 'jane'
is of the same type and is interpreted the same way.
For an 'ad-hoc' structure the keys **do** signal both the nature of the data and
even the type of data.
Consider for each entry for a person we have a full name and age.
A dictionary could be used to hold this information, but this time it is an
ad-hoc structure.  As a dictionary we always expect the same two keys, and each
is specific to the information and different keys even have different types of data.
This is not a dictionary as a collection, but as an ad-hoc structure. These are two
very different uses of a dictionary, the collection the dictionary was designed for,
and the ad-hoc structure or ad-hoc object as a second use.

Introducing the ObjDict
+++++++++++++++++++++++

An ObjDict is a subclass of dictionary designed to support this second
'ad-hoc object' mode of use. An ObjDict supports all normal dict operations, but
adds support for accessing and setting entries as attributes.

So::

    bob['full_name'] = 'Robert Roberts'

is equivalent to::

    bob.full_name = 'Robert Roberts'

Either form can be used. ObjDicts also have further uses.

Multiple modes of dictionary use and JSON
+++++++++++++++++++++++++++++++++++++++++

The standard JSON dump and load map JSON 'objects' to python dictionaries.
JSON objects even look like python dictionaries (using {}
braces and a ':'). In JavaScript, objects can also
be treated similarly to dictionaries in python. The reality is some JSON
objects are best represented in python as objects, yet others are best
represented as dictionaries.

Consider::

    { "name": {"first": "fred", "last": "blogs" }
     "colour_codes": {"red": 100, "green": 010, "yellow": 110, "white": 111 }
    }

In this data, the 'name' is really an object but 'color_codes' is a
true dictionary. Name is not a true dictionary because it is not a collection
of similar objects, but rather something with two specific properties.
Iterating through name does not really make sense, however iterating through
our colours does make sense. Adding to the collection of colours and their
being a variable number of colours in the collection is all consistent.
Treating 'name' is not ideal as the 'keys' rather than being entries in a collections
each have specific meaning.  Keys should not really have meaning, and these keys
are really 'attributes' of name, and name better represented as an object.

So two types of information are represented in the same way in JSON.

Another limitation of working with python dictionaries and JSON is that in messages,
order can be significant but dictionaries are not ordered.

The solution provided here is to map JSON 'objects' to a new python ObjDict
(Object Dictionaries).  These act like OrderedDictionaries, but can also be treated
as python objects.

So 'dump' or '__JSON__()' or 'str()' / '__str__()' of the 'names' and
'colour_codes' example above produces an
outer ObjDict containing two inner 'ObjDict's,  'name' and 'colour_codes'.
Assume the outer ObjDict is assigned to a variable called 'data'.
Each ObjDict can be treated as either an object or a dictionary, so all the code
below is valid::

    data = ObjDict(string_from_above)
    name = data['name'] # works, but as 'data' is not a real 'dict' not ideal
    name = data.name  # better
    first_name = data.name.first
    first_name = data["name"]["first"]  # works but again not ideal

    red_code = data.colour_codes["red"]
    # as colour codes is a true collection it will be unlikely to set
    # members to individual variables, but the code is valid

ObjDict items also 'str' or 'dump' back to the original JSON as above.
However if the original string was changed to::

    { "name": {"first": "fred", "last": "blogs", "__type__": "Name" }
     "colour_codes":{"red": 100, "green": 010, "yellow": 110, "white": 111 }
    }

The JSON 'load' used to load or initialise ObjDict uses an 'object_pairs_hook'
that checks a table of registered class names and corresponding classes.

If there is an entry in the table, then that class will be used for embedded objects.
Entries with no :code:`__type__` result in ObjDict objects, and if the 'DefaultType' is
set then a class derived from the default type, with the name from the value
of '__type__' will be returned.  If 'DefaultType' is None, then an exception will
be generated.

See the instructions section for further information.

ObjDict JSON general
++++++++++++++++++++

The tools provided allow for dumping any class to JSON, and loading any class
from JSON data.  There is no requirement for the basing classes on the ObjDict
class.  The main use of ObjDict is to decode JSON data which is **NOT** already
identified as matching a class within the application.  The ObjDict provides the
catchall.

The main challenge is not the specific class being loaded or dumped, but the
objects **within** that class.

Consider loading an object properties from JSON. A simple loop to use each JSON field
to set each attribute, and the class to be set is simply one class. However, what if
some of those fields are themselves objects, and possibly fields within those
again objects?  Within the single 'top-level' object, there may be many embedded
objects and identifying and processing these embedded objects is the actual challenge.

In general, handling embedded objects is achieved through the '__from_JSON__' class method
within each class for the 'JSON.load', or the '__JSON__' method within each
object for the 'JSON.dump'.

Standard routines to perform these methods are available, together with the tools
to easily decorate classes and other utilities.

ObjDict JSON load tools
+++++++++++++++++++++++

The three main tools for loading JSON objects are an 'object_pairs_hook' method to
be passed to the standard 'JSON.load' function, the '__from_JSON__' class method that
can be added to any class to control instancing the class from JSON and
the 'from_JSON' decorator.

The philosophy is the use of simple, flexible building blocks.

:code:`object_pairs_hook`
~~~~~~~~~~~~~~~~~~~~~~~~~
A class within the objdict module, 'ObjPairHook', is a wrapper tool to provide
a function for the standard library JSON.load() function. Simply instance an ObjPairHook
and pass the 'from_JSON' method to JSON_load(). eg::

    hook=ObjPairHook().from_JSON
    JSON.load(object_pairs_hook=hook)

    class ObjPairsHook()
        def __init__(classes_list=[],BaseHook=None,BaseType=None):


The 'from_JSON' method will check all JSON objects for a '__type__' entry, or use
'default' processing. For objects with a '__type__', both the entries in the
'classes_list' parameter and the default_classes_list maintained within
the objdict module and added to through
the 'from_JSON' decorator, can be instanced if there is a name match.

For objects with '__type__' entries but no name match with either source of classes
then the a dynamic class based on 'BaseClass' is generated and selected as the 'class'.

For objects with no '__type__' entry, then the 'BaseHook' is selected as the
'class' (although in practice is it also
possible to use a method rather than a class).

Once a class is selected, then if this class has a '__from_JSON__' attribute, then
this class method is called to instance an object, otherwise the normal init method
for the class is called.

:code:`__from_JSON__` class method
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Providing a '__from_JSON__' class method is called to instance an the object
by the 'object_pairs_hook' if an attribute of this name is present.

:code:`from_JSON` decorator
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The from_JSON decorator, when used to decorate a class, adds the class to
default_class list used by the object_pairs_hook.

ObjDict JSON dump tools
+++++++++++++++++++++++

The '__JSON__' method, JSONEncoder class, the :code:`@to_JSON` decorator and the
JSON_registry of to_JSON converters are the main
tools for encoding JSON. Whereas JsonWeb takes an approach of decorating classes
with configuration information to allow the encoder class to produce the JSON
output, ObjDict uses a JSONEncoder that delegates the encoding to '__JSON__'
method within each object, or from a table of class/converter pairs.

JSONEncoder class
~~~~~~~~~~~~~~~~~

The JSON_encoder class does the actual encoding, and for each object it first
checks for a '__JSON__' method and class that method if present. For objects
defined outside of scope e.g. Decimal(), the encoder checks the encoder_table
for a matching entry and if present calls that encoder.

:code:`to_JSON` decorator
~~~~~~~~~~~~~~~~~~~~~~~~~

This decorator checks if the class has a '__JSON__' method, and if not, decorates
the class with a default '__JSON__' method. The '__JSON__' method itself is then
decorated with any configuration data.

:code:`__JSON__` method
~~~~~~~~~~~~~~~~~~~~~~~

For any object this is either a function or a bound method to be called with
the object to be encoded as a parameter. The method should return either a
string or a dictionary to be included included in the JSON output.

JSON_registry
~~~~~~~~~~~~~

This is an object which can be imported from the objdict module to access the
'add_to' method (:code:`JSON_registry.add_to(<class>,<method/function>`). By default, the
table contains entries for Decimal, datetime.datetime and datetime.time.
Any entry can be overwritten by simply adding new values for the same class.


_`Instructions`
---------------
    - `General notes and restrictions`_.
    - `Initialisation and JSON load`_.
    - `'str' and JSON dumps`_.
    - `Custom classes and JSON`_.
    - `Maintaining order with custom classes and defaults`_.


General notes and restrictions
++++++++++++++++++++++++++++++

Since valid keys for an ObjDict may not necessarily be valid attribute names (for example an
integer can be a dictionary key but not an attribute name, and dictionary keys
can contain spaces), not all
key entries can be accessed as attributes. Similarly, there are attributes
which are not considered to be key data, and these attributes have an underscore
preceding the name. Some attributes are part of the scaffolding of the ObjDict
class and these all have a leading underscore, as well as a trailing underscore.
It is recommended to use a leading underscore for all class 'scaffolding' added as
extensions to the ObjDict class or to derived classes, where this scaffolding
is not to be included as also dictionary data.


Initialisation and JSON load
++++++++++++++++++++++++++++

ObjDict can be initialised from lists, from JSON strings, from dictionaries,
from parameter lists or from keyword parameter lists. Struct also provides 
intialisation from lists (with __keys__ or from keyword parameter lists.

Examples::

    a = ObjDict('{"a": 1, "b": 2}')

    class XYZ(ObjDict):
        __keys__ = 'x y z'

    xyz = XYZ(10,20,30)
    xyz.y == 20

Initialisation from lists or parameter lists
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Initialisation from a list of key value pairs, as with OrderedDict class is
supported. Beyond key value pairs, there is also support for direct initialisation
from lists. The '_keys__' parameter must be included for initialisation from lists.
Also, Classes
derived from ObjDict or Struct can have '_keys__' as a class attribute, providing a similar
use pattern to the 'namedtuple'.  '_keys__' can be either
a list of strings, or a string with space or comma separated values. When
initialising from a list or parameter list, the list size must match the number
of keys created through '_keys__', however other items can be added after
initialisation.

So this code produces True::

    class XY(ObjDict):
        __keys__ = 'x y'

    sample = XY(1, 3)
    sample.x, sample.y == 1, 3


    class XYS(Struct):
        __keys__ = 'x y'

    sample2 = XYS(1, 3)
    sample2.x, sample2.y == 1, 3

Alternatively the form to produce a similar result but with the SubClass would be::

    sample = ObjDict(1, 3, __keys__='x y')
    sample = Struct(1, 3 ,__keys__='x y')

Initialisation from JSON strings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For more complex initialisation, JSON strings can provide an ideal solution.
This allows for complex structures with nested/embedded 'ObjDict' or other objects.

Note that initialising from either dictionaries or keyword parameters will result
in the order being lost.

For example::

    >>> ObjDict(a=1, b=2, c=3)
    {"c": 3, "b": 2, "a": 1}

    >>> ObjDict({"a": 1, "b": 2, "c": 3})
    {"a": 1, "b": 2, "c": 3}

So initialisation from a JSON string is useful if key order is important.

Initialisation from dict, OrderedDict, or key word arguments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As discussed already, initialisation from dict or key word arguments will
not maintain order of keys, but if order is not important, such as when the data
has already been inserted into a dictionary.

'str' and JSON dumps
++++++++++++++++++++

A limitation with OrderDict objects is that 'str' representation can be clumsy
when the structure is nested.

The '__str__' method of ObjDict class calls the '__JSON__' method. '__str__' can
be overridden without disturbing the '__JSON__' method. To convert an ObjDict
to JSON, simply call either of these methods.

JsonEncoder and objdict.dumps
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For working with ObjDict objects or other objects using 'json.dumps' the
objdict module provides a 'JsonEncoder' object to use as a parameter to
'json.dumps', and an alternative 'dumps' with the encoder as a default
parameter::

    import json
    from objdict import JsonEncoder

    json.dumps(<object>, cls=JsonEncoder)

         or

    import objDict

    objdict.dumps(<object>)

Additional Uses for the Encoder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Simple decorate other classes with the 'to_json' decorator and these will also
then encode using their __json__ method.

Also other classes, including classes already defined without a __json__
method can register together with an appropriate method of function to produce
json from those objects.

Custom classes and JSON
+++++++++++++++++++++++

Custom classes allow for JSON data to result in instantiating objects other
than ObjDict from JSON data.  These custom classes can be sub-classed from ObjDict
or built simply using the :code:`@to_JSON()` and/or :code:`@from_JSON()` decorators.

Sub-classing ObjDict
~~~~~~~~~~~~~~~~~~~~

If sub-classing from ObjDict, then your class should not need to be decorated
with either of the from/to decorators. Such class will make use of code in
the standard __init__ method of ObjDict and standard ObjDict json
encoding/decoding method.

The reality is that ObjDict is best subclasses by JSON decode presented with classes 
that are not declared, so it is not known if a collection or object is best.

Classes created with JSON representation as a criteria are recommended to be based 
on Struct, rather than ObjDict.

Note that if subclassing objdict and defining an __init__ method, or adding
specialised instancing from json, then some steps are needed.

The ObjDict init method allows for an OrderedDictionary first parameter
to effectively provide a set of key word values for the class.  Either simply
test for first parameter being and ordered dictionary and bypass other intialisation
or have custon initialisation::

    class MyClass(ObjDict):
        def __init__(a,b,c):
            if isinstance(a,dict):
                #instancing from json
                super().__init__(a)
            else:
                #regular init
                self.a = a
                self.b = b
                self.c = c

    # alternate code
    @from_json()
    class MyClass(ObjDict):
        def __init__(a,b,c):
            self.a = a
            self.b = b
            self.c = c

        @classmethod
        def __from_json__(cls,odict):
            return cls(odict.pop('a'),odict.pop('b'),odict.pop('c'))


JSON.dumps from decorators
~~~~~~~~~~~~~~~~~~~~~~~~~~

The alternative to subclassing ObjDict avoids inheriting other properties of
ObjDict which may not be relevant to the application. The :code:`@to_JSON` decorator
decorates a class with a '__JSON__' method, and if JSON.dumps() is called as follows::

    from objdict import JSONEncoder
    import JSON

    JSON.dumps(my_object, cls = JSONEncoder)

Alternate method using objdict.dumps::

    import objdict

    objdict.dumps(my_object)

Then all decorated classes will be encoded using their '__JSON__' method, in
addition to any classes in the JSON_registry.

JSONEncoder and JSON_registry
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The JSONEncoder encodes all classes added to the JSON_registry, as well
as any class with a '__JSON__' method.  Classes such as datetime.date or
decimal.Decimal are standard library classes and it may not be convenient to
sub-class these to have a '__JSON__' method. For these cases, calling the
add_to method of the JSON_registry allows adding these objects to be encoded.

For example::

    from objdict import JSON_registry

    JSON_registry.add_to(datetime.date, str)

This will ensure JSONEncoder will use the 'str' function to encode dates.

json.loads from decorators
~~~~~~~~~~~~~~~~~~~~~~~~~~

The :code:`@from_json()` decorator adds the class to the class register internal to the
objdict module, to then be used by the 'object_hook_pair' function provided
as a parameter to the json.loads function.

Either call json.loads with the object_hook_pair= or use the objdict.loads
function as follows::

    import json
    from objdict import make_pairs_hook, ObjDict

    classes = <list of classes and loaders>  # use 'None' for default
    obj = json.loads(<string>,
            object_hook_pairs=make_pairs_hook(classes,ObjDict,ObjDict)
            )

    #   or alternate method
    import objdict

    obj = objdict.loads(<string>)

from_json decorator
~~~~~~~~~~~~~~~~~~~~
The from_json(type_name=None,use=None) can be supplied with a alternate name
if desired to overide the class name for __type__ entries in the json text,
plus a 'use ' setting which applies for cases where no '__from_json__ class
method is present.  The 'use' setting can specify a fuction to instantiate
objects.  The method must take two parameters, a class, and an orderdictionary
of values.

Alternately, 'use' as None, will simply instantiate a class from the __init__
method and supply all values from the json text as keyword arguments.

Setting 'use' to True, will also use the __init__ method of the class, but
supply the data from json in a single OrderedDict parameter.

As follows::

    json_text = '{"a":1,"b":2,"c":3}'
    @from_json()
    class Test:
        def __init__(self,a=None,b=None,c=None,**kwargs):
            # note: if kwargs is not present, than any additional
            # fields in the json will create an exception
            self.a=a
            self.b=b
            self.c=c

    @from_json(use=True)
    class Test:
        def __init__(self,a,b=None,c=None):
            # if called from json, then all data will be in a dictionary a
            #parameter - then will preserve json data order
            if isinstance(a,dict):
                self.parms=a
                self.a = a.get('a')
                self.b = a.get('b')
                self.c = a.get('c')
            else:
                self.a = a
                self.b = b
                self.c = c


ObjPairHook().decode()
~~~~~~~~~~~~~~~~~~~~~~

To call json.loads, instance an ObjPairHook object and then pass the decode
method of that object to json.loads.

The decode method will, for all classes in the load_class_register, check if
the class has a '__from_JSON__' class method, and if present, call the '__from_JSON__'
class method will be called to instance an object from the set of key, value pairs.

For example, if you have::

    { "name":{
            "first": "joe",
            "last": "foo"
        }
    }

    # now code
    @objdict.from_JSON()
    class Name:
        def __init__(self, first=None, last=None, **kwargs):
            self.first = first
            self.last = last


Read with::

    loads(string)

then convert the name
dictionary into an object and put that object back in the original tree::

    tree = combiParse(string)
    tree['name'] = Name(**tree['name'])  # kwargs!!! i.e. "**" required :-)

The result would be 'unParsed' ::

    { "name":{
            __type__: "Name"
            "first": "joe",
            "last": "foo"
        }
    }


Decoding automatically to objects can then be added at a later time.

Maintaining order with custom classes and defaults
++++++++++++++++++++++++++++++++++++++++++++++++++

ObjDict classes and automatically created classes currently maintain key order,
but of course cannot provide for default values for attributes.

Custom classes can specify default values for attributes, but currently custom
classes do not automatically maintain order, even if based on ObjDict classes.

Maintaining order and supporting default values are available with an '__init__'
method. Note, the order attributes are set will be their order in a message.
Classes sub-classed from ObjDict will have '__type__' at the end of JSON output.

If a custom class is decorated with :code:`@decode.from_object(JSONSimpleHandler)`,
then all fields in the raw JSON will be sent in a single dict. Of course, as
a dict order is lost and also there are no default values.
The recommended code for the init is something like this::

     @objdict.from_JSON()
     class Custom(ObjDict):
        def __init__(self, *args, **kwargs):
            super(Custom,self).__init__()
            if args:
                arg0 = args[0]
                assert len(args) == 0, "unexpected argument"
                self.arg1 = arg0.pop('arg1', default)
                self.arg2 = arg0.pop('arg2', default)
                ........
                self.update(arg0)
            self.update(**kwargs)

Life is much simpler with :code:`@decode.from_object()`, but at the expense of ignoring
any unexpected arguments. Currently \*\*kwargs will always be empty in this case
but a future update will likely address this.

Example::

    @decode.from_object()
    class Custom(ObjDict):
       def __init__(self,arg1=None, arg2=None ...., **kwargs):
           super(Custom,self).__init__()
           self.arg1 = arg1
           self.arg2 = arg1
           ........
           self.update(**kwargs) # currently kwargs is empty


All that is needed as imports is above.

This system supports both 'ObjDict' and custom classes. In JSON representation
a '__type__' field is used to indicate actual type.  For your own classes use::

    @encode.to_object()
    @decode.from_object()
    class Sample:
        def __init(self, p1, p2, ...):
            self.p1 = p1
            self.p2 = p2
            ....

to map between::

    { "p1": 1, "p2": 2, "__type__": "Sample"}

and::

    Sample(1,2)

However simple examples such as this could also use the default 'ObjDict' objects.


