# coding=UTF-8
import re
import copy
import os
from bs4 import BeautifulSoup


class HTMLDo:
    dom = []
    allTemplateName = []
    allTemplate = []

    ####### public functions #######

    # @staticmethod
    # this function is buggy
    # cannot handle properly when file has '
    def htmlToHtmld(self, html):
        html = self.prettifyHTML(html)
        result = ''
        for line in html.split('\n'):
            # create ""
            if '<' not in line and '>' not in line:
                line = re.sub(r'^(\s*)(.+)', r"\1'\2'", line)
            # preserv <!-- and -->
            line = re.sub('<!--','\'######', line)
            line = re.sub('-->','######\'', line)
            # remove <>
            line = re.sub(r'/>', '{}', line)
            line = re.sub(r'</.+>','}', line)
            line = re.sub(r'<', '', line)
            line = re.sub(r'>', '{', line)
            # recover <!-- and -->
            line = re.sub('\'######','\'<!--', line)
            line = re.sub('######\'','-->\'', line)

            result = result + line + '\n' 
        return result


    def htmldToHtml(self, htmld):
        htmld, lineNumberTable =  self.preprocess(htmld)
        dom = self.htmldToObject(htmld, lineNumberTable)
        self.dom = dom

        self.templateLoad()
        self.templateLink()
        # print(dom)
        # return 0
        html = self.objectToHTML(dom, lineNumberTable)
        print('\033[92m Done\033[0m')
        return html



    ####### parser #######

    # 1. separate each word and symbol and put them in a list.
    # 2. generate line number mapping table for debug
    def preprocess(self, htmld):
        # ensure the space between words and '{'/'}'
        htmld = re.sub('{',' { ', htmld)
        htmld = re.sub('}',' } ', htmld)
        htmld = re.sub(':',' : ', htmld)
        # remove space and preserve \n
        htmld = re.sub("\n",' \n ',htmld)
        htmld = re.sub("\r+|\t+",'',htmld)
        # split into list of words
        htmld = re.sub(' +',' ',htmld)
        htmld = htmld.split(' ')

        # remove ''
        htmld = [x for x in htmld if x is not '']

        # construct line number mapping table using \n information
        lineNumberTable = []
        counter = 1
        for x in htmld:
            if x == '\n':
                counter = counter + 1
            else:
                lineNumberTable.append(counter)

        # remove \n
        htmld = [x for x in htmld if x is not '\n']

        return htmld, lineNumberTable
    


    def htmldToObject(self, htmld, lineNumberTable):
        # find next {
        # return -1 if not found
        # return -2 if found } before finding any {
        def findNearestUpperBracket(htmld, nextPos):
            nextBracket = nextPos + 1
            while nextBracket <= len(htmld):
                if nextBracket == len(htmld):
                    nextBracket = -1
                    break
                if htmld[nextBracket] is '{':
                    break
                if htmld[nextBracket] is '}':
                    nextBracket = -2
                    break
                nextBracket = nextBracket + 1

            return nextBracket
        
        dom = []
        # main parser
        nextPos = 0
        buffer = []
        while nextPos < len(htmld):
            # special handling for template
            if buffer and type(buffer[len(buffer) - 1]) is dict:
                # {
                if htmld[nextPos] is '{':
                    self.dumpLineNumber(lineNumberTable, nextPos)
                    self.fatalError('unexpected "{"')
                # }
                elif htmld[nextPos] is '}':
                    buffer.pop()
                    self.dumpLineNumber(lineNumberTable, nextPos)
                    print('jump out template')
                # xx'xx
                elif "'" in htmld[nextPos]:
                    self.dumpLineNumber(lineNumberTable, nextPos)
                    self.fatalError('unexpected \'')
                # xxx :
                elif htmld[nextPos + 1] is '{':
                    self.dumpLineNumber(lineNumberTable, nextPos)
                    self.fatalError('missing template item name or :')
                # xxx : {
                elif htmld[nextPos + 1] is ':' and htmld[nextPos + 2] is '{':
                    newList = []
                    buffer[len(buffer) - 1]['content'][htmld[nextPos]] = newList
                    buffer.append(newList)

                    nextPos = nextPos + 2
                # other invalid
                else:
                    self.dumpLineNumber(lineNumberTable, nextPos)
                    self.fatalError('invalid template item syntax (sould be: template XXX { item:{...} item2:{...} })')
                
            
            # normal situation
            # {
            elif htmld[nextPos] is '{':
                self.dumpLineNumber(lineNumberTable, nextPos)
                self.fatalError('unexpected "{"')
            # }
            elif htmld[nextPos] is '}':
                if len(buffer) <= 1:
                    self.dumpLineNumber(lineNumberTable, nextPos)
                    self.fatalError('unexpected "}"')
                buffer.pop()
                self.dumpLineNumber(lineNumberTable, nextPos)
                print('jump out')
            # string
            elif re.match(r"^'.*", htmld[nextPos]):
                if len(buffer) <= 0:
                    self.dumpLineNumber(lineNumberTable, nextPos)
                    self.fatalError('unexpected string')
                # find nearest "
                nextQuot = nextPos + (1 if len(htmld[nextPos]) is 1 else 0)
                while nextQuot <= len(htmld):
                    if nextQuot == len(htmld):
                        nextQuot = -1
                        break
                    if re.match(r".*'$", htmld[nextQuot]):
                        break
                    nextQuot = nextQuot + 1
                if nextQuot is -1:
                    self.dumpLineNumber(lineNumberTable, nextPos)
                    self.fatalError('missing \' ')
                # extract
                string = ' '.join(htmld[nextPos:nextQuot + 1]) # recover the string
                string = string[1:len(string) - 1] # remove ""
                
                buffer[len(buffer) - 1].append({'type':'__string__', 'content':string})
                nextPos = nextQuot                
            # empty
            elif htmld[nextPos] is '':
                0
            # slot    <%...%>
            elif re.match(r'<%.+%>',htmld[nextPos]):
                a = re.match(r'<%(.+)%>',htmld[nextPos])
                
                buffer[len(buffer) - 1].append({'type':'__slot__', 'content':a.group(1)})
            # template
            elif htmld[nextPos] == 'template':
                nextBracket = findNearestUpperBracket(htmld, nextPos)
                if nextBracket is -2:
                    self.dumpLineNumber(lineNumberTable, nextPos)
                    self.fatalError('unexpected "}"')
                if nextBracket is -1:
                    self.dumpLineNumber(lineNumberTable, nextPos)
                    self.fatalError('missing "{"')

                if nextBracket > (nextPos + 2):
                    self.dumpLineNumber(lineNumberTable, nextPos)
                    self.fatalError('too many paramter for template (should has exactly one)')
                if nextBracket < (nextPos + 2):
                    self.dumpLineNumber(lineNumberTable, nextPos)
                    self.fatalError('missing template name')
                
                if "'" in htmld[nextPos + 1]:  # check template name
                    self.dumpLineNumber(lineNumberTable, nextPos)
                    self.fatalError('invalid template name (contains \')')
                
                # put template into buffer
                newTemplate = {
                    'type': '__template__', 
                    'param': htmld[nextPos + 1],
                    'content': {
                        # format: 'template_item_name': []
                    }
                }
                buffer[len(buffer) - 1].append(newTemplate)
                buffer.append(newTemplate)

                # record the template name
                if htmld[nextPos + 1] not in self.allTemplateName:
                    self.allTemplateName.append(htmld[nextPos + 1])
                
                self.dumpLineNumber(lineNumberTable, nextPos)
                print('go into template')

                nextPos = nextBracket # the '{' will be skipped later

            # word or anything else
            else:
                nextBracket = findNearestUpperBracket(htmld, nextPos)
                if nextBracket is -2:
                    self.dumpLineNumber(lineNumberTable, nextPos)
                    self.fatalError('unexpected "}"')
                if nextBracket is -1:
                    self.dumpLineNumber(lineNumberTable, nextPos)
                    self.fatalError('missing "{"')

                # init buffer if it is empty
                if len(buffer) is 0:
                    buffer.append(dom)
                # create object and update buffer
                curBuffer = buffer[len(buffer) - 1]
                curBuffer.append({
                    'type': htmld[nextPos], 
                    'param': ' '.join(htmld[nextPos + 1:nextBracket]),
                    'content':[]})
                buffer.append(curBuffer[len(curBuffer) - 1]['content'])
                
                self.dumpLineNumber(lineNumberTable, nextPos)
                print('go into')

                nextPos = nextBracket # the '{' will be skipped later

            nextPos = nextPos + 1
        
        return dom

    def objectToHTML(self, dom, lineNumberTable):
        def renderOneLayer(dom, output):
            
            for obj in dom:

                if obj['type'] is '__string__':
                    output[0] = output[0] + obj['content']
                elif obj['type'] is '__template__':
                    self.fatalError('template not loaded')
                elif obj['type'] is '__slot__':
                    output[0] = output[0] + obj['content']
                    self.warning('this file is a template')
                else: # general element
                    output[0] = output[0] + '<' + obj['type'] + ' ' + obj['param'] +'>'
                    renderOneLayer(obj['content'], output)
                    output[0] = output[0] + '</' + obj['type'] + '>'

        if len(dom) is 0:
            self.warning('empty output')
        html = ['']
        renderOneLayer(dom, html)
        html = self.prettifyHTML(html[0])
        return html


    ####### File I/O #######

    def loadHtmld(self, fileName, prefix):
        htmld = None
        with open(os.path.join(prefix, fileName+'.htmld'), 'r', encoding='utf-8') as f:
            htmld = f.read()
        return htmld


    ####### template #######

    # load and parse templates whose names are in the self.allTemplateName
    # and store parsed DOM object into self.allTemplate
    def templateLoad(self):
        while len(self.allTemplate) < len(self.allTemplateName):
            idxOfTemplateToLoad = len(self.allTemplate)
            templateFileNameToLoad = self.allTemplateName[idxOfTemplateToLoad]
            print('load template: ', templateFileNameToLoad)

            htmld = self.loadHtmld(templateFileNameToLoad, '')
            htmld, lineNumberTable =  self.preprocess(htmld)
            dom = self.htmldToObject(htmld, lineNumberTable)

            self.allTemplate.append(dom)

    # start from self.dom, load every template
    def templateLink(self):
        def walkDomAndFillSlot(dom, slots):
            for element in dom:
                if element['type'] == '__template__':
                    for i, x in element['content'].items():
                        walkDomAndFillSlot(x, slots)
                elif element['type'] == '__slot__':
                    elementInd = dom.index(element)
                    if element['content'] not in slots:
                        self.fatalError('unfilled slot: ' + element['content'])
                    dom[elementInd:(elementInd + 1)] = slots[element['content']]
                # general element
                elif not re.match(r'^__.*__$', element['type']):
                    walkDomAndFillSlot(element['content'], slots)
        
        def walkDomAndLink(dom):
            templateFound = False
            for element in dom:
                # template
                if element['type'] == '__template__':
                    templateFound = True
                    # get template
                    templateInd = self.allTemplateName.index(element['param'])
                    template = copy.deepcopy(self.allTemplate[templateInd])
                    # load slots
                    slots = element['content']
                    walkDomAndFillSlot(template, slots)
                    # load template
                    elementInd = dom.index(element)
                    dom[elementInd:(elementInd + 1)] = template

                # general element
                elif not re.match(r'^__.*__$', element['type']):
                    if walkDomAndLink(element['content']):
                        templateFound = True
                    
            return templateFound
        
        if walkDomAndLink(self.dom):
            self.templateLink()


    
    ####### helper functions #######
    # @staticmethod
    def prettifyHTML(self, html, indent = 4):
        soup = BeautifulSoup(html, 'html.parser')
        html = soup.prettify(formatter="html")
        result = ''
        for line in html.split('\n'):
            result = result + re.sub(r"^(\s+)(\w|<|>|')", r'\1\1\1\1\2', line) + '\n'
        return result
    


    ####### log #######

    def fatalError(self, msg):
        print('\033[91m FATAL ERROR: ' + msg +'\033[0m')
        exit(-1)
    def warning(self, msg):
        print('\033[93m WARNING: ' + msg +'\033[0m')

    def dumpLineNumber(self, lineNumberTable, pos):
        print('At line ' + str(lineNumberTable[pos]) + ':')

