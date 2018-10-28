# -*- coding: utf-8 -*-
# author:Sunqi

import xadmin
from .models import CityDict, CourseOrg, Teacher


class CirtDictAdmin():
    list_display = ['name', 'add_time', 'desc']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'add_time', 'desc']


class CourseOrgAdmin():
    list_display = ['id', 'name', 'desc', 'address', 'click_nums', 'fav_nums', 'image', 'city', 'add_time']
    search_fields = ['name', 'desc', 'address', 'image', 'city']
    list_filter = ['name', 'desc', 'address', 'image', 'city', 'add_time']
    reifield_style = 'fk_ajax'

class TeacherAdmin():
    list_display = ['id', 'org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums',
                    'fav_nums', 'add_time']
    search_fields = ['org', 'name', 'work_years', 'work_company', 'work_position']
    list_filter = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'add_time']


xadmin.site.register(CityDict, CirtDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
