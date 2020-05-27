from BasicStructure import PuppetVisitor


class ImperativeAbstractionResults:
    def __init__(self, _class, _define, _file, _package, _service, _exec, isSmellPresent):
        self._class = _class
        self._define = _define
        self._file = _file
        self._package = _package
        self._service = _service
        self._exec = _exec
        self.isSmellPresent = isSmellPresent


def runner(ast):
    classDeclarationCounterVisitor = DeclarationCounterVisitor('class')
    defineDeclarationCounterVisitor = DeclarationCounterVisitor('define')
    fileDeclarationCounterVisitor = DeclarationCounterVisitor('file')
    packageDeclarationCounterVisitor = DeclarationCounterVisitor('package')
    serviceDeclarationCounterVisitor = DeclarationCounterVisitor('service')
    execDeclarationCounterVisitor = DeclarationCounterVisitor('exec')

    ast.accept(classDeclarationCounterVisitor)
    ast.accept(defineDeclarationCounterVisitor)
    ast.accept(fileDeclarationCounterVisitor)
    ast.accept(packageDeclarationCounterVisitor)
    ast.accept(serviceDeclarationCounterVisitor)
    ast.accept(execDeclarationCounterVisitor)

    isCodeSmellPresent = False

    if (execDeclarationCounterVisitor.counter > 2):
        totalDeclarationsButExec = classDeclarationCounterVisitor.counter \
            + defineDeclarationCounterVisitor.counter \
            + fileDeclarationCounterVisitor.counter \
            + packageDeclarationCounterVisitor.counter \
            + serviceDeclarationCounterVisitor.counter

        if ((execDeclarationCounterVisitor.counter / totalDeclarationsButExec) >= 0.02):
            isCodeSmellPresent = True

    return ImperativeAbstractionResults(
        classDeclarationCounterVisitor.counter,
        defineDeclarationCounterVisitor.counter,
        fileDeclarationCounterVisitor.counter,
        packageDeclarationCounterVisitor.counter,
        serviceDeclarationCounterVisitor.counter,
        execDeclarationCounterVisitor.counter,
        isCodeSmellPresent
    )


class DeclarationCounterVisitor(PuppetVisitor.PuppetVisitor):
    def __init__(self, declarationType):
        self.declarationType = declarationType
        self.counter = 0

    def begin_call(self, call):
        if (str(call.func_name) == 'resource'):
            if (str(call.params[0].get('type')) == self.declarationType):
                self.counter += 1
        elif (str(call.func_name) == self.declarationType):
            self.counter += 1

        return True
