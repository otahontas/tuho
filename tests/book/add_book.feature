Feature: User can add new books

Scenario: Database is empty when no books have been added
    Given I haven't added any books
    When I check what's in database
    Then System will report that db is empty

Scenario: User added books are saved persistently
    Given I have a new book with name, writer and isbn
    When I try to add new book with name, writer and isbn
    Then System will add book to db

# TODO: implement these scanarios later

    #Scenario: User cannot add new books without specifying isbn, name and author
    #    Given I have a new book with only comment
    #    When I try to add new book 
    #    Then System will not add book to db
    #
    #Scenario: User cannot add a book twice with the same name
    #    Given I have a book with name that is already in db
    #    When I try to add new book 
    #    Then System will not add book to db
    #
    #
    #Scenario: User cannot add a book twice with the same isbn
    #    Given I have a book with isbn that is already in db
    #    When I try to add new book 
    #    Then System will not add book to db
