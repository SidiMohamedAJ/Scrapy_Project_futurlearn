import scrapy
from urllib.parse import urljoin
import hashlib
from ..items import Categorie, SubCategorie, Course, Instructor, CourseInstructor, Organization, CourseOrganization, InstructorOrganization

class FuturlearnSpiderSpider(scrapy.Spider):
    name = "futurlearn_spider"
    allowed_domains = ["www.futurelearn.com"]
    start_urls = ["https://www.futurelearn.com/subjects"]


    def parse(self, response):
        # Sélectionner tous les éléments li avec la classe "list-listItem_NceHt"
        subjects = response.xpath('//li[@class="list-listItem_NceHt"]')

        for subject in subjects:
            # Extraire l'URL du sujet
            link = subject.xpath('.//a/@href').get()

            # Extraire le titre du sujet
            title = subject.xpath('.//p[@class="subjectCard-title_q-L51"]/text()').get()

            # Extraire la description du sujet
            description = subject.xpath(
                './/p[@class="text-module_wrapper__Dg6SG text-module_white__-TrpJ text-module_sBreakpointSizesmall__6hBFg text-module_sBreakpointAlignmentleft__NFsd7 text-module_isRegular__cAvX9"]/text()').get()

            url = urljoin(self.start_urls[0], link)

            # Générer un identifiant unique pour le sujet à partir de son URL
            subject_id = hashlib.sha256(url.encode()).hexdigest()

            categorie_item = Categorie(
                id=subject_id,
                name=title.strip() if title else None,
                description=description.strip() if description else None,
                link=url,
            )
            yield categorie_item

            yield scrapy.Request(
                url,
                callback=self.parse_subSubject,
                meta=dict(
                    categorie_id=subject_id,
                )
            )

    def parse_subSubject(self, response):
        subjects = response.xpath('//div[@class="RelatedLinks-link_gt+eO"]')

        for subject in subjects:
            # Extraire le titre du sujet
            title = subject.xpath('.//span[contains(@class, "index-module_content__pkuA-")]/span/text()').get()

            # Extraire le lien du sujet
            link = subject.xpath('.//a/@href').get()
            url = urljoin(self.start_urls[0], link)

            # Générer un identifiant unique pour le sujet à partir de son URL
            subject_id = hashlib.sha256(url.encode()).hexdigest()

            SubCategorie_item = SubCategorie(
                id=subject_id,
                name=title,
                link=urljoin(response.url, link),
                categorie_id=response.meta['categorie_id'],
            )
            yield SubCategorie_item

            yield scrapy.Request(
                url,
                callback=self.parse_courses,
                meta=dict(
                    subject_id=subject_id,
                )
            )

    def parse_courses(self, response):
        courses = response.xpath('//div[@class="m-card Container-wrapper_7nJ95 Container-grey_75xp-"]')

        for course in courses:
            title = course.xpath('.//div[@class="Title-wrapper_5eSVQ"]/h3/text()').get()
            # durations = course.xpath(
            #     './/div[@class="align-module_wrapper__RpD0z align-module_sBreakpointDirectionhorizontal__aCYX5"]//p/text()').getall()
            link = course.xpath('.//a[@class="link-wrapper_djqc+"]/@href').get()
            url = urljoin(response.url, link)

            # Générer un identifiant unique pour le cours à partir de son title
            course_id = hashlib.sha256(title.encode()).hexdigest()

            course_list = []
            Course_item = {
                'id': course_id,
                'title': title,
                'url': url,
                'sub_categorie_id': response.meta['subject_id'],
            }
            course_list.append(Course_item)

            yield scrapy.Request(
                url,
                callback=self.parse_details,
                meta=dict(
                    course_id=course_id,
                    course_list=course_list,
                )
            )



    def parse_details(self, response):

        # Récupérer tous les éléments contenant les informations sur les cours
        course_elements = response.xpath('//div[@class="PageHeader-keyInfoWrapper_Av5ok"]')
        courses = response.xpath('//div[@class="InformationWidget-widgetWrapper_6ZMLn"]')

        for course_element, course_info in zip(course_elements, courses):
            # extract title
            title = course_info.xpath('.//h1/text()').extract_first()
            rating = course_info.xpath('.//div[contains(@class,"ReviewStars-text_ABUtn")]/text()').get()
            # Extraction de la durée
            duration = course_element.xpath(
                './/p[contains(text(), "Duration")]/following-sibling::span/text()').get()
            # Extraction du type (100% online)
            online_type = course_element.xpath('.//p[contains(text(), "100% online")]/text()').get()
            # extract price
            price = course_element.xpath('.//span[contains(@id, "sale-price")]/text()').get()

            # Générer un identifiant unique pour le cours à partir de son title
            course_id = hashlib.sha256(title.encode()).hexdigest()

            # Récupérer les données des détails des cours
            course_list = response.meta['course_list']
            for course in course_list:
                if course_id == response.meta['course_id']:
                    # create your course item with all details
                    course_item = Course(
                        id=course_id,
                        title=title,
                        url=course['url'],
                        rating=rating,
                        duration=duration,
                        type=online_type,
                        price=price,
                        sub_categorie_id=course['sub_categorie_id'],
                    )
                    yield course_item

        # Initialiser les dictionnaires pour stocker les correspondances
        course_instructor_dict = {}
        course_organization_dict = {}

        # Sélectionner la section contenant les formateurs de cours
        educators_section = response.xpath('//section[@id="section-educators"]')

        # Sélectionner tous les éléments div contenant les informations sur les formateurs
        educators = educators_section.xpath(
            './/div[@class="mediaElement-wrapper_AE2Pr mediaElement-isEducatorGrid_8-QdV"]')

        for educator in educators:
            # Extraire le nom du formateur
            name = educator.xpath('.//h3//text()').get()

            # Extraire la description du formateur
            description = educator.xpath('.//div[@class="educators-shortDescription_qvIAh"]//p//text()').get()

            # Extraire l'url image formateur
            image_url = educator.xpath('.//img[@class="image-module_image__hvXRh"]/@src').get()

            # Générer un identifiant unique pour le formateur à partir de son name
            formateur_id = hashlib.sha256(name.encode()).hexdigest()

            # Instructor item
            instructor_item = Instructor(
                id=formateur_id,
                name=name,
                description=description,
                url=None,
                image_url=image_url,
            )

            yield instructor_item

            # CourseInstructor item
            courseInstructor_item = CourseInstructor(
                course_id=response.meta['course_id'],
                instructor_id=formateur_id,
            )
            yield courseInstructor_item

            # Enregistrer les ids de cours et d'entités dans les dictionnaires
            course_instructor_dict.setdefault(response.meta['course_id'], []).append(formateur_id)


        # Extraire les informations de l'organisation
        organization_elements = response.xpath('//div[contains(@class, "spotlight-wrapper_wkcs+")]')

        for org_elem in organization_elements:
            # Extraire le nom de l'organisation
            organisation_name = org_elem.xpath('.//h2/text()').get()

            # Extraire la description de l'organisation
            organisation_description = org_elem.xpath('.//div[@data-testid="dangerously-set"]/p/text()').get()
            image_url = org_elem.xpath('.//img[contains(@class, "image-module_image__hvXRh")]/@src').get()
            details_url = org_elem.xpath('.//a/@href').get()

            # Générer un identifiant unique pour l'organisation à partir de son name
            organisation_id = hashlib.sha256(organisation_name.encode()).hexdigest()

            # Organization item
            organization_item = Organization(
                id=organisation_id,
                name=organisation_name,
                description=organisation_description,
                img_url=image_url,
                contact_url=urljoin('https://www.futurelearn.com', details_url),
                phone=None,
                e_mail=None,
            )
            yield organization_item

            courseOrganization = CourseOrganization(
                course_id=response.meta['course_id'],
                organization_id=organisation_id,
            )
            yield courseOrganization

            # Enregistrer les ids de cours et d'entités dans les dictionnaires
            course_organization_dict.setdefault(response.meta['course_id'], []).append(organisation_id)

        course_id = response.meta['course_id']
        # Comparer les ids de cours pour trouver les correspondances
        if course_id in course_instructor_dict and course_id in course_organization_dict:
            formateurs = course_instructor_dict[course_id]
            organisations = course_organization_dict[course_id]

            for formateur_id, organisation_id in zip(formateurs,organisations):
                # Correspondance trouvée, enregistrement dans la table InstructorOrganization
                instructor_organization_item = InstructorOrganization(
                    instructor_id=formateur_id,
                    organization_id=organisation_id,
                )
                yield instructor_organization_item