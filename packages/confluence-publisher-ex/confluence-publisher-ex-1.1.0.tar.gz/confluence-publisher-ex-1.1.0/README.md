# Confluence Publisher

A tool to help publish documentation to Confluence.
This tools use own configuration file.

For now it supports:

 - confluence versions: 5.5 - 5.9
 - sphinx-build formats: "fjson", "html"

## Why?

This tools are written as part of our Documentation Toolkit which we use in our job daily.
The main idea of toolkit is to make a process of creating and updating documentation able to be automated

# Install

Install Confluence Publisher from [PyPI](https://pypi.python.org/pypi/confluence-publisher-ex) with

```
$ pip install confluence-publisher-ex
```

## Publisher

```
$ conf_publisher config.yml --auth XXXXXjpwYXNzdXXXXX==
```

If a config doesn't contain page.id, the tool can automatically create pages 
on-the-fly when ``-ac`` flag is set up.

```
usage: conf_publisher [-h] [-u URL] (-a AUTH | -U USER) [-F] [-w WATERMARK]
                      [-l LINK] [-ht] [-v] [-ac] [-fo]
                      config

Publish documentation (Sphinx fjson) to Confluence

positional arguments:
  config                Configuration file

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     Confluence Url
  -a AUTH, --auth AUTH  Base64 encoded user:password string
  -U USER, --user USER  Username (prompt password)
  -F, --force           Publish not changed page.
  -w WATERMARK, --watermark WATERMARK
                        Overrides the watermarks. Also can be "False" to
                        remove all watermarks; or "True" to add watermarkswith
                        default text: "Automatically generated content. Do not
                        edit directly." on all pages.
  -l LINK, --link LINK  Overrides page link. If value is "False" then removes
                        the link.
  -ht, --hold-titles    Do not change page titles while publishing.
  -v, --verbose
  -ac, --auto-create    Auto create pages on-the-fly when they do not exist.
  -fo, --fix-order      Fix ordering of the pages so that it matches the order
                        in the configuration file.  
```
## Configuration file format

Directives:

- **version** (required) Config version. Current is ``2``.
- **url** (required) Base Confluence URL.
- **base_dir** (required) Directory containing json to be published.
- **downloads_dir** (optional) Default is _downloads
- **images_dir** (optional) Default is _images
- **source_ext** (optional) Default is .fjson
- **space_key** (required) The key for a space where the documentation should be created.
- **parent_page** (required) A page id which should be the root node for the documentation.
- **pages** (required) Pages to be published.

    - **id** (optional with -ac flag)  Confluence page ID. If page does not exists, create it with ``conf_page_maker``.
    - **title** (optional)
    - **source** (required)  Path to json associated with the page
    - **link** (optional)  Link under watermark (for example to source rst in repo).
    - **watermark** (optional)  Watermark  to put on page. E.g.: "Automatically generated content. Do not edit directly"".
    - **attachments** (optional) Files to be attached.

        - **images**
            - path_to_img1
            - path_to_img2
        - **downloads**
            - path_to_file1
            - path_to_file2
    - **pages** Subpages to be published.

        - **...** same structure as for pages


### Config example

```
  version: 2
  url: https://confluence.example.com
  base_dir: _build/confluence
  space_key: BIT
  parent_page: 23451238
  pages:
  - title: "Getting started"
    source: getting-started/index
    pages: 
    - title: "Architecture"
      source: getting-started/architecture
      attachments:
        images:
        - first-arch.png
        - second-arch.png
    - title: "Writing first app"
      source: getting-started/writing-first-app
      attachments:
        downloads:
        - sample1.properties
        - sample2.properties
```

or more JSONify style:

```
{
  version: 2,
  base_dir: "result",
  pages: [
    {
      id: 52136662,
      source: "release_history"
    }
  ]
}
```
