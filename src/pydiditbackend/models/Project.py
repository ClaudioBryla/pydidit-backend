from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import Unicode
from sqlalchemy import Integer
from sqlalchemy import Enum
from sqlalchemy import DateTime

from sqlalchemy.orm import relation
from sqlalchemy.orm import backref

import pydiditbackend.models
from pydiditbackend.models.Model import Model
Base = pydiditbackend.models.Base


class Project(Model, Base):
    '''Project object'''
    __tablename__ = 'projects'

    id = Column(Integer, autoincrement=True, nullable=False, primary_key=True)
    description = Column(Unicode(length=255), nullable=True)
    state = Column(Enum(
        'active',
        'completed',
    ), nullable=False)
    due = Column(DateTime(), nullable=True)
    created_at = Column(DateTime(), nullable=False, default=datetime.now)
    completed_at = Column(DateTime(), nullable=True)
    modified_at = Column(DateTime(), nullable=False, onupdate=datetime.now)
    display_position = Column(Unicode(length=50), nullable=False)

    prereq_projects = relation(
        'Project',
        backref=backref('dependent_projects', lazy='joined', join_depth=1),
        secondary='projects_prereq_projects',
        primaryjoin=
                id == pydiditbackend.models.
                projects_prereq_projects.c.project_id,
        secondaryjoin=
                id == pydiditbackend.models.
                projects_prereq_projects.c.prereq_id,
        lazy='joined',
        join_depth=1,
    )

    child_projects = relation(
        'Project',
        backref=backref('parent_projects', lazy='joined', join_depth=1),
        secondary='projects_contain_projects',
        primaryjoin=
                id == pydiditbackend.models.
                projects_contain_projects.c.parent_id,
        secondaryjoin=
                id == pydiditbackend.models.
                projects_contain_projects.c.child_id,
        lazy='joined',
        join_depth=1,
    )

    child_todos = relation(
        'Todo',
        backref=backref('parent_projects', lazy='joined', join_depth=1),
        secondary='projects_contain_todos',
        lazy='joined',
        join_depth=1,
    )

    notes = relation(
        'Note',
        backref=backref('projects', lazy='joined', join_depth=1),
        secondary='projects_notes',
        lazy='joined',
        join_depth=1,
    )

    tags = relation(
        'Tag',
        backref=backref('projects', lazy='joined', join_depth=1),
        secondary='projects_tags',
        lazy='joined',
        join_depth=1,
    )

    def __init__(self, description, state=u'active', due=None, show_from=None):
        '''Create a new Project instance

        :param description:

        :param state: 'active' or 'completed', optional (defaults to 'active')
        :param due: Due date, optional

        '''
        self.description = description
        self.state = state

        self.due = due

    def __str__(self):
        return '<Project: {0} {1}>'.format(self.id, self.description)
