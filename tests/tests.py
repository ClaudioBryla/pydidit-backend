#import ConfigParser

from pydiditbackend import *

#ini = ConfigParser.SafeConfigParser()
#ini.read('pydidit.ini')
#settings = dict(ini.items('app:main'))

def setUp():
    initialize('pydidit_test.ini')
    Base.metadata.create_all()

def testCheckForCleanDB():
    assert len(get('Todo', all = True)) == 0

def testTodo():
    todo = make('Todo', u'TESTDESCRIPTION')
    assert todo.description == u'TESTDESCRIPTION'

def testTodoState():
    todo = make('Todo', u'TESTDESCRIPTION')
    assert todo.state == u'active'
    todo.set_completed()
    assert todo.state == u'completed'

def testTodoFilterBy():
    completed_todos = get('Todo', filter_by = {'state': u'completed'})
    todo = put('Todo', u'TESTDESCRIPTION')
    assert todo.state == u'active'
    todo.set_completed()
    assert todo.state == u'completed'
    new_completed_todos = get('Todo', filter_by = {'state': u'completed'})
    assert len(new_completed_todos) - len(completed_todos) == 1

def testTodoDisplayPositionDefined():
    todo = put('Todo', u'TESTDESCRIPTION', u'1.1')
    another_todo = put('Todo', u'TESTDESCRIPTION')
    assert another_todo.display_position == u'2.0'

def testTodoDisplayPosition():
    todo = put('Todo', u'TESTDESCRIPTION')
    another_todo = put('Todo', u'TESTDESCRIPTION')
    initial_dp_components = todo.display_position.split(u'.')
    another_dp_components = another_todo.display_position.split(u'.')
    assert len(initial_dp_components) == len(another_dp_components)
    assert int(initial_dp_components[0]) + 1 == int(another_dp_components[0])
    for i in xrange(1, len(initial_dp_components)):
        assert initial_dp_components[i] == another_dp_components[i]

def testTodoDisplayPositionNoAdd():
    todo = make('Todo', u'TESTDESCRIPTION')
    another_todo = make('Todo', u'TESTDESCRIPTION')
    assert todo.display_position == another_todo.display_position

def testTodoCommit():
    todos = get('Todo', all = True)
    for todo in todos:
        delete_from_db(todo)
        del todo
    commit()
    todos = get('Todo', all = True)
    assert len(todos) == 0
    todo = put('Todo', u'TESTDESCRIPTION')
    commit()
    del todo
    todos = get('Todo', all = True)
    assert len(todos) == 1
    assert todos[0].description == u'TESTDESCRIPTION'

def testTag():
    tag = make('Tag', u'TESTNAME')
    assert tag.name == u'TESTNAME'

def testProject():
    project = make('Project', u'PROJECTDESC')
    assert project.description == u'PROJECTDESC'

def testProjectState():
    project = make('Project', u'PROJECTDESC')
    assert project.state == u'active'
    project.set_completed()
    assert project.state == u'completed'

def testNote():
    note = make('Note', u'NOTETEXT')
    assert note.text == u'NOTETEXT'

