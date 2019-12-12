# Sprint 3:
- as a user, I want preview book details after giving ISBN
    - Confirmators:
        - Book can be previewed before adding to database
- as a user, I want to filter my bookmarks based on read status
    - Confirmators:
        - Read status used as filter in main view
        - Filtering works like filtering with bookmark type
- as a user, I want my book bookmarks to have book covers
    - Confirmators:
        - App gets book cover from google api and in cover is not present, uses a placeholder
- as a user, I want to comment my bookmarks from individual bookmarks view page
    - Confirmators:
        - Comment can be added when viewing individual bookmarks, no need to go to edit page
- as a user, I want to have all youtube link details to be added automatically
    - Confirmators:
        - User can add video link and it updates automatically
- as a user, I want to have colors on read/unread -status
    - Confirmators:
        - Some color is added to the UI

# Sprint 2:
- as a user, I want to add new YouTube video
    - Confirmators:
        - Video can be added by YouTube URL
- as a user, I want to categorises bookmarks on the list view
    - Confirmators:
        - List only videos or books
        - Use buttons for selecting category
- as a user, I want to add book by ISBN
    - Confirmators:
        - Book information (title, author) fetched automatically and added to database
- as a user, I want to view single bookmark
    - Confirmators:
        - All bookmark information viewable
        - Embed YouTube video on video bookmark page
- as a user, I want to edit single bookmark
    - Confirmators:
        - All fields editable
        - Edit updates database correctly

# Sprint 1:
- as a user, I want to add new books
    - Confirmators:
        - Each book can be only added once via form
        - Book cannot be added without name, writer and isbn.
- as a user, I list my books
    - Confirmators:
        - All books are listed in listing view
- as a user, I want to modify books
    - Confirmators:
        - Book cannot be changed to already unique book
        - Changes made via form are also updated in db
- as a user, I want to delete books

# Rest:
- as a user, I browse my bookmarks based on name
- as a user, I browse my bookmarks based on tag
- as a user, I want to add new podcasts
- as a user, I want to add new links
- as a user, I want to tag my bookmarks
- as a user, I want to add related courses to my bookmarks
- as a user, I want to search for my bookmarks based on name
- as a user, I want to search for my bookmarks based on reading status
- as a user, I want to search for my bookmarks based on tag
- as a user, I want to register to bookmark website
- as a user, I want to modify my account information
- as a user, I want to login and logout
