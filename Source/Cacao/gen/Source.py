from Shared import * 

classes = pickle.load(open(picklepath, "rb"))

functionBody = """
functionOf{Pless}({defaults}) {const}{{
{function}
}}
"""

destructorBody = """
{cl}::{name}({params}) {{
	if (destructorLock[this]) return;
	destructorLock[this] = true;
{function}
}}
"""

constructorBody = """
{cl}::{name}({params}) : {cl}(*this) {{
{function}
}}
"""

out = """// 
// Copyright camila314 & alk1m123 2021. 
// Autogenerated using a python script
//
#include <Header.hpp>
#define dl decltype
#define dv std::declval
"""

i = 0
for cl in classes:
	for info in cl.info:
		if "cocos2d" in cl.name and platform == "Win32":
			continue
			
		if isinstance(info, str) and "cocos2d" in cl.name:
			out += "\n" + info.replace("\n\t", "\n") + "\n"
			continue
		if not isinstance(info, GenFunction):
			continue
		if linkable(info):
			continue
		if info.getAddress(platform) == "None":
			continue

		body = functionBody
		if not info.declare.type: # ctor or dtor
			if "~" in info.declare.name:
				body = destructorBody
			else:
				body = constructorBody

		out += body.format(
			name = info.declare.name,
			cl = cl.name,
			offset = info.getOffset(platform, i), 
			params = ', '.join(arg.getExpr(i) for i, arg in enumerate(info.parameters)),
			params2 = (', ' if not info.static and len(info.parameters) > 0 else "") + ', '.join(arg.getType(i) for i, arg in enumerate(info.parameters)),
			defaults = ', '.join([cl.name, info.declare.name] + [arg.getType(i) for i, arg in enumerate(info.parameters)]),
			Pless = 'P' if len(info.parameters) == 0 else '',
			const = "const " if info.const else "",
			id = i,
			function = getFunctionImplementation(cl, info, i).replace("\t\t", "\t"),
		)
		i += 1

out += """
#undef dl
#undef dv
"""

writeIfDifferent("Source.cpp", out)
 
