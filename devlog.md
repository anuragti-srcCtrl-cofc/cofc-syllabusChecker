## Support for .pages - Not successful yet
Adding support for Apple's .pages files requires some additional handling since .pages files are not straightforward text-based files like .docx or .md. Instead, they are ZIP archives that contain several files, including XML files where the actual content is stored.

 can extract and read the text content from .pages files using the zipfile module.