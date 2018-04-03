
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'programfilenonassocEPSILONASSERT ASSIGNMENT_OPERATOR BOTHOUT BOTHPIPE COLON COMMA DEDENT DOCSTRING ELIF ELSE END_COLON ERROUT ERRPIPE FILEAPPEND FILEOUT FOR IF IN INDENT LPAREN NL PIPE PYTHON RETURN RPAREN SEMICOLON SHELL_DELIMITER STREAM_IN STREAM_OUT STRING VARNAME WHILE WORD YIELDprogramfile : nonempty_block\n                   | emptynonempty_block : statement_complex empty\n                      | statement_complex nonempty_blockstatement_complex : loop\n                         | conditional\n                         | statement_multi NL\n                         | statement_multi SEMICOLON NLstatement_multi : statement_multi SEMICOLON statement_multistatement_multi : statement_simplestatement_simple : statement_result\n                        | statement_no_resultstatement_result : assignment\n                        | return\n                        | assert\n                        | yieldstatement_no_result : shellblock_run\n                           | python_codeloop : while_loop\n            | for_loopwhile_loop : WHILE expression END_COLON suitefor_loop : FOR PYTHON IN expression END_COLON suiteconditional : IF expression END_COLON suite conditional_extension\n                   | IF expression END_COLON suite emptyconditional_extension : ELIF expression END_COLON suite conditional_extensionconditional_extension : ELSE END_COLON suiteassignment : python_code ASSIGNMENT_OPERATOR expressionreturn : RETURN empty\n              | RETURN expressionassert : ASSERT expressionyield : YIELD expressionexpression : shellblock\n                  | python_codepython_code : PYTHON python_code\n                   | STRING python_code\n                   | DOCSTRING python_code\n                   | COLON python_code\n                   | PYTHON empty\n                   | STRING empty\n                   | DOCSTRING emptysuite : NL INDENT nonempty_block DEDENTsuite : statement_simple NLshellblock_run : shellblockshellblock : SHELL_DELIMITER statement SHELL_DELIMITERempty : %prec EPSILONstatement : proc\n                 | procinprocin : command STREAM_IN instream procout\n              | command STREAM_IN instream emptyproc : command empty\n            | command procoutcommand : WORD arglist\n               | WORD emptyarglist : arg empty\n               | arg arglistarg : WORD\n           | var\n           | STRINGprocout : pipeout\n               | streamout\n               | fileoutpipeout : PIPE empty proc empty empty empty\n               | PIPE LPAREN proc COMMA proc RPAREN\n               | ERRPIPE empty empty empty proc emptypipeout : BOTHPIPE procstreamout : STREAM_OUT VARNAME\n                 | STREAM_OUT LPAREN VARNAME COMMA VARNAME RPAREN\n                 | ERROUT VARNAME\n                 | BOTHOUT VARNAMEfileout : FILEOUT file\n               | FILEAPPEND fileinstream : WORD\n                | var\n                | STRINGfile : WORD\n            | var\n            | STRINGvar : VARNAME'
    
