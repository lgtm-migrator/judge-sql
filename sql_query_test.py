# pylint: disable=missing-docstring

import unittest

from sql_query import SQLQuery


# @formatter:off
class TestSQLQuery(unittest.TestCase):
    def single_query(self, raw: str):
        queries = SQLQuery.from_raw_input(raw)
        self.assertEqual(len(queries), 1)
        return queries[0]

    def test_from_raw_input_1(self):
        queries = SQLQuery.from_raw_input(
            """-- First query:
        SELECT * from Users Where ";#" = 1;
        -- 2nd query:
        SELECT 1 # random comment"""
        )

        self.assertEqual(len(queries), 2)

        self.assertEqual(queries[0].without_comments, 'SELECT * from Users Where ";#" = 1;')
        self.assertEqual(queries[0].has_ending_semicolon, True)
        self.assertEqual(queries[1].without_comments, "SELECT 1")
        self.assertEqual(queries[1].has_ending_semicolon, False)

    def test_from_raw_input_2(self):
        queries = SQLQuery.from_raw_input("\n\r")
        self.assertEqual(len(queries), 0)

    def test_from_raw_input_3(self):
        queries = SQLQuery.from_raw_input(
            """
        SELECT NAME, RATE
        FROM CUSTOMER,
            DISCOUNT_CODE
        WHERE CUSTOMER.DISCOUNT_CODE = DISCOUNT_CODE.DISCOUNT_CODE;
        -- Alternatief
        -- SELECT NAME, RATE
        -- FROM CUSTOMER
        --          INNER JOIN DISCOUNT_CODE
        --                     ON CUSTOMER.DISCOUNT_CODE = DISCOUNT_CODE.DISCOUNT_CODE;
        """
        )
        self.assertEqual(len(queries), 1)

    def test_query_1(self):
        query = self.single_query('SELECT * from Users Where ";" = 1 ORdER BY Name ASC;')

        self.assertEqual(
            query.without_comments,
            'SELECT * from Users Where ";" = 1 ORdER BY Name ASC;',
        )
        self.assertEqual(query.has_ending_semicolon, True)
        self.assertEqual(query.is_select, True)
        self.assertEqual(query.is_ordered, True)

    def test_query_2(self):
        query = self.single_query('--SELECT\n   INSERT INTO table2 /**/  SELECT * FROM Users Where ";#ORDER BY" = 1;')

        self.assertEqual(
            query.without_comments,
            'INSERT INTO table2  SELECT * FROM Users Where ";#ORDER BY" = 1;',
        )
        self.assertEqual(query.has_ending_semicolon, True)
        self.assertEqual(query.is_select, False)
        self.assertEqual(query.is_ordered, False)

    def test_formatted(self):
        query = self.single_query("\n  SELeCT\n*\tFROm   USERS  \n\r")
        self.assertEqual(query.without_comments, "SELeCT\n*\tFROm   USERS")
        self.assertEqual(query.canonical, "SELeCT * FROm USERS")

        query = self.single_query(
            """
        SELECT *
            from users



            /* test */
        """
        )
        self.assertEqual(
            query.without_comments,
            """SELECT *
            from users""",
        )
        self.assertEqual(query.canonical, "SELECT * from users")

        query = self.single_query(
            """--Select all:
        SELECT * FROM Customers;"""
        )
        self.assertEqual(query.without_comments, "SELECT * FROM Customers;")
        self.assertEqual(query.canonical, "SELECT * FROM Customers ;")

        query = self.single_query("""SELECT * FROM Customers; --Select all:""")
        self.assertEqual(query.without_comments, "SELECT * FROM Customers;")
        self.assertEqual(query.canonical, "SELECT * FROM Customers ;")

        query = self.single_query(
            """# Select all:
        Select * FROM Customers;"""
        )
        self.assertEqual(query.without_comments, "Select * FROM Customers;")
        self.assertEqual(query.canonical, "Select * FROM Customers ;")

        query = self.single_query("""SELECT * FROM Customers; # Select all:""")
        self.assertEqual(query.without_comments, "SELECT * FROM Customers;")
        self.assertEqual(query.canonical, "SELECT * FROM Customers ;")

        query = self.single_query(
            """/* Select all employees whose compensation is
        greater than that of Pataballa. */
        SELECT * FROM Customers; # Select all:"""
        )
        self.assertEqual(query.without_comments, "SELECT * FROM Customers;")
        self.assertEqual(query.canonical, "SELECT * FROM Customers ;")

        query = self.single_query(
            """/* Select all employees whose compensation is
        greater than that of Pataballa. */
        SELECT * FROM Customers; # Select all:"""
        )
        self.assertEqual(query.without_comments, "SELECT * FROM Customers;")
        self.assertEqual(query.canonical, "SELECT * FROM Customers ;")

    def test_canonical_special(self):
        query = self.single_query(
            """-- /* aa*/
            /*
                    -- qq
            */
            SELECT'test'FROM[Customers]WHERE 1=1 OR 2-4=33 OR '    like   ' LIKE'%%'; # Select all:"""
        )
        self.assertEqual(
            query.canonical, "SELECT 'test' FROM [Customers] WHERE 1 = 1 OR 2 -4 = 33 OR '    like   ' LIKE '%%' ;"
        )

        query = self.single_query(
            """SELECT'test'FROM[Customers]WHERE 1=1 OR 2-4=33 OR '    like   ' LIKE'%%'; # Select all:"""
        )
        self.assertEqual(
            query.canonical, "SELECT 'test' FROM [Customers] WHERE 1 = 1 OR 2 -4 = 33 OR '    like   ' LIKE '%%' ;"
        )

        query = self.single_query("select'asdf'as[asdf]into[#MyTable]")
        self.assertEqual(query.canonical, "select 'asdf' as [asdf] into [#MyTable]")

        query = self.single_query("SELECT(COUNT(id))FROM(users)where(id>5)")
        self.assertEqual(query.canonical, "SELECT ( COUNT ( id ) ) FROM ( users ) where ( id > 5 )")

        query = self.single_query("SELECT(count(name))[aaaaa],[name]as'test'FROM(sqlite_master);")
        self.assertEqual(
            query.canonical, "SELECT ( count ( name ) ) [aaaaa], [name] as 'test' FROM ( sqlite_master ) ;"
        )

        query = self.single_query("SELECT'\n\n\n',(\ncount\n(name))\n[aaaaa],[name]as'test'FROM(sqlite_master);")
        self.assertEqual(
            query.canonical, "SELECT '\n\n\n', ( count ( name ) ) [aaaaa], [name] as 'test' FROM ( sqlite_master ) ;"
        )

    def test_is_select(self):
        query = self.single_query("  SELeCT\n*\tFROm   USERS  \n\r")
        self.assertEqual(query.canonical, "SELeCT * FROm USERS")
        self.assertEqual(query.is_select, True)

        query = self.single_query("\nSELECT *\n    from\n       users\n")
        self.assertEqual(query.canonical, "SELECT * from users")
        self.assertEqual(query.is_select, True)

        query = self.single_query(
            """
        INSERT INTO table2
        SELECT * FROM table1
        WHERE condition;
        """
        )
        self.assertEqual(query.canonical, "INSERT INTO table2 SELECT * FROM table1 WHERE condition ;")
        self.assertEqual(query.is_select, False)

        query = self.single_query(
            """
        -- Comment
        SELECT * FROM table1
        WHERE condition;
        """
        )
        self.assertEqual(query.canonical, "SELECT * FROM table1 WHERE condition ;")
        self.assertEqual(query.is_select, True)

    def test_is_ordered(self):
        query = self.single_query(
            """SELECT column1, column2
        FROM table_name
        ORDER BY column1, column2 ASC|DESC;
        """
        )
        self.assertEqual(
            query.canonical, "SELECT column1, column2 FROM table_name ORDER BY column1, column2 ASC | DESC ;"
        )
        self.assertEqual(query.is_ordered, True)

        query = self.single_query(
            """# ORDER BY
        SELECT column1, column2
        FROM table_name
        """
        )
        self.assertEqual(query.canonical, "SELECT column1, column2 FROM table_name")
        self.assertEqual(query.is_ordered, False)

        query = self.single_query("select * from users")
        self.assertEqual(query.canonical, "select * from users")
        self.assertEqual(query.is_ordered, False)

        query = self.single_query('select "ORDER BY" from users')
        self.assertEqual(query.canonical, 'select "ORDER BY" from users')
        self.assertEqual(query.is_ordered, False)

        query = self.single_query('select "ORDER BY", (SELECT 1 ORDER BY test) from users')
        self.assertEqual(query.canonical, 'select "ORDER BY", ( SELECT 1 ORDER BY test ) from users')
        self.assertEqual(query.is_ordered, False)

    def test_query_type(self):
        query = self.single_query('select * from users WHERE zip LIKE "test"')
        self.assertEqual(query.type, "SELECT")

        query = self.single_query('INSERT INTO table_name (column) VALUES ("value");')
        self.assertEqual(query.type, "INSERT")

        query = self.single_query("DELETE FROM table_name WHERE condition;")
        self.assertEqual(query.type, "DELETE")

        query = self.single_query("INSERT INTO table2 SELECT * FROM table1 WHERE condition;")
        self.assertEqual(query.type, "INSERT")

    def test_match_keywords(self):
        query = self.single_query('select * from users WHERE zip LIKE "test"')
        self.assertEqual(query.match_regex("LIKE"), "LIKE")

        query = self.single_query('select * from users WHERE zip = "LIKE"')
        self.assertEqual(query.match_regex("select"), "select")
        self.assertEqual(query.match_regex("sel"), None)
        self.assertEqual(query.match_regex("sel..."), "select")
        self.assertEqual(query.match_regex("from"), "from")
        self.assertEqual(query.match_regex("users"), "users")
        self.assertEqual(query.match_regex("WHERE"), "WHERE")
        self.assertEqual(query.match_regex("zip"), "zip")
        self.assertEqual(query.match_regex('"LIKE"'), '"LIKE"')
        self.assertEqual(query.match_regex("LIKE"), None)

        query = self.single_query('select (SELECT COUNT(*) FROM table WHERE zip = "LIKE") from users')
        self.assertEqual(query.match_regex("select"), "select")
        self.assertEqual(query.match_regex("count"), "COUNT")
        self.assertEqual(query.match_regex("from"), "FROM")
        self.assertEqual(query.match_regex("table"), "table")
        self.assertEqual(query.match_regex("WHERE"), "WHERE")
        self.assertEqual(query.match_regex("zip"), "zip")
        self.assertEqual(query.match_regex("users"), "users")

        query = self.single_query("select CITY as like from users")
        self.assertEqual(query.match_regex("select"), "select")
        self.assertEqual(query.match_regex("CITY"), "CITY")
        self.assertEqual(query.match_regex("as"), "as")
        self.assertEqual(query.match_regex("like"), "like")
        self.assertEqual(query.match_regex("from"), "from")
        self.assertEqual(query.match_regex("users"), "users")

        query = self.single_query("select DISTICT CITY from users")
        self.assertEqual(query.match_regex("select"), "select")
        self.assertEqual(query.match_regex("DISTICT"), "DISTICT")
        self.assertEqual(query.match_regex("CITY"), "CITY")
        self.assertEqual(query.match_regex("from"), "from")
        self.assertEqual(query.match_regex("users"), "users")

        query = self.single_query("select DISTICT CITY from users where name not like 'test%'")
        self.assertEqual(query.match_regex(".*like"), "not like")


# @formatter:on

if __name__ == "__main__":
    unittest.main()
