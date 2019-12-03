from pytest_bdd import given, scenarios, then, when


"""Define cucumber tests here with BDD stylings"""


# Scenarios
scenarios('add_book.feature')


# Given steps

@given("I haven't added any books")
def pass_without_books():
    pass


@given("I have a new book with name, writer and isbn")
def create_book_with_needed_details():
    return dict(header='test',
                writer='writer',
                ISBN=123,
                comment='comment')

# When steps


@when("I check what's in database")
def check_db():
    pass


@when("I try to add new book with name, writer and isbn")
def add_book(client):
    client.post('/bookmarks',
                data=dict(
                    header='test',
                    writer='writer',
                    ISBN=123,
                    comment='comment'
                ),
                follow_redirects=True)


# Then steps

@then("System will report that db is empty")
def check_db_is_empty(client):
    rv = client.get('/list')
    assert b'Tietokanta on tyhj' in rv.data


@then("System will add book to db")
def check_db_has_book(client):
    rv = client.get('/list')
    assert b'test' in rv.data
    assert b'Tietokanta on tyhj' not in rv.data
