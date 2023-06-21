from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user_model

class Recipes:

    DB = 'recipes_schema'
    tables = 'recipes'

    def __init__(self, data) -> None:
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instruction = data['instruction']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def get_all(cls):
        query = f'SELECT * FROM {cls.tables};'
        results = connectToMySQL(cls.DB).query_db(query)
        recipes = []
        if results:
            for recipe in results:
                recipes.append( cls(recipe) )
        return recipes
    
    @classmethod
    def get_one(cls, id):
        query = f'SELECT * FROM {cls.tables} WHERE id = %(id)s;'
        data={'id':id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results)< 1:
            return False
        return cls(results[0])
    
    @classmethod
    def save(cls, data):
        query = f'''INSERT INTO {cls.tables} 
                (name, description, instruction, under_30, user_id, updated_at) 
                VALUES (  %(name)s, %(description)s, %(instruction)s, %(under_30)s, %(user_id)s, %(updated_at)s  );'''
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def update(cls, data):
        query = f'''UPDATE {cls.tables} SET
                name = %(name)s, 
                description = %(description)s, 
                instruction = %(instruction)s, 
                updated_at = %(updated_at)s,
                under_30 = %(under_30)s
                WHERE id = %(id)s;'''
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def delete(cls, id):
        query = f'DELETE FROM {cls.tables} WHERE id = %(id)s;'
        data = {'id' : id}
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_one_recipe_info(cls, id):
        query = '''
                SELECT recipes.id, name, description, instruction, recipes.updated_at, under_30, user_id, first_name
                FROM recipes
                LEFT JOIN users ON users.id = user_id
                WHERE recipes.id = %(id)s;'''
        data = {'id':id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results)< 1:
            return False
        recipe_info = results[0]
        return recipe_info

    @classmethod
    def get_one_recipe_info2(cls, id):
        query = '''
                SELECT * FROM recipes
                LEFT JOIN users ON users.id = user_id
                WHERE recipes.id = %(id)s;'''
        data = {'id':id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results)< 1:
            return False
        recipe_info = []
        for row in results:
            user_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            one_recipe = cls(row)
            one_recipe.user = user_model.Users(user_data)
            recipe_info.append(one_recipe)
        return recipe_info[0]

    # more than just data. access recipe and append user info
    # updated get recipe format
    @classmethod
    def get_all_recipe_info(cls):
        query = '''
            SELECT * FROM recipes
            JOIN users ON users.id = user_id;
        '''
        results = connectToMySQL(cls.DB).query_db(query)
        all_recipes = []
        if results:
            for row in results:
                user_data = {
                    'id': row['users.id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['email'],
                    'password': row['password'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at']
                }
                one_recipe = cls(row)
                one_recipe.user = user_model.Users(user_data)
                all_recipes.append(one_recipe)
        return all_recipes
    
    # added static method to validate forms
    @staticmethod
    def validate_recipe(form):
        is_valid = True
        if len(form['name']) < 3:
            flash('Name must be at least 3 characters')
            is_valid = False
        if len(form['description']) < 3:
            flash('Description must be at least 3 characters')
            is_valid = False
        if len(form['instruction']) < 3:
            flash('Instructions must be at least 3 characters')
            is_valid = False
        if len(form['updated_at']) < 1:
            flash('Please select a date')
            is_valid = False
        return is_valid
