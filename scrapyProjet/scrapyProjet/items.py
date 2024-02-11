# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class Categorie(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    link = scrapy.Field()

class SubCategorie(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    link = scrapy.Field()
    categorie_id = scrapy.Field()

class Course(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    desc = scrapy.Field(default="pas disponible")
    img_url = scrapy.Field(default="pas disponible")
    rating = scrapy.Field(default="pas disponible")
    num_reviews = scrapy.Field(default="pas disponible")
    duration = scrapy.Field(default="pas disponible")
    price = scrapy.Field(default="pas disponible")
    level = scrapy.Field(default="pas disponible")
    type = scrapy.Field(default="pas disponible")
    sub_categorie_id = scrapy.Field(default="pas disponible")


class CourseInstructor(scrapy.Item):
    course_id = scrapy.Field(default="pas disponible")
    instructor_id = scrapy.Field(default="pas disponible")

class CourseOrganization(scrapy.Item):
    course_id = scrapy.Field(default="pas disponible")
    organization_id = scrapy.Field(default="pas disponible")

class InstructorOrganization(scrapy.Item):
    instructor_id = scrapy.Field(default="pas disponible")
    organization_id = scrapy.Field(default="pas disponible")

class Instructor(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field(default="pas disponible")
    image_url = scrapy.Field(default="pas disponible")
    desc = scrapy.Field(default="pas disponible")


class Organization(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    contact_url = scrapy.Field(default="pas disponible")
    img_url = scrapy.Field(default="pas disponible")
    desc = scrapy.Field(default="pas disponible")
    phone = scrapy.Field(default="pas disponible")
    e_mail = scrapy.Field(default="pas disponible")
