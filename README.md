# Web Map

Creates a map of at most 10 nearest to given coordinates movie locations
in HTML format. Show the distance between the specified coordinates and created markers, outlines the country within which the coordinates have been specified.

### Warning

Please, treat the module with respect and do not enter invalid data (e.g.,
300 years BC, international waters

## HTML file structure

A brief analysis of Hypertext Markup Language file structure.

### General

* `<html>` tag defines the beginning of the HTML file, the header (*<head>*) and the document body (*<body>*) are stored inside it.
* `<head>` is the title of the document, may contain text and tags, but the contents of this section are not displayed directly on the page.
* `<body>` is intended for the placement of tags and content of the web page.

HTML offers six different levels of text headings that show the relative importance of the section after the heading. So, the `<h1>` tag represents the most important heading of the first level, and the `<h6>` tag serves to indicate the heading of the sixth level and is the least significant. By default, the title of the first level is displayed in the largest font in bold, the headings of the next level are smaller in size.

The HTML file also supports embedding images, hyperlinks and more.

### In particular

In this case, HTML file contains traces of using a geojson file to create layers.
## Conclusions

There are many opensource and paid services that provide localization services and vice versa. Geojson files are a powerful tool for adding layers to your map for customization. HTML is not a programming language.

## Launch example

```python
>>> python main.py

Enter a year you would like to have a map for: 2000
Enter the coordinates of desired location separated by coma (format: lat, long): 45, 45
Initializing map creation process. Estimated time is 3-4 minutes.
Reading file...
Creating map...
Your map is created.
```
![2013_web_map](https://github.com/kenticent9/web_map/blob/master/images/Ukraine_2013.png)

## Contributing

Comments on bugs in the issues are welcomed. Contact email: yasinovskyi@ucu.edu.ua
