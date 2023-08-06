# djangocms-local-navigation

This package provides a DjangoCMS plugin that displays a menu based on the
structure of the current page. You can for example create a local menu that is
based on all the h2 elements on your page.

## Installation

`$ pip install djangocms-local-navigation`

Then add it to INSTALLED_APPS:

```python
INSTALLED_APPS = (
    # ...
    'djangocms_local_navigation',
)
```

Also add the plugin processor, which will add the `id` attributes to your
navigation elements, allowing you to actually linking to them:

```python
CMS_PLUGIN_PROCESSORS = (
    # ...
    'djangocms_local_navigation.cms_plugin_processors.patch_elements',
)
```

You should now be able to add the plugin "Local menu" to your pages.

## Configuration

### CMS_LOCAL_NAVIGATION_NAV_ELEMENTS

Default: `h2`

Defines which elements are used to create the local menu. This is a CSS
selector so if you want for example only elements with the class
`local-navigation-heading` to be included in the navigation you could use
`h2.local-navigation-heading`.

### CMS_LOCAL_NAVIGATION_XML_PARSER

Default: `None` (means automatic detection)

Defines which XML parser is used to add anchors to the elements and create the
menu. Refer to [the BeautifulSoup documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#specifying-the-parser-to-use)
for more information. Be advised that [lxml has known issues with
mod_python](http://lxml.de/FAQ.html#my-program-crashes-when-run-with-mod-python-pyro-zope-plone)
and can cause your processes to hang.

## Development

To run the tests, use `./setup.py test`.
