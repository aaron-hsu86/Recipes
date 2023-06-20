from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

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
                (name, description, instruction, under_30, user_id) 
                VALUES (  %(name)s, %(description)s, %(instruction)s, %(under_30)s, %(user_id)s  );'''
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
    def get_recipe_info(cls, id):
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
    def get_all_recipe_info(cls):
        query = '''
                SELECT recipes.id, name, under_30, user_id, first_name
                FROM recipes
                LEFT JOIN users ON users.id = user_id;'''
        results = connectToMySQL(cls.DB).query_db(query)
        recipes = []
        if results:
            for recipe in results:
                recipes.append( recipe )
        return recipes