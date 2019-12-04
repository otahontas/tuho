Feature: User can add new books

Scenario: Database is empty when no books have been added
    Given I haven't added any books
    When I check what's in database
    Then System will report that db is empty

Scenario: User added books are saved persistently
    Given I have a new book with name, writer and isbn
    When I try to add new book with name, writer and isbn
    Then System will add book to db
