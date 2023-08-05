UIUC CourseExplorer API
=======================
What is this?
-------------
This is an interface to the UIUC Course Explorer API.  It allows for the easy querying of class statuses from inside Python.
This library supports both async and standard queries to the API, as well as querying for specific CRNs.

Basic usage
-----------
The API is very simple to use:
::
    from uiucapi.query import get_course
    course = get_course("CS 374 FA17")
    for section in course.sections:
        print(section.registration_status)

Advanced features
-----------------
If aioquery is used instead of query, all of the methods are async coroutines, allowing for efficient querying.



