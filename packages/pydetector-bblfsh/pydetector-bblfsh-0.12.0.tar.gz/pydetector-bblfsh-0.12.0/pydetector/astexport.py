"""
Export an improved version of the Python AST for the given codestr
as a Python Dictionary or JSON object
"""

from __future__ import print_function

__all__ = ["export_dict", "export_json", "DictExportVisitor"]

import ast
import sys
import token as token_module
import tokenize
from ast import literal_eval
from codecs import encode
from collections import Iterable, Mapping
from six import StringIO, string_types


def export_dict(codestr):
    """ Returns the AST as a Python dictionary """
    visitor = DictExportVisitor(codestr)
    return visitor.parse()


def export_json(codestr, pretty_print=False):
    """ Returns the AST as a JSON object """
    import json
    dict_ = {'AST': export_dict(codestr)}
    json_ = json.dumps(dict_, indent=2 if pretty_print else 0, ensure_ascii=False)
    return json_, dict_


def map_dict_rec(i, func):
    if isinstance(i, Mapping):
        func(i)

    if isinstance(i, Iterable) and not isinstance(i, string_types):
        values = i.values() if isinstance(i, Mapping) else i
        for x in values:
            map_dict_rec(x, func)


TOKEN_TYPE = 0
TOKEN_VALUE = 1
TOKEN_STARTLOC = 2
TOKEN_ENDLOC = 3
TOKEN_RAWVALUE = 4

TOKENROW = 0
TOKENCOL = 1

NOOP_TOKENS_LINE = {'COMMENT', 'INDENT', 'NL', 'NEWLINE'}


def _token_name(t):
    return token_module.tok_name[t[TOKEN_TYPE]]


def _create_tokenized_lines(codestr, tokens):
    lines = codestr.splitlines() if codestr else []
    result = []
    for i in range(0, len(lines) + 1):
        result.append([])

    for token in tokens:
        # Save noops in the line of the starting row except for strings where
        # we save it in the last line (because they can be multiline)
        if _token_name(token) == 'STRING':
            line = token[TOKEN_ENDLOC][TOKENROW] - 1
        else:
            line = token[TOKEN_STARTLOC][TOKENROW] - 1
        result[line].append(token)
    assert len(lines) + 1 == len(result), len(result)
    return result


class TokenNotFoundException(Exception):
    pass


