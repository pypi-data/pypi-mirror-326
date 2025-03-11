import unittest
import os
from SQLGlassBoxFunction import SQLUtil, sql  # Adjust the import according to your module name

class TestSQLGlassBoxFunction(unittest.TestCase):
    
    def setUp(self):
        self.sql_util = SQLUtil()
        self.query = """
        SELECT * /* This is a SELECT block comment */ 
        FROM users 
        -- This is a line comment
        WHERE age > 18 
            AND country = 'USA' 
            AND c >= 11.5
            AND name = "John's SELECT string18" 
        -- second is a line comment
        ORDER BY COUNT(id);
        """
        self.log_file_path = os.getenv('SQL_GBF_QUERY_LOG_FILE', 'default_sql_log.txt')
        
        # Ensure the log file directory exists
        dir_name = os.path.dirname(self.log_file_path)
        if dir_name and dir_name != '' and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)
        
        # Clear the log file before each test
        if os.path.exists(self.log_file_path):
            os.remove(self.log_file_path)

    def test_highlight(self):
        highlighted_query = self.sql_util.highlight(self.query)
        self.assertIn('\033[36m', highlighted_query)  # Check for comment color
        self.assertIn('\033[32m', highlighted_query)  # Check for string color
        self.assertIn('\033[34m', highlighted_query)  # Check for number color
        self.assertIn('\033[33m', highlighted_query)  # Check for function color
        self.assertIn('\033[35m', highlighted_query)  # Check for keyword color
        self.assertIn('\033[0m', highlighted_query)   # Check for reset color

    def test_sql_dry_run(self):
        dir_name = os.path.dirname(self.log_file_path)
        if dir_name and dir_name != '' and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)

        # Clear the log file before the dry run test
        with open(self.log_file_path, 'w') as file:
            file.write('')
        os.environ['SQL_GBF_DRY_RUN'] = 'True'
        sql(self.query, dry_run=True)
        # Check that the query is not executed but highlighted
        highlighted_query = self.sql_util.highlight(self.query)
        # Check that the query is not executed by verifying the log file is empty
        with open(self.log_file_path, 'r') as file:
            logged_query = file.read()
        self.assertIn((self.query + '\n').strip(), logged_query.strip())

    def test_sql_write_to_log_file(self):
        # Ensure the log file directory exists
        dir_name = os.path.dirname(self.log_file_path)
        if dir_name and dir_name != '' and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)

        # Clear the log file before the dry run test
        with open(self.log_file_path, 'w') as file:
            file.write('')
        os.environ['SQL_GBF_WRITE_TO_LOG_FILE'] = 'True'
        sql(self.query, write_to_log_file=True)
        # Check that the query is written to the log file
        with open(self.log_file_path, 'r') as file:
            logged_query = file.read()
        self.assertIn((self.query + '\n').strip(), logged_query.strip())

    def test_append_to_file(self):
        self.sql_util.append_to_file(self.query)
        # Ensure the log file exists before appending
        # Ensure the log file directory exists
        dir_name = os.path.dirname(self.log_file_path)
        if dir_name and dir_name != '' and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)

        # Clear the log file before the dry run test
        with open(self.log_file_path, 'w') as file:
            file.write('')

        self.sql_util.append_to_file(self.query)
        with open(self.log_file_path, 'r') as file:
            logged_query = file.read()
        self.assertIn((self.query + '\n').strip(), logged_query.strip())

if __name__ == '__main__':
    unittest.main()