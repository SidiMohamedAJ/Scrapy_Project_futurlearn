import os

import psycopg2
from itemadapter import ItemAdapter
from .items import Categorie, SubCategorie, Course, Instructor, CourseInstructor, Organization, CourseOrganization, InstructorOrganization


class FutureLearnPipeline:
    def open_spider(self, spider):
        self.conn = psycopg2.connect(
            dbname='big_format_db',
            user='postgres',
            password='1234',
            host='localhost',
            port='5432',
        )
        self.cur = self.conn.cursor()

        file_path = os.path.join(os.path.dirname(__file__), 'files', 'db_setup.txt')
        self.setup(file_path)
    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

    def setup(self, setup_file):
        try:
            with open(setup_file, 'r') as file:
                sql_queries = file.read()
            queries = sql_queries.split(';')
            for query in queries:
                if query.strip():
                    self.cur.execute(query)
                    self.conn.commit()

            print("SQL file executed successfully!")

        except psycopg2.Error as e:
            print("Error: Unable to connect to the PostgreSQL database or execute SQL file.")
            print(e)

    def process_item(self, item, spider):
        if isinstance(item, Categorie):
            self.insert_categorie(item)
        elif isinstance(item, SubCategorie):
            self.insert_subcategorie(item)
        elif isinstance(item, Course):
            self.insert_course(item)
        elif isinstance(item, Instructor):
            self.insert_instructor(item)
        elif isinstance(item, CourseInstructor):
            self.insert_course_instructor(item)
        elif isinstance(item, Organization):
            self.insert_organization(item)
        elif isinstance(item, CourseOrganization):
            self.insert_course_organization(item)
        elif isinstance(item, InstructorOrganization):
            self.insert_instructor_organization(item)


        return item

    def insert_categorie(self, item):
        try:
            self.cur.execute(
                "INSERT INTO categorie (id, name, description, link) VALUES (%s, %s, %s, %s)",
                (item['id'], item['name'], item['description'], item['link'])
            )
            self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            print(e)

    def insert_subcategorie(self, item):
        try:
            self.cur.execute(
                "INSERT INTO SubCategorie (id, name, link, categorie_id) VALUES (%s, %s, %s, %s)",
                (item['id'], item['name'], item['link'], item['categorie_id'])
            )
            self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            print(e)

    def insert_course(self, item):
        try:
            self.cur.execute(
                "INSERT INTO Course (id, title, url, duration,rating,type,price,  sub_categorie_id) VALUES (%s, %s, %s, %s, %s,%s,%s,%s)",
                (item['id'], item['title'], item['url'], item['duration'],item['rating'],
                 item['type'], item['price'], item['sub_categorie_id'])
            )
            self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            print(e)

    def insert_instructor(self, item):
        try:
            self.cur.execute(
                "INSERT INTO Instructor (id, name, url, image_url, description) VALUES (%s, %s, %s, %s, %s)",
                (item['id'], item['name'], item['url'], item['image_url'], item['description'])
            )
            self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            print(e)

    def insert_course_instructor(self, item):
        try:
            self.cur.execute(
                "INSERT INTO CourseInstructor (course_id, instructor_id) VALUES (%s, %s)",
                (item['course_id'], item['instructor_id'])
            )
            self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            print(e)

    def insert_organization(self, item):
        try:
            self.cur.execute(
                "INSERT INTO Organization (id, name, contact_url, img_url, description, phone, e_mail) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (item['id'], item['name'], item['contact_url'], item['img_url'], item['description'], item['phone'],
                 item['e_mail'])
            )
            self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            print(e)

    def insert_course_organization(self, item):
        try:
            self.cur.execute(
                "INSERT INTO CourseOrganization (course_id, organization_id) VALUES (%s, %s)",
                (item['course_id'], item['organization_id'])
            )
            self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            print(e)

    def insert_instructor_organization(self, item):
        try:
            self.cur.execute(
                "INSERT INTO InstructorOrganization (instructor_id, organization_id) VALUES (%s, %s)",
                (item['instructor_id'], item['organization_id'])
            )
            self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            print(e)