_lr_action_items = {'ERRPIPE':([49,50,76,77,78,79,80,81,82,93,95,96,97,98,108,109,],[65,-45,-52,-78,-53,-57,-45,-58,-56,65,65,-73,-74,-72,-55,-54,]),'PYTHON':([0,1,2,4,6,8,9,10,11,13,17,21,24,25,26,28,38,39,52,57,59,60,84,86,87,110,111,112,113,121,122,123,124,130,132,137,138,144,],[1,1,1,35,1,1,-6,1,-20,1,1,-19,1,1,1,-5,-7,1,1,1,-8,1,1,1,-21,-45,1,1,-42,-23,1,-24,-22,1,-41,-26,1,-25,]),'DOCSTRING':([0,1,2,6,8,9,10,11,13,17,21,24,25,26,28,38,39,52,57,59,60,84,86,87,110,111,112,113,121,122,123,124,130,132,137,138,144,],[2,2,2,2,2,-6,2,-20,2,2,-19,2,2,2,-5,-7,2,2,2,-8,2,2,2,-21,-45,2,2,-42,-23,2,-24,-22,2,-41,-26,2,-25,]),'YIELD':([0,6,9,11,21,28,38,39,59,60,84,86,87,110,111,112,113,121,123,124,130,132,137,138,144,],[24,24,-6,-20,-19,-5,-7,24,-8,24,24,24,-21,-45,24,24,-42,-23,-24,-22,24,-41,-26,24,-25,]),'FOR':([0,6,9,11,21,28,38,59,87,110,112,113,121,123,124,132,137,144,],[4,4,-6,-20,-19,-5,-7,-8,-21,-45,4,-42,-23,-24,-22,-41,-26,-25,]),'RPAREN':([50,63,64,66,68,71,76,77,78,79,80,81,82,93,94,99,100,102,103,104,105,106,107,108,109,114,126,133,134,135,136,139,140,141,142,],[-45,-61,-59,-60,-51,-50,-52,-78,-53,-57,-45,-58,-56,-45,-65,-68,-69,-66,-70,-76,-77,-75,-71,-55,-54,-45,-45,-45,140,-45,142,-62,-63,-64,-67,]),'IN':([35,],[57,]),'VARNAME':([50,69,70,72,73,74,75,77,79,80,81,82,101,129,],[77,77,99,100,102,77,77,-78,-57,77,-58,-56,119,136,]),'$end':([0,3,5,6,9,11,14,21,28,36,37,38,59,87,110,113,121,123,124,132,137,144,],[-45,-2,-1,-45,-6,-20,0,-19,-5,-3,-4,-7,-8,-21,-45,-42,-23,-24,-22,-41,-26,-25,]),'PIPE':([49,50,76,77,78,79,80,81,82,93,95,96,97,98,108,109,],[62,-45,-52,-78,-53,-57,-45,-58,-56,62,62,-73,-74,-72,-55,-54,]),'STRING':([0,1,2,6,8,9,10,11,13,17,21,24,25,26,28,38,39,50,52,57,59,60,69,74,75,77,79,80,81,82,84,86,87,110,111,112,113,121,122,123,124,130,132,137,138,144,],[8,8,8,8,8,-6,8,-20,8,8,-19,8,8,8,-5,-7,8,81,8,8,-8,8,97,105,105,-78,-57,81,-58,-56,8,8,-21,-45,8,8,-42,-23,8,-24,-22,8,-41,-26,8,-25,]),'SEMICOLON':([1,2,7,8,12,15,16,18,20,22,23,26,27,29,30,31,32,33,34,40,41,42,43,45,46,53,55,56,58,61,83,],[-45,-45,39,-45,-15,-10,-16,-13,-18,-14,-43,-45,-11,-17,-12,-38,-34,-40,-36,-39,-35,-37,-33,-32,-30,-31,-28,-29,86,-44,-27,]),'COLON':([0,1,2,6,8,9,10,11,13,17,21,24,25,26,28,38,39,52,57,59,60,84,86,87,110,111,112,113,121,122,123,124,130,132,137,138,144,],[10,10,10,10,10,-6,10,-20,10,10,-19,10,10,10,-5,-7,10,10,10,-8,10,10,10,-21,-45,10,10,-42,-23,10,-24,-22,10,-41,-26,10,-25,]),'FILEAPPEND':([49,50,76,77,78,79,80,81,82,93,95,96,97,98,108,109,],[75,-45,-52,-78,-53,-57,-45,-58,-56,75,75,-73,-74,-72,-55,-54,]),'LPAREN':([62,73,],[91,101,]),'WORD':([19,50,62,65,67,69,74,75,77,79,80,81,82,90,91,92,116,127,128,],[50,82,-45,-45,50,98,106,106,-78,-57,82,-58,-56,50,50,-45,-45,50,50,]),'WHILE':([0,6,9,11,21,28,38,59,87,110,112,113,121,123,124,132,137,144,],[13,13,-6,-20,-19,-5,-7,-8,-21,-45,13,-42,-23,-24,-22,-41,-26,-25,]),'NL':([1,2,7,8,12,15,16,18,20,22,23,26,27,29,30,31,32,33,34,39,40,41,42,43,45,46,53,55,56,58,60,61,83,84,89,111,130,138,],[-45,-45,38,-45,-15,-10,-16,-13,-18,-14,-43,-45,-11,-17,-12,-38,-34,-40,-36,59,-39,-35,-37,-33,-32,-30,-31,-28,-29,-9,88,-44,-27,88,113,88,88,88,]),'SHELL_DELIMITER':([0,6,9,11,13,17,21,24,25,26,28,38,39,47,48,49,50,51,52,57,59,60,63,64,66,68,71,76,77,78,79,80,81,82,84,86,87,93,94,95,96,97,98,99,100,102,103,104,105,106,107,108,109,110,111,112,113,114,117,118,121,122,123,124,126,130,132,133,135,137,138,139,140,141,142,144,],[19,19,-6,-20,19,19,-19,19,19,19,-5,-7,19,-47,61,-45,-45,-46,19,19,-8,19,-61,-59,-60,-51,-50,-52,-78,-53,-57,-45,-58,-56,19,19,-21,-45,-65,-45,-73,-74,-72,-68,-69,-66,-70,-76,-77,-75,-71,-55,-54,-45,19,19,-42,-45,-48,-49,-23,19,-24,-22,-45,19,-41,-45,-45,-26,19,-62,-63,-64,-67,-25,]),'END_COLON':([1,2,8,31,32,33,34,40,41,42,43,44,45,54,61,85,120,131,],[-45,-45,-45,-38,-34,-40,-36,-39,-35,-37,-33,60,-32,84,-44,111,130,138,]),'COMMA':([50,63,64,66,68,71,76,77,78,79,80,81,82,93,94,99,100,102,103,104,105,106,107,108,109,114,115,119,126,133,135,139,140,141,142,],[-45,-61,-59,-60,-51,-50,-52,-78,-53,-57,-45,-58,-56,-45,-65,-68,-69,-66,-70,-76,-77,-75,-71,-55,-54,-45,127,129,-45,-45,-45,-62,-63,-64,-67,]),'ASSERT':([0,6,9,11,21,28,38,39,59,60,84,86,87,110,111,112,113,121,123,124,130,132,137,138,144,],[17,17,-6,-20,-19,-5,-7,17,-8,17,17,17,-21,-45,17,17,-42,-23,-24,-22,17,-41,-26,17,-25,]),'ELIF':([110,113,132,143,],[122,-42,-41,122,]),'BOTHPIPE':([49,50,76,77,78,79,80,81,82,93,95,96,97,98,108,109,],[67,-45,-52,-78,-53,-57,-45,-58,-56,67,67,-73,-74,-72,-55,-54,]),'INDENT':([88,],[112,]),'ELSE':([110,113,132,143,],[120,-42,-41,120,]),'STREAM_IN':([49,50,76,77,78,79,80,81,82,108,109,],[69,-45,-52,-78,-53,-57,-45,-58,-56,-55,-54,]),'ASSIGNMENT_OPERATOR':([1,2,8,20,31,32,33,34,40,41,42,],[-45,-45,-45,52,-38,-34,-40,-36,-39,-35,-37,]),'ERROUT':([49,50,76,77,78,79,80,81,82,93,95,96,97,98,108,109,],[70,-45,-52,-78,-53,-57,-45,-58,-56,70,70,-73,-74,-72,-55,-54,]),'IF':([0,6,9,11,21,28,38,59,87,110,112,113,121,123,124,132,137,144,],[25,25,-6,-20,-19,-5,-7,-8,-21,-45,25,-42,-23,-24,-22,-41,-26,-25,]),'FILEOUT':([49,50,76,77,78,79,80,81,82,93,95,96,97,98,108,109,],[74,-45,-52,-78,-53,-57,-45,-58,-56,74,74,-73,-74,-72,-55,-54,]),'RETURN':([0,6,9,11,21,28,38,39,59,60,84,86,87,110,111,112,113,121,123,124,130,132,137,138,144,],[26,26,-6,-20,-19,-5,-7,26,-8,26,26,26,-21,-45,26,26,-42,-23,-24,-22,26,-41,-26,26,-25,]),'BOTHOUT':([49,50,76,77,78,79,80,81,82,93,95,96,97,98,108,109,],[72,-45,-52,-78,-53,-57,-45,-58,-56,72,72,-73,-74,-72,-55,-54,]),'STREAM_OUT':([49,50,76,77,78,79,80,81,82,93,95,96,97,98,108,109,],[73,-45,-52,-78,-53,-57,-45,-58,-56,73,73,-73,-74,-72,-55,-54,]),'DEDENT':([6,9,11,21,28,36,37,38,59,87,110,113,121,123,124,125,132,137,144,],[-45,-6,-20,-19,-5,-3,-4,-7,-8,-21,-45,-42,-23,-24,-22,132,-41,-26,-25,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'shellblock_run':([0,6,39,60,84,86,111,112,130,138,],[29,29,29,29,29,29,29,29,29,29,]),'arg':([50,80,],[80,80,]),'statement_result':([0,6,39,60,84,86,111,112,130,138,],[27,27,27,27,27,27,27,27,27,27,]),'instream':([69,],[95,]),'nonempty_block':([0,6,112,],[5,37,125,]),'statement_complex':([0,6,112,],[6,6,6,]),'statement_multi':([0,6,39,86,112,],[7,7,58,58,7,]),'file':([74,75,],[103,107,]),'conditional':([0,6,112,],[9,9,9,]),'command':([19,67,90,91,127,128,],[49,93,93,93,93,93,]),'pipeout':([49,93,95,],[64,64,64,]),'conditional_extension':([110,143,],[121,144,]),'var':([50,69,74,75,80,],[79,96,104,104,79,]),'for_loop':([0,6,112,],[11,11,11,]),'assert':([0,6,39,60,84,86,111,112,130,138,],[12,12,12,12,12,12,12,12,12,12,]),'programfile':([0,],[14,]),'loop':([0,6,112,],[28,28,28,]),'suite':([60,84,111,130,138,],[87,110,124,137,143,]),'procin':([19,],[47,]),'yield':([0,6,39,60,84,86,111,112,130,138,],[16,16,16,16,16,16,16,16,16,16,]),'statement':([19,],[48,]),'streamout':([49,93,95,],[66,66,66,]),'procout':([49,93,95,],[68,68,117,]),'python_code':([0,1,2,6,8,10,13,17,24,25,26,39,52,57,60,84,86,111,112,122,130,138,],[20,32,34,20,41,42,43,43,43,43,43,20,43,43,20,20,20,20,20,43,20,20,]),'while_loop':([0,6,112,],[21,21,21,]),'return':([0,6,39,60,84,86,111,112,130,138,],[22,22,22,22,22,22,22,22,22,22,]),'shellblock':([0,6,13,17,24,25,26,39,52,57,60,84,86,111,112,122,130,138,],[23,23,45,45,45,45,45,23,45,45,23,23,23,23,23,45,23,23,]),'arglist':([50,80,],[76,108,]),'assignment':([0,6,39,60,84,86,111,112,130,138,],[18,18,18,18,18,18,18,18,18,18,]),'fileout':([49,93,95,],[63,63,63,]),'empty':([0,1,2,6,8,26,49,50,62,65,80,92,93,95,110,114,116,126,133,135,],[3,31,33,36,40,55,71,78,90,92,109,116,71,118,123,126,128,133,139,141,]),'expression':([13,17,24,25,26,52,57,122,],[44,46,53,54,56,83,85,131,]),'statement_simple':([0,6,39,60,84,86,111,112,130,138,],[15,15,15,89,89,15,89,15,89,89,]),'proc':([19,67,90,91,127,128,],[51,94,114,115,134,135,]),'statement_no_result':([0,6,39,60,84,86,111,112,130,138,],[30,30,30,30,30,30,30,30,30,30,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> programfile","S'",1,None,None,None),
  ('programfile -> nonempty_block','programfile',1,'p_programfile','pyshell_parser.py',19),
  ('programfile -> empty','programfile',1,'p_programfile','pyshell_parser.py',20),
  ('nonempty_block -> statement_complex empty','nonempty_block',2,'p_nonempty_block','pyshell_parser.py',24),
  ('nonempty_block -> statement_complex nonempty_block','nonempty_block',2,'p_nonempty_block','pyshell_parser.py',25),
  ('statement_complex -> loop','statement_complex',1,'p_statement_complex','pyshell_parser.py',29),
  ('statement_complex -> conditional','statement_complex',1,'p_statement_complex','pyshell_parser.py',30),
  ('statement_complex -> statement_multi NL','statement_complex',2,'p_statement_complex','pyshell_parser.py',31),
  ('statement_complex -> statement_multi SEMICOLON NL','statement_complex',3,'p_statement_complex','pyshell_parser.py',32),
  ('statement_multi -> statement_multi SEMICOLON statement_multi','statement_multi',3,'p_statement_multi','pyshell_parser.py',36),
  ('statement_multi -> statement_simple','statement_multi',1,'p_statement_single','pyshell_parser.py',40),
  ('statement_simple -> statement_result','statement_simple',1,'p_statement_simple','pyshell_parser.py',44),
  ('statement_simple -> statement_no_result','statement_simple',1,'p_statement_simple','pyshell_parser.py',45),
  ('statement_result -> assignment','statement_result',1,'p_statement_result','pyshell_parser.py',49),
  ('statement_result -> return','statement_result',1,'p_statement_result','pyshell_parser.py',50),
  ('statement_result -> assert','statement_result',1,'p_statement_result','pyshell_parser.py',51),
  ('statement_result -> yield','statement_result',1,'p_statement_result','pyshell_parser.py',52),
  ('statement_no_result -> shellblock_run','statement_no_result',1,'p_statement_no_result','pyshell_parser.py',56),
  ('statement_no_result -> python_code','statement_no_result',1,'p_statement_no_result','pyshell_parser.py',57),
  ('loop -> while_loop','loop',1,'p_loop','pyshell_parser.py',62),
  ('loop -> for_loop','loop',1,'p_loop','pyshell_parser.py',63),
  ('while_loop -> WHILE expression END_COLON suite','while_loop',4,'p_while','pyshell_parser.py',67),
  ('for_loop -> FOR PYTHON IN expression END_COLON suite','for_loop',6,'p_for','pyshell_parser.py',71),
  ('conditional -> IF expression END_COLON suite conditional_extension','conditional',5,'p_conditional','pyshell_parser.py',76),
  ('conditional -> IF expression END_COLON suite empty','conditional',5,'p_conditional','pyshell_parser.py',77),
  ('conditional_extension -> ELIF expression END_COLON suite conditional_extension','conditional_extension',5,'p_conditional_extension_elif','pyshell_parser.py',81),
  ('conditional_extension -> ELSE END_COLON suite','conditional_extension',3,'p_conditional_extension_else','pyshell_parser.py',85),
  ('assignment -> python_code ASSIGNMENT_OPERATOR expression','assignment',3,'p_assignment','pyshell_parser.py',90),
  ('return -> RETURN empty','return',2,'p_return','pyshell_parser.py',94),
  ('return -> RETURN expression','return',2,'p_return','pyshell_parser.py',95),
  ('assert -> ASSERT expression','assert',2,'p_assert','pyshell_parser.py',99),
  ('yield -> YIELD expression','yield',2,'p_yield','pyshell_parser.py',103),
  ('expression -> shellblock','expression',1,'p_expression','pyshell_parser.py',107),
  ('expression -> python_code','expression',1,'p_expression','pyshell_parser.py',108),
  ('python_code -> PYTHON python_code','python_code',2,'p_python_code','pyshell_parser.py',112),
  ('python_code -> STRING python_code','python_code',2,'p_python_code','pyshell_parser.py',113),
  ('python_code -> DOCSTRING python_code','python_code',2,'p_python_code','pyshell_parser.py',114),
  ('python_code -> COLON python_code','python_code',2,'p_python_code','pyshell_parser.py',115),
  ('python_code -> PYTHON empty','python_code',2,'p_python_code','pyshell_parser.py',116),
  ('python_code -> STRING empty','python_code',2,'p_python_code','pyshell_parser.py',117),
  ('python_code -> DOCSTRING empty','python_code',2,'p_python_code','pyshell_parser.py',118),
  ('suite -> NL INDENT nonempty_block DEDENT','suite',4,'p_suite_block','pyshell_parser.py',122),
  ('suite -> statement_simple NL','suite',2,'p_suite_inline','pyshell_parser.py',126),
  ('shellblock_run -> shellblock','shellblock_run',1,'p_shellblock_run','pyshell_parser.py',130),
  ('shellblock -> SHELL_DELIMITER statement SHELL_DELIMITER','shellblock',3,'p_shellblock','pyshell_parser.py',134),
  ('empty -> <empty>','empty',0,'p_empty','pyshell_parser.py',138),
  ('statement -> proc','statement',1,'p_statement','pyshell_parser.py',142),
  ('statement -> procin','statement',1,'p_statement','pyshell_parser.py',143),
  ('procin -> command STREAM_IN instream procout','procin',4,'p_procin','pyshell_parser.py',147),
  ('procin -> command STREAM_IN instream empty','procin',4,'p_procin','pyshell_parser.py',148),
  ('proc -> command empty','proc',2,'p_proc','pyshell_parser.py',152),
  ('proc -> command procout','proc',2,'p_proc','pyshell_parser.py',153),
  ('command -> WORD arglist','command',2,'p_command','pyshell_parser.py',157),
  ('command -> WORD empty','command',2,'p_command','pyshell_parser.py',158),
  ('arglist -> arg empty','arglist',2,'p_arglist','pyshell_parser.py',162),
  ('arglist -> arg arglist','arglist',2,'p_arglist','pyshell_parser.py',163),
  ('arg -> WORD','arg',1,'p_arg','pyshell_parser.py',167),
  ('arg -> var','arg',1,'p_arg','pyshell_parser.py',168),
  ('arg -> STRING','arg',1,'p_arg','pyshell_parser.py',169),
  ('procout -> pipeout','procout',1,'p_procout','pyshell_parser.py',173),
  ('procout -> streamout','procout',1,'p_procout','pyshell_parser.py',174),
  ('procout -> fileout','procout',1,'p_procout','pyshell_parser.py',175),
  ('pipeout -> PIPE empty proc empty empty empty','pipeout',6,'p_pipe','pyshell_parser.py',179),
  ('pipeout -> PIPE LPAREN proc COMMA proc RPAREN','pipeout',6,'p_pipe','pyshell_parser.py',180),
  ('pipeout -> ERRPIPE empty empty empty proc empty','pipeout',6,'p_pipe','pyshell_parser.py',181),
  ('pipeout -> BOTHPIPE proc','pipeout',2,'p_bothpipe','pyshell_parser.py',185),
  ('streamout -> STREAM_OUT VARNAME','streamout',2,'p_streamout','pyshell_parser.py',189),
  ('streamout -> STREAM_OUT LPAREN VARNAME COMMA VARNAME RPAREN','streamout',6,'p_streamout','pyshell_parser.py',190),
  ('streamout -> ERROUT VARNAME','streamout',2,'p_streamout','pyshell_parser.py',191),
  ('streamout -> BOTHOUT VARNAME','streamout',2,'p_streamout','pyshell_parser.py',192),
  ('fileout -> FILEOUT file','fileout',2,'p_fileout','pyshell_parser.py',196),
  ('fileout -> FILEAPPEND file','fileout',2,'p_fileout','pyshell_parser.py',197),
  ('instream -> WORD','instream',1,'p_instream','pyshell_parser.py',201),
  ('instream -> var','instream',1,'p_instream','pyshell_parser.py',202),
  ('instream -> STRING','instream',1,'p_instream','pyshell_parser.py',203),
  ('file -> WORD','file',1,'p_file','pyshell_parser.py',207),
  ('file -> var','file',1,'p_file','pyshell_parser.py',208),
  ('file -> STRING','file',1,'p_file','pyshell_parser.py',209),
  ('var -> VARNAME','var',1,'p_var','pyshell_parser.py',213),
]
