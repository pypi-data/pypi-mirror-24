# -*- coding: utf-8 -*-


"""
 Copyright 2016 cocoatomo

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

from pygments.lexer import RegexLexer, include, default
from pygments.token import Text, Whitespace, Keyword, Name, Literal, String, Number, Operator, Punctuation, Comment

def list_with_separator(rule_name, element_rule, element_type, separator_rule, separator_type):
    sub_rule = '_following-' + rule_name
    element_rule_name = '_element-of-' + rule_name
    return {
        rule_name: [
            include('skip'),
            (element_rule, element_type, ('#pop', sub_rule)),
        ],
        sub_rule: [
            include('skip'),
            (separator_rule, separator_type, element_rule_name),
            default('#pop'),
        ],
        element_rule_name: [
            include('skip'),
            (element_rule, element_type, '#pop'),
        ],
    }

class DmdlLexer(RegexLexer):
    name = 'Dmdl'
    aliases = ['dmdl']
    filenames = ['*.dmdl']

    import re
    flags = re.MULTILINE | re.DOTALL

    # regular expressions for tokens
    # <name>:
    #      <first-word>
    #      <name> '_' <word>
    # <first-word>:
    #      ['a'-'z'] ['a'-'z', '0'-'9']*
    # <word>:
    #      ['a'-'z', '0'-'9']+
    NAME = r'[a-z]([a-z0-9])*(_[a-z0-9]+)*'

    PSEUDO_ELEMENT = r'<.+?>'

    tokens = {
        ## lexing
        'skip': [ # only for include
            (r'[ \t\r\n]', Whitespace),
            (r'/\*', Comment.Multiline, 'block-comment'),
            (r'--.*?$', Comment.Singleline),
            (r'//.*?$', Comment.Singleline),
            (r'\.\.\.', Punctuation),
        ],
        'block-comment': [
            (r'\*/', Comment.Multiline, '#pop'),
            (r'.', Comment.Multiline),
        ],
        # <string-literal>:
        #      '"' <string-char>* '"'
        # <string-char>:
        #      ~['"', '\']
        #      '\' ['b', 't', 'n', 'f', 'r', '\', '"']
        #      '\' 'u' ['0'-'9', 'A'-'F', 'a'-'f']{4}
        #      '\' '0' ['0'-'3']? ['0'-'7']? ['0'-'7']
        'string-literal': [
            (r'[^"\\]', String.Double),
            (r'\\[btnfr\\"]', String.Double),
            (r'\\0[0-3]?[0-7]?[0-7]', String.Double),
            (r'"', String.Double, '#pop'),
        ],
        # <type>:
        #      <basic-type>
        #      <reference-type>
        #      <collection-type>
        'type': [
            include('skip'),
            (PSEUDO_ELEMENT, Keyword.Type, '#pop'),
            include('basic-type'),
            include('reference-type'),
            include('collection-type'),
        ],
        # <basic-type>:
        #      'INT'
        #      'LONG'
        #      'BYTE'
        #      'SHORT'
        #      'DECIMAL'
        #      'FLOAT'
        #      'DOUBLE'
        #      'TEXT'
        #      'BOOLEAN'
        #      'DATE'
        #      'DATETIME'
        'basic-type': [
            (r'INT', Keyword.Type, '#pop'),
            (r'LONG', Keyword.Type, '#pop'),
            (r'BYTE', Keyword.Type, '#pop'),
            (r'SHORT', Keyword.Type, '#pop'),
            (r'DECIMAL', Keyword.Type, '#pop'),
            (r'FLOAT', Keyword.Type, '#pop'),
            (r'DOUBLE', Keyword.Type, '#pop'),
            (r'TEXT', Keyword.Type, '#pop'),
            (r'BOOLEAN', Keyword.Type, '#pop'),
            # avoid a hasty decision
            (r'DATETIME', Keyword.Type, '#pop'),
            (r'DATE', Keyword.Type, '#pop'),
        ],
        # <reference-type>:
        #     <name>
        'reference-type': [
            include('skip'),
            (NAME, Keyword.Type, '#pop'),
        ],
        # <collection-type>:
        #     '{' <type> '}'
        #     '{' ':' <type> '}'
        'collection-type': [
            include('skip'),
            # '{', ':', '}' should be treated as a part of type?
            (r'\{', Punctuation, ('#pop', 'collection-type-array-or-map')),
        ],
        'collection-type-array-or-map': [
            include('skip'),
            (r':', Punctuation, ('#pop', 'closing-curly-brace', 'type')),
            default(('#pop', 'closing-curly-brace', 'type')),
        ],
        # <name>:
        #      <first-word>
        #      <name> '_' <word>
        # <first-word>:
        #      ['a'-'z'] ['a'-'z', '0'-'9']*
        # <word>:
        #      ['a'-'z', '0'-'9']+
        'name': [
            include('skip'),
            (NAME, Name, '#pop'),
        ],
        'name-or-pseudo-element': [
            include('skip'),
            (NAME, Name, '#pop'),
            (PSEUDO_ELEMENT, Name, '#pop'),
        ],
        # <literal>:
        #      <string>
        #      <integer>
        #      <decimal>
        #      <boolean>
        'literal': [
            include('skip'),
            (r'"', String.Double, ('#pop', 'string-literal')),
            include('decimal-literal'),
            include('integer-literal'),
            include('boolean-literal'),
        ],
        # <integer-literal>:
        #      '0'
        #      ['1'-'9']['0'-'9']*
        'integer-literal': [
            (r'0', Number.Integer, '#pop'),
            (r'[1-9][0-9]*', Number.Integer, '#pop'),
        ],
        # <decimal-literal>:
        #      '.' ['0'-'9']+
        #      '0.' ['0'-'9']*
        #      ['1'-'9']['0'-'9']* '.' ['0'-'9']*
        'decimal-literal': [
            (r'\.[0-9]+', Number.Float, '#pop'),
            (r'0\.[0-9]*', Number.Float, '#pop'),
            (r'[1-9][0-9]*\.[0-9]*', Number.Float, '#pop'),
        ],
        # <boolean-literal>:
        #      'TRUE'
        #      'FALSE'
        'boolean-literal': [
            (r'TRUE', Literal, '#pop'),
            (r'FALSE', Literal, '#pop'),
        ],

        ## parsing
        # entry point
        # <script>:
        #      <model-definition>*
        # <model-definition>:
        #      <record-model-definition>
        #      <projective-model-definition>
        #      <joined-model-definition>
        #      <summarized-model-definition>
        'root': [
            include('skip'),
            (r'"', String.Double, ('model-name-bind', 'attribute-list', 'description')),
            default(('model-name-bind', 'attribute-list')),
        ],
        # <description>:
        #      <string>
        'description': [
            default(('#pop', 'string-literal')),
        ],
        # <attribute-list>:
        #      <attribute>*
        'attribute-list': [
            include('skip'),
            (r'@', Name.Attribute, 'attribute'),
            default('#pop'),
        ],
        # <attribute>:
        #      '@' <qname>
        #      '@' <qname> '(' ')'
        #      '@' <qname> '(' <attribute-element-list> ','? ')'
        # rule ','? is processed at following-attribute-element
        'attribute': [
            include('skip'),
            default(('#pop', 'attribute-option-tuple', 'attribute-name')),
        ],
        'attribute-option-tuple': [
            include('skip'),
            (r'\(', Punctuation, ('#pop', 'attribute-option')),
            default('#pop'),
        ],
        'attribute-option': [
            include('skip'),
            (r'\)', Punctuation, '#pop'),
            default(('#pop', 'attribute-element-list')),
        ],
        # <attribute-element-list>:
        #      <attribute-element-list> ',' <attribute-element>
        #      <attribute-element>
        'attribute-element-list': [
            include('skip'),
            default(('#pop', 'following-attribute-element', 'attribute-element')),
        ],
        'following-attribute-element': [
            include('skip'),
            (r'\)', Punctuation, '#pop'),
            (r',', Punctuation, 'attribute-element'),
        ],
        # <attribute-element>:
        #      <name> '=' <attribute-value>
        'attribute-element': [
            include('skip'),
            (r'\)', Punctuation, '#pop:2'),
            default(('#pop', 'attribute-value', 'bind', 'name')),
        ],
        'bind': [
            include('skip'),
            (r'=', Operator, '#pop'),
        ],
        # <attribute-value>:
        #      <attribute-value-array>
        #      <attribute-value-map>
        #      <qname>
        #      <literal>
        'attribute-value': [
            include('skip'),
            (r'\{', Punctuation, ('#pop', 'attribute-value-array-or-map-1')),
            include('literal'),
            default(('#pop', 'qualified-name')),
        ],
        # <attribute-value-map>:
        #      '{' ':' '}'
        #      '{' <attribute-pair-list> ','? '}'
        # rule ','? is processed at following-attribute-pair
        'attribute-value-array-or-map-1': [
            include('skip'),
            # '\}' -> empty array
            (r'\}', Punctuation, '#pop'),
            # ':' -> empty map
            (r':', Punctuation, ('#pop', 'closing-curly-brace')),
            # lookahead assertion for literal
            (r'(?=[".0-9TF])', Literal, ('#pop', 'attribute-value-array-or-map-2', 'literal')),
            # otherwise
            default(('#pop', 'attribute-value-array')),
        ],
        'attribute-value-array-or-map-2': [
            include('skip'),
            # ':' -> map
            (r':', Punctuation, ('#pop', 'following-attribute-pair', 'attribute-value')),
            # otherwise -> array
            default(('#pop', 'following-attribute-value')),
        ],
        'closing-curly-brace': [
            include('skip'),
            (r'\}', Punctuation, '#pop')
        ],
        # <attribute-value-array>:
        #      '{' '}'
        #      '{' <attribute-value-list> ','? '}'
        # rule ','? is processed at following-attribute-value
        'attribute-value-array': [
            include('skip'),
            (r'\}', Punctuation, '#pop'),
            default(('#pop', 'attribute-value-list')),
        ],
        # <attribute-value-list>:
        #      <attribute-value-list> ',' <attribute-value>
        #      <attribute-value>
        'attribute-value-list': [
            include('skip'),
            default(('#pop', 'following-attribute-value', 'attribute-value')),
        ],
        'following-attribute-value': [
            include('skip'),
            (r'\}', Punctuation, '#pop'),
            (r',', Punctuation, 'attribute-value-ext'),
        ],
        'attribute-value-ext': [
            include('skip'),
            (r'\}', Punctuation, '#pop:2'),
            default(('#pop', 'attribute-value')),
        ],
        # <attribute-pair-list>:
        #      <attribute-pair-list> ',' <attribute-pair>
        #      <attribute-pair>
        'following-attribute-pair': [
            include('skip'),
            (r'\}', Punctuation, '#pop'),
            (r',', Punctuation, 'attribute-pair-ext'),
        ],
        'attribute-pair-ext': [
            include('skip'),
            (r'\}', Punctuation, '#pop:2'),
            default(('#pop', 'attribute-pair')),
        ],
        #  <attribute-pair>:
        #      <literal> ':' <attribute-value>
        'attribute-pair': [
            include('skip'),
            default(('#pop', 'attribute-value', 'colon', 'literal')),
        ],
        'colon': [
            include('skip'),
            (r':', Punctuation, '#pop'),
        ],
        # <model-definition>:
        #      <record-model-definition>
        #      <projective-model-definition>
        #      <joined-model-definition>
        #      <summarized-model-definition>
        'model-name-bind': [
            include('skip'),
            # NOTE: this implementation does not allow model names 'projective', 'joined' and 'summarized'
            # negative lookahead assertion
            (r'projective(?![a-z0-9_])', Keyword.Type, ('#pop', 'record-expression', 'bind', 'model-name')),
            (r'joined(?![a-z0-9_])', Keyword.Type, ('#pop', 'join-expression', 'bind', 'model-name')),
            (r'summarized(?![a-z0-9_])', Keyword.Type, ('#pop', 'summarize-expression', 'bind', 'model-name')),
            default(('#pop', 'record-expression', 'bind', 'model-name')),
        ],
        'model-name': [
            include('skip'),
            (NAME, Name.Class, '#pop'),
            (PSEUDO_ELEMENT, Name.Class, '#pop'),
        ],
        # <record-expression>:
        #      <record-expression> '+' <record-term>
        #      <record-term>
        'record-expression': [
            include('skip'),
            default(('#pop', 'following-record-term', 'record-term')),
        ],
        # <record-term>:
        #      '{' <property-definition>* '}' ← allow empty record-term issue #11
        #      <model-reference>
        'record-term': [
            include('skip'),
            (PSEUDO_ELEMENT, Name.Variable.Instance, '#pop'),
            (r'\{', Punctuation, ('#pop', 'property-definition')),
            default(('#pop', 'model-reference')),
        ],
        'following-record-term': [
            include('skip'),
            (r';', Punctuation, '#pop'),
            (r'\+', Operator, 'record-term'),
        ],
        # <property-definition>:
        #      <description>? <attribute>* <name> ':' <type> ';'
        #      <description>? <attribute>* <name> '=' <property-value> ';'
        #      <description>? <attribute>* <name> ':' <type> '=' <property-value> ';'
        'property-definition': [
            include('skip'),
            (r'\}', Punctuation, '#pop'),
            (r'"', String.Double, ('end-of-declaration', 'property-definition-latter-half', 'name-or-pseudo-element', 'attribute-list', 'description')),
            default(('end-of-declaration', 'property-definition-latter-half', 'name-or-pseudo-element', 'attribute-list')),
        ],
        'property-definition-latter-half': [
            include('skip'),
            # TODO property-value? property-expression?
            (r':', Punctuation, ('#pop', 'property-definition-with-type', 'type')),
            (r'=', Operator, ('#pop', 'property-expression')),
        ],
        'property-definition-with-type': [
            include('skip'),
            (r'=', Operator, ('#pop', 'property-expression')),
            default('#pop'),
        ],
        # <property-expression>:
        #     <property-expression-list>      ← <attribute-value-array> と同じ
        #     <property-expression-map>       ← <attribute-value-map> と同じ
        #     <property-expression-reference> ← <qname> と同じ
        'property-expression': [
            include('skip'),
            (r'\{', Punctuation, ('#pop', 'attribute-value-array-or-map-1')),
            default(('#pop', 'qualified-name')),
        ],
        # <model-reference>:
        #      <name>
        'model-reference': [
            include('skip'),
            (NAME, Name.Class, '#pop'),
            (PSEUDO_ELEMENT, Name.Class, '#pop'),
        ],
        # <join-expression>:
        #      <join-expression> '+' <join-term>
        #      <join-term>
        'join-expression': [
            include('skip'),
            default(('#pop', 'following-join-term', 'join-term')),
        ],
        # <join-term>:
        #      <model-reference> <model-mapping>? <grouping>?
        'join-term': [
            include('skip'),
            default(('#pop', 'grouping', 'model-mapping', 'model-reference')),
        ],
        # <model-mapping>:
        #      '->' '{' <property-mapping>* '}' ← allow empty model-mapping issue #11
        'model-mapping': [
            include('skip'),
            (r'->', Operator, ('#pop', 'model-mapping-body')),
            default('#pop'),
        ],
        'model-mapping-body': [
            include('skip'),
            (r'\{', Punctuation, ('#pop', 'property-mapping')),
            (PSEUDO_ELEMENT, Name.Variable.Instance, '#pop'),
        ],
        # <property-mapping>:
        #      <description>? <attribute>* <name> '->' <name> ';'
        'property-mapping': [
            include('skip'),
            (r'\}', Punctuation, '#pop'),
            (r'"', String.Double, ('end-of-declaration', 'name-or-pseudo-element', 'mapping-arrow', 'name-or-pseudo-element', 'attribute-list', 'description')),
            default(('end-of-declaration', 'name-or-pseudo-element', 'mapping-arrow', 'name-or-pseudo-element', 'attribute-list')),
        ],
        'mapping-arrow': [
            include('skip'),
            (r'->', Operator, '#pop'),
        ],
        # <grouping>:
        #      '%' <property-list>
        # <property-list>:
        #      <property-list> ',' <name>
        #      <name>
        'grouping': [
            include('skip'),
            (r'%', Operator, ('#pop', 'property-list')),
            default('#pop'),
        ],
        'following-join-term': [
            include('skip'),
            (r';', Punctuation, '#pop'),
            (r'\+', Operator, 'join-term'),
        ],
        # <summarize-expression>:
        #      <summarize-expression> '+' <summarize-term>
        #      <summarize-term>
        'summarize-expression': [
            include('skip'),
            default(('#pop', 'following-summarize-term', 'summarize-term')),
        ],
        # <summarize-term>:
        #      <name> <model-folding> <grouping>?
        'summarize-term': [
            include('skip'),
            default(('#pop', 'grouping', 'model-folding', 'model-name')),
        ],
        # similar to model-mapping
        # <model-folding>:
        #      '=>' '{' <property-folding>* '}' ← allow empty model-folding issue #11
        'model-folding': [
            include('skip'),
            (r'=>', Operator, ('#pop', 'model-folding-body')),
        ],
        'model-folding-body': [
            include('skip'),
            (r'\{', Punctuation, ('#pop', 'property-folding')),
        ],
        # <property-folding>:
        #      <description>? <attribute>* <aggregator> <name> '->' <name> ';'
        'property-folding': [
            include('skip'),
            (r'\}', Punctuation, '#pop'),
            (r'"', String.Double, ('end-of-declaration', 'name-or-pseudo-element', 'mapping-arrow', 'name-or-pseudo-element', 'aggregator', 'attribute-list', 'description')),
            default(('end-of-declaration', 'name-or-pseudo-element', 'mapping-arrow', 'name-or-pseudo-element', 'aggregator', 'attribute-list')),
        ],
        # <aggregator>:
        #      'any'
        #      'sum'
        #      'max'
        #      'min'
        #      'count'
        'aggregator': [
            include('skip'),
            # negative lookahead assertion
            (r'any(?![a-z0-9_])', Name.Function, '#pop'),
            (r'sum(?![a-z0-9_])', Name.Function, '#pop'),
            (r'max(?![a-z0-9_])', Name.Function, '#pop'),
            (r'min(?![a-z0-9_])', Name.Function, '#pop'),
            (r'count(?![a-z0-9_])', Name.Function, '#pop'),
            (PSEUDO_ELEMENT, Name.Function, '#pop'),
        ],
        'following-summarize-term': [
            include('skip'),
            (r';', Punctuation, '#pop'),
            (r'\+', Operator, 'summarize-term'),
        ],
        'end-of-declaration': [
            include('skip'),
            (r';', Punctuation, '#pop')
        ],
    }

    tokens.update(list_with_separator('attribute-name', NAME, Name.Attribute, r'\.', Name.Attribute))
    tokens.update(list_with_separator('qualified-name', NAME, Name, r'\.', Name))
    tokens.update(list_with_separator('property-list', '|'.join([NAME, PSEUDO_ELEMENT]), Name, r',', Punctuation))


def debug(code):
    dl = DmdlLexer()
    for t in dl.get_tokens_unprocessed(code):
        print(t)


if __name__ == '__main__':
    import sys
    sys.exit(debug(sys.argv[1]))