class LocationFixer(object):
    """
    For every line, get the exact position of every token. This will be used by the
    visitor to fix the position of some nodes that the Python's AST doesn't give or give
    in a questionable way (sys.stdout.write -> gives the same column for the three).
    """

    def __init__(self, codestr, token_lines):
        self._current_line = None

        # _lines will initially hold the same list of tokens per line as received (in a
        # dict so speed lookups), but the tokens inside will be removed as they're found
        # by the visitor (so we still can infer real positions for several tokens with the
        # same name on the same line)
        self._lines = {idx: val for idx, val in enumerate(token_lines)}

    def _pop_token(self, lineno, token_value):
        tokensline = self._lines[lineno - 1]

        # Pop the first token with the same name in the same line
        for t in tokensline:
            linetok_value = t[TOKEN_VALUE]

            if _token_name(t) != 'STRING':
                line_value = linetok_value
            else:
                if linetok_value[0] == 'f' and linetok_value[1] in ('"', "'"):
                    # fstring: token identify as STRING but they parse into the AST as a
                    # collection of nodes so the token_value is  different. To find the
                    # real token position we'll search  inside the fstring token value.
                    tok_subpos = linetok_value.find(str(token_value))
                    if tok_subpos != -1:
                        real_col = t[TOKEN_STARTLOC][TOKENCOL] + tok_subpos

                        # We don't remove the fstring token from the line in this case; other
                        # nodes could match different parts of it
                        return (t[TOKEN_TYPE], t[TOKEN_VALUE], (t[TOKEN_STARTLOC][0], real_col),
                                t[TOKEN_ENDLOC], t[TOKEN_RAWVALUE])

                    raise TokenNotFoundException("Could not find token '{}' inside f-string '{}'"
                            .format(token_value, linetok_value))
                else:
                    # normal string; they include the single or double quotes so we liteval
                    line_value = literal_eval(linetok_value)

            if str(line_value) == str(token_value):
                tokensline.remove(t)
                return t

        raise TokenNotFoundException("Token named '{}' not found in line {}"
                .format(token_value, lineno))

    def _fix_virtualnode_pos(self, nodedict):
        """
        These "virtual parent" nodes don't have tokens but we could get the location from
        the first child.
        """
        node_type = nodedict['ast_type']

        if node_type == "Call":
            nodedict["col_offset"] = nodedict["func"]["col_offset"]
            return True
        elif node_type == "arguments" and len(nodedict["args"]):
            nodedict["lineno"] = nodedict["args"][0]["lineno"]
            nodedict["end_lineno"] = nodedict["args"][-1]["end_lineno"]

            nodedict["col_offset"] = nodedict["args"][0]["col_offset"]
            nodedict["end_col_offset"] = nodedict["args"][-1]["end_col_offset"]
            return True
        elif node_type == "FormattedValue":
            nodedict["col_offset"] = nodedict["value"]["col_offset"] - 1
            return True
        elif node_type == "FunctionDef":
            nodedict["lineno"] = nodedict["args"]["lineno"]

        return False

    def _sync_node_pos(self, nodedict, add = 0):
        """
        Check the column position, updating the column if needed (this changes the
        nodedict argument). Some Nodes have questionable column positions in the Python
        given AST (e.g. all items in sys.stdout.write have column 1). This fixes if the
        linenumber is right, using the more exact position given by the tokenizer.

        When a node is checked, it's removed from its line list, so the next token with
        the same name will not consume that token again (except for fstrings that are
        a special case of a token mapping to several possible AST nodes).
        """
        if self._fix_virtualnode_pos(nodedict):
            return

        node_line = nodedict.get('lineno')
        if node_line is None:
            return

        # We take these node properties as token name if they exists
        # (same used in the Bblfsh Python driver parser.go):
        node_keyset = set(nodedict.keys())
        token_keys = list(node_keyset.intersection(_TOKEN_KEYS))

        if token_keys:
            node_token = nodedict[token_keys[0]]
        else:
            node_token = _SYNTHETIC_TOKENS.get(nodedict["ast_type"])
            if not node_token:
                return  # token not found
        try:
            # Pop the fist token with the same name in the same line.
            token = self._pop_token(node_line, node_token)
        except TokenNotFoundException:
            # Only happens with multiline string and the original
            # position in that case is fine (uses the last line in that case)
            return

        node_column = nodedict.get('col_offset')
        token_startcolumn = token[TOKEN_STARTLOC][TOKENCOL]

        if node_column is None or node_column != token_startcolumn:
            nodedict["col_offset"] = token_startcolumn + add

        # For grouping nodes; this will be improved in _fix_endposition if needed
        nodedict["end_lineno"] = token[TOKEN_ENDLOC][TOKENROW]
        nodedict["end_col_offset"] = token[TOKEN_ENDLOC][TOKENCOL]

    def _max_child_endpos(self, nd, lower_pos = ()):
        """
        Return the end position of the farthest child node. Used to update containers
        nodes where the tokenizer doesn't have a token or it's the token of the symbol and
        not the contents.
        """

        if '__cached_endpos' in nd:
            return nd["__cached_endpos"]

        if isinstance(nd, list):
            max_children = [self._max_child_endpos(i, lower_pos)
                            for i in nd if isinstance(i, Iterable) and
                            not isinstance(i, string_types)]
            lower_pos = max([lower_pos] + max_children)

        elif isinstance(nd, dict):
            cur_pos = (nd["end_lineno"], nd["end_col_offset"]) if "end_lineno" in nd else ()
            max_children = [self._max_child_endpos(i, lower_pos)
                            for i in nd.values() if isinstance(i, Iterable) and
                            not isinstance(i, string_types)]
            lower_pos = max([lower_pos, cur_pos] + max_children)
            if lower_pos:
                nd['__cached_endpos'] = lower_pos

        return lower_pos

    def _fix_endposition(self, nodedict):
        """
        Set the endposition to the endposition of the latest child
        """

        max_position = self._max_child_endpos(nodedict)
        if max_position:
            nodedict["end_lineno"], nodedict["end_col_offset"] = max_position

    def fix_embeded_pos(self, nodedict, add):
        """
        For nodes that wrongly start from 1 (like subcode inside f-strings)
        this fixes the lineno field adding the argument (which should be
        the parent node correct lineno)
        """
        nodedict["lineno"] += add - 1

        for key in nodedict:
            if isinstance(nodedict[key], dict):
                self.fix_embeded_pos(nodedict[key], add)

        self._sync_node_pos(nodedict, add = 1)
        return nodedict

    def apply_fixes(self, nodedict):
        self._sync_node_pos(nodedict)
        self._fix_endposition(nodedict)


