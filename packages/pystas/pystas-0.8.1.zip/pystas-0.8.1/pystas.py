from decorator import decorate
from datetime import datetime
import traceback

from peewee import SqliteDatabase, Model, JOIN, fn, OperationalError
from peewee import CharField, SmallIntegerField, DateTimeField
from peewee import ForeignKeyField, FloatField, TextField


DB = SqliteDatabase('pystas.db')


class BaseModel(Model):
    class Meta:
        database = DB


class PreFunctionSave:
    def __init__(self, module, klass, name):
        self.name = name
        self.klass = klass
        self.module = module

    @classmethod
    def For(cls, _function):
        _module = getattr(_function, '__module__', '')
        klass = getattr(_function, 'im_class', '')
        name = getattr(_function, 'func_name', '')
        return cls(module=_module, klass=klass, name=name)

    def update_class(self, args):
        classname = ''
        if len(args) >0:
            call_self = args[0]
            bound = getattr(call_self, self.name, None)
            if not bound is None:
                classname = bound.im_class.__name__
        _function, created = self.get(classname)
        _function.save()
        return _function

    def get(self, classname):
        return Function.get_or_create(module=self.module, klass=classname,
                                      name=self.name)


class Function(BaseModel):
    module = CharField(db_column='package')
    klass = CharField(db_column='class')
    name = CharField(db_column='function')

    def __repr__(self):
        return '%s.%s.%s' % (self.module, self.klass, self.name)

    def update_class(self, args):
        return self


class Src(BaseModel):
    name = CharField(db_column='filename')
    line = SmallIntegerField()

    @classmethod
    def For(cls, _function):
        func_code = _function.func_code
        name = getattr(func_code, 'co_filename', '')
        line = getattr(func_code, 'co_firstlineno', -1)
        ent, created = cls.get_or_create(name=name, line=line)
        return ent

    def __repr__(self):
        return '<%s:%d>' % (self.name, self.line)


class ProgExecution(BaseModel):
    start = DateTimeField()

    def __repr__(self):
        return '#%d' % self.id


class Errors(BaseModel):
    excep = CharField(db_column='Exception')
    error = TextField(db_column='Data')

    @classmethod
    def For(cls, exc):
        ent, create = cls.get_or_create(excep=exc.__class__.__name__,
                                        error=traceback.format_exc())
        return ent

    def __repr__(self):
        return self.excep


class Execution(BaseModel):
    function = ForeignKeyField(Function, related_name='executions')
    src = ForeignKeyField(Src, related_name='executions')
    prg = ForeignKeyField(ProgExecution, related_name='executions')
    start = DateTimeField(default=datetime.now)
    duration = FloatField(null=True)
    error = ForeignKeyField(Errors, related_name='executions', null=True)

    def __repr__(self):
        excp = '[%r]' % self.error if self.error else ''
        return '%s| %3.02fs. %s %s' % (self.prg, self.duration, self.function,
                                       excp)


ExecutionStart = None


class Pistas(object):
    @classmethod
    def log(cls, f):
        dbfunc = PreFunctionSave.For(f)
        dbsrc = Src.For(f)
        f.dbfunc = dbfunc
        f.dbsrc = dbsrc
        return decorate(f, cls.log_decorator)

    @classmethod
    def log_decorator(cls, f, *args, **kw):
        f.dbfunc = f.dbfunc.update_class(args)
        f.dbsrc.save()
        execution = Execution(function=f.dbfunc, src=f.dbsrc,
                              prg=ExecutionStart)
        execution.save()
        try:
            return f(*args, **kw)
        except Exception, exc:
            execution.error = Errors.For(exc)
            execution.save()
            raise
        finally:
            end = datetime.now()
            execution.duration = (end-execution.start).total_seconds()
            execution.save()

    def __init__(self):
        raise RuntimeError("No instances of this class are required!")


logpista = Pistas.log


def get_last_exec():
    for prgexec in ProgExecution.select().order_by(ProgExecution.start.desc()):
        return prgexec


def show_stats(condition, title):
    print
    print title
    print 'calls (excp) t.total media  | function'
    for _function in Function.select(Function,
                                    fn.Count(Execution.id).alias('count'),
                                    fn.SUM(Execution.duration).alias('total'),
                                    fn.Count(Errors.id).alias('errors'),
                                    ).join(Execution
                                    ).join(Errors, JOIN.LEFT_OUTER
                                    ).where(condition).group_by(Function):
        print ('%5d (%4d) %6.02fs %4.02fs  | %s' % (
                _function.count, _function.errors, _function.total,
                _function.total / _function.count, _function))


if not __name__ == "__main__":
    # loaded as helper module..
    try:
        DB.create_tables([Function, Src, Execution, Errors, ProgExecution])
    except OperationalError, e:
        msg = e.message
        if not (msg.startswith("table ") and msg.endswith(" already exists")):
            raise

    ExecutionStart = ProgExecution(start=datetime.now())
    ExecutionStart.save()
else:
    # loaded as executable..
    lastprg = get_last_exec()
    print ('last execution is: %r started: %s complete dump:' % (lastprg,
                                                                 lastprg.start))
    for _execution in Execution.select(
                        ).where(Execution.prg == lastprg
                        ).order_by(Execution.start.desc()):
        print _execution

    show_stats(Function.id == Function.id, "all-history")
    show_stats(Execution.prg == lastprg, "last-exec")
