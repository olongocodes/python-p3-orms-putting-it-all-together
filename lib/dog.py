import sqlite3

DATABASE = 'example.db'


CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    
    def __init__(self, name, breed):
        self.id = None  # Initialize the id attribute to None for new instances
        self.name = name  # Set the name attribute with the provided value
        self.breed = breed  # Set the breed attribute with the provided value

    @classmethod
    def create_table(cls):
       
        #Create the 'dogs' table if it does not already exist.
        
        sql = '''
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        '''
        CURSOR.execute(sql)

    @classmethod
    def drop_table(cls):
       
       # Drop the 'dogs' table if it exists.
       
        sql = 'DROP TABLE IF EXISTS dogs'
        CURSOR.execute(sql)

    def save(self):
        
        # Save the Dog instance to the database.
        # If the instance has an ID, update the existing record; otherwise, insert a new record.
        
        if self.id is None:
            sql = 'INSERT INTO dogs (name, breed) VALUES (?, ?)'
            CURSOR.execute(sql, (self.name, self.breed))
            self.id = CURSOR.lastrowid
        else:
            sql = 'UPDATE dogs SET name=?, breed=? WHERE id=?'
            CURSOR.execute(sql, (self.name, self.breed, self.id))

        CONN.commit()

    @classmethod
    def create(cls, name, breed):
    
        #Create a new Dog instance, save it to the database, and return the instance.
    
        new_dog = cls(name, breed)
        new_dog.save()
        return new_dog

    @classmethod
    def new_from_db(cls, row):
       
        #Create a new Dog instance from a database row.
       
        dog = cls(name=row[1], breed=row[2])
        dog.id = row[0]
        return dog

    @classmethod
    def get_all(cls):
        
        #Retrieve all records from the 'dogs' table and return a list of Dog instances.
        
        sql = 'SELECT * FROM dogs'
        CURSOR.execute(sql)
        rows = CURSOR.fetchall()
        dogs = [cls.new_from_db(row) for row in rows]
        return dogs

    @classmethod
    def find_by_name(cls, name):
        
        #Find a Dog instance by name in the 'dogs' table.
        
        sql = 'SELECT * FROM dogs WHERE name=? LIMIT 1'
        CURSOR.execute(sql, (name,))
        row = CURSOR.fetchone()
        if row:
            dog = cls.new_from_db(row)
            return dog
        else:
            return None

    @classmethod
    def find_by_id(cls, dog_id):
        
        #Find a Dog instance by ID in the 'dogs' table.
        
        sql = 'SELECT * FROM dogs WHERE id=? LIMIT 1'
        CURSOR.execute(sql, (dog_id,))
        row = CURSOR.fetchone()
        if row:
            dog = cls.new_from_db(row)
            return dog
        else:
            return None

    @classmethod
    def find_or_create_by(cls, name, breed):
        
        # Find a Dog instance by name in the 'dogs' table.
        # If not found, create a new Dog instance with the provided name and breed.
        
        existing_dog = cls.find_by_name(name)
        if existing_dog:
            return existing_dog
        else:
            return cls.create(name, breed)

    def update(self):
        
        #Update the corresponding database record to match the current attribute values.
        
        self.save()

        pass