class NoopExtractor(object):
    """
    Extract lines with tokens from the tokenized source that Python's AST generator ignore
    like blanks and comments.
    """

    def __init__(self, codestr, token_lines):
        self._current_line = None
        self._all_lines = tuple(token_lines)
        self.astmissing_lines = self._create_astmissing_lines()

        # This set is used to avoid adding the "same line-remainder noops" nodes as a child
        # of every "real" node to avoid having this node duplicated on all semantic
        # nodes in the same line, thus avoiding duplication. It will contain just the
        # line numbers of already added sameline_noops
        self._sameline_added_noops = set()

    def _create_astmissing_lines(self):
        """
        Return a copy of line_tokens containing lines ignored by the AST
        (comments and blanks-only lines)
        """
        lines = []
        nl_token = (token_module.NEWLINE, '\n', (0, 0), (0, 0), '\n')

        for i, linetokens in enumerate(self._all_lines):
            if len(linetokens) == 1 and _token_name(linetokens[0]) == 'NL':
                lines.append(nl_token)
            else:
                for token in linetokens:
                    if _token_name(token) == 'COMMENT' and \
                            token[TOKEN_RAWVALUE].lstrip().startswith('#'):
                        lines.append(token)
                        break
                else:
                    lines.append(None)
        assert len(lines) == len(self._all_lines)

        for i, linetokens in enumerate(lines):
            if linetokens:
                self._current_line = i
                break
        else:
            self._current_line = len(lines)
        return lines

    def previous_nooplines(self, node):
        """Return a list of the preceding comment and blank lines"""
        previous = []
        first_lineno = None
        lastline = None
        lastcol = None

        if hasattr(node, 'lineno'):
            while self._current_line < node.lineno:
                token = self.astmissing_lines[self._current_line]
                if token:
                    s = token[TOKEN_RAWVALUE].rstrip() + '\n'
                    previous.append(s)

                    # take only the first line of the noops as the start and the last
                    # one (overwriteen every iteration)
                    if not first_lineno:
                        first_lineno = self._current_line + 1
                    lastline = self._current_line + 1
                    lastcol = token[TOKEN_ENDLOC][TOKENCOL]
                self._current_line += 1
        return previous, first_lineno, lastline, lastcol

    def sameline_remainder_noops(self, node):
        """
        Return a string containing the trailing (until EOL) noops for the
        node, if any. The ending newline is implicit and thus not returned
        """

        # Without a line number for the node we can't know
        if not hasattr(node, 'lineno'):
            return ''

        # Skip remainder comments already added to a node in this line to avoid every node
        # in the same line having it (which is not conceptually wrong, but not DRY)
        if node.lineno in self._sameline_added_noops:
            return ''

        # Module nodes have the remaining comments but since we put their first line as "1"
        # any comment on the first line would wrongly show as sameline comment for the module
        if node.__class__.__name__ == 'Module':
            return ''

        tokens = self._all_lines[node.lineno - 1]
        trailing = []

        for token in tokens:
            if _token_name(token) not in NOOP_TOKENS_LINE:
                # restart
                trailing = []
            else:
                trailing.append({
                    'rowstart': token[TOKEN_STARTLOC][TOKENROW],
                    'colstart': token[TOKEN_STARTLOC][TOKENCOL],
                    'rowend': token[TOKEN_ENDLOC][TOKENROW],
                    'colend': token[TOKEN_ENDLOC][TOKENCOL],
                    'value': token[TOKEN_VALUE]
                    })
        if not trailing:
            return ''

        self._sameline_added_noops.add(node.lineno)
        nonewline_trailing = trailing[:-1] if trailing[-1]['value'] == '\n' else trailing
        return nonewline_trailing

    def remainder_noops(self):
        """return any remaining ignored lines."""
        trailing = []
        lastline = None
        lastcol = 1

        i = self._current_line
        first_lineno = self._current_line + 1

        while i < len(self.astmissing_lines):
            token = self.astmissing_lines[i]
            if token:
                s = token[TOKEN_RAWVALUE]
                trailing.append(s)

            i += 1
            if token:
                lastline = i
                lastcol = len(token)
            else:
                lastcol = 1
        self._current_line = i
        return trailing, first_lineno, lastline, lastcol


_TOKEN_KEYS = set(
    ("module", "name", "id", "attr", "arg", "LiteralValue")
)

_SYNTHETIC_TOKENS = {
    "Print": "print",
    "Ellipsis": "...",
    "Add": "+",
    "Sub": "-",
    "Mult": "*",
    "Div": "/",
    "FloorDiv": "//",
    "Mod": "%%",
    "Pow": "**",
    "AugAssign": "+=",
    "BitAnd": "&",
    "BitOr": "|",
    "BitXor": "^",
    "LShift": "<<",
    "RShift": ">>",
    "Eq": "==",
    "NotEq": "!=",
    "Not": "not",
    "Lt": "<",
    "LtE": "<=",
    "Gt": ">",
    "GtE": ">=",
    "Is": "is",
    "IsNot": "not is",
    "In": "in",
    "NotIn": "not in",
    "UAdd": "+",
    "USub": "-",
    "Invert": "~",
    "Pass": "pass"
}


class DictExportVisitor(object):
    ast_type_field = "ast_type"

    def __init__(self, codestr, ast_parser=ast.parse):
        """
        Initialize the Token Syncer composited object, parse the source code
        and start visiting the node tree to add comments and other modifications

        Args:
            codestr (string): the string with the source code to parse and visit.

            ast_parser (function, optional): the AST parser function to use. It needs to take
            a string with the code as parameter. By default it will be ast.parse from stdlib.
        """
        # Tokenize and create the noop extractor and the position fixer
        self._tokens = tokenize.generate_tokens(StringIO(codestr).readline)
        token_lines = _create_tokenized_lines(codestr, self._tokens)
        self.noops_sync = NoopExtractor(codestr, token_lines)
        self.pos_sync   = LocationFixer(codestr, token_lines)
        self.codestr    = codestr

        # This is used to store the parent node of the current one; currently is only
        # used to inherit the lineno and col_offset of the parent for "arguments" and other grouping
        # nodes that the Python AST doesn't add location info.
        self._lastlocation_parent = None

        # Some nodes (f-strings currently) must update the columns after the've done some
        # previous line number fixing, so this state member enable or disable the checking/fixing
        self._checkpos_enabled = True

        # This will store a dict of nodes to end positions, it will be filled
        # on parse()
        self._node2endpos = None

    def _update_lastloc_parent(self, node):
        if hasattr(node, 'lineno') and hasattr(node, 'col_offset'):
            self._lastlocation_parent = node

    def _nodedict(self, node, newdict, ast_type=None):
        """
        Shortcut that adds ast_type (if not specified),
        lineno and col_offset to the node-derived dictionary
        """
        if ast_type is None:
            ast_type = node.__class__.__name__

        parent = self._lastlocation_parent

        newdict["ast_type"] = ast_type
        if hasattr(node, "lineno"):
            newdict["lineno"] = node.lineno
        elif parent and hasattr(parent, "lineno"):
            newdict["lineno"] = parent.lineno

        if hasattr(node, "col_offset"):
            newdict["col_offset"] = node.col_offset
        elif parent and hasattr(parent, "col_offset"):
            newdict["col_offset"] = parent.col_offset
        else:
            newdict["col_offset"] = 1

        return newdict

    def _add_noops(self, node, visit_dict, root):
        if not isinstance(visit_dict, dict):
            return visit_dict

        def _create_nooplines_list(startline, noops_previous):
            nooplines = []
            curline = startline
            for noopline in noops_previous:
                nooplines.append({
                    "ast_type": "NoopLine",
                    "noop_line": noopline,
                    "lineno": curline,
                    "col_offset": 1,
                })
                curline += 1
            return nooplines

        # Add all the noop (whitespace and comments) lines between the
        # last node and this one
        noops_previous, startline, endline, endcol =\
            self.noops_sync.previous_nooplines(node)
        if noops_previous:
            visit_dict['noops_previous'] = {
                "ast_type": "PreviousNoops",
                "lineno": startline,
                "col_offset": 1,
                "end_lineno": endline,
                "end_col_offset": max(endcol, 1),
                "lines": _create_nooplines_list(startline, noops_previous)
            }

        # Other noops at the end of its significative line except the implicit
        # finishing newline
        noops_sameline = self.noops_sync.sameline_remainder_noops(node)
        joined_sameline = ''.join([x['value'] for x in noops_sameline])
        if noops_sameline:
            visit_dict['noops_sameline'] = {
                "ast_type": "SameLineNoops",
                "lineno": node.lineno if hasattr(node, "lineno") else 0,
                "col_offset": noops_sameline[0]["colstart"],
                "noop_line": joined_sameline,
                "end_lineno": node.lineno,
                "end_col_offset": max(noops_sameline[-1]["colend"], 1)
            }

        # Finally, if this is the root node, add all noops after the last op node
        if root:
            noops_remainder, startline, endline, endcol =\
                    self.noops_sync.remainder_noops()
            if noops_remainder:
                visit_dict['noops_remainder'] = {
                    "ast_type": "RemainderNoops",
                    "lineno": startline,
                    "col_offset": 1,
                    "end_lineno": endline,
                    "end_col_offset": max(endcol, 1),
                    "lines": _create_nooplines_list(startline, noops_remainder)
                    }

    def parse(self):
        tree = ast.parse(self.codestr, mode='exec')
        res = self.visit(tree, root=True)
        # Remove the catching position key
        map_dict_rec(res, lambda x: x.pop('__cached_endpos', None))
        return res

    def visit(self, node, root=False):
        node_type = node.__class__.__name__

        if node_type == 'Module':
            # add line and col since Python doesnt adds them
            node.__dict__['lineno'] = 1
            node.__dict__['col_offset'] = 0

        # the ctx property always has a "Load"/"Store"/etc nodes that
        # can be perfectly converted to a string value since they don't
        # hold anything more than the name
        if hasattr(node, 'ctx'):
            node.ctx = node.ctx.__class__.__name__

        meth = getattr(self, "visit_" + node_type, self.visit_other)
        visit_result = meth(node)
        self._add_noops(node, visit_result, root)

        if self._checkpos_enabled:
            self.pos_sync.apply_fixes(visit_result)

        if not self.codestr:
            # empty files are the only case where 0-indexes are allowed
            visit_result['col_offset'] = visit_result['end_col_offset'] = \
                    visit_result['lineno'] = visit_result['end_lineno'] = 0
        else:
            # Python AST gives a 0 based column for the starting col, bblfsh uses 1-based
            visit_result['col_offset'] = max(visit_result.get('col_offset', 1) + 1, 1)

            if "end_col_offset" in visit_result:
                visit_result['end_col_offset'] = max(visit_result['end_col_offset'], 1)

        return visit_result

    def visit_other(self, node):
        node_type = node.__class__.__name__
        nodedict = self._nodedict(node, {}, ast_type = node_type)

        # Visit fields
        self._update_lastloc_parent(node)
        for field in node._fields:
            meth = getattr(self, "visit_" + node_type, self.visit_other_field)
            nodedict[field] = meth(getattr(node, field))

            # these must inherit their position from the parent
            # FIXME: move to a method
            if field in ('args', 'op', 'ops', 'alias', 'keywords'):
                if isinstance(nodedict[field], dict):
                    toprocess = [nodedict[field]]
                elif isinstance(nodedict[field], list):
                    toprocess = nodedict[field]
                else:
                    continue

                for proc in toprocess:
                    if 'lineno' not in proc and hasattr(node, 'lineno'):
                        proc['lineno'] = node.lineno
                    # doesnt make sense to inherit col_offset since it would be different

        # Visit attributes
        for attr in node._attributes:
            meth = getattr(self, "visit_" + node_type + "_" + attr, self.visit_other_field)
            nodedict[attr] = meth(getattr(node, attr))

        return nodedict

    def visit_other_field(self, node):
        if isinstance(node, ast.AST):
            return self.visit(node)
        elif isinstance(node, list) or isinstance(node, tuple):
            return [self.visit(x) for x in node]
        else:
            # string attribute
            return node

    def visit_str(self, node):
        """
        This visits str fields inside nodes (which are represented as keys
        in the node dictionary), not Str AST nodes
        """
        return str(node)

    def visit_Str(self, node):
        return self._nodedict(node, {"LiteralValue": node.s}, ast_type="StringLiteral")

    def visit_Bytes(self, node):
        try:
            s = node.s.decode()
            encoding = 'utf8'
        except UnicodeDecodeError:
            # try with base64
            s = encode(node.s, 'base64').decode().strip()
            encoding = 'base64'

        return self._nodedict(node, {"LiteralValue": s, "encoding": encoding},
                         ast_type="ByteLiteral")

    def visit_NoneType(self, node):
        return self._nodedict(node, {"LiteralValue": "None"}, ast_type="NoneLiteral")

    def visit_Global(self, node):
        # Python AST by default stores global and nonlocal variable names
        # in a "names" array of strings. That breaks the structure of everything
        # else in the AST (dictionaries, properties or list of objects) so we
        # convert those names to Name objects
        names_as_nodes = [{"ast_type": "Name",
                          "id": i,
                          "lineno": node.lineno,
                          "col_offset": node.col_offset} for i in node.names]
        return self._nodedict(node, {"names": names_as_nodes}, ast_type="Global")

    def visit_Nonlocal(self, node):
        # ditto
        names_as_nodes = [{"ast_type": "Name",
                          "id": i,
                          "lineno": node.lineno,
                          "col_offset": node.col_offset} for i in node.names]
        return self._nodedict(node, {"names": names_as_nodes}, ast_type="Nonlocal")

    def visit_NameConstant(self, node):
        if hasattr(node, 'value'):
            repr_val = repr(node.value)
            if repr_val in ('True', 'False'):
                return self._nodedict(node, {"LiteralValue": node.value},
                        ast_type="BoolLiteral")
            elif repr_val == 'None':
                return self._nodedict(node, {"LiteralValue": node.value},
                                 ast_type="NoneLiteral")
        return self._nodedict(node, {}, ast_type='NameConstant')

    def visit_Num(self, node):
        if isinstance(node.n, int):
            ret_dict = { "NumType": "int", "LiteralValue": node.n }
        elif isinstance(node.n, float):
            ret_dict = { "NumType": "float", "LiteralValue": node.n }
        elif isinstance(node.n, complex):
            ret_dict = {
                        "NumType": "complex",
                        "LiteralValue": {"real": node.n.real, "imaginary": node.n.imag},
                       }

        return self._nodedict(node, ret_dict, ast_type="NumLiteral")

    def visit_FormattedValue(self, node):
        # Subcode inside the FormattedValue.value nodes have their lineno starting from 1,
        # so we'll fix that storing the FormattedValue lineno and adding it to the subcode
        # nodes lineno
        self._checkpos_enabled = False  # it wouldn't work without correct lineno
        try:
            value_dict = self.pos_sync.fix_embeded_pos(self.visit(node.value),
                                                       node.lineno)
            fspec = self.visit(node.format_spec) if node.format_spec else None
            nodedict = {
                    "conversion": node.conversion,
                    "format_spec": fspec,
                    "value": value_dict,
            }
            retdict = self._nodedict(node, nodedict, ast_type="FormattedValue")
        finally:
            self._checkpos_enabled = True

        return retdict


if __name__ == '__main__':
    # for manual tests

    if len(sys.argv) > 1:
        with open(sys.argv[1]) as codefile:
            content = codefile.read()
    else:
        content = \
'''if True:
    if False:
        a = 6 + 7
    else:
        print('LAST')

'''

    from pprint import pprint
    pprint(export_dict(content))
