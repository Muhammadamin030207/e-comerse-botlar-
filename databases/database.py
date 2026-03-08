import asyncpg
from config import config


class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(
            database=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            host=config.DB_HOST,
            port=config.DB_PORT
        )

    async def check_user(self, user_id):
        query = "SELECT * FROM users2 WHERE user_id = $1"
        return await self.pool.fetchrow(query, user_id)

    async def user_profile(self, user_id):
        query = "SELECT full_name, age, email, contact FROM users2 WHERE user_id = $1"
        return await self.pool.fetchrow(query, user_id)



    async def add_user(self, user_id, full_name, age, email, contact):
        query = """
        INSERT INTO users2 (user_id, full_name, age, email, contact)
        VALUES ($1, $2, $3, $4, $5)
        ON CONFLICT (user_id) DO NOTHING;
        """
        await self.pool.execute(query, user_id, full_name, int(age), email, contact)

    async def get_user_role(self, user_id):
        query = """
        SELECT role FROM users2 WHERE user_id = $1;
        """
        return await self.pool.fetchval(query, user_id)

    async def get_users(self):
        query = """
        SELECT full_name, role,user_id FROM users2 order by id;
        """
        return await self.pool.fetch(query)
    
    async def get_user_id(self,user_id):
        query = """
        select id from users2 where user_id=$1"""
        return await self.pool.fetchval(query, user_id)

    async def set_user_role(self, user_id, role):
        query = """
        UPDATE users2 SET role = $1 WHERE user_id = $2;
        """
        await self.pool.execute(query, role, user_id)   

    async def get_products(self):
        query = """
        select id,name,price,description from products order by id;
        """
        return await self.pool.fetch(query)

    async def add_product(self, name, price, description):
        query = """
        insert into products(name,price,description) values($1,$2,$3);
        """
        await self.pool.execute(query, name, int(price), description)

    async def delete_product(self, product_id):
        query = """
        delete from products where id = $1;
        """
        await self.pool.execute(query, product_id)

    async def update_product(self, product_id, name, price, description):
        query = """
        update products set name = $1, price = $2, description = $3 where id = $4;
        """
        await self.pool.execute(query, name, int(price), description, product_id)

    async def get_or_create_cart(self,user_id):
        order = await self.pool.fetchrow("SELECT id FROM orders WHERE user_id = $1 AND order_status = 'cart'", user_id)

        if order:
            return order["id"]

        
        order = await self.pool.fetchrow("""
            INSERT INTO orders (user_id) VALUES ($1) RETURNING id
        """, user_id)

        return order["id"]
    

    async def add_product_to_cart(self, user_id, product_id):
        order_id = await self.get_or_create_cart(user_id)

        await self.pool.execute("""
            INSERT INTO order_items (order_id, product_id) VALUES ($1, $2)
        """, order_id, product_id)

    async def get_cart_products(self,user_id):
        order_id = await self.get_or_create_cart(user_id)
        return await self.pool.fetch("""
            SELECT p.id, p.name, p.price, p.description
            FROM order_items ci
            JOIN products p ON ci.product_id = p.id
            WHERE ci.order_id = $1
        """, order_id)
