from BasicStructure import PuppetVisitor


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

    print('Class Declarations:', classDeclarationCounterVisitor.counter)
    print('Define Declarations:', defineDeclarationCounterVisitor.counter)
    print('File Declarations:', fileDeclarationCounterVisitor.counter)
    print('Package Declarations:', packageDeclarationCounterVisitor.counter)
    print('Service Declarations:', serviceDeclarationCounterVisitor.counter)
    print('Exec Declarations:', execDeclarationCounterVisitor.counter)

    if (execDeclarationCounterVisitor.counter > 2):
        totalDeclarationsButExec = classDeclarationCounterVisitor.counter \
            + defineDeclarationCounterVisitor.counter \
            + fileDeclarationCounterVisitor.counter \
            + packageDeclarationCounterVisitor.counter \
            + serviceDeclarationCounterVisitor.counter

        print(execDeclarationCounterVisitor.counter,
              totalDeclarationsButExec, execDeclarationCounterVisitor.counter / totalDeclarationsButExec)


class DeclarationCounterVisitor(PuppetVisitor.PuppetVisitor):
    def __init__(self, declarationType):
        self.declarationType = declarationType
        self.counter = 0

    def begin_call(self, call):
        if (str(call.func_name) == 'resource'):
            if (str(call.params[0].get('type')) == self.declarationType):
                print(call.params[0].get('type'), self.declarationType)
                self.counter += 1
        elif (str(call.func_name) == self.declarationType):
            print('func_name', str(call.func_name))
            self.counter += 1

        return True
