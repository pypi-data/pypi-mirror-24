Nbconvert Markdown -> JekyllMarkdown
------------------------------------

There are a few ways to extend nbconvert so that it works with Jekyll Markdown.
nbconvert uses templates to define how it creates a particular file format out
of a notebook, and these templates are relatively easy to extend to your
purposes.

What isn't clear is the "right" way to go about creating and extending these
templates in the first place. This is a short guide on doing so with three
different approaches.

Defining the template file
--------------------------
If the goal is to convert a Jupyter notebook into a jekyll-flavored
markdown file, the first thing to recognize is that nbconvert supports
markdown out of the box. This means that we probably only need to *extend* the
markdown template, rather than create our own template.

You can extend a pre-existing template by adding::

  {%- extends 'markdown.tpl' -%}

at the top of your template file.

Now we need to define how our template behaves *differently* from the
markdown template. Let's keep it simple by adding a single tag to the
beginning of each input cell. To do this, we'll add the following
text to our template file::

  {%- block input scoped %}
  {:.input}
  {{ cell.source }}
  {%- endblock input %}

This tells nbconvert to add ``{:.input}`` just before the source of a
text cell. Jekyll Markdown should take this text and turn it into an HTML
class of whatever is created.

Telling nbconvert about the existence of this template
------------------------------------------------------

There are a few ways to get nbconvert to actually *use* this template. The
first thing we can do is simply point nbconvert directly to this file when
we run ``nbconvert``. We can do that with the following:
